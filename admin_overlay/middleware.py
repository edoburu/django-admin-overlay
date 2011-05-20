"""

Integration in the HTML for frontend editing.
"""
import re
from django.core.urlresolvers import NoReverseMatch, reverse
from django.template import RequestContext
from django.template.loader import render_to_string


class AdminOverlayMiddleware(object):
    """
    Middleware to display the admin toolbar at frontend pages.

    It can be easily overwritten, to write a specialized middleware.
    For example, overwrite ``get_context_data()`` to change the context data,
    or overwrite ``can_show_overlay()`` to change when the overlay should be displayed.
    """
    # Settings which can be overwritten
    allowed_status_codes  = (200,)
    allowed_content_types = ("text/html", "application/xhtml+xml")
    head_end_template   = "admin_overlay/head_end.html"
    body_start_template = "admin_overlay/body_start.html"
    body_end_template   = "admin_overlay/body_end.html"


    def process_request(self, request):
        return


    def process_response(self, request, response):
        if self.is_regular_page(request, response) and self.can_show_overlay(request, response):
            self.insert_overlay(request, response)
        return response


    # -- determine whether to show the overlay


    def is_regular_page(self, request, response):
        return response.status_code in self.allowed_status_codes \
           and not request.is_ajax() \
           and response['Content-Type'].split(';')[0] in self.allowed_content_types


    def can_show_overlay(self, request, response):
        """
        Return whether the current visitor should see the overlay.

        This check can be fine tuned by overwriting the methods
        ``is_staff()`` and ``is_frontend_page()``.
        """
        return self.is_valid_user(request) and self.is_frontend_page(request)


    def is_valid_user(self, request):
        # hasattr(request, 'user') is needed for /admin without slash
        return hasattr(request, 'user') \
           and request.user.is_authenticated() \
           and request.user.is_staff


    def is_frontend_page(self, request):
        try:
            return not request.path.startswith(reverse('admin:index'))
        except NoReverseMatch:
            return True


    # -- Inserting HTML overlay

    def insert_overlay(self, request, response):
        """
        Insert the overlay in the passed resposne.
        """
        # Find tags
        html = response.content.lower()
        head_match = re.compile(r'[ \t]*</head>').search(html)
        body_match = re.compile(r'<body([^>]*)>\r?\n?').search(html, head_match.end() if head_match else 0)
        end_match  = re.compile(r'[ \t]*</body>').search(html, html.rfind("</body>") - 10)  # seed with start position
        if not head_match and not body_match and not end_match:
            return

        # Render HTML
        # The encode("utf-8") is needed to avoid an UnicodeDecodeError
        context_instance = RequestContext(request, self.get_context_data(request))
        head_content = render_to_string(self.head_end_template, context_instance=context_instance).encode("utf-8")
        body_content = render_to_string(self.body_start_template, context_instance=context_instance).encode("utf-8")
        end_content  = render_to_string(self.body_end_template, context_instance=context_instance).encode("utf-8")

        # Insert
        html = response.content
        head_end   = head_match.start()
        body_start = body_match.end()
        body_end   = end_match.start()
        response.content = html[:head_end]           + head_content \
                         + html[head_end:body_start] + body_content \
                         + html[body_start:body_end] + end_content \
                         + html[body_end:]

        response['Content-Length'] = len(response.content)


    def get_context_data(self, request):
        """
        Return the context data for the overlay templates.

        By default this contains ``user``.
        """
        return {
            'user': request.user
        }

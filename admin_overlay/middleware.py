"""
Integration in the HTML for frontend editing.
"""
import re
from django.template import RequestContext
from django.template.loader import render_to_string


class AdminOverlayMiddleware(object):
    """
    Middleware to display the admin toolbar at frontend pages.
    """

    def process_request(self, request):
        return

    def process_response(self, request, response):
        if self._can_show_overlay(request, response):
            self._insert_overlay(request, response)

        return response


    # -- determine whether to show the overlay

    def _can_show_overlay(self, request, response):
        # hasattr(request, 'user') is needed for /admin without slash
        return response['Content-Type'].startswith("text/html") \
           and hasattr(request, 'user') \
           and request.user.is_authenticated() \
           and request.user.is_staff \
           and self._is_frontend_page(request)

    def _is_frontend_page(self, request):
        return not request.path.startswith('/admin/')


    # -- Inserting HTML overlay

    def _insert_overlay(self, request, response):
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
        context_instance = RequestContext(request)
        head_content = render_to_string("admin_overlay/head_end.html", {}, context_instance)
        body_content = render_to_string("admin_overlay/body_start.html", {}, context_instance)
        end_content  = render_to_string("admin_overlay/body_end.html", {}, context_instance)

        # Insert
        html = response.content
        head_end   = head_match.start()
        body_start = body_match.end()
        body_end   = end_match.start()
        response.content = html[:head_end]  + head_content \
                         + html[head_end:body_start] + body_content \
                         + html[body_start:body_end] + end_content \
                         + html[body_end:]

        response['Content-Length'] = len(response.content)

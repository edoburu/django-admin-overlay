Django admin-overlay
====================

This package displays an overlay (i.e. toolbar) at the frontend pages, when the user is logged in as administrator.
It makes it easier to navigate through the site, or add a frontend-editoring toolbar to your project.
This is implemented as Django middleware, which can be extended and customized for your own projects.

Feel free to fork the project, and contribute patches!

Installation
------------

The ``setup.py`` has to suffice for now::

    python setup.py install

Enabling the overlay
--------------------

Settings to add::

    INSTALLED_APPS += (
        'admin_overlay',
    )
    
    MIDDLEWARE_CLASSES += (
        'admin_overlay.middleware.AdminOverlayMiddleware',
    )

Optionally the templates can be updated:

- ``admin_overlay/head_end.html``: the content which is added just before the ``</head>`` tag.
- ``admin_overlay/body_start.html``: the content which is added just after the ``<body>`` tag.
- ``admin_overlay/body_end.html``: the content which is added just before the ``</body>`` tag.

The templates receive a ``RequestContext`` with the ``request`` field. No other context information is given.

Extending the overlay
---------------------

It's perfectly fine (even encouraged) to inhert the ``AdminOverlayMiddleware`` class,
to add your own presentation logic. The class defines some public settings,
and methods which you can override.

The settings are:

- ``allowed_status_codes``: which HTTP status codes should enable the overlay. By default 200.
- ``allowed_content_types``: which content type does the overlay respond to? By default ``text/html`` and ``application/xhtml+xm``.
- ``head_end_template``: which template to use for the content before the ``</head>`` tag, By default ``admin_overlay/head_end.html``.
- ``body_start_template``: which template to use for the content after the ``<body>`` tag. By default ``admin_overlay/body_start.html``.
- ``body_end_template``: which template to use for the content before the ``</body>`` tag. By default ``admin_overlay/body_end.html``.


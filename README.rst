
h2. Enabling the overlay

Settings to add:

    INSTALLED_APPS += (
        'admin_overlay',
    )
    
    MIDDLEWARE_CLASSES += (
        'admin_overlay.middleware.AdminOverlayMiddleware',
    )

Optionally the templates can be updated:

* @admin_overlay/head_end.html@: the content which is added just before the @</head>@ tag.
* @admin_overlay/body_start.html@: the content which is added just after the @<body>@ tag.
* @admin_overlay/body_end.html@: the content which is added just before the @</body>@ tag.

The templates receive a @RequestContext@ with the @request@ field. No other context information is given.

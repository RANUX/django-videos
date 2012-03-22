# -*- coding: utf-8 -*-
import os

try:
    from pluggableapp import PluggableApp
except ImportError:
    # pluggableapp is not installed
    pass


def pluggableapp(**kw):
    app = PluggableApp('djangovideos', distribution='django-videos', **kw)
    app.append_app()
    app.append("TEMPLATE_CONTEXT_PROCESSORS", "django.core.context_processors.i18n",
                                              "django.core.context_processors.request")
    app.register_pattern('', r'^videos/', 'djangovideos.urls')
    app.insert_templates(__file__)
    return app


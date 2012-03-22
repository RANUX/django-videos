# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django_webtest import WebTest as Base
from webtest import Form
from djangovideos import models

__all__ = ('WebTest', 'UserWebTest', 'models', 'reverse')

class WebTest(Base):
    def _patch_settings(self):
        Base._patch_settings(self)
        from django.conf import settings
        settings.MIDDLEWARE_CLASSES = tuple([m for m in settings.MIDDLEWARE_CLASSES if 'Csrf' not in m])

class UserWebTest(WebTest):

    login = 'user1'
    extra_environ = {'REMOTE_USER': login}
    user = None

    def setUp(self):
        super(UserWebTest, self).setUp()
        user = models.User.objects.create_user(self.login, '%s@example.com' % self.login)
        user.is_superuser = True
        user.save()
        self.user = user


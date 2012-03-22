from datetime import datetime
import os
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _

class VideoManager(models.Manager):
    def videos_for_object(self, obj):
        object_type = ContentType.objects.get_for_model(obj)
        return self.filter(content_type__pk=object_type.id,
                           object_id=obj.id)

class Video(models.Model):

    objects = VideoManager()

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    creator = models.ForeignKey(User, related_name="created_videos", verbose_name=_('creator'))
    url = models.CharField(_('url'), max_length=255)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)


    class Meta:
        ordering = ['-created']
        permissions = (
            ('delete_foreign_videos', 'Can delete foreign videos'),
        )

    def __unicode__(self):
        return '%s - %s' % (self.creator.username, self.url)


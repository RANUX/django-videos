from djangovideos.models import Video
from django.contrib.contenttypes import generic

class VideoInlines(generic.GenericStackedInline):
    model = Video
    extra = 1

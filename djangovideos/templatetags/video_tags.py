from django.template import Library, Node, Variable
from django.template.loader import get_template
from django.template import Context
from django.core.urlresolvers import reverse
from djangovideos.views import add_url_for_obj
from djangovideos.forms import VideoForm
from djangovideos.models import Video

register = Library()

@register.inclusion_tag('djangovideos/add_form.html', takes_context=True)
def video_form(context, obj):
    """
    Renders a "upload video" form.

    The user must own ``videos.add_video permission`` to add
    videos.
    """
    try:
        perm = context['user'].has_perm('djangovideos.add_video')
    except Exception:
        # gae
        perm = not context['user'].is_anonymous()

    if perm:
        return {
            'form': VideoForm(),
            'form_url': add_url_for_obj(obj),
            'next': context['request'].build_absolute_uri(),
        }
    else:
        return {
            'form': None,
        }

@register.inclusion_tag('djangovideos/delete_link.html', takes_context=True)
def video_delete_link(context, video):
    """
    Renders a html link to the delete view of the given video. Returns
    no content if the request-user has no permission to delete videos.

    The user must own either the ``videos.delete_video`` permission
    and is the creator of the video, that he can delete it or he has
    ``videos.delete_foreign_videos`` which allows him to delete all
    videos.
    """
    if context['user'].has_perm('djangovideos.delete_foreign_videos') \
       and (context['user'] == video.creator or \
           context['user'].has_perm('videos.delete_video')):
        return {
            'next': context['request'].build_absolute_uri(),
            'delete_url': reverse('delete_video', kwargs={'video_pk': video.pk})
        }
    return {'delete_url': None,}



class VideosForObjectNode(Node):
    def __init__(self, obj, var_name):
        self.obj = obj
        self.var_name = var_name

    def resolve(self, var, context):
        """Resolves a variable out of context if it's not in quotes"""
        if var[0] in ('"', "'") and var[-1] == var[0]:
            return var[1:-1]
        else:
            return Variable(var).resolve(context)

    def render(self, context):
        obj = self.resolve(self.obj, context)
        var_name = self.resolve(self.var_name, context)
        context[var_name] = Video.objects.videos_for_object(obj)
        return ''

@register.tag
def get_videos_for(parser, token):
    """
    Resolves videos that are attached to a given object. You can specify
    the variable name in the context the videos are stored using the `as`
    argument. Default context variable name is `videos`.

    Syntax::

        {% get_videos_for obj %}
        {% for att in videos %}
            {{ att }}
        {% endfor %}

        {% get_videos_for obj as "my_videos" %}

    """
    def next_bit_for(bits, key, if_none=None):
        try:
            return bits[bits.index(key)+1]
        except ValueError:
            return if_none

    bits = token.contents.split()
    args = {
        'obj': next_bit_for(bits, 'get_videos_for'),
        'var_name': next_bit_for(bits, 'as', '"videos"'),
    }
    return VideosForObjectNode(**args)

class VideoNode(Node):
    def __init__(self, obj, size):
        self.obj = obj
        self.size = size

    def resolve(self, var, context):
        """Resolves a variable out of context if it's not in quotes"""
        if var[0] in ('"', "'") and var[-1] == var[0]:
            return var[1:-1]
        else:
            return Variable(var).resolve(context)

    def render(self, context):
        obj = self.resolve(self.obj, context)
        width, height = self.size.split('x')
        t = get_template('djangovideos/video.html')
        return t.render(Context(dict(object=obj, width=width, height=height)))

@register.tag
def embed_video(parser, token):
    """
    Resolves videos that are attached to a given object. You can specify
    the variable name in the context the videos are stored using the `as`
    argument. Default context variable name is `videos`.

    Syntax::

        {% video obj %}

    """

    size = '640x505'
    bits = token.contents.split()
    if len(bits) == 3:
        name, obj, size = bits
    else:
        name, obj = bits
    args = {
        'obj': obj,
        'size': size,
    }
    return VideoNode(**args)

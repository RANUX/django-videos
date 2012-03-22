from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from djangovideos.models import Video

class VideoForm(forms.ModelForm):
    url = forms.CharField(label=_('Video url'))

    def clean_url(self):
        data = self.cleaned_data['url'].strip()
        if 'src=' in data:
            data = data.split('src=', 1)[1]
            data = data.split(' ')[0]
            data = data.strip(''' '" ''')
        if data.startswith('http://vimeo.com/'):
            splited = data.split('/')
            clip_id = splited[-1]
            if clip_id.isdigit():
                data = ('http://vimeo.com/moogaloop.swf?'
                        'clip_id=%s&amp;server=vimeo.com&amp;'
                        'show_title=1&amp;show_byline=1&amp;'
                        'show_portrait=0&amp;color=&amp;'
                        'fullscreen=1') % clip_id
        elif data.startswith('http://www.dailymotion.com/video/'):
            data = data.split('_')[0]
            data = data.replace('http://www.dailymotion.com/video/',
                                'http://www.dailymotion.com/swf/video/')
        elif data.startswith('http://www.youtube.com/watch?v='):
            data = data.replace('http://www.youtube.com/watch?v=',
                                'http://www.youtube.com/v/')
        if data.startswith('http'):
            return data
        else:
            raise forms.ValidationError("No valid link found")

    class Meta:
        model = Video
        fields = ('url',)

    def save(self, request, obj, *args, **kwargs):
        self.instance.creator = request.user
        self.instance.content_type = ContentType.objects.get_for_model(obj)
        self.instance.object_id = obj.id
        super(VideoForm, self).save(*args, **kwargs)

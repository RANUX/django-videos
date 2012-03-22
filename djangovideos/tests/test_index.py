# -*- coding: utf-8 -*-
from djangovideos.tests.functionnal import *
from djangovideos.models import Video

class TestYoutubeUrl(UserWebTest):

    input = "http://www.youtube.com/watch?v=ZFeHUdEQ1Zs"
    output = '<param name="movie" value="http://www.youtube.com/v/ZFeHUdEQ1Zs'

    def test_index(self):
        resp = self.app.get(reverse('index'), user='user1')
        resp.mustcontain('submit')
        form = resp.form
        form['url'] = self.input
        resp = form.submit()
        resp = resp.follow()
        resp.mustcontain(self.output)

class TestYoutubeObject(TestYoutubeUrl):
    input = '<object width="640" height="505"><param name="movie" value="http://www.youtube.com/v/ZFeHUdEQ1Zs&hl=fr_FR&fs=1&"></param><param name="allowFullScreen" value="true"></param><param name="allowscriptaccess" value="always"></param><embed src="http://www.youtube.com/v/ZFeHUdEQ1Zs&hl=fr_FR&fs=1&" type="application/x-shockwave-flash" allowscriptaccess="always" allowfullscreen="true" width="640" height="505"></embed></object>'


class TestDaylimotionUrl(TestYoutubeUrl):
    input = 'http://www.dailymotion.com/video/xdhrzy_eiffel-tower-jump-skater-breaks-rec_news'
    output = '<param name="movie" value="http://www.dailymotion.com/swf/video/xdhrzy"'

class TestDaylimotionObject(TestDaylimotionUrl):
    input = '<object width="480" height="360"><param name="movie" value="http://www.dailymotion.com/swf/video/xdhrzy" /></param><param name="allowFullScreen" value="true" /></param><param name="allowScriptAccess" value="always" /></param><embed type="application/x-shockwave-flash" src="http://www.dailymotion.com/swf/video/xdhrzy" width="480" height="360" allowfullscreen="true" allowscriptaccess="always"></embed></object></embed></object>'

class TestVimeoUrl(TestYoutubeUrl):
    input = 'http://vimeo.com/2237879'
    output = '<param name="movie" value="http://vimeo.com/moogaloop.swf?clip_id=2237879&amp;'

class TestVimeoObject(TestVimeoUrl):
    input = '''<object width="400" height="267"><param name="allowfullscreen" value="true" /><param name="allowscriptaccess" value="always" /><param name="movie" value="http://vimeo.com/moogaloop.swf?clip_id=2237879&amp;server=vimeo.com&amp;show_title=1&amp;show_byline=1&amp;show_portrait=0&amp;color=&amp;fullscreen=1" /><embed src="http://vimeo.com/moogaloop.swf?clip_id=2237879&amp;server=vimeo.com&amp;show_title=1&amp;show_byline=1&amp;show_portrait=0&amp;color=&amp;fullscreen=1" type="application/x-shockwave-flash" allowfullscreen="true" allowscriptaccess="always" width="400" height="267"></embed></object><p><a href="http://vimeo.com/2237879">Bob's Mega ramp</a> from <a href="http://vimeo.com/cexa">Cexa </a> on <a href="http://vimeo.com">Vimeo</a>.</p>'''


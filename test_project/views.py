# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from django.db.models.loading import get_model
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext, ugettext_lazy as _
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required

def add_form(request):
    context = dict(
            object=request.user
            )
    return render_to_response('index.html', context,
                              RequestContext(request))


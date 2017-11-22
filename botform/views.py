# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render


def index_view(request):
    """
    Show botform default page
    """
    return render(request, 'botform/index.html', {})
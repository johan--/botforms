# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from .models  import Forms


def index_view(request):
    """
    Show form default page
    """
    forms = Forms.objects.all()
    return render(request, 'botform/index.html', {'forms': forms})


def create_form_view(request):
    """
    Add new form page
    """
    return render(request, 'botform/create.html',{})
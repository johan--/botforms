# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models  import Forms


@login_required()
def index_view(request):
    """
    Show form default page
    """
    forms = Forms.objects.all()
    return render(request, 'forms/index.html', {'forms': forms})

@login_required()
def create_form_view(request):
    """
    Add new form page
    """
    return render(request, 'forms/create.html',{})

@login_required()
def manage_form_view(request, pk):
    """
    Manage form page
    """
    return render(request, 'forms/manage.html',{})


def share_form_view(request, pk):
    """
    Open form page: Share form page
    """
    return render(request, 'forms/share.html',{})
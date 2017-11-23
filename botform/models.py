# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Forms(models.Model):
    title = models.CharField(max_length=140)
    description = models.TextField(blank=True, null=True)
    schema = models.TextField(blank=True, null=True, help_text="JSON rep of the form schema")
    
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


class Submissions(models.Model):
    form = models.ForeignKey(Forms, related_name="submissions")
    data = models.TextField(blank=True, null=True, help_text="JSON rep of user input")

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
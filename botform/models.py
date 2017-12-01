# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save

from .tasks import generate_pdf

class Forms(models.Model):
    title = models.CharField(max_length=140)
    description = models.TextField(blank=True, null=True)
    schema = models.TextField(blank=True, null=True, help_text="JSON rep of the form schema")

    # PDF Output fields
    generate_pdf = models.BooleanField(default=False)
    pdf_output_template = models.TextField(blank=True, null=True)

    # Webhook url
    webhook_url = models.URLField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


class Submissions(models.Model):
    form = models.ForeignKey(Forms, related_name="submissions")
    data = models.TextField(blank=True, null=True, help_text="JSON rep of user input")
    pdf = models.URLField(max_length=400, blank=True, null=True, help_text='PDF Output URL')
    reference = models.CharField(max_length=45, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

def on_new_submission(sender, instance, created, **kwargs):
    try:
        if created and instance.form.generate_pdf:
            submission_id = instance.pk
            generate_pdf.delay({'submission_id': submission_id})
            if instance.form.webhook_url:
                notify_webhook.delay({
                    'submission_id': submission_id,
                    'webhook_url': instance.form.webhook_url
                })
    except Exception as ex:
        print(str(ex))
post_save.connect(on_new_submission, sender=Submissions)

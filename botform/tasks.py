from celery import task
from xhtml2pdf import pisa
from slugify import slugify
from django.conf import settings
from django.forms.models import model_to_dict
from django.template import loader, Context, Template
import json
import os

def convertHtmlToPdf(sourceHtml, outputFilename):
    """
    Utility function
    """
    pdf_generated = True
    with open(outputFilename, "w+b") as resultFile:
        pisaStatus = pisa.CreatePDF(sourceHtml, dest=resultFile)
        if pisaStatus.err:
            pdf_generated = False
    
    return pdf_generated

@task
def generate_pdf(payload):
    """
    Generate pdf based on submission
    """
    from botform.models import Submissions

    submission_id = payload.get('submission_id')
    submission_obj = Submissions.objects.get(pk=submission_id)
    form_obj = submission_obj.form
    submission_data = json.loads(submission_obj.data)

    form_slug = slugify(form_obj.title)
    domain = os.environ.get('DOMAIN')
    file_name = '%s/%s-%s.pdf' % (settings.MEDIA_ROOT, form_slug, submission_id)
    pdf_url = 'http://%s%s/%s-%s.pdf' % (domain, settings.MEDIA_URL, form_slug, submission_id)

    context = Context(
        {
            'FORM': model_to_dict(form_obj),
            'SUBMISSION': model_to_dict(submission_obj),
            'SUBMISSION_DATA': submission_data
        }
    )
    pdf_output_template = form_obj.pdf_output_template
    template = Template(str(pdf_output_template))
    source_html = template.render(context)
    pdf_generated = convertHtmlToPdf(source_html, file_name)
    if pdf_generated:
        submission_obj.pdf = pdf_url
        submission_obj.save()


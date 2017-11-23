from celery import task
from xhtml2pdf import pisa
from slugify import slugify
from django.conf import settings

def convertHtmlToPdf(sourceHtml, outputFilename):
    """
    Utility function
    """
    with open(outputFilename, "w+b") as resultFile:
        pisaStatus = pisa.CreatePDF(sourceHtml, dest=resultFile)
        return pisaStatus.err

@task
def generate_pdf(payload):
    """
    Generate pdf based on submission
    """
    from botform.models import Submissions

    submission_id = payload.get('submission_id')
    submission_obj = Submissions.objects.get(pk=submission_id)
    form_obj = submission_obj.form

    form_slug = slugify(form_obj.title)
    file_name = '%s/%s-%s.pdf' % (settings.MEDIA_ROOT, form_slug, submission_id)
    source_html = form_obj.pdf_output_template
    convertHtmlToPdf(source_html, file_name)

import json
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route, api_view

from .models import Forms, Submissions
from .serializers import FormsSer, SubmissionsSer, FormsWithSubmissionsSer


class FormsViewSet(viewsets.ModelViewSet):
    """
    Forms API
    """
    queryset = Forms.objects.all()
    serializer_class = FormsSer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return FormsWithSubmissionsSer
        return FormsSer

    @detail_route(methods=['PUT',])
    def design(self, request, pk):
        form_obj = self.get_object()
        data = request.data
        # Save design changes
        form_obj.schema = data.get('schema')
        form_obj.save()
        ser_data = FormsSer(form_obj, many=False).data
        return Response(ser_data)

    @detail_route(methods=['PUT',])
    def pdf_output_setting(self, request, pk):
        form_obj = self.get_object()
        data = request.data
        # Save output changes
        form_obj.generate_pdf = data.get('generate_pdf')
        form_obj.pdf_output_template = data.get('pdf_output_template')
        form_obj.save()
        ser_data = FormsSer(form_obj, many=False).data
        return Response(ser_data)

class SubmissionsViewSet(viewsets.ModelViewSet):
    """
    Form submission API
    """
    queryset = Submissions.objects.all()
    serializer_class = SubmissionsSer

    def delete(self, request):
        return Response('Method not allowed', 403)

@api_view(http_method_names=['GET', ])
def grid_details(request, pk):
    form_obj = Forms.objects.get(pk=pk)
    components = json.loads(form_obj.schema).get('components', [])
    data = {
        '_id': form_obj.id,
        'components': components,
        'title': form_obj.title,
        'type': 'form',
        'display': 'form',
        'path': 'form',
        'name': form_obj.title
    }
    return Response(data)

@api_view(http_method_names=['GET', ])
def grid_submissions(request, pk):
    form_obj = Forms.objects.get(pk=pk)
    response = []
    submissions = form_obj.submissions.all()
    for submission in submissions:
        form_data = {
            'form': form_obj.id
        }
        form_data.update(json.loads(submission.data))
        response.append(form_data)
    return Response(response)
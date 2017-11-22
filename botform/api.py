from rest_framework import viewsets

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
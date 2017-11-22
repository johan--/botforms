from rest_framework import serializers

from .models import Forms, Submissions


class FormsSer(serializers.ModelSerializer):
    class Meta:
        model = Forms
        fields = "__all__"

class SubmissionsSer(serializers.ModelSerializer):
    class Meta:
        model = Submissions
        fields = "__all__"

class FormsWithSubmissionsSer(serializers.ModelSerializer):
    submissions = SubmissionsSer(many=True)
    
    class Meta:
        model = Forms
        fields = "__all__"
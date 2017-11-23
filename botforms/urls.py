"""botform URL Configuration

"""
from django.conf.urls import url, include
from rest_framework import routers

from botform import api as form_api

router = routers.DefaultRouter()
router.register(r'forms', form_api.FormsViewSet)
router.register(r'submissions', form_api.SubmissionsViewSet)

urlpatterns = [
    url(r'^api/v1/', include(router.urls)),
    url(r'^api/v1/forms/(?P<pk>\d+)/details/?$', form_api.grid_details),
    url(r'^api/v1/forms/(?P<pk>\d+)/details/submission/?$', form_api.grid_submissions),
    url(r'^', include('botform.urls')),
    url(r'^accounts/', include('allauth.urls')),
]

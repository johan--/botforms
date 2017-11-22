"""botform URL Configuration

"""
from django.conf.urls import url, include
from rest_framework import routers

from botform import api as form_api

router = routers.DefaultRouter()
router.register(r'forms', form_api.FormsViewSet)

urlpatterns = [
    url(r'^api/v1/', include(router.urls)),
    url(r'^', include('botform.urls')),
]

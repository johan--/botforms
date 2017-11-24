from django.conf.urls import url, include

from .views import index_view, create_form_view, \
    manage_form_view, share_form_view, success_feedback_view

urlpatterns = [
    url(r'^', include([
        url(r'^$', index_view, name='index'),
        url(r'^create/$', create_form_view, name='create_form'),
        url(r'^(?P<pk>\d+)/manage/$', manage_form_view, name='manage_form'),
        url(r'^(?P<pk>\d+)/share/$', share_form_view, name='share_form'),
        url(r'^success/$', success_feedback_view, name='success'),
    ], namespace='form')),
]
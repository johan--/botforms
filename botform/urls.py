from django.conf.urls import url, include

from .views import index_view, create_form_view

urlpatterns = [
    url(r'^', include([
        url(r'^$', index_view, name='index'),
        url(r'^create/', create_form_view, name='create_form'),
    ], namespace='form')),
]
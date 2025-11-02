from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('test-email/', views.test_email_config, name='test_email'),
    path('projects/learnhub/', views.learnhub_demo, name='learnhub_demo'),
    path('projects/bookclass/', views.bookclass_demo, name='bookclass_demo'),
]
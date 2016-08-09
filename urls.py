from avi import views
from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', views.TutorialModelList.as_view(), name='tutorialmodel-list'),
)

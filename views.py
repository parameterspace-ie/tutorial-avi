from avi.models import TutorialModel
from avi.serializers import TutorialModelSerializer
from rest_framework import generics
from rest_framework.renderers import JSONRenderer, AdminRenderer

class TutorialModelList(generics.ListCreateAPIView):
    queryset = TutorialModel.objects.all()
    serializer_class = TutorialModelSerializer
    renderer_classes = (JSONRenderer, AdminRenderer)
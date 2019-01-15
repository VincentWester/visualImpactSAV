from rest_framework import generics
from visualImpactSAV.models import SAV_file
from visualImpactSAV.serializers.home_page_serializers import SAV_filesSerializer

class SAV_fileList(generics.ListAPIView):
    queryset = SAV_file.objects.all()
    serializer_class = SAV_filesSerializer
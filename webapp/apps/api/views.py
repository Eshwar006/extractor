# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response

from webapp.apps.api.service import ObjectExtractor


class ExtractObjects(APIView):

    def post(self, request):
        data = request.data
        response = ObjectExtractor().get_objects(data)
        return Response(data=response, status=200)


class Ruok(APIView):

    def get(self, request):
        return Response(data='imok', status=200)

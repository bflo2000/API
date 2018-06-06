from rest_framework import generics, views
from rest_framework.decorators import parser_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.reverse import reverse

class app_view(views.APIView):

	def get(self,request):
        return Response(template_name='index.html')
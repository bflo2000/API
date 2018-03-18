from rest_framework import generics, views
from Amazon.models import Amazon_Variation
from Amazon.serializers import Amazon_Variation_Serializer
from rest_framework.decorators import parser_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.reverse import reverse
import csv

class amazon_variation_list(generics.ListCreateAPIView):
    queryset = Amazon_Variation.objects.all()
    serializer_class = Amazon_Variation_Serializer

class amazon_variation_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Amazon_Variation.objects.all()
    serializer_class = Amazon_Variation_Serializer

class amazon_variation_upload(views.APIView):
    renderer_classes = (TemplateHTMLRenderer,)

    def get(self,request):
        return Response(template_name='upload_csv_amazon.html')

    def post(self, request):
        try:
            csv_file = request.FILES['csv_file']

            if not csv_file.name.endswith('.csv'):
                print ('File is not a CSV.')
                return Response(template_name='failure_csv_amazon.html')

            file_data = csv_file.read().decode("utf-8")  
            lines = file_data.split("\n")
            reader = csv.DictReader(lines, delimiter=',', quotechar='|')

            if (self.consume_csv(reader)):
                print ('is')
            else:
                print ('not')
                return Response(template_name='failure_csv_amazon.html')

            return Response(template_name='success_csv_amazon.html')
        
        except Exception as error:
            print (error)
            return Response(template_name='failure_csv_amazon.html')

    def consume_csv(self, reader):        

	    for row in reader:
	        try:
	            serializer = Amazon_Variation_Serializer(data=row)
	            if serializer.is_valid():
	                serializer.save()
	            else:
	                print (serializer.errors)
	                return False
	                
	        except Exception as error:
	            print(error)
	            return False

	    return True
from rest_framework import generics, views
from Images.models import Image
from Images.serializers import ImageSerializer
from rest_framework.decorators import parser_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.reverse import reverse
import csv

class image_list(generics.ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

class image_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

class image_upload(views.APIView):
    #parser_classes = (FileUploadParser,)
    renderer_classes = (TemplateHTMLRenderer,)

    def get(self,request):
        return Response(template_name='upload_csv.html')

    def post(self, request):
        try:
            csv_file = request.FILES['csv_file']

            if not csv_file.name.endswith('.csv'):
                print ('File is not a CSV.')
                return Response(template_name='failure_csv.html')

            file_data = csv_file.read().decode("utf-8")  
            lines = file_data.split("\n")
            reader = csv.DictReader(lines, delimiter=',', quotechar='|')
            '''
            if not (self.verify_keys(reader)):
                print ("key failure")
                return Response(template_name='failure_csv.html')
            '''
            if (self.consume_csv(reader)):
                print ('is')
            else:
                print ('not')
                return Response(template_name='failure_csv.html')

            return Response(template_name='success_csv.html')
        
        except Exception as error:
            print (error)
            return Response(template_name='failure_csv.html')

    def consume_csv(self, reader):        

        for row in reader:
            try:
               
                serializer = ImageSerializer(data=row)
                if serializer.is_valid():
                    serializer.save()
                    return True
                print (serializer.errors)
                return False
            except Exception as error:
                print(error)
                return False

    def validate_fields(self, row):
        return True

    def verify_keys(self, reader):
        keys = reader.fieldnames
        schema = ['sku', 'name', 'height', 'width', 'description', 'url', 'path',
            'category', 'collection', 'sub_collection']

        if keys != schema:
            return False

        return True

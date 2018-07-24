from rest_framework import generics, views, status
from Images.models import Image
from Images.serializers import ImageSerializer
from rest_framework.decorators import parser_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.reverse import reverse
import csv, glob, datetime

class image_list(generics.ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

class image_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

class image_upload(views.APIView):

    def get(self,request):
        return Response(template_name='upload_csv.html')
           
    def post(self, request):

        try:
            csv_file = request.data['csv_file']

            if not csv_file.name.endswith('.csv'):
                data = "The file you have provided is not a .csv file. Please upload a .csv file."
                response_status = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
                return Response(data, response_status)

            file_data = csv_file.read().decode("utf-8")  
            lines = file_data.split("\n")
            reader = csv.DictReader(lines)

            reader_response = consume_csv(reader, False)

            if (reader_response[0]):
                response_status = status.HTTP_202_ACCEPTED
                response_data = reader_response[1]
                return Response(response_data, response_status)
            else:
                response_status = status.HTTP_400_BAD_REQUEST
                response_data = reader_response[1]
                return Response(response_data, response_status)
       
        except Exception as error:
            data = "CSV required in upload."
            response_status = status.HTTP_400_BAD_REQUEST
            return Response(data, response_status)

    def put(self, request):

        try:
            csv_file = request.FILES['csv_file']

            if not csv_file.name.endswith('.csv'):
                print ('File is not a CSV.')
                return Response(template_name='failure_csv.html')

            file_data = csv_file.read().decode('utf-8')
            lines = file_data.split("\n")
            reader = csv.DictReader(lines)
            if (consume_csv(reader, True)):
                print ('is')
            else:
                print ('not')
                return Response(template_name='failure_csv.html')

            return Response(template_name='success_csv.html')

        except Exception as error:
            print (error)
            return Response(template_name='failure_csv.html')

class images_sftp(views.APIView):

    def get(self,request):
        return Response(template_name='upload_csv_amazon.html')

    def post(self, request):

        try:

            for infile in glob.glob("ftp/Images/*.csv"):

                with open(infile, 'r') as csvfile:
                    reader = csv.DictReader(csvfile)
                    consume_csv(reader, False)

            return Response(template_name='success_csv_amazon.html')

        except Exception as error:
            print (error)
            return Response(template_name='failure_csv_amazon.html')

    def put(self, request):

        try:

            for infile in glob.glob("ftp/Images/*.csv"):

                with open(infile, 'r') as csvfile:
                    reader = csv.DictReader(csvfile)
                    consume_csv(reader, True)

            return Response(template_name='success_csv_amazon.html')

        except Exception as error:
            print (error)
            return Response(template_name='failure_csv_amazon.html')

def consume_csv(reader, partial):

    '''
    time = datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
    filename = "ftp/Images_error_log_" + time +  ".txt"
    error_log = open(filename, 'a+')
    '''    
    log = ''

    for row in reader:
        try:
            item_sku = row['sku']
        except Exception as e:
            log = "Please format a sku field."
            return (False, log)
        
	    #remove any blank values
        row = {k: v for k, v in row.items() if v is not ''}

        # if partial, update records
        if partial:
            try:
                image = Image.objects.get(sku=item_sku)
            except Exception as error:
                error_string = "Couldn't find image sku: " + item_sku
                error_log.write(error_string)
                continue
            try:
                serializer = ImageSerializer(image, data=row, partial=True)
                if serializer.is_valid():
                    serializer.save()
                else:
                    error_string = item_sku + " "

                    for key, value in serializer.errors.items():
                        error_string = error_string + key + ": " + value[0]

                    error_log.write(error_string)
                    continue

            except Exception as error:
                error_string = item_sku + " " + error
                error_log.write(error_string)
                continue
        else:
            try:
                serializer = ImageSerializer(data=row)
                if serializer.is_valid():
                    serializer.save()
                    log = log + item_sku + ' added successfully.\n'
                else:
                    error_string = item_sku + " "

                    for key, value in serializer.errors.items():
                        log = log + item_sku + ' : '+ key + ": " + value[0] + '\n'
                    continue

            except Exception as error:
                log = log + item_sku + " " + error + '\n'
                continue

    '''
    response_status = status.HTTP_202_ACCEPTED
    data = error_string 
    return Response(data, response_status)
    '''
    return (True, log)
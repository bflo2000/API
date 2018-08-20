from django.db import IntegrityError
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
            print(error)
            data = "CSV required in upload."
            response_status = status.HTTP_400_BAD_REQUEST
            return Response(data, response_status)

    def delete(self, request):
        
        log = ""
        
        try:            
            csv_file = request.data['csv_file']

            if not csv_file.name.endswith('.csv'):
                data = "The file you have provided is not a .csv file. Please upload a .csv file."
                response_status = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
                return Response(data, response_status)

            file_data = csv_file.read().decode("utf-8")  
            lines = file_data.split("\n")
            reader = csv.DictReader(lines)

            for row in reader:
                try:
                    sku = row['sku_delete']
                    try:
                        image = Image.objects.get(sku=sku)
                        image.delete()
                        log = log + sku + ' : ' + 'Deleted successfully.' + '\n'
                    except Image.DoesNotExist:
                        log = log + sku + ' : ' + 'Not found.' + '\n'
                        continue
                except:
                    response_message = "Please format an sku_delete field. This is to prevent any accidental deletes."
                    response_status = status.HTTP_400_BAD_REQUEST
                    return Response(response_message, response_status)  

            response_status = status.HTTP_202_ACCEPTED
            return Response(log, response_status)

        except Exception as error:
            data = "CSV required in upload."
            response_status = status.HTTP_400_BAD_REQUEST
            return Response(data, response_status)

    def patch(self, request):
        try:
            csv_file = request.data['csv_file']

            if not csv_file.name.endswith('.csv'):
                data = "The file you have provided is not a .csv file. Please upload a .csv file."
                response_status = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
                return Response(data, response_status)

            file_data = csv_file.read().decode("utf-8")  
            lines = file_data.split("\n")
            reader = csv.DictReader(lines)

            reader_response = consume_csv(reader, True)

            if (reader_response[0]):
                response_status = status.HTTP_202_ACCEPTED
                response_data = reader_response[1]
                return Response(response_data, response_status)
            else:
                response_status = status.HTTP_400_BAD_REQUEST
                response_data = reader_response[1]
                return Response(response_data, response_status)
        except IntegrityError as e:
            print(e.message)

        except Exception as error:
            print(error)
            data = "Error during upload"
            response_status = status.HTTP_400_BAD_REQUEST
            return Response(data, response_status)

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

    log = ''

    for row in reader:
        try:
            sku = row['sku']
        except:
            log = "Please format a sku field."
            return (False, log)
        
	#remove any blank values
        row = {k: v for k, v in row.items() if v is not ''}
        
        # if partial, update records
        if partial:
            try:
                image = Image.objects.get(sku=sku)
            except Image.DoesNotExist:
                log = log + sku + ' : ' + 'Not found.' + '\n'
                continue

            # special functionality for changing the sku
            #if row['new_sku']:
            #    row['sku'] = row['new_sku'] 
            
            try:
                serializer = ImageSerializer(image, data=row, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    log = log + sku + ' updated successfully.\n'
                else:
                    for key, value in serializer.errors.items():
                        log = log + sku  + ": " + value[0] + '\n'
                        
            except Exception as error:
                error_string = sku + " " + error
                error_log.write(error_string)
                continue
        else:
            try:
                serializer = ImageSerializer(data=row)
                if serializer.is_valid():
                    serializer.save()
                    log = log + sku + ' added successfully.\n'
                else:
                    for key, value in serializer.errors.items():
                        log = log + sku + ' : '+ key + ": " + value[0] + '\n'
                    continue

            except Exception as error:
                log = log + sku + " " + error + '\n'
                continue

    return (True, log)

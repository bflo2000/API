from rest_framework import generics, views, status
from Images.models import Image
from Images.serializers import ImageSerializer
from rest_framework.response import Response
import csv
import glob


class ImageList(generics.ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class ImageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class ImageUpload(views.APIView):

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

            if reader_response[0]:
                response_status = status.HTTP_202_ACCEPTED
                response_data = reader_response[1]
                return Response(response_data, response_status)
            else:
                response_status = status.HTTP_400_BAD_REQUEST
                response_data = reader_response[1]
                return Response(response_data, response_status)
       
        except Exception as error:
            data = "CSV required in upload."
            print(error)
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

            reader_response = consume_csv(reader, True)

            if reader_response[0]:
                response_status = status.HTTP_202_ACCEPTED
                response_data = reader_response[1]
                return Response(response_data, response_status)
            else:
                response_status = status.HTTP_400_BAD_REQUEST
                response_data = reader_response[1]
                return Response(response_data, response_status)

        except Exception as error:
            data = "CSV required in upload."
            print(error)
            response_status = status.HTTP_400_BAD_REQUEST
            return Response(data, response_status)


class ImagesSFTP(views.APIView):

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
    mutations = 0
    errors = 0

    for row in reader:
        try:
            item_sku = row['sku']
        except Exception as e:
            log = "Please format a sku field."
            return False, log

        if not partial:
            try:
                row['collection']
            except Exception as e:
                log = "Please format a collection field."
                return False, log

        # if partial, update records
        if partial:

            # remove any blank values
            row = {k: v for k, v in row.items() if v is not ''}

            try:
                image = Image.objects.get(sku=item_sku)
            except Exception as error:
                log = log + "Couldn't find image sku: " + item_sku + '\n'
                errors += 1
                continue
            try:
                serializer = ImageSerializer(image, data=row, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    mutations += 1
                else:
                    error_string = item_sku + " "
                    errors += 1

                    for key, value in serializer.errors.items():
                        log = log + error_string + key + ": " + value[0] + '\n'
                    continue

            except Exception as error:
                log = log + item_sku + " " + error + '\n'
                errors += 1
                continue
        else:
            try:
                serializer = ImageSerializer(data=row)
                if serializer.is_valid():
                    serializer.save()
                    # log = log + item_sku + ' added successfully.\n'
                    mutations += 1
                else:
                    errors += 1

                    for key, value in serializer.errors.items():
                        log = log + item_sku + ' : '+ key + ": " + value[0] + '\n'
                    continue

            except Exception as error:
                errors += 1
                log = log + item_sku + " " + error + '\n'
                continue

    log = 'Mutations: ' + str(mutations) + '\n' + 'Errors: ' + str(errors) + '\n' + log
    return True, log

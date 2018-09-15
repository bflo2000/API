from rest_framework import generics
from rest_framework import views
from rest_framework import status
from Amazon.models import Amazon_Variation
from Amazon.serializers import Amazon_Variation_Serializer
from Images.models import Image
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
import csv
import glob
from django.db import IntegrityError


class AmazonVariationList(generics.ListCreateAPIView):
    queryset = Amazon_Variation.objects.all()
    serializer_class = Amazon_Variation_Serializer


class AmazonVariationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Amazon_Variation.objects.all()
    serializer_class = Amazon_Variation_Serializer


class AmazonVariationUpload(views.APIView):

    def get(self,request):
        return Response(template_name='upload_csv_amazon.html')

    def post(self, request):
        try:
            csv_file = request.FILES['csv_file']

            if not csv_file.name.endswith('.csv'):
                data = "The file you have provided is not a .csv file. Please upload a .csv file."
                response_status = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
                return Response(data, response_status)

            reader = csv.DictReader(self.decode_utf8(csv_file))

            if (self.consume_csv(reader)):
                print ('is')
            else:
                print ('not')
                return Response(template_name='failure_csv_amazon.html')

            return Response(template_name='success_csv_amazon.html')

        except Exception as error:
            print (error)
            return Response(template_name='failure_csv_amazon.html')
    
    def delete(self, request):
        
        csv_file = request.FILES['csv_file']

        if not csv_file.name.endswith('.csv'):
            data = "The file you have provided is not a .csv file. Please upload a .csv file."
            response_status = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
            return Response(data, response_status)

        reader = csv.DictReader(self.decode_utf8(csv_file))
        
        for row in reader:
            try:
                item_sku = row['item_sku_delete']
                obj = Amazon_Variation.objects.get(item_sku=item_sku)
                obj.delete()
            except Exception as e:
                print (e)
                continue    
                
        return Response(template_name='success_csv_amazon.html')

    def decode_utf8(self, input_iterator):
        
        for l in input_iterator:
            yield l.decode('utf-8')


class AmazonVariationSFTP(views.APIView):

    def post(self, request):
        try:
            for infile in glob.glob("ftp/Amazon/*.csv"):

                with open(infile, 'r') as csvfile:
                    reader = csv.DictReader(csvfile)
                    consume_csv(reader, False)

            return Response(template_name='success_csv_amazon.html')

        except Exception as error:
            print (error)
            return Response(template_name='failure_csv_amazon.html')
    
    def put(self, request):
        try:

            for infile in glob.glob("ftp/Amazon/*.csv"):

                with open(infile, 'r') as csvfile:
                    reader = csv.DictReader(csvfile)
                    consume_csv(reader, True)

            return Response(template_name='success_csv_amazon.html')

        except Exception as error:
            print (error)
            return Response(template_name='failure_csv_amazon.html')

    def delete(self, request):
        
        csv_file = request.FILES['csv_file']

        if not csv_file.name.endswith('.csv'):
            print ('File is not a CSV.')
            return Response(template_name='failure_csv_amazon.html')
        reader = csv.DictReader(decode_utf8(csv_file))
        for row in reader:
            try:
                item_sku = row['item_sku_delete']
                obj = Amazon_Variation.objects.get(item_sku=item_sku)
                obj.delete()
            except Exception as e:
                print (e)
                continue    
                
        return Response(template_name='success_csv_amazon.html')


def consume_csv(reader, partial):

    log = ''    

    for row in reader:

        try:
            item_sku = row['item_sku']
        except Exception:
            log = "Please format an item_sku field."
            return (False, log)

        if partial:
            try:
                variation = Amazon_Variation.objects.get(item_sku=item_sku)
            except Exception:
                log = log + "Couldn't find item sku: " + item_sku + '\n'
                continue
            try:
                serializer = Amazon_Variation_Serializer(variation, data=row, partial=True)
                if serializer.is_valid():
                    serializer.save()
                else:
                    error_string = item_sku + " "

                    for key, value in serializer.errors.items():
                        log = log + error_string + key + ": " + value[0] + '\n'
                    continue

            except Exception as error:
                log = log + item_sku + " " + error + '\n'
                continue             
        else:
            try:
                serializer = Amazon_Variation_Serializer(data=row)

                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                else:
                    for key, value in serializer.errors.items():
                        log = log + item_sku + ' : '+ key + ": " + value[0] + '\n'
                    continue

            except Exception as error:
                log = log + item_sku + " " + error + '\n'

    return True, log


class CategoryReportUpload(views.APIView):

    def get(self,request):
        return Response(template_name='upload_csv_amazon.html')

    def post(self, request):

        try:
            csv_file = request.FILES['csv_file']

            if not csv_file.name.endswith('.csv'):
                data = "The file you have provided is not a .csv file. Please upload a .csv file."
                response_status = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
                return Response(data, response_status)

            file_data = csv_file.read().decode("utf-8")
            lines = file_data.split("\n")
            reader = csv.DictReader(lines)

            reader_response = consume_category_report(reader)

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
            response_status = status.HTTP_400_BAD_REQUEST
            return Response(data, response_status)

    def delete(self, request):

        mutations = 0
        errors = 0
        csv_file = request.FILES['csv_file']

        if not csv_file.name.endswith('.csv'):
            data = "The file you have provided is not a .csv file. Please upload a .csv file."
            response_status = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
            return Response(data, response_status)

        reader = csv.DictReader(decode_utf8(csv_file))

        for row in reader:
            try:
                item_sku = row['item_sku_delete']
                obj = Amazon_Variation.objects.get(item_sku=item_sku)
                obj.delete()
                mutations += 1

            except Exception as e:
                data = "Please include an item_sku delete field."
                response_status = status.HTTP_400_BAD_REQUEST
                return Response(data, response_status)

        log = 'Mutations: ' + str(mutations) + '\n'
        response_status = status.HTTP_202_ACCEPTED
        return Response(log, response_status)

class category_report_sftp(views.APIView):

    def get(self,request):
        return Response(template_name='upload_csv_amazon.html')

    def post(self, request):

        try:

            for infile in glob.glob("ftp/Amazon/*.csv"):

                with open(infile, 'r') as csvfile:
                    reader = csv.DictReader(csvfile)
                    consume_category_report(reader)

            return Response(template_name='success_csv_amazon.html')

        except Exception as error:
            print (error)
            return Response(template_name='failure_csv_amazon.html')


def consume_category_report(reader):

    log = ''
    mutations = 0
    errors = 0

    for row in reader:

        data = {}

        if row['parent_child'] == 'parent':
            data['is_parent'] = True
            parent_sku = row['item_sku']
        else:
            if row['parent_sku'] == "":
                data['is_parent'] = True
                parent_sku = row['item_sku']
                data['is_unique'] = True
            else:
                data['is_parent'] = False
                parent_sku = row['parent_sku']

        # if parent does not exist, ignore
        parent_sku = parent_sku.replace("P", "")

        try:
            image = Image.objects.get(sku=parent_sku)
            data['is_orphan'] = False
            data['image_sku'] = image.sku

        except:
            data['is_orphan'] = True
            image = ""

        data['item_sku'] = row['item_sku']

        # retrieve the product description - and check unicode
        item_name = row['item_name']
        data['item_name'] = item_name

        try:
            test = item_name.encode('latin1')
        except:
            data['check_unicode'] = True

        # retrieve the product description - and check unicode
        product_description = row['product_description']
        data['product_description'] = product_description

        try:
            test = product_description.encode('latin1')
        except:
            data['check_unicode'] = True

        try:
            bullet1 = row['bullet_point1']
            if len(bullet1) > 200:
                bullet1 = bullet1[:200]
                data['check_bullets'] = True
        except Exception as error:
            bullet1 = ''

        data['bullet1'] = bullet1

        # retrieve the fifth bullet, as it may be a copy of the title - and check unicode
        try:
            bullet5 = row['bullet_point5']
            if len(bullet5) > 200:
                bullet5 = bullet5[:200]
                data['check_bullets'] = True

        except Exception as error:
            log = log + data['item_sku'] + " " + error + '\n'

        try:
            test = bullet5.encode('latin1')
        except:
            data['check_unicode'] = True

        # retrieve keywords, check unicode
        keywords = row['generic_keywords1']
        data['keywords'] = keywords

        try:
            test = keywords.encode('latin1')
        except:
            data['check_unicode'] = True

        try:
            data['asin'] = row['external_product_id']
        except:
            data['asin'] = ""

        try:
            data['currency'] = row['currency']
        except:
            data['currency'] = "usd"

        data['catalog_number'] = row['catalog_number']
        data['part_number'] = row['part_number']
        data['size_name'] = row['size_name']
        data['variation_theme'] = row['variation_theme']
        data['product_tax_code'] = row['product_tax_code']
        data['bullet2'] = row['bullet_point2']
        data['bullet3'] = row['bullet_point3']
        data['bullet4'] = row['bullet_point4']

        # set default price to 0.00 if empty
        if row['standard_price'] == "":
            data['price'] = '0.00'
        else:
            data['price'] = row['standard_price']

        try:
            serializer = Amazon_Variation_Serializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                mutations += 1
            else:
                errors += 1
                for key, value in serializer.errors.items():
                    log = log + data['item_sku'] + ' : ' + key + ": " + value[0] + '\n'

        except IntegrityError as e:
            errors += 1
            log = log + data['item_sku'] + ' : Integrity Error.' + '\n'
        except Exception as error:
            errors += 1
            log = log + data['item_sku'] + " " + error + '\n'

    log = 'Mutations: ' + str(mutations) + '\n' + 'Errors: ' + str(errors) + '\n' + log
    return True, log

def decode_utf8(input_iterator):
        
    for l in input_iterator:
        yield l.decode('utf-8')

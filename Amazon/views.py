from rest_framework import generics, views
from Amazon.models import Amazon_Variation
from Amazon.serializers import Amazon_Variation_Serializer
from Images.models import Image
from rest_framework.decorators import parser_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.reverse import reverse
import csv, glob, os
from decimal import Decimal
import datetime
import sizer_utils
from django.db import IntegrityError

class amazon_variation_list(generics.ListCreateAPIView):
	queryset = Amazon_Variation.objects.all()
	serializer_class = Amazon_Variation_Serializer

class amazon_variation_detail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Amazon_Variation.objects.all()
	serializer_class = Amazon_Variation_Serializer

class amazon_variation_upload(views.APIView):

	def get(self,request):
		return Response(template_name='upload_csv_amazon.html')

	def post(self, request):
		try:
			csv_file = request.FILES['csv_file']

			if not csv_file.name.endswith('.csv'):
				print ('File is not a CSV.')
				return Response(template_name='failure_csv_amazon.html')

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
			print ('File is not a CSV.')
			return Response(template_name='failure_csv_amazon.html')

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

class amazon_variation_sftp(views.APIView):

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
	time = datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
	filename = "ftp/error_log_" + time +  ".txt"
	number_of_records_written = 0

	error_log = open(filename, 'a+')

	for row in reader:

		try:
			item_sku = row['item_sku']
		except Exception as e:
			print('Exception', e, row)

		if partial == True:
			try:
				variation = Amazon_Variation.objects.get(item_sku=item_sku)
			except Exception as error:
				error_string = "Couldn't find Sku: " + item_sku
				error_log.write(error_string)
				continue
			try:
				serializer = Amazon_Variation_Serializer(variation, data=row, partial=True)
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
				serializer = Amazon_Variation_Serializer(data=row)

				if serializer.is_valid(raise_exception=True):
					serializer.save()
					number_of_records_written += 1
				else:
					error_log.write(serializer.errors[0])

			except Exception as error:
				string = "Validation error in sku: " + row['item_sku'] + '\n'
				error_log.write(string)

	print('Wrote ' + str(number_of_records_written) + ' records.')
	error_log.close()

	return True

class category_report_upload(views.APIView):
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
			#file_data = csv_file.read()
			lines = file_data.split("\n")
			reader = csv.DictReader(lines)

			if (consume_category_report(reader)):
				print ('is')
			else:
				print ('not')
				return Response(template_name='failure_csv_amazon.html')

			return Response(template_name='success_csv_amazon.html')

		except Exception as error:
			print (error)
			return Response(template_name='failure_csv_amazon.html')
	
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

	time = datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
	filename = "ftp/amazon_error_log_" + time +  ".txt"
	number_of_records_written = 0

	error_log = open(filename, 'a+')

	for row in reader:

		data = {}
		#print(row)
		#print(row['item_sku'])
		#exit()
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
			error_log.write(error)
			bullet1 = ''

		data['bullet1'] = bullet1

		# retrieve the fifth bullet, as it may be a copy of the title - and check unicode
		try:
			bullet5 = row['bullet_point5']
			if len(bullet5) > 200:
				bullet5 = bullet5[:200]
				data['check_bullets'] = True
		except Exception as error:
			error_log.write(error)

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
				number_of_records_written += 1
			else:
				error_log.write(serializer.errors[0])
		except IntegrityError as e:
			print(e)
		except Exception as error:
			string = "Validation error in sku: " + row['item_sku'] + '\n'
			error_log.write(string)
			#print(string)
			#print(error.detail)
	print('Wrote ' + str(number_of_records_written) + ' records.')
	error_log.close()

	return True

def decode_utf8(input_iterator):
		
    for l in input_iterator:
        yield l.decode('utf-8')

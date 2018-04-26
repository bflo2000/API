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
		print ('delete request received')

		return Response(template_name='success_csv_amazon.html')

	def decode_utf8(self, input_iterator):
		
		for l in input_iterator:
			yield l.decode('utf-8')

	def consume_csv(self, reader):

		time = datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
		filename = "ftp/error_log_" + time +  ".txt"
		number_of_records_written = 0

		error_log = open(filename, 'a+')

		for row in reader:

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
				#print(error)

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

			#file_data = csv_file.read().decode("utf-8")
			file_data = csv_file.read()
			lines = file_data.split("\n")
			reader = csv.DictReader(lines)

			if (self.consume_category_report(reader)):
				print ('is')
			else:
				print ('not')
				return Response(template_name='failure_csv_amazon.html')

			return Response(template_name='success_csv_amazon.html')

		except Exception as error:
			print (error)
			return Response(template_name='failure_csv_amazon.html')

	def consume_category_report(self, reader):
		#try:

		for row in reader:
			data = {}

			if row['parent_child'] == 'parent':
				data['is_parent'] = True
				parent_sku = row['item_sku']
			else:
				data['is_parent'] = False
				parent_sku = row['parent_sku']

			# if parent does not exist, ignore
			try:
				image = Image.objects.get(sku=parent_sku)
				data['is_orphan'] = False
				data['parent_sku'] = image.sku

			except:
				data['is_orphan'] = True

			data['item_sku'] = row['item_sku']

			# retrieve the product description - and check unicode
			data['item_name'] = row['item_name']

			try:
				test = (unicode(data['item_name']))
			except:
				data['item_name'] = row['item_name'].decode('utf-8')
				data['check_unicode'] = True

			# retrieve the product description - and check unicode
			data['product_description'] = row['product_description']

			try:
				test = (unicode(data['product_description']))
			except:
				data['product_description'] = row['product_description'].decode('utf-8')
				data['check_unicode'] = True

			# retrieve the fifth bullet, as it may be a copy of the title - and check unicode
			bullet5 = row['bullet_point5']
			if len(bullet5) > 200:
				bullet5 = bullet5[:200]
				data['check_bullets'] = True

			try:
				test = (unicode(bullet5))
			except:
				data['bullet5'] = bullet5.decode('utf-8')
				data['check_unicode'] = True

			# retrieve keywords, check unicode
			data['keywords'] = row['generic_keywords1']

			try:
				test = (unicode(data['keywords']))
			except:
				data['keywords'] = row['generic_keywords1'].decode('utf-8')
				data['check_unicode'] = True

			data['asin'] = row['external_product_id']
			data['catalog_number'] = row['catalog_number']
			data['part_number'] = row['part_number']
			data['size_name'] = row['size_name']
			data['variation_theme'] = row['variation_theme']
			data['product_tax_code'] = row['product_tax_code']
			data['currency'] = row['currency']
			data['bullet1'] = row['bullet_point1']
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
				if serializer.is_valid():
					serializer.save()
				else:
					print ('Amazon Serializer:', serializer.errors)
					print (data['item_sku'])
					#return False
					#pass

			except UnicodeDecodeError as error:
				print('Exception', error)
				print (row['item_sku'])
				return False

		return True

class category_report_sftp(views.APIView):

	def get(self,request):
		return Response(template_name='upload_csv_amazon.html')

	def post(self, request):

		try:

			for infile in glob.glob("ftp/Amazon/*.csv"):

				with open(infile, 'r') as csvfile:
					reader = csv.DictReader(csvfile)
					self.consume_csv(reader)

			if (self.consume_category_report(reader)):
				print ('is')
			else:
				print ('not')
				return Response(template_name='failure_csv_amazon.html')

			return Response(template_name='success_csv_amazon.html')

		except Exception as error:
			print (error)
			return Response(template_name='failure_csv_amazon.html')

	def consume_category_report(self, reader):

		time = datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
		filename = "ftp/error_log_" + time +  ".txt"
		number_of_records_written = 0

		error_log = open(filename, 'a+')

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
			try:
				image = Image.objects.get(sku=parent_sku)
				data['is_orphan'] = False
				data['parent_sku'] = image.sku

			except:
				data['is_orphan'] = True

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

			data['asin'] = row['external_product_id']
			data['catalog_number'] = row['catalog_number']
			data['part_number'] = row['part_number']
			data['size_name'] = row['size_name']
			data['variation_theme'] = row['variation_theme']
			data['product_tax_code'] = row['product_tax_code']
			data['currency'] = row['currency']
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

			except Exception as error:
				string = "Validation error in sku: " + row['item_sku'] + '\n'
				error_log.write(string)
				#print(error)

		print('Wrote ' + str(number_of_records_written) + ' records.')
		error_log.close()

		return True

class amazon_variation_size_verify(views.APIView):

	def get(self, request):
		return Response(template_name='upload_csv_amazon.html')

	def post(self, request):
		skus = Amazon_Variation.objects.all().filter(item_name__contains='Vue de Saigon')
		print (len(skus))
		count = 0
		for sku in skus:
			count += 1
			print (sku.item_sku)

		print(count)


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
			reader = csv.DictReader(lines)

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
			data = {}

			try:
				row['parent_sku'] = '101579P'

				image = Image.objects.get(sku=row['parent_sku'])
				data['parent_sku'] = image.id
				data['item_sku'] = row['item_sku']
				data['item_name'] = row['item_name']
				data['product_description'] = row['product_description']
				data['asin'] = row['external_product_id']
				data['catalog_number'] = row['catalog_number']
				data['part_number'] = row['part_number']
				data['size_name'] = row['size_name']
				data['variation_theme'] = row['variation_theme']
				data['product_tax_code'] = row['product_tax_code']
				data['currency'] = row['currency']
				
				if row['parent_child'] == 'parent':
					data['is_parent'] = True
				else:
					data['is_parent'] = False

				data['bullet1'] = row['bullet_point1']
				data['bullet2'] = row['bullet_point2']
				data['bullet3'] = row['bullet_point3']
				data['bullet4'] = row['bullet_point4']
				data['bullet5'] = row['bullet_point5']

				data['keywords'] = row['generic_keywords1']
				data['price'] = (row['standard_price'])

			except Exception as error:
				print(error)
				return False

			try:
				serializer = Amazon_Variation_Serializer(data=data)
				if serializer.is_valid():
					serializer.save()
				else:
					print (serializer.errors)
					return False
					
			except Exception as error:
				print(error)
				return False

		return True
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

            if not (self.verify_keys(reader)):
                print ("key failure")
                return Response(template_name='failure_csv.html')

            if (self.consume_csv(reader)):
                print ('is')
            else:
                print ('not')

            return Response(template_name='success_csv.html')
        
        except Exception as error:
            print (error)
            return Response(template_name='failure_csv.html')

    def consume_csv(self, reader):        

        #row = next(reader)
        # print (reader.fieldnames)
        for row in reader:
            try:
                rowtest = {'item_sku': '2544', 'item_name': 'test1', 'image_height': 1, 'image_width':1, 
            'main_image_url':'test', 'main_image_path':'test', 'category':'test', 'collection':'test', 'sub_collection':'test'}
                serializer = ImageSerializer(data=rowtest)
                if serializer.is_valid():
                    serializer.save()
                    return True
                return False
            except Exception as error:
                print(error)
                return False
            #print(row['item_sku'])


        #return data_dict

    def validate_fields(self, row):
        return True

    def verify_keys(self, reader):
        keys = reader.fieldnames

        schema = ['item_sku', 'item_name', 'image_height', 'image_width', 
            'main_image_url', 'main_image_path', 'category', 'collection', 'sub_collection']

        if keys != schema:
            return False

        return True

        '''
        reader = csv.DictReader(file)
        for row in reader:
            print (row)
        try:
            reader = csv.DictReader(file)
        except Exception as e:
            print(e)
        '''
        #row1 = next(reader)
        

        '''
        try:
            with open(file, 'rb') as csvfile:
                print ('hello')
                reader = csv.DictReader(csvfile)
                row1 = next(reader)
                row1 = next(reader)

                print('dix')
                if self.validate_fields(row1):
                    for row in reader:
                        newCsv.append(row)

        except Exception as e:
            print (e)
        '''
        #for item in newCsv:
        #    print(item)  




'''
 data = {}
    if "GET" == request.method:
        return render(request, "myapp/upload_csv.html", data)
    # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request,'File is not CSV type')
            return HttpResponseRedirect(reverse("myapp:upload_csv"))
        #if file is too large, return
        if csv_file.multiple_chunks():
            messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
            return HttpResponseRedirect(reverse("myapp:upload_csv"))
 
        file_data = csv_file.read().decode("utf-8")        
 
        lines = file_data.split("\n")
        #loop over the lines and save them in db. If error , store as string and then display
        for line in lines:                        
            fields = line.split(",")
            data_dict = {}
            data_dict["name"] = fields[0]
            data_dict["start_date_time"] = fields[1]
            data_dict["end_date_time"] = fields[2]
            data_dict["notes"] = fields[3]
            try:
                form = EventsForm(data_dict)
                if form.is_valid():
                    form.save()                    
                else:
                    logging.getLogger("error_logger").error(form.errors.as_json())                                                
            except Exception as e:
                logging.getLogger("error_logger").error(form.errors.as_json())                    
                pass
 
    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
        messages.error(request,"Unable to upload file. "+repr(e))
 
    return HttpResponseRedirect(reverse("myapp:upload_csv"))
    '''
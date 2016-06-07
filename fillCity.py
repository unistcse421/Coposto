import os, csv, sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coposto.settings")
import django
django.setup()
from head.models import City

# City.objects.filter(id__in=[257518, 352150]).delete()

# print list(City.objects.all().filter(country='Kor').values_list('country'))
korList = City.objects.filter(country='Kor').update(country=u'Korea');
print list(City.objects.all().filter(country='Korea').values_list('country'))

# maxInt = sys.maxsize
# decrement = True

# while decrement:
#     # decrease the maxInt value by factor 10 
#     # as long as the OverflowError occurs.

#     decrement = False
#     try:
#         csv.field_size_limit(maxInt)
#     except OverflowError:
#         maxInt = int(maxInt/10)
#         decrement = True

# fileName = 'citiesUpdate.csv'
# with open(fileName) as f:
# 	reader = csv.reader(f)
#     # print(l[23240:23250])
# 	try:
# 		for row in reader:
# 			valid_utf8 = True
# 			try:
# 				row[0].decode('utf-8')
# 				row[1].decode('utf-8')
# 				_, created = City.objects.get_or_create(
# 					city=row[0],
# 					country=row[1],
# 	        	)
# 			except UnicodeDecodeError:
# 				print(row)
# 				valid_utf8 = False
# 	except csv.Error, e:
# 	    sys.exit('file %s, line %d: %s' % (fileName, reader.line_num, e))
        
        # creates a tuple of the new object or
        # current object and a boolean of if it was created

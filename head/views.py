from django.shortcuts import render_to_response, render
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.template.loader import render_to_string
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from registration.backends.simple.views import RegistrationView
from head.forms import RegistrationFormUniqueEmail
import datetime
import json
from head.models import City
from head.forms import ParcelForm

def index(request):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    send_form = send_form_view(request)
    context = {'title': 'COPOSTO',
    			'description': 'From people to people',
    			'send_title': 'Sending form!',
    			'parcel_category': ['< 1kg', '1-3kg', '3-6kg', '6-10kg', '> 10kg'],}
    return render(request, 'index.html', context)

@csrf_protect
def send_form_view(request):
	html = ''
	if request.is_ajax():
		if request.method == 'GET':
			send_form = ParcelForm(auto_id=False)
			html = render_to_string('send_form.html', {'form': send_form}, RequestContext(request))
		elif request.method == 'POST':
			# A POST request
			send_form = ParcelForm(request.POST)
			# If data is valid, proceeds to create a new post and redirect the user
			if send_form.is_valid():
				goal = form.save()
		        # Serialize the goal in json format and send the
		        # newly created object back in the reponse
				data = serializers.serialize('json', [goal,])
			else:
		        # Since form.errors is a proxy need to create a dict from it with unicode
				data = json.dumps(dict([(k, [unicode(e) for e in v]) for k,v in form.errors.items()]))
			return HttpResponse(data, mimetype='application/json')	
			 # If data is valid, proceeds to create a new post and redirect the user
			if send_form.is_valid():
				destination_a = form.cleaned_data['destination_a']
				destination_b = form.cleaned_data['destination_b']
				name = form.cleaned_data['name']
				description = form.cleaned_data['description']
				weight = form.cleaned_data['weight']
				price = form.cleaned_data['price']
				image = form.cleaned_data['image']
				post = m.Post.objects.create(destination_a=destination_a,
	                                         destination_b=destination_b,
	                                         name=name,
	                                         description=description,
	                                         weight=weight,
	                                         price=price,
	                                         image=image)
				return HttpResponseRedirect(reverse('post_detail',
	                                                kwargs={'post_id': post.id}))
			else:
				print('asdasd')
	return HttpResponse(html)


def city_search(request):
	def getCities(input_string):
		return City.objects.filter(city__startswith=input_string)
	input_string = request.GET.get('q')
	objs = getCities(input_string);
	cities = [ ('{0}, {1}'.format(p.city, p.country)) for p in objs ]
	idler = [ ('{0}'.format(p.id)) for p in objs ]
	res = {}
	res['values'] = cities
	res['ids'] = idler
	print(res)
	return JsonResponse(cities, safe=False)

class RegistrationViewUniqueEmail(RegistrationView):
	form_class = RegistrationFormUniqueEmail


def send_form_result(request):
	return HttpResponse('YES!')

def send_form_validator(request):
	key, value = request.GET.dict().popitem()
	value = value.strip()
	
	if key == 'destination_a' or key == 'destination_b':
		try:
			arr = value.split(", ")
			if not City.objects.filter(city=arr[0], country=arr[1]).exists():
				print('City does not exist in db')
			else:
				return HttpResponse(status = 200);
		except:
			return HttpResponse('Destinations are in wrong format', status = 400);
	elif key == 'date_a' or key == 'date_b':
		try:
			date_obj = datetime.datetime.strptime(value, "%m/%d/%Y").date()
			date_today = datetime.date.today()
			if (date_obj < date_today):
				raise Exception('date invalid')
			# print date_obj
			# print date_today
		except:
			return HttpResponse('Dates are in wrong format', status = 400);
	return HttpResponse('FUCKKKKK!', status = 200);
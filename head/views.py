from django.shortcuts import render_to_response, render
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
import json
from head.models import City
from head.forms import Parcel

def getCities(input_string):
	return City.objects.filter(city__startswith=input_string)

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
		send_form = Parcel(auto_id=False)
		html = render_to_string('send_form.html', {'form': send_form}, RequestContext(request))
	else:
		# A POST request
		send_form = Parcel(request.POST)
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
 
	return HttpResponse(html)

def city_search(request):
	input_string = request.GET.get('q')
	cities = [ ('{0}, {1}'.format(p.city, p.country)) for p in getCities(input_string) ]
	return JsonResponse(cities, safe=False)

def send_form_result(request):
	return HttpResponse('YES!')
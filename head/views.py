from django.shortcuts import render_to_response, render
from django.http import HttpResponse, JsonResponse
import json
from head.models import City

def getCities(input_string):
	return City.objects.filter(city__startswith=input_string)

def index(request):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'title': 'COPOSTO',
    			'description': 'From people to people',
    			'send_title': 'Sending form!',
    			'parcel_category': ['< 1kg', '1-3kg', '3-6kg', '6-10kg', '> 10kg'],}
    return render(request, 'land.html', context)


def city_search(request):
	input_string = request.GET.get('q')
	cities = [ ('{0}, {1}'.format(p.city, p.country)) for p in getCities(input_string) ]
	return JsonResponse(cities, safe=False)
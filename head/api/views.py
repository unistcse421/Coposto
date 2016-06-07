from head.models import City_Russian, Profile, Parcel
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from head.api.serializers import UserSerializer
from django.core import serializers
import head.functions as functions
from head.views import get_destination, get_date 

@api_view(['POST'])
def login(request):
	if request.method == 'GET':
		return Response(status=status.HTTP_403_FORBIDDEN)
	email = request.POST.get('email')
	paswrd = request.POST.get('password')

	email = email.strip()
	paswrd = functions.hashPass(paswrd)

	profile = Profile.objects.filter(email=email)
	res_obj = serializers.serialize('json', profile)

	if profile.exists() and profile[0].password == paswrd:
		return Response({'data': res_obj}, status=status.HTTP_200_OK)

	return Response({'response': 'fail'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def register(request):
	if request.method == 'GET':
		return Response(status=status.HTTP_403_FORBIDDEN)
	payload = {}

	payload['first_name'] = request.POST.get('first_name')
	payload['last_name'] = request.POST.get('last_name')
	payload['email'] = request.POST.get('email')
	payload['password'] = request.POST.get('password')

	profile = Profile(first_name = payload['first_name'], 
						last_name = payload['last_name'],
						email = payload['email'],
						password = functions.hashPass(payload['password']))

	if Profile.objects.filter(email=payload['email']).exists():
		return Response({'response': 'exists'}, status=status.HTTP_400_BAD_REQUEST)

	profile.save()

	if request.FILES and request.FILES['avatar']:		
		avatar = Avatar(user = profile, avatar = request.FILES['avatar'])
		avatar.save()

	return Response({'response': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def send(request):
	if request.method == 'GET':
		return Response(status=status.HTTP_403_FORBIDDEN)
	print ('api_send')
	destination_a = request.POST.get('destination_a').encode('utf-8').strip()
	destination_b = request.POST.get('destination_b').encode('utf-8').strip()

	city_a = get_destination(destination_a)
	city_b = get_destination(destination_b)
	
	if (not isinstance(city_a, City_Russian) or not isinstance(city_b, City_Russian)):
		return Response({'response': 'dests_error'}, status=status.HTTP_400_BAD_REQUEST)	

	date_a = request.POST.get('date_a').strip()
	date_b = request.POST.get('date_b').strip()

	date_a = get_date(date_a)
	date_b = get_date(date_b)

	if (not isinstance(date_a, str) or not isinstance(date_b, str)):
		return Response({'response': 'dates_error'}, status=status.HTTP_400_BAD_REQUEST)	

	parcel_name = request.POST.get('parcel_name').strip()
	description = request.POST.get('description').strip()
	weight = request.POST.get('weight').strip()
	price = request.POST.get('price').strip()

	user_id = request.POST.get('user_id').strip()

	if (weight < 0 or price < 0):
		return Response({'response': 'weight | price < 0'}, status=status.HTTP_400_BAD_REQUEST)

	if Profile.objects.filter(id=user_id).exists():
		profile = Profile.objects.get(id=user_id)
		
		parcel = Parcel(profile_a = profile,
						destination_a = city_a,
						destination_b = city_b,
						date_a = date_a,
						date_b = date_b,
						parcel_name = parcel_name,
						description = description,
						weight=weight,
						price=price)

		if request.FILES and request.FILES['image']:
			parcel.save()
			image = Image(item = parcel, image = request.FILES['image'])
			image.save()
			return Response({'response': 'success'}, status=status.HTTP_200_OK)
	else:
		return Response({'response': 'not_logged_in'}, status=status.HTTP_400_BAD_REQUEST)

	return Response({'response': 'fail'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def bring(request):
	if request.method == 'GET':
		return Response(status=status.HTTP_403_FORBIDDEN)
	print ('api_bring')
	location_a = request.POST.get('from').encode('utf-8').strip()
	location_b = request.POST.get('to').encode('utf-8').strip()
	date = request.POST.get('date').strip()

	city_a = get_destination(location_a)
	city_b = get_destination(location_b)
	
	if (not isinstance(city_a, City_Russian) or not isinstance(city_b, City_Russian)):
		return Response({'response': 'dests_error'}, status=status.HTTP_400_BAD_REQUEST)	

	date = get_date(date)

	if (not isinstance(date, str)):
		return Response({'response': 'dates_error'}, status=status.HTTP_400_BAD_REQUEST)	

	user_id = request.POST.get('user_id').strip()

	if Profile.objects.filter(id=user_id).exists():
		logged_profile = Profile.objects.get(id = logged_id)

		p = Parcel.objects.filter(done=False,destination_a=city_a,destination_b=city_b,date_a__lte=date,date_b__gte=date).exclude(profile_a=logged_profile)
		if p.exists():
			res_obj = serializers.serialize('json', p)
			return Response({'data': res_obj}, status=status.HTTP_200_OK)
		else:
			return Response({'data': ''}, status=status.HTTP_200_OK)
	else:
		return Response(status=status.HTTP_403_FORBIDDEN)
	
	return Response({'response': 'fail'}, status=status.HTTP_400_BAD_REQUEST)	
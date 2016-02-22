from head.models import Profile, Parcel
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from head.api.serializers import UserSerializer
import head.functions as functions

@api_view(['POST'])
def login(request):
	if request.method == 'GET':
		return Response(status=status.HTTP_403_FORBIDDEN)
	email = request.POST.get('email')
	paswrd = request.POST.get('password')

	email = email.strip()
	paswrd = functions.hashPass(paswrd)

	profile = Profile.objects.filter(email=email)

	data = {'article': 'yes'}

	if profile.exists() and profile[0].password == paswrd:
		return Response(data, status=status.HTTP_200_OK)

	return Response({'article': 'no'}, status=status.HTTP_400_BAD_REQUEST)
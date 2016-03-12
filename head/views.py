import datetime
import json
import sys
import functions

from django.conf import settings
from django.shortcuts import render_to_response, render
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.template.loader import render_to_string
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect

from registration.backends.simple.views import RegistrationView
from head.forms import RegistrationFormUniqueEmail
from head.models import City, City_Russian, Avatar, Profile, Parcel, Image
from head.forms import ParcelForm


def index(request):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    send_form = send_form_view(request)
    context = functions.home_context
    return render(request, 'index.html', context)


def city_search(request):
    def getCities(input_string):
        return City_Russian.objects.filter(city__startswith=input_string).extra(select={'length':'Length(city)'}).order_by('length')
    input_string = request.GET.get('q').encode('utf-8').strip()

    objs = getCities(input_string)
    cities = [('{0}, {1}'.format(p.city.encode('utf-8'),
              p.country.encode('utf-8'))) for p in objs]
    idler = [('{0}'.format(p.id)) for p in objs]
    res = {}
    res['values'] = cities
    res['ids'] = idler
    return JsonResponse(cities, safe=False)


@csrf_protect
def send_form_view(request):
    html = ''
    if request.is_ajax():
        if request.method == 'GET':
            send_form = ParcelForm(auto_id=False)
            context = functions.home_context
            context['form'] = send_form
            html = render_to_string('send_form.html', context, RequestContext(request))
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
                print ('creating....')
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


class RegistrationViewUniqueEmail(RegistrationView):
    form_class = RegistrationFormUniqueEmail


def login(request):
    if request.method == 'POST':
        return HttpResponse('no!')
    return render(request, 'login_form.html', functions.home_context)


def register(request):
    if request.method == 'POST':
        return HttpResponse('no!')
    return render(request, 'registration/registration_form.html', functions.home_context)


@csrf_protect
def login_result(request):
    if request.method == 'GET':
        return HttpResponse('no!')
    email = request.POST.get('email')
    paswrd = request.POST.get('password')

    email = email.strip()
    paswrd = functions.hashPass(paswrd)

    profile = Profile.objects.filter(email=email)

    if profile.exists() and profile[0].password == paswrd:
        print ('Successfully logged in')
        request.session['is_logged'] = True
        request.session['logged_id'] = profile[0].id
        request.session['logged_name'] = profile[0].first_name
        if 'parcel_id' in request.session:
            try:
                parcel_id = request.session['parcel_id']
                parcel = Parcel.objects.get(id=parcel_id)
                parcel.profile_a = profile
                parcel.save(update_fields=['profile_a'])
                del request.session['parcel_id']
            except Parcel.DoesNotExist:
                print 'problem'
                return HttpResponse('fail')
        return HttpResponse('success')

    print ('Login or password is wrong')

    return HttpResponse('fail')


@csrf_protect
def bring_result(request):
    if request.method == 'GET':
        return HttpResponse('no!')
    location_a = request.POST.get('from').encode('utf-8')
    location_b = request.POST.get('to').encode('utf-8')
    date = request.POST.get('date')

    location_a, location_b, date = \
        location_a.strip(), location_b.strip(), date.strip()

    city_a = get_destination(location_a)
    city_b = get_destination(location_b)

    if (not isinstance(city_a, City_Russian) or not isinstance(city_b, City_Russian)):
        return HttpResponse('fail') # dests_error

    date = get_date(date)

    if (not isinstance(date, str)):
        return HttpResponse('fail') # date error

    logged_profile = 0
    if 'logged_id' in request.session and request.session['logged_id']:
        logged_id = request.session['logged_id']
        logged_profile = Profile.objects.get(id = logged_id)

    p = Parcel.objects.filter(done=False,destination_a=city_a,destination_b=city_b,date_a__lte=date,date_b__gte=date).exclude(profile_a=logged_profile)

    if p.exists():
        csrf_token_value = request.COOKIES['csrftoken']
        # c = {"panelDisplays": panelDisplays, }
        context = functions.home_context
        context['parcels'] = p
        context['csrf_token'] =  csrf_token_value
        html = render_to_string('bring_result.html', context)
    else:
        html = '<h1>' + functions.home_context['no_records'] + '</h1>'

    # if profile.exists() and profile[0].password == paswrd:
    #   print ('Successfully logged in')
    #   request.session['is_logged'] = True
    #   request.session['logged_id'] = profile[0].id
    #   request.session['logged_name'] = profile[0].first_name
    #   return HttpResponse('success')

    # print ('Login or password is wrong')
    res = {'result_text': 'success',
           'html': html}
    return HttpResponse(json.dumps(res), content_type="application/json")


@csrf_protect
def bring_submit(request):
    if request.method == 'GET':
        return HttpResponse('no!')

    if 'is_logged' in request.session and request.session['is_logged']:
        profile = Profile.objects.get(id=request.session['logged_id'])
        parcel_ids = map(int, request.POST.getlist("parcel_ids[]"))

        for parcel in Parcel.objects.filter(id__in=parcel_ids):
            functions.bring_parcel_email(parcel, profile) # send email to sender
            parcel.profiles_b.add(profile)
        return HttpResponse('success')
    else:
        return HttpResponse('not_logged')

    return HttpResponse('fail')


@csrf_protect
def send_result(request):
    if request.method == 'GET':
        return HttpResponse('no!')

    destination_a = request.POST.get('destination_a').encode('utf-8').strip()
    destination_b = request.POST.get('destination_b').encode('utf-8').strip()

    city_a = get_destination(destination_a)
    city_b = get_destination(destination_b)

    if (not isinstance(city_a, City_Russian) or
            not isinstance(city_b, City_Russian)):
        return HttpResponse('dests_error')

    date_a = request.POST.get('date_a').strip()
    date_b = request.POST.get('date_b').strip()

    date_a = get_date(date_a)
    date_b = get_date(date_b)

    if (not isinstance(date_a, str) or not isinstance(date_b, str)):
        return HttpResponse('dates_error')

    parcel_name = request.POST.get('parcel_name').strip()
    description = request.POST.get('description').strip()
    weight = request.POST.get('weight').strip()
    price = request.POST.get('price').strip()

    if (weight < 0 or price < 0):
        return HttpResponse('weight | price < 0')

    profile = Profile.objects.get(email=settings.PARCELS_DEFAULT_OWNER_EMAIL)

    parcel = Parcel(profile_a=profile,
                    destination_a=city_a,
                    destination_b=city_b,
                    date_a=date_a,
                    date_b=date_b,
                    parcel_name=parcel_name,
                    description=description,
                    weight=weight,
                    price=price)

    if request.FILES and request.FILES['image']:
        parcel.save()
        image = Image(item=parcel, image=request.FILES['image'])
        image.save()
        # send email to admins
        functions.notice_admin('parcel')
        if ('is_logged' in request.session and
                request.session['is_logged'] and
                'logged_id' in request.session):
            logged_id = request.session['logged_id']
            profile = Profile.objects.get(id=logged_id)
            parcel.profile_a = profile
            parcel.save(update_fields=['profile_a'])
            return HttpResponse('success')
        else:
            print('not logged in')
            request.session['parcel_id'] = parcel.id
            return HttpResponse('not_logged')
    else:
        print('not logged in')
        request.session['filled_bring_form'] = True
        return HttpResponse('not_logged')

    return HttpResponse('fail')


def send_form_validator(request):
    key, value = request.GET.dict().popitem()
    value = value.strip()

    if key == 'destination_a' or key == 'destination_b':
        try:
            arr = value.split(", ")
            if not City_Russian.objects.filter(city=arr[0], country=arr[1]).exists():
                print('City does not exist in db')
            else:
                return HttpResponse(status = 200)
        except:
            return HttpResponse('Destinations are in wrong format', status = 400)
    elif key == 'date_a' or key == 'date_b':
        try:
            date_obj = datetime.datetime.strptime(value, "%m/%d/%Y").date()
            date_today = datetime.date.today()
            if (date_obj < date_today):
                raise Exception('date invalid')
            # print date_obj
            # print date_today
        except:
            return HttpResponse('Dates are in wrong format', status = 400)
    elif key == 'date_a' or key == 'date_b':
        try:
            date_obj = datetime.datetime.strptime(value, "%m/%d/%Y").date()
            date_today = datetime.date.today()
            if (date_obj < date_today):
                raise Exception('date invalid')
            # print date_obj
            # print date_today
        except:
            return HttpResponse('Dates are in wrong format', status=400)
    return HttpResponse('FUCKKKKK!', status = 200)


def reg_form_validator(request):
    key, value = request.GET.dict().popitem()
    value = value.strip()

    if key == 'email':
        try:
            if Profile.objects.filter(email=value).exists():
                print('Email exists already')
                return HttpResponse('This email is already registered', status = 400)
            else:
                return HttpResponse('Good', status=200)
        except:
            return HttpResponse('This email is already registered', status=400)
    return HttpResponse('Good', status=200)


@csrf_protect
def reg_result(request):
    payload = {}
    print 'Inside reg_result'

    payload['first_name'] = request.POST.get('first_name')
    payload['last_name'] = request.POST.get('last_name')
    payload['email'] = request.POST.get('email')
    payload['password'] = request.POST.get('password')

    profile = Profile(first_name=payload['first_name'],
                      last_name=payload['last_name'],
                      email=payload['email'],
                      password=functions.hashPass(payload['password']))
    if Profile.objects.filter(email=payload['email']).exists():
        print('Email exists already')
        return('exists')

    print ('Successfully new user saved')
    profile.save()

    if 'parcel_id' in request.session:
        print request.session['parcel_id']
        try:
            parcel_id = request.session['parcel_id']
            parcel = Parcel.objects.get(id=parcel_id)
            parcel.profile_a = profile
            parcel.save(update_fields=['profile_a'])
            del request.session['parcel_id']
        except Parcel.DoesNotExist:
            print 'problem'
            return HttpResponse('fail')

    # send email to admins
    functions.notice_admin('profile')

    if request.FILES and request.FILES['avatar']:
        print('avatar')
        avatar = Avatar(user=profile, avatar=request.FILES['avatar'])
        avatar.save()

    print ('Successfully new user saved')

    request.session['is_logged'] = True
    request.session['logged_id'] = profile.id
    request.session['logged_name'] = profile.first_name

    return HttpResponse('success')


@csrf_protect
def logout(request):
    print('logout')
    try:
        request.session.flush()
        request.session['is_logged'] = False
    except KeyError:
        pass
    return HttpResponse('logged out')


def account_view(request):
    html = ''
    if 'is_logged' in request.session and request.session['is_logged'] and 'logged_id' in request.session:
        logged_id = request.session['logged_id']
        try:
            if Profile.objects.filter(id=logged_id).exists():
                p = Profile.objects.get(id=logged_id)
                has_avatar = Avatar.objects.filter(user=p).exists()
                context = {
                    'user_id': p.id,
                    'first_name': p.first_name,
                    'last_name': p.last_name,
                    'has_avatar': has_avatar
                }
                print(context)
                html = render(request, 'account_view.html', context)
        except:
            print "Unexpected error:", sys.exc_info()

    return HttpResponse(html)


def user_send_list(request):
    return HttpResponse('Send list')


def user_bring_list(request):
    return HttpResponse('Bring list')

# Helper functions


def get_destination(dest):
    try:
        arr = dest.split(", ")
        city = City_Russian.objects.filter(city=arr[0], country=arr[1])
        if not city.exists():
            return -2 # City does not exist in db
        else:
            return city[0]
    except:
        print "Unexpected error:", sys.exc_info()
        return -3 # Destinations are in wrong format
    return -1


def get_date(value):
    try:
        date_obj = datetime.datetime.strptime(value, "%m/%d/%Y").date()
        return date_obj.strftime("%Y-%m-%d")
    except:
        print "Unexpected error:", sys.exc_info()
    return -1 # Destinations are in wrong formats

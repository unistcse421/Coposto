from django.shortcuts import render_to_response

# from .models import Question

def index(request):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # context = {'latest_question_list': latest_question_list}
    return render_to_response('index.html')
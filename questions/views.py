from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from questions.models import Question
from django.http import HttpResponse

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from faker import lorem
from random import shuffle

def test_gu(request):
    text_lst = []
    msg = ''
    if request.method == 'GET':
        req_lists = request.GET.lists()
    if request.method == 'POST':
        req_lists = request.POST.lists()
    for key, lst in req_lists:
        if key == 'csrfmiddlewaretoken':
            continue
        for word in lst:
            msg = msg + key + '=' + word
            text_lst.append(msg)
            msg = ''
    return render(request, 'test_gu.html', {'text': text_lst})



def paginate(objects, request):
    if request.method == 'GET':
        page_num = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 5))
    p = Paginator(objects, limit)
    p.limiturl = 'limit='+str(limit)
    try:
        pageN = p.page(page_num)
    except PageNotAnInteger:
        pageN = p.page(1)
    except EmptyPage:
        pageN = p.page(p.num_pages)
    object_page = pageN.object_list
    return object_page, pageN

# Create your views here.

def index(request):
    qlist = Question.objects.new_questions()
    page_qlist, pageN = paginate(qlist, request)
    return render(request, 'questions/new.html', {'questions': page_qlist, 'page': pageN})

def hot(request):
    qlist = Question.objects.top_questions()
    page_qlist, pageN = paginate(qlist, request)
    return render(request, 'questions/hot.html', {'questions': page_qlist, 'page': pageN})

def tag(request, tag_word):
    q_tag_list = Question.objects.questions_tag(tag_word)
    page_qlist, pageN = paginate(q_tag_list, request)
    return render(request, 'questions/tag.html', {'questions': page_qlist, 'page': pageN, 'tag_word': tag_word,})

def question_detail(request, question_id):
    post = get_object_or_404(Question, id=question_id)
    return render(request, 'questions/question_detail.html', {'post': post,})

def signin(request):
    return render(request, 'signin.html', {'title': 'ASK.me-sign in'})

def signup(request):
    return render(request, 'signup.html', {'title': 'ASK.me-sign up'})

#def onequestion(request):
#    return render(request, 'onequestion.html', {'title': 'ASK.me - One question'})

def userset(request):
    return render(request, 'userset.html', {'title': 'ASK.me - user settings'})

def ask(request):
    return render(request, 'questions/ask.html', {'title': 'ASK.me - Ask'})



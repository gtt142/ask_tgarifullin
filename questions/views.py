from __future__ import unicode_literals
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse

from cgi import parse_qsl

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from faker import lorem
from random import shuffle

def test_gu(request):
    msg = ' '
    if request.method == 'GET':
        msg = request.GET.get('test', '')
    if request.method == 'POST':
        msg = request.POST.get('test', '')
    return render(request, 'test_gu.html', {'text': msg})

class AboutView(TemplateView):
   template_name = "about.html"

def paginate(objects, request):
    page_num = 1
    if request.method == 'GET':
        page_num = int(request.GET.get('page', '1'))
    p = Paginator(objects, 20)
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
    ctx = dict()
    qlist = list()
    tags = lorem.words(5)
    for i in range(1,71):
        shuffle(tags)
        qlist.append({
            'idx': i,
            'title': ' '.join(lorem.words(3)).title(),
            'text': lorem.sentences(3),
            'tags': tags[0:2],
        })
    page_qlist, pageN = paginate(qlist, request)
    ctx['questions'] = page_qlist
    ctx['page'] = pageN
    return render(request, 'index.html', ctx)

def hot(request):
    ctx = dict()
    qlist = list()
    tags = lorem.words(5)
    for i in range(1,101):
        shuffle(tags)
        qlist.append({
            'idx': i,
            'title': ' '.join(lorem.words(3)).title(),
            'text': lorem.sentences(3),
            'tags': tags[0:2],
        })
    page_qlist, pageN = paginate(qlist, request)
    ctx['questions'] = page_qlist
    ctx['page'] = pageN
    return render(request, 'hot.html', ctx)

def tag(request, tag_word):
    ctx = dict()
    qlist = list()
    tags = lorem.words(5)
    for i in range(1,48):
        shuffle(tags)
        qlist.append({
            'idx': i,
            'title': ' '.join(lorem.words(3)).title(),
            'text': lorem.sentences(3),
            'tags': tags[0:2],
        })
    page_qlist, pageN = paginate(qlist, request)
    ctx['page'] = pageN
    ctx['questions'] = page_qlist
    ctx['tag_word'] = tag_word
    return render(request, 'tag.html', ctx)

def question_detail(request, question_id):
    ctx = dict()
    ctx['q_id'] = question_id
    answlist = list()
    qlist = list()
    tags = lorem.words(5)
    for i in range(1,6):
        answlist.append({
            'idx': i,
            'text': lorem.sentences(3),
        })
    ctx['answers'] = answlist
    shuffle(tags)
    qlist.append({
        'idx': question_id,
        'title': ' '.join(lorem.words(3)).title,
        'text': lorem.sentences(3),
        'tags': tags[0:3],
    })
    ctx['question'] = qlist
    return render(request, 'onequestion.html', ctx)

def signin(request):
    return render(request, 'signin.html', {'title': 'ASK.me-sign in'})

def signup(request):
    return render(request, 'signup.html', {'title': 'ASK.me-sign up'})

#def onequestion(request):
#    return render(request, 'onequestion.html', {'title': 'ASK.me - One question'})

def userset(request):
    return render(request, 'userset.html', {'title': 'ASK.me - user settings'})

def ask(request):
    return render(request, 'ask.html', {'title': 'ASK.me - Ask'})




def foo(request):
    return render(request, 'base.html', {
        'title': 'Hello Title',
        'text': 'Some Text222',
    })

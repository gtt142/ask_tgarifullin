from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from questions import forms
from questions.models import Question, Answer, Tag, User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from django.contrib import auth

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
    limit = 5
    page_num = 1
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


def is_set_like(request):
    like = None
    if request.method == 'POST':
        like = request.POST.get('like')
    if like:
        req_type = request.POST.get('type')
        if req_type == 'question':
            q_id=request.POST.get('id')
            if like == 'p':
                Question.objects.set_like(q_id, 1)
            if like == 'm':
                Question.objects.set_like(q_id, -1)
        if req_type == 'answer':
            a_id = request.POST.get('id')
            if like == 'p':
                Answer.objects.set_like(a_id, 1)
            if like == 'm':
                Answer.objects.set_like(a_id, -1)


def get_top_tags():
    return Tag.objects.get_top_N(5)

def get_top_users():
    return User.objects.get_top_N(5)


# Create your views here.

def index(request):
    ctx = dict()
    qlist = Question.objects.new_questions()
    page_qlist, pageN = paginate(qlist, request)
    is_set_like(request)
    tag_list = get_top_tags()
    user_list = get_top_users()
    ctx['user_list'] = user_list
    ctx['questions'] = page_qlist
    ctx['page'] = pageN
    ctx['tag_list'] = tag_list
    return render(request, 'new.html', ctx)

def hot(request):
    ctx = dict()
    qlist = Question.objects.top_questions()
    page_qlist, pageN = paginate(qlist, request)
    is_set_like(request)
    tag_list = get_top_tags()
    user_list = get_top_users()
    ctx['user_list'] = user_list
    ctx['questions'] = page_qlist
    ctx['page'] = pageN
    ctx['tag_list'] = tag_list
    return render(request, 'hot.html', ctx)

def tag(request, tag_word):
    ctx = dict()
    q_tag_list = Question.objects.questions_tag(tag_word)
    is_set_like(request)
    page_qlist, pageN = paginate(q_tag_list, request)
    tag_list = get_top_tags()
    user_list = get_top_users()
    ctx['user_list'] = user_list
    ctx['questions'] = page_qlist
    ctx['page'] = pageN
    ctx['tag_list'] = tag_list
    ctx['tag_word'] = tag_word
    return render(request, 'tag.html', ctx)

def question_detail(request, question_id):
    ctx = dict()
    post = get_object_or_404(Question, id=question_id)
    is_set_like(request)
    tag_list = get_top_tags()
    user_list = get_top_users()
    ctx['user_list'] = user_list
    ctx['post'] = post
    ctx['tag_list'] = tag_list
    if request.POST:
        form = forms.AnswerForm(request.POST)
        if form.is_valid():
            answId = form.save(question_id, request.user.id)
            return redirect('./#'+str(answId))
    else:
        form = forms.AnswerForm()
    ctx['form'] = form
    return render(request, 'question_detail.html', ctx)

def signin(request):
    ctx = dict()
    tag_list = get_top_tags()
    user_list = get_top_users()
    ctx['user_list'] = user_list
    ctx['title'] = 'ASK.me-sign in'
    ctx['tag_list'] = tag_list
    if request.POST:
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                redir = request.GET.get('next', '/')
                return redirect(redir)
    else:
        form = forms.LoginForm
    ctx['form'] = form
    return render(request, 'signin.html', ctx)

@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')

def signup(request):
    ctx = dict()
    tag_list = get_top_tags()
    user_list = get_top_users()
    ctx['user_list'] = user_list
    ctx['title'] = 'ASK.me-sign up'
    ctx['tag_list'] = tag_list
    if request.POST:
        form = forms.UserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            return redirect('/')
    else:
        form = forms.UserCreationForm()
    ctx['form'] = form
    return render(request, 'signup.html', ctx)

#def onequestion(request):
#    return render(request, 'onequestion.html', {'title': 'ASK.me - One question'})

@login_required
def userset(request):
    ctx = dict()
    tag_list = get_top_tags()
    user_list = get_top_users()
    ctx['user_list'] = user_list
    ctx['title'] = 'ASK.me-user settings'
    ctx['tag_list'] = tag_list
    if request.POST:
        user = User.objects.get(id=request.user.id)
        form = forms.ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('./')
    else:
        user = User.objects.get(id = request.user.id)
        form = forms.ProfileForm(instance=user)
    ctx['form'] = form
    return render(request, 'userset.html', ctx)

@login_required
def ask(request):
    ctx = dict()
    tag_list = get_top_tags()
    user_list = get_top_users()
    
    ctx['user_list'] = user_list
    ctx['title'] = 'ASK.me-Ask'
    ctx['tag_list'] = tag_list
    if request.POST:
        form = forms.AddQuestionForm(request.POST)
        if form.is_valid():
            qId = form.save(request)
            return redirect(reverse('question_detail', kwargs={'question_id': qId}))
    else:
        form = forms.AddQuestionForm()
    ctx['form'] = form
    return render(request, 'ask.html', ctx)
# def profile(request):
#     prof = request.user.username
#     print(prof)
#
#     return render(request, 'userset.html')
#

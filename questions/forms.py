from django import forms
from django.contrib import auth
from questions import models

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=20, required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = auth.authenticate(username=username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(u'Неверное имя или пароль', code=11)

        return self.cleaned_data



class UserCreationForm(forms.Form):
    username = forms.CharField(label='Login', max_length=20, required=True)
    email = forms.EmailField(label='E-mail', required=True)
    nickname = forms.CharField(label='Nick name', max_length=20, required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Password(repeat)', widget=forms.PasswordInput, required=True)
    avatar=forms.ImageField(label='Avatar',
        widget=forms.FileInput (
            attrs={'class': 'form-control-file'}
        ), required=False)

    def clean_username(self):
        name = self.cleaned_data.get("username")
        user = models.User.objects.filter(username=name)[:1]
        if user:
            raise forms.ValidationError(u'Такой логин уже занят', code=21)
        return name

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(u'Пароли не совпадают', code=22)
        return password2

    def save(self, commit=True):
        name = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password1')
        user = models.User.objects.create_user(name, email, password)
        user.first_name = self.cleaned_data.get('nickname')
        if self.cleaned_data.get('avatar'):
            user.upload = self.cleaned_data['avatar']
        user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['username', 'email', 'upload']


class AnswerForm(forms.ModelForm):
    class Meta:
        model = models.Answer
        fields = ['text']

    def save(self, qId, userId):
        text = self.cleaned_data['text']
        answer = models.Answer(author_id = userId, text = text, question_id = qId)
        answer.save()
        return answer.id


class AddQuestionForm(forms.Form):
    title = forms.CharField(label='Title', max_length=50, required=True)
    category = forms.CharField(label='Category', max_length=50, required=True)
    text = forms.CharField(widget=forms.Textarea, label='Text', required=True)
    tags = forms.CharField(label='Tags', max_length=50, required=True)

    def clean_tags(self):
        tags = self.cleaned_data["tags"].split(',')
        if len(tags) > 3:
            raise forms.ValidationError(u'Введите не более трех тегов', code=21)
        for tag in tags:
            tag = tag.lower().lstrip(' \t').rstrip(' \t')
            if tag is '':
                raise forms.ValidationError(u'Пустые теги', code=21)
        return tags

    def save(self, request):
        stat = models.Status()
        stat.save()
        catName = self.cleaned_data['category'].lower().lstrip(' \t').rstrip(' \t')
        try:
            cat = models.Category.objects.get(title=catName)
        except models.Category.DoesNotExist:
            cat = None
        if cat is None:
            cat = models.Category(title=catName)
            cat.save()
        question = models.Question(author_id=request.user.id, title=self.cleaned_data['title'], text=self.cleaned_data['text'], category=cat,
                     status=stat)
        question.save()
        tags = self.cleaned_data["tags"].split(',')
        if len(tags) > 3:
            tags = tags[:3]
        for tag in tags:
            tag = tag.lower().lstrip(' \t').rstrip(' \t')
            try:
                newTag = models.Tag.objects.get(title = tag)
            except models.Tag.DoesNotExist:
                newTag = None
            if newTag is None:
                newTag = models.Tag(title=tag)
                newTag.save()
            question.tags.add(newTag)
        question.save()
        return question.id


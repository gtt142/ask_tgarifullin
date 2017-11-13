from django.contrib import admin
from questions.models import Question, User, Tag, Category, Status, Answer

# Register your models here.

admin.site.register(Question)
admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Status)
admin.site.register(Answer)
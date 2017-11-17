from django.core.management.base import BaseCommand, CommandError
from questions.models import Question, Tag, User, Category, Status
from faker import lorem
from faker import Faker
from random import shuffle

class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker()
        tid_lst = []
        user_lst = []
        cat_lst = []
        tagall = Tag.objects.all()
        userall = User.objects.all()[1:]
        catall = User.objects.all()
        for tag in tagall:
            tid_lst.append(tag.id)

        for user in userall:
            user_lst.append(user.id)

        for cat in catall:
            cat_lst.append(cat.id)

        for i in range(30):
            shuffle(user_lst)
            shuffle(tid_lst)
            tid3 = tid_lst[:3]
            shuffle(cat_lst)
            cat = cat_lst[0]
            stat = Status()
            stat.save()
            q = Question(author_id = user_lst[0], title = ' '.join(lorem.words(3)).title(), text = fake.text(), category_id=cat, status = stat)
            q.save()
            for tagid in tid3:
                t = Tag.objects.get(id=tagid)
                q.tags.add(t)
            q.save()
            self.stdout.write(self.style.SUCCESS(q.title))
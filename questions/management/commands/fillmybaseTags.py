from django.core.management.base import BaseCommand, CommandError
from questions.models import Tag
from faker import lorem
from random import shuffle

class Command(BaseCommand):
    def handle(self, *args, **options):
        n = 20
        tags = lorem.words(n)
        for tag in tags:
            t = Tag(title = tag)
            t.save()
        self.stdout.write(self.style.SUCCESS('Base successfully created. Add "%s" new tags' % n))
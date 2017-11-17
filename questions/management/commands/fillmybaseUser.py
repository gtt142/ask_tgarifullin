from django.core.management.base import BaseCommand, CommandError
from questions.models import User
from faker import Faker
from faker import lorem
from random import shuffle

class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker('ru_RU')
        for i in range(10):
            user = User(username=fake.first_name(), password='qwerty')
            user.save()
        self.stdout.write(self.style.SUCCESS(fake.first_name()))
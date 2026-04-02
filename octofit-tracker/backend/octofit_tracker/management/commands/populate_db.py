from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import connection
from djongo import models

from octofit_tracker import settings

from django.apps import apps

from django.conf import settings as django_settings

from django.db import transaction

# Modelos mínimos para poblar las colecciones
from django.contrib.auth.models import User

from django.db import models as dj_models

# Modelos temporales para poblar MongoDB
class Team(dj_models.Model):
    name = dj_models.CharField(max_length=100, unique=True)
    class Meta:
        app_label = 'octofit_tracker'

class Activity(dj_models.Model):
    name = dj_models.CharField(max_length=100)
    user = dj_models.CharField(max_length=100)
    team = dj_models.CharField(max_length=100)
    class Meta:
        app_label = 'octofit_tracker'

class Leaderboard(dj_models.Model):
    user = dj_models.CharField(max_length=100)
    team = dj_models.CharField(max_length=100)
    score = dj_models.IntegerField()
    class Meta:
        app_label = 'octofit_tracker'

class Workout(dj_models.Model):
    name = dj_models.CharField(max_length=100)
    description = dj_models.TextField()
    user = dj_models.CharField(max_length=100)
    class Meta:
        app_label = 'octofit_tracker'

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        UserModel = get_user_model()
        # Borrar datos existentes
        UserModel.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Crear equipos
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Crear usuarios
        users = [
            UserModel.objects.create_user(username='ironman', email='ironman@marvel.com', password='test'),
            UserModel.objects.create_user(username='spiderman', email='spiderman@marvel.com', password='test'),
            UserModel.objects.create_user(username='batman', email='batman@dc.com', password='test'),
            UserModel.objects.create_user(username='superman', email='superman@dc.com', password='test'),
        ]

        # Crear actividades
        Activity.objects.create(name='Run', user='ironman', team='Marvel')
        Activity.objects.create(name='Swim', user='spiderman', team='Marvel')
        Activity.objects.create(name='Fly', user='superman', team='DC')
        Activity.objects.create(name='Drive', user='batman', team='DC')

        # Crear leaderboard
        Leaderboard.objects.create(user='ironman', team='Marvel', score=100)
        Leaderboard.objects.create(user='spiderman', team='Marvel', score=80)
        Leaderboard.objects.create(user='batman', team='DC', score=90)
        Leaderboard.objects.create(user='superman', team='DC', score=95)

        # Crear workouts
        Workout.objects.create(name='Chest Day', description='Bench press, push-ups', user='ironman')
        Workout.objects.create(name='Web Training', description='Climbing, swinging', user='spiderman')
        Workout.objects.create(name='Bat Training', description='Martial arts, gadgets', user='batman')
        Workout.objects.create(name='Kryptonian Power', description='Flight, strength', user='superman')

        self.stdout.write(self.style.SUCCESS('Test data populated successfully!'))

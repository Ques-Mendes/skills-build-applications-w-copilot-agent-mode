from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import connection

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        User = get_user_model()
        # Delete all data
        User.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Deleted all users.'))

        # Create test users (superheroes)
        marvel = 'Team Marvel'
        dc = 'Team DC'
        users = [
            User(username='ironman', email='ironman@marvel.com', first_name='Tony', last_name='Stark'),
            User(username='spiderman', email='spiderman@marvel.com', first_name='Peter', last_name='Parker'),
            User(username='batman', email='batman@dc.com', first_name='Bruce', last_name='Wayne'),
            User(username='wonderwoman', email='wonderwoman@dc.com', first_name='Diana', last_name='Prince'),
        ]
        for user in users:
            user.set_password('password')
            user.save()
        self.stdout.write(self.style.SUCCESS('Created test users for Marvel and DC.'))

        # Create test teams, activities, leaderboard, workouts collections using raw pymongo
        db = connection.cursor().db_conn.client['octofit_db']
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        db.teams.insert_many([
            {'name': marvel, 'members': ['ironman', 'spiderman']},
            {'name': dc, 'members': ['batman', 'wonderwoman']},
        ])
        db.activities.insert_many([
            {'user': 'ironman', 'activity': 'run', 'distance': 5},
            {'user': 'spiderman', 'activity': 'cycle', 'distance': 10},
            {'user': 'batman', 'activity': 'swim', 'distance': 2},
            {'user': 'wonderwoman', 'activity': 'run', 'distance': 8},
        ])
        db.leaderboard.insert_many([
            {'team': marvel, 'points': 150},
            {'team': dc, 'points': 120},
        ])
        db.workouts.insert_many([
            {'name': 'Morning Cardio', 'duration': 30},
            {'name': 'Strength Training', 'duration': 45},
        ])
        db.users.create_index('email', unique=True)
        self.stdout.write(self.style.SUCCESS('Created teams, activities, leaderboard, workouts, and unique index on users.email.'))
        self.stdout.write(self.style.SUCCESS('Database population complete.'))

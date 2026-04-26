
from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):
	name = models.CharField(max_length=100, unique=True)
	members = models.ManyToManyField(User, related_name='teams')
	def __str__(self):
		return self.name

class Activity(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
	activity = models.CharField(max_length=50)
	distance = models.FloatField()
	timestamp = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return f"{self.user.username} - {self.activity}"

class Leaderboard(models.Model):
	team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='leaderboard')
	points = models.IntegerField()
	def __str__(self):
		return f"{self.team.name} - {self.points}"

class Workout(models.Model):
	name = models.CharField(max_length=100)
	duration = models.IntegerField(help_text='Duration in minutes')
	def __str__(self):
		return self.name

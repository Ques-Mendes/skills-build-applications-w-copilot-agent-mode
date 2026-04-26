
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Team, Activity, Leaderboard, Workout

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'username', 'email', 'first_name', 'last_name']

class TeamSerializer(serializers.ModelSerializer):
	members = UserSerializer(many=True, read_only=True)
	class Meta:
		model = Team
		fields = ['id', 'name', 'members']

class ActivitySerializer(serializers.ModelSerializer):
	user = UserSerializer(read_only=True)
	class Meta:
		model = Activity
		fields = ['id', 'user', 'activity', 'distance', 'timestamp']

class LeaderboardSerializer(serializers.ModelSerializer):
	team = TeamSerializer(read_only=True)
	class Meta:
		model = Leaderboard
		fields = ['id', 'team', 'points']

class WorkoutSerializer(serializers.ModelSerializer):
	class Meta:
		model = Workout
		fields = ['id', 'name', 'duration']

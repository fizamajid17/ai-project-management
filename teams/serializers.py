from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Team, TeamMember

User = get_user_model()

class TeamMemberUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class TeamMemberSerializer(serializers.ModelSerializer):
    user = TeamMemberUserSerializer(read_only=True)
    class Meta:
        model = TeamMember
        fields = ['id', 'user', 'role', 'joined_at']

class TeamSerializer(serializers.ModelSerializer):
    # This magic line extracts the full user profiles for the JavaScript dropdown
    members = TeamMemberUserSerializer(many=True, read_only=True)
    owner_username = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'owner', 'owner_username', 'members', 'created_at']
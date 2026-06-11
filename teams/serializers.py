from rest_framework import serializers
from .models import Team, TeamMember
from accounts.serializers import UserSerializer

class TeamMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = TeamMember
        fields = ['id','user','role','joined_at']

class TeamSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    member_count = serializers.SerializerMethodField()
    class Meta:
        model = Team
        fields = ['id','name','description','owner','member_count','created_at']

    def get_member_count(self, obj):
        return obj.members.count()
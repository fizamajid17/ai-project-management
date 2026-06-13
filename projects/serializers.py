from rest_framework import serializers
from .models import Project, Sprint, Task, Comment
from teams.serializers import TeamSerializer  # Import your updated team serializer

class ProjectSerializer(serializers.ModelSerializer):
    # This reads the full team data for the front-end layout
    team_details = TeamSerializer(source='team', read_only=True)
    # This accepts the incoming team ID when creating/updating a project
    team_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    owner_username = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'status', 'owner', 
            'owner_username', 'team', 'team_details', 'team_id', 
            'deadline', 'created_at', 'updated_at'
        ]

    def create(self, validated_data):
        # Extract team_id if passed, and link it to the project model field
        team_id = validated_data.pop('team_id', None)
        project = Project.objects.create(**validated_data)
        if team_id:
            from teams.models import Team
            try:
                project.team = Team.objects.get(pk=team_id)
                project.save()
            except Team.DoesNotExist:
                pass
        return project

    def update(self, instance, validated_data):
        team_id = validated_data.pop('team_id', None)
        if team_id is not None:
            if team_id == '':
                instance.team = None
            else:
                from teams.models import Team
                try:
                    instance.team = Team.objects.get(pk=team_id)
                except Team.DoesNotExist:
                    pass
        return super().update(instance, validated_data)


# Keep your existing Task, Sprint, and Comment serializers below this line
class TaskSerializer(serializers.ModelSerializer):
    assignee_username = serializers.ReadOnlyField(source='assignee.username')
    project_name = serializers.ReadOnlyField(source='project.name')
    class Meta:
        model = Task
        fields = '__all__'

class SprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sprint
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = Comment
        fields = '__all__'
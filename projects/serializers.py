from rest_framework import serializers
from .models import Project, Sprint, Task, Comment
from accounts.serializers import UserSerializer

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ['id','author','content','created_at']

class TaskSerializer(serializers.ModelSerializer):
    assignee = UserSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    assignee_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    class Meta:
        model = Task
        fields = ['id','title','description','project','sprint','assignee','assignee_id',
                  'created_by','priority','status','due_date','estimated_hours',
                  'comments','created_at','updated_at']

class SprintSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    task_count = serializers.SerializerMethodField()
    class Meta:
        model = Sprint
        fields = ['id','name','project','start_date','end_date','goal','is_active','tasks','task_count','created_at']

    def get_task_count(self, obj):
        return obj.tasks.count()

class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    task_count = serializers.SerializerMethodField()
    completed_tasks = serializers.SerializerMethodField()
    class Meta:
        model = Project
        fields = ['id','name','description','status','owner','team','deadline',
                  'task_count','completed_tasks','created_at','updated_at']

    def get_task_count(self, obj):
        return obj.tasks.count()

    def get_completed_tasks(self, obj):
        return obj.tasks.filter(status='done').count()
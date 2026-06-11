from google import genai
from google.genai import types
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Project, Sprint, Task, Comment
from .serializers import ProjectSerializer, SprintSerializer, TaskSerializer, CommentSerializer
from accounts.views import get_user_from_request

def get_user(request):
    user = get_user_from_request(request)
    if not user:
        return None, Response({'error':'Unauthorized'}, status=401)
    return user, None

class ProjectListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        user, err = get_user(request)
        if err: return err
        projects = Project.objects.filter(owner=user)
        return Response(ProjectSerializer(projects, many=True).data)

    def post(self, request):
        user, err = get_user(request)
        if err: return err
        p = Project.objects.create(
            name=request.data.get('name'),
            description=request.data.get('description',''),
            status=request.data.get('status','planning'),
            deadline=request.data.get('deadline') or None,
            owner=user
        )
        return Response(ProjectSerializer(p).data, status=201)

class ProjectDetailView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, pk):
        user, err = get_user(request)
        if err: return err
        try:
            p = Project.objects.get(pk=pk, owner=user)
            return Response(ProjectSerializer(p).data)
        except Project.DoesNotExist:
            return Response({'error':'Not found'}, status=404)

    def put(self, request, pk):
        user, err = get_user(request)
        if err: return err
        try:
            p = Project.objects.get(pk=pk, owner=user)
            s = ProjectSerializer(p, data=request.data, partial=True)
            if s.is_valid():
                s.save()
                return Response(s.data)
            return Response(s.errors, status=400)
        except Project.DoesNotExist:
            return Response({'error':'Not found'}, status=404)

    def delete(self, request, pk):
        user, err = get_user(request)
        if err: return err
        try:
            Project.objects.get(pk=pk, owner=user).delete()
            return Response({'message':'Deleted'})
        except Project.DoesNotExist:
            return Response({'error':'Not found'}, status=404)

class TaskListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        user, err = get_user(request)
        if err: return err
        project_id = request.query_params.get('project')
        sprint_id = request.query_params.get('sprint')
        tasks = Task.objects.filter(project__owner=user)
        if project_id: tasks = tasks.filter(project_id=project_id)
        if sprint_id: tasks = tasks.filter(sprint_id=sprint_id)
        return Response(TaskSerializer(tasks, many=True).data)

    def post(self, request):
        user, err = get_user(request)
        if err: return err
        try:
            project = Project.objects.get(pk=request.data.get('project_id'), owner=user)
            task = Task.objects.create(
                title=request.data.get('title'),
                description=request.data.get('description',''),
                project=project,
                created_by=user,
                priority=request.data.get('priority','medium'),
                status=request.data.get('status','todo'),
                due_date=request.data.get('due_date') or None,
                estimated_hours=request.data.get('estimated_hours', 0),
            )
            if request.data.get('assignee_id'):
                from accounts.models import User as U
                task.assignee = U.objects.get(pk=request.data['assignee_id'])
                task.save()
            if request.data.get('sprint_id'):
                task.sprint = Sprint.objects.get(pk=request.data['sprint_id'])
                task.save()
            return Response(TaskSerializer(task).data, status=201)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

class TaskDetailView(APIView):
    permission_classes = [AllowAny]
    def put(self, request, pk):
        user, err = get_user(request)
        if err: return err
        try:
            task = Task.objects.get(pk=pk)
            for field in ['title','description','priority','status','due_date','estimated_hours']:
                if field in request.data:
                    setattr(task, field, request.data[field])
            if 'assignee_id' in request.data:
                from accounts.models import User as U
                task.assignee = U.objects.get(pk=request.data['assignee_id']) if request.data['assignee_id'] else None
            if 'sprint_id' in request.data:
                task.sprint = Sprint.objects.get(pk=request.data['sprint_id']) if request.data['sprint_id'] else None
            task.save()
            return Response(TaskSerializer(task).data)
        except Task.DoesNotExist:
            return Response({'error':'Not found'}, status=404)

    def delete(self, request, pk):
        user, err = get_user(request)
        if err: return err
        try:
            Task.objects.get(pk=pk).delete()
            return Response({'message':'Deleted'})
        except Task.DoesNotExist:
            return Response({'error':'Not found'}, status=404)

class SprintListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        user, err = get_user(request)
        if err: return err
        project_id = request.query_params.get('project')
        sprints = Sprint.objects.filter(project__owner=user)
        if project_id: sprints = sprints.filter(project_id=project_id)
        return Response(SprintSerializer(sprints, many=True).data)

    def post(self, request):
        user, err = get_user(request)
        if err: return err
        try:
            project = Project.objects.get(pk=request.data.get('project_id'), owner=user)
            sprint = Sprint.objects.create(
                name=request.data.get('name'),
                project=project,
                start_date=request.data.get('start_date'),
                end_date=request.data.get('end_date'),
                goal=request.data.get('goal',''),
                is_active=request.data.get('is_active', False)
            )
            return Response(SprintSerializer(sprint).data, status=201)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

class CommentView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, task_id):
        user, err = get_user(request)
        if err: return err
        try:
            task = Task.objects.get(pk=task_id)
            comment = Comment.objects.create(
                task=task,
                author=user,
                content=request.data.get('content')
            )
            return Response(CommentSerializer(comment).data, status=201)
        except Task.DoesNotExist:
            return Response({'error':'Task not found'}, status=404)

class AITaskBreakdownView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        user, err = get_user(request)
        if err: return err
        goal = request.data.get('goal','')
        if not goal:
            return Response({'error':'Goal required'}, status=400)
        try:
            import json
            from google import genai as gai
            client = gai.Client(api_key=os.environ.get('GEMINI_API_KEY',''))
            result = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=f"""Break down this project goal into specific tasks.
Goal: {goal}
Return ONLY a JSON array like this:
[{{"title":"Task name","description":"Details","priority":"high","estimated_hours":2}}]
Return 5-8 tasks. No extra text, just JSON.""")
            text = result.text.strip().replace('```json','').replace('```','').strip()
            tasks = json.loads(text)
            return Response({'tasks': tasks})
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class AISprintPlanView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        user, err = get_user(request)
        if err: return err
        project_id = request.data.get('project_id')
        duration = request.data.get('duration_days', 14)
        try:
            import json
            from google import genai as gai
            project = Project.objects.get(pk=project_id, owner=user)
            tasks = Task.objects.filter(project=project, status='todo')
            task_list = [f"- {t.title} ({t.priority}, {t.estimated_hours}h)" for t in tasks]
            client = gai.Client(api_key=os.environ.get('GEMINI_API_KEY',''))
            result = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=f"""Create a sprint plan.
Project: {project.name}
Duration: {duration} days
Pending tasks:
{chr(10).join(task_list) if task_list else 'No tasks yet'}
Return ONLY JSON:
{{"sprint_name":"Sprint 1","goal":"goal here","recommended_tasks":["task1","task2"],"total_hours":40,"advice":"advice here"}}""")
            text = result.text.strip().replace('```json','').replace('```','').strip()
            plan = json.loads(text)
            return Response({'plan': plan})
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class DashboardView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        user, err = get_user(request)
        if err: return err
        from teams.models import Team
        projects = Project.objects.filter(owner=user)
        tasks = Task.objects.filter(project__owner=user)
        return Response({
            'total_projects': projects.count(),
            'active_projects': projects.filter(status='active').count(),
            'total_tasks': tasks.count(),
            'todo': tasks.filter(status='todo').count(),
            'in_progress': tasks.filter(status='in_progress').count(),
            'review': tasks.filter(status='review').count(),
            'done': tasks.filter(status='done').count(),
            'teams': Team.objects.filter(owner=user).count(),
            'my_tasks': tasks.filter(assignee=user).count(),
        })
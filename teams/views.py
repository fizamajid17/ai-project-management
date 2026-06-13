from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Team, TeamMember
from .serializers import TeamSerializer, TeamMemberSerializer
from accounts.views import get_user_from_request
from accounts.models import User

class TeamListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        user = get_user_from_request(request)
        if not user: return Response({'error':'Unauthorized'}, status=401)
        teams = (Team.objects.filter(members=user) | Team.objects.filter(owner=user)).distinct()
        result = []
        for team in teams:
            data = TeamSerializer(team).data
            members = TeamMember.objects.filter(team=team)
            data['members'] = TeamMemberSerializer(members, many=True).data
            result.append(data)
        return Response(result)

    def post(self, request):
        user = get_user_from_request(request)
        if not user: return Response({'error':'Unauthorized'}, status=401)
        team = Team.objects.create(
            name=request.data.get('name'),
            description=request.data.get('description',''),
            owner=user
        )
        TeamMember.objects.create(team=team, user=user, role='admin')
        return Response(TeamSerializer(team).data, status=201)

class TeamDetailView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, pk):
        user = get_user_from_request(request)
        if not user: return Response({'error':'Unauthorized'}, status=401)
        try:
            team = Team.objects.get(pk=pk)
            members = TeamMember.objects.filter(team=team)
            data = TeamSerializer(team).data
            data['members'] = TeamMemberSerializer(members, many=True).data
            return Response(data)
        except Team.DoesNotExist:
            return Response({'error':'Not found'}, status=404)

    def delete(self, request, pk):
        user = get_user_from_request(request)
        if not user: return Response({'error':'Unauthorized'}, status=401)
        try:
            team = Team.objects.get(pk=pk, owner=user)
            team.delete()
            return Response({'message':'Deleted'})
        except Team.DoesNotExist:
            return Response({'error':'Not found'}, status=404)

class AddMemberView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, pk):
        user = get_user_from_request(request)
        if not user: return Response({'error':'Unauthorized'}, status=401)
        try:
            team = Team.objects.get(pk=pk)
            email = request.data.get('email')
            new_user = User.objects.get(email=email)
            member, created = TeamMember.objects.get_or_create(team=team, user=new_user, defaults={'role': request.data.get('role','member')})
            return Response(TeamMemberSerializer(member).data, status=201)
        except Exception as e:
            return Response({'error': str(e)}, status=400)
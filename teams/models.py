from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    owner = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='owned_teams')
    members = models.ManyToManyField('accounts.User', through='TeamMember', related_name='teams')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'teams'

class TeamMember(models.Model):
    ROLE_CHOICES = [('admin','Admin'),('member','Member'),('viewer','Viewer')]
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'team_members'
        unique_together = ('team', 'user')
from django.conf import settings
from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=100)
    club = models.CharField(max_length=100)
    season = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} — {self.season}"


class TeamMembership(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="team_memberships",
    )

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="memberships",
    )

    number = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "team"],
                name="unique_user_team_membership",
            ),
        ]

    def __str__(self):
        return f"{self.user} → {self.team}"
from django import forms

from accounts.models import User
from .models import Team, TeamMembership


class CreateTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ["name", "club", "season"]


class AddMemberForm(forms.Form):
    member = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Utilisateur",
    )

    number = forms.IntegerField(
        required=False,
        min_value=1,
        max_value=99,
        label="Numéro",
    )

    def __init__(self, *args, team=None, **kwargs):
        super().__init__(*args, **kwargs)

        if team is not None:
            existing_members = TeamMembership.objects.filter(
                team=team
            ).values_list("user_id", flat=True)

            self.fields["member"] = forms.ModelChoiceField(
                queryset=User.objects.exclude(
                    id__in=existing_members
                ),
                label="Utilisateur",
            )
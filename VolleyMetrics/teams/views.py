from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import AddMemberForm, CreateTeamForm
from .models import Team, TeamMembership


def user_is_coach(user):
    return user.is_superuser or user.role == "COACH"


@login_required
def team_list(request):
    teams = (
        Team.objects
        .filter(memberships__user=request.user)
        .distinct()
        .order_by("season", "name")
    )

    return render(
        request,
        "teams/team_list.html",
        {
            "teams": teams,
        },
    )


@login_required
def team_detail(request, team_id):
    team = get_object_or_404(
        Team.objects.prefetch_related(
            "memberships__user"
        ),
        pk=team_id,
        memberships__user=request.user,
    )

    memberships = team.memberships.select_related("user") # type: ignore

    return render(
        request,
        "teams/team_detail.html",
        {
            "team": team,
            "memberships": memberships,
        },
    )


@login_required
@require_http_methods(["GET", "POST"])
def create_team(request):
    if not user_is_coach(request.user):
        return HttpResponseForbidden(
            "Seuls les coachs peuvent créer une équipe."
        )

    if request.method == "POST":
        form = CreateTeamForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                team = form.save()

                TeamMembership.objects.create(
                    user=request.user,
                    team=team,
                )

            return redirect("team_detail", team_id=team.pk)

    else:
        form = CreateTeamForm()

    return render(
        request,
        "teams/team_form.html",
        {
            "form": form,
        },
    )


@login_required
@require_http_methods(["GET", "POST"])
def add_member(request, team_id):
    if not user_is_coach(request.user):
        return HttpResponseForbidden(
            "Seuls les coachs peuvent ajouter des membres."
        )

    team = get_object_or_404(
        Team,
        pk=team_id,
        memberships__user=request.user,
    )

    if request.method == "POST":
        form = AddMemberForm(
            request.POST,
            team=team,
        )

        if form.is_valid():
            try:
                TeamMembership.objects.create(
                    user=form.cleaned_data["member"],
                    team=team,
                    number=form.cleaned_data["number"],
                )
            except IntegrityError:
                form.add_error(
                    "member",
                    "Cet utilisateur appartient déjà à cette équipe.",
                )
            else:
                return redirect(
                    "team_detail",
                    team_id=team.pk,
                )
    else:
        form = AddMemberForm(team=team)

    return render(
        request,
        "teams/add_member.html",
        {
            "form": form,
            "team": team,
        },
    )


@login_required
@require_http_methods(["POST"])
def remove_member(request, team_id, membership_id):
    if not user_is_coach(request.user):
        return HttpResponseForbidden(
            "Seuls les coachs peuvent supprimer des membres."
        )

    team = get_object_or_404(
        Team,
        pk=team_id,
        memberships__user=request.user,
    )

    membership = get_object_or_404(
        TeamMembership,
        pk=membership_id,
        team=team,
    )

    membership.delete()

    return redirect(
        "team_detail",
        team_id=team.pk,
    )
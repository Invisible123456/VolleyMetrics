from django.urls import path

from . import views


urlpatterns = [
    path(
        "",
        views.team_list,
        name="team_list",
    ),

    path(
        "create/",
        views.create_team,
        name="create_team",
    ),

    path(
        "<int:team_id>/",
        views.team_detail,
        name="team_detail",
    ),

    path(
        "<int:team_id>/members/add/",
        views.add_member,
        name="add_member",
    ),

    path(
        "<int:team_id>/members/<int:membership_id>/remove/",
        views.remove_member,
        name="remove_member",
    ),
]
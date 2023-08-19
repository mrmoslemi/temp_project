from django.urls import re_path
from . import views

app_name = "authentication"
urlpatterns = [
    re_path(r"^modules/$", views.ModulesView.as_view(actions={"get": "list"})),
    re_path(
        r"^groups/$",
        views.GroupsView.as_view(actions={"get": "list", "post": "create"}),
    ),
    re_path(
        r"^groups/(?P<uuid>[\w-]+)/$",
        views.GroupsView.as_view(
            actions={"get": "retrieve", "patch": "edit", "delete": "delete"}
        ),
    ),
]

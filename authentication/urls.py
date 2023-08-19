from django.urls import re_path
from . import views

app_name = "authentication"
urlpatterns = [
    re_path(r"^register/$", views.RegisterView.as_view(actions={"post": "create"})),
    re_path(r"^login/$", views.LoginView.as_view(actions={"post": "create"})),
    # re_path(r"^access-tokens/$", views.TokensView.as_view(actions={"post": "create"})),
    # re_path(
    #     r"^access-tokens/verify/$",
    #     views.VerifyTokenView.as_view(actions={"post": "verify"}),
    # ),
    # re_path(
    #     r"^access-token/$",
    #     views.AccessTokenView.as_view(actions={"post": "create"}),
    # ),
   
]

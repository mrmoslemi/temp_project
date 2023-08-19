from django.shortcuts import render
from rest_framework.permissions import AllowAny
from utils import views, requests
from utils.permissions import access_permission, crud_access_permission
from . import models
from authentication import models as auth_models
from . import serializers
from . import messages

# Create your views here.


class GroupsView(
    views.ModelViewSet,
    views.RetrieveModelMixin,
    views.CreateModelMixin,
    views.ListModelMixin,
    views.EditModelMixin,
    views.DeleteModelMixin,
):
    model = models.Group
    permission_classes = [crud_access_permission("Authentication", "Group")]
    serializer_class = {
        "retrieve": serializers.GroupRetrieveSerializer,
        "list": serializers.GroupListSerializer,
    }


class ModulesView(views.ModelViewSet, views.ListModelMixin):
    permission_classes = [access_permission("Authorization.Module.list")]
    model = models.Module
    serializer_class = serializers.ModuleSerializer


from rest_framework.views import APIView


class AuthorizeView(APIView):
    permission_classes = [AllowAny]

    def post(self, *args, **kwargs):
        data: dict = self.request.data
        path = data.get("path", None)
        token = data.get("token", None)
        metadata = data.get("metadata", None)

        if not path or not token:
            return requests.BadRequest(messages.authorization_bad_request_error)
        action = models.Action.get_with_path(path)
        if not action:
            raise requests.BadRequest(messages.wrong_key_path_error)

        user = auth_models.AccessToken.verify_token(token)
        if not user:
            return requests.UnAuthorized(messages.invalid_token_error)

        has_access = action.has_access(user)
        if not has_access:
            raise requests.Forbidden(messages.wrong_key_path_error)
        models.Log.objects.create(user=user, action=action, metadata=metadata)
        user_info = serializers.UserInfoSerializer(user)
        return requests.Ok(data={"has_access": True, "user_info": user_info.data})

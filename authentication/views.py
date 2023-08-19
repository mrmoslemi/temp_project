from django.shortcuts import render
from rest_framework.permissions import AllowAny
from utils import views, requests
from utils.permissions import access_permission, crud_access_permission
from . import models
from . import serializers

# Create your views here.


class RegisterView(views.ModelViewSet, views.CreateModelMixin):
    pass


class LoginView(views.ModelViewSet):
    pass


class UsersTokenView(views.ModelViewSet):
    permission_classes = [AllowAny]
    model = models.User
    serializer_class = serializers.UserRetrieveSerializer

    def retrieve_authenticated(self, *args, **kwargs):
        pass

    def retrieve_authorized(self, *args, **kwargs):
        try:
            token = self.request.data.get("token")
            module = self.request.data.get("module")
            entity = self.request.data.get("entity", None)
            action = self.request.data.get("action", None)
            instance = self.request.data.get("instance", None)
            user = models.AccessToken.verify_token(token)
            if not user:
                return requests.UnAuthorized()
            has_access = user.has_access(module, entity, action, instance)
            if has_access:
                models.AccessLog.objects.create(
                    user=user,
                    module=module,
                    entity=entity,
                    action=action,
                    instance=instance,
                )
                return requests.Ok(
                    {
                        "has_access": True,
                        "user": serializers.UserSerializer(
                            user, context=self.get_serializer_context
                        ),
                    }
                )
        except KeyError:
            return requests.BadRequest()


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
    permission_classes = [access_permission("Authentication", "Access")]
    model = models.Module
    serializer_class = serializers.ModuleSerializer

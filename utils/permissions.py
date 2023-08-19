from rest_framework.permissions import IsAuthenticated


def access_permission(path: str):
    class PermissionClass(IsAuthenticated):
        def has_permission(self, request, view):
            from authorization.models import Grant, Action

            if request.user.is_superuser:
                return True
            action = Action.get_with_path(path)
            has_grant = Grant.objects.filter(action=action, group__user=request.user)
            return super().has_permission(request, view) and has_grant

    return PermissionClass


def crud_access_permission(module: str, entity: str = None):
    class PermissionClass(IsAuthenticated):
        def has_permission(self, request, view):
            if not request.user.is_authenticated:
                return False
            if view.action in [
                "list",
                "paginate",
                "create",
                "find",
                "retrieve",
                "delete",
                "update",
            ]:
                return request.user.has_access(
                    module=module, entity=entity, action=view.action
                )

            if view.action in ["retrieve", "delete", "edit"]:
                return request.user.has_access(
                    module=module,
                    entity=entity,
                    action=view.action,
                )

    return PermissionClass

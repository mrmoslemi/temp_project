from rest_framework.permissions import IsAuthenticated


def access_permission(
    module: str, entity: str = None, action: str = None, instance: str = None
):
    class PermissionClass(IsAuthenticated):
        def has_permission(self, request, view):
            return super(self, IsAuthenticated) and request.user.has_access(
                module, entity, action, instance
            )

    return PermissionClass


def crud_access_permission(module: str, entity: str = None):
    class PermissionClass(IsAuthenticated):
        def has_permission(self, request, view):
            if not request.user.is_authenticated:
                return False
            if view.action in ["create", "list", "paginated_list", "find"]:
                return request.user.has_access(
                    module=module, entity=entity, action=view.action
                )

            if view.action in ["retrieve", "delete", "edit"]:
                return request.user.has_access(
                    module=module,
                    entity=entity,
                    action=view.action,
                    instance=view.kwargs["pk"],
                )

    return PermissionClass

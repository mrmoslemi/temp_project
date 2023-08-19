from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

from . import messages
from utils.requests import Ok, BadRequest, NotFound, Created, Forbidden
from django.db import models

from drf_yasg.utils import swagger_auto_schema


class ModelViewSet(ViewSet):
    model = None
    serializer_class = None
    lookup_fields = None
    text_lookup_fields = None
    max_results = None
    queryset = None
    page_size = None
    order_fields = None
    default_order = None
    operator = Q.AND

    def get_user_ip(self):
        x_forwarded_for = self.request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = self.request.META.get("REMOTE_ADDR")
        return ip

    def get_queryset(self):
        queryset = self.get_unsliced_queryset()
        order_by = self.request.query_params.get("order_by")
        if self.order_fields and order_by in self.order_fields:
            queryset = queryset.order_by(order_by)
        elif self.default_order:
            queryset = queryset.order_by(self.default_order)

        if self.max_results != -1:
            queryset = queryset[: self.max_results]
        return queryset

    def get_unsliced_queryset(self):
        query = None
        if self.lookup_fields:
            for lookup_field in self.lookup_fields:
                filter_query = dict()
                if lookup_field.endswith("__in"):
                    key = lookup_field + "[]"
                    value = self.request.query_params.getlist(key, None)
                else:
                    key = lookup_field
                    value = self.request.query_params.get(key, None)
                if value:
                    if value == "true":
                        value = True
                    if value == "false":
                        value = False
                    if value == "null":
                        value = None
                    filter_query[lookup_field] = value
                    q = Q(**filter_query)
                    if query is None:
                        query = q
                    else:
                        query.add(q, self.operator)
        if not query:
            query = Q(id__isnull=False)
        if self.queryset is not None:
            query_set = self.queryset.filter(query)
        else:
            query_set = self.model.objects.filter(query)
        if self.text_lookup_fields:
            text_query = self.request.query_params.get("q", None)
            if text_query:
                args = []
                for text_lookup_field in self.text_lookup_fields:
                    args.append(text_lookup_field)
                    from django.db.models import Value

                    args.append(Value(" "))
                from django.db.models.functions import Concat
                from django.db.models import TextField

                concat = Concat(*args, output_field=TextField())
                query_set = query_set.annotate(texts=concat).filter(
                    texts__icontains=text_query
                )
        return query_set

    def get_serializer_class(self):
        if isinstance(self.serializer_class, dict):
            return self.serializer_class.get(self.action)
        return self.serializer_class

    def get_serializer_context(self):
        return {"request": self.request, "view": self}

    def get_object(
        self,
        queryset: models.QuerySet = None,
        keyword: str = "uuid",
        lookup_field: str = "uuid",
    ):
        if not queryset:
            queryset = self.get_queryset()

        try:
            obj = queryset.get(**{lookup_field: self.kwargs[keyword]})
            self.check_object_permissions(self.request, obj)
            return obj
        except ObjectDoesNotExist:
            raise NotFound(self.get_not_found_message())

    def find_object(self):
        try:
            obj = self.get_queryset().first()
            self.check_object_permissions(self.request, obj)
            return obj
        except ObjectDoesNotExist:
            raise NotFound(self.get_not_found_message())

    def check_object_permissions(self, request, obj):
        for permission in self.get_permissions():
            if permission.has_object_permission(request, self, obj):
                return True
        raise Forbidden(self.get_forbidden_message(obj))

    def get_forbidden_message(self, instance):
        return messages.default_forbidden_message

    def get_not_found_message(self):
        return messages.default_not_found_message


class RetrieveModelMixin:
    @action(detail=True, methods=["GET"])
    def retrieve(self, *args, **kwargs):
        try:
            obj = self.get_object()
            self.check_object_permissions(self.request, obj)
            serializer_class = self.get_serializer_class()
            serializer_context = self.get_serializer_context()
            serializer = serializer_class(obj, context=serializer_context)
            data = serializer.data
            return Ok(data)
        except ObjectDoesNotExist:
            return NotFound(self.get_not_found_message())
        except BadRequest as response:
            return response


class FindModelMixin:
    @action(detail=True, methods=["GET"])
    def find(self, *args, **kwargs):
        try:
            obj = self.find_object()
            self.check_object_permissions(self.request, obj)
            serializer_class = self.get_serializer_class()
            serializer_context = self.get_serializer_context()
            serializer = serializer_class(obj, context=serializer_context)
            data = serializer.data
            return Ok(data)
        except BadRequest as response:
            return response


class ListModelMixin:
    @action(detail=True, methods=["GET"])
    def list(self, *args, **kwargs):
        try:
            self.queryset = self.get_queryset()
            for obj in self.queryset:
                try:
                    self.check_object_permissions(self.request, obj)
                except Exception as error:
                    raise error

            serializer_class = self.get_serializer_class()
            serializer_context = self.get_serializer_context()
            serializer = serializer_class(
                self.queryset, many=True, context=serializer_context
            )
            data = serializer.data
            return Ok(data)
        except BadRequest as response:
            return response


class PaginateModelMixin:
    page_size = 20

    @action(detail=True, methods=["GET"])
    def paginate(self, *args, **kwargs):
        try:
            self.queryset = self.get_queryset()

            page = self.get_page()
            start_index = (page - 1) * self.page_size
            end_index = page * self.page_size
            for obj in instances:
                try:
                    self.check_object_permissions(self.request, obj)
                except Exception as error:
                    raise error
            instances = self.queryset[start_index:end_index]
            serializer_class = self.get_serializer_class()
            serializer_context = self.get_serializer_context()
            serializer = serializer_class(
                instances, many=True, context=serializer_context
            )
            data = serializer.data
            return Ok(
                {
                    "results": data,
                    "next": "",
                    "pages": self.get_page_count(),
                    "page": page,
                }
            )

        except BadRequest as response:
            return response

    def get_page(self):
        try:
            page = int(self.request.query_params.get("page", 1))
            if page < 1:
                raise ValueError
        except ValueError:
            page = 1
        return page

    def get_page_count(self):
        count = self.queryset.count()
        pages = int(count / self.page_size) + 1
        if count % self.page_size == 0:
            pages -= 1
        return pages


class CreateModelMixin:
    @action(detail=False, methods=["POST"])
    def create(self, *args, **kwargs):
        try:
            serializer_class = self.get_serializer_class()
            serializer_context = self.get_serializer_context()
            serializer = serializer_class(
                context=serializer_context, data=self.request.data
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Created(self.get_create_message(serializer.instance))
        except BadRequest as response:
            return response

    def get_create_message(self, instance):
        return messages.default_created_message


class EditModelMixin:
    @action(detail=True, methods=["POST"])
    def edit(self, *args, **kwargs):
        try:
            obj = self.get_object()
            self.check_object_permissions(self.request, obj)
            serializer_class = self.get_serializer_class()
            serializer_context = self.get_serializer_context()
            serializer = serializer_class(
                obj, context=serializer_context, data=self.request.data
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Ok(self.get_edit_message(serializer.instance))
        except ObjectDoesNotExist:
            return NotFound(self.get_not_found_message())
        except BadRequest as response:
            return response

    def get_edit_message(self, instance):
        return messages.default_edited_message


class DeleteModelMixin:
    @action(detail=True, methods=["POST"])
    def delete(self, *args, **kwargs):
        try:
            obj = self.get_object()
            self.check_object_permissions(self.request, obj)
            obj.delete()
            return Ok(self.get_delete_message(obj))
        except ObjectDoesNotExist:
            return NotFound(self.get_not_found_message())
        except BadRequest as response:
            return response

    def get_delete_message(self, instance):
        return messages.default_deleted_message

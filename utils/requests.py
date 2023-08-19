import sys
import utils.method as m

GET = "get"
POST = "post"
DELETE = "delete"
PATCH = "patch"
METHODS = (GET, POST, DELETE, PATCH)
OK = 200
CREATED = 201
PARTIAL_CONTENT = 206
ALREADY_REPORTED = 208

MOVED = 301
FOUND = 302

BAD_REQUEST = 400
UNAUTHORIZED = 401
PAYMENT_REQUIRED = 402
FORBIDDEN = 403
NOT_FOUND = 404
METHOD_NOT_ALLOWED = 405
NOT_ACCEPTABLE = 406
CONFLICT = 409
GONE = 410
TOO_LARGE = 413
UNSUPPORTED_MEDIA_TYPE = 415
TOO_MANY_REQUESTS = 429

STATUS_CODES = (
    # OK
    OK,
    CREATED,
    PARTIAL_CONTENT,
    # Redirect
    MOVED,
    # Bad request
    BAD_REQUEST,
    UNAUTHORIZED,
    PAYMENT_REQUIRED,
    FORBIDDEN,
    NOT_FOUND,
    METHOD_NOT_ALLOWED,
    NOT_ACCEPTABLE,
    CONFLICT,
    GONE,
    TOO_LARGE,
    UNSUPPORTED_MEDIA_TYPE,
    TOO_MANY_REQUESTS,
)


def requests(url, method, data, absolute_path=None, headers=None):
    if headers is None:
        headers = {}
    if method not in m.METHODS:
        raise Exception("invalid method")

    if "test" in sys.argv:
        from django.test import Client

        requester = Client()
        if method == m.POST:
            return requester.post(path="/" + url, data=data, **headers)
        if method == m.GET:
            return requester.get(path="/" + url, data=data, **headers)
    if "test" not in sys.argv:
        import requests as requester

        if method == m.POST:
            return requester.post(url=absolute_path + url, data=data, headers=headers)
        if method == m.GET:
            return requester.get(url=absolute_path + url, data=data, headers=headers)
        if method == m.DELETE:
            return requester.delete(url=absolute_path + url, data=data, headers=headers)
        if method == m.PATCH:
            return requester.patch(url=absolute_path + url, data=data, headers=headers)


from rest_framework.response import Response


class Ok(Response):
    status = OK
    template_name = None

    def __init__(self, data=None, status=None, template_name=None):
        if status is None:
            status = self.status
        if template_name is None:
            status = self.template_name
        super().__init__(data=data, status=status, template_name=template_name)


class Page(Response):
    pass


class Created(Ok):
    status = CREATED


class PartialContent(Ok):
    status = PARTIAL_CONTENT


class AlreadyReported(Ok):
    status = ALREADY_REPORTED


class Found(Ok):
    status = FOUND

    def __init__(self, location, data=None, status=None):
        super().__init__(data=data, status=status)
        self["Location"] = location


class BadRequest(Ok, Exception):
    status = BAD_REQUEST

    def __init__(self, data=None, status=None, template_name=None):
        if status is None:
            status = self.status

        if template_name is None:
            status = self.template_name
        self.status_code = self.status
        super().__init__(data=data, status=status, template_name=template_name)


class Conflict(BadRequest):
    status = CONFLICT


class PaymentRequired(BadRequest):
    status = PAYMENT_REQUIRED


class NotFound(BadRequest):
    status = NOT_FOUND


class Forbidden(BadRequest):
    status = FORBIDDEN


class NotAcceptable(BadRequest):
    status = NOT_ACCEPTABLE


class TooManyRequests(BadRequest):
    status = TOO_MANY_REQUESTS


class UnAuthorized(BadRequest):
    status = UNAUTHORIZED

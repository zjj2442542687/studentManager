from drf_yasg import openapi
from drf_yasg.openapi import Schema


def request_body(properties, required=None):
    return openapi.Schema(
        description="python/Django",
        title="中小学生管理系统",
        type=openapi.TYPE_OBJECT,
        required=required,
        properties=properties
    )


def string_schema(description=None, default=None, title=None, f=None):
    return openapi.Schema(type=openapi.TYPE_STRING, description=description, default=default, title=title, format=f)


def integer_schema(description=None, default=None, title=None):
    return openapi.Schema(type=openapi.TYPE_INTEGER, description=description, default=default, title=title)


def array_schema(description=None, default=None, it=None):
    if not it:
        it = openapi.Schema(type=openapi.TYPE_INTEGER)
    return openapi.Schema(type=openapi.TYPE_ARRAY, description=description, default=default, items=it)


def schema(type=openapi.TYPE_STRING, description=None, default=None):
    return openapi.Schema(type=type, description=description, default=default)

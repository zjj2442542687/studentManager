from drf_yasg import openapi


def request_body(properties, required=None):
    return openapi.Schema(
        description="python/Django",
        title="中小学生管理系统",
        type=openapi.TYPE_OBJECT,
        required=required,
        properties=properties
    )


def string_schema(description=None, default=None):
    return openapi.Schema(type=openapi.TYPE_STRING, description=description, default=default)


def integer_schema(description=None, default=None):
    return openapi.Schema(type=openapi.TYPE_INTEGER, description=description, default=default)


def schema(type=openapi.TYPE_STRING, description=None, default=None):
    return openapi.Schema(type=type, description=description, default=default)

from drf_yasg import openapi


def request_body(properties, required=None):
    return openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=required,
        properties=properties
    )


def string_schema(description):
    return openapi.Schema(type=openapi.TYPE_STRING, description=description)


def integer_schema(description):
    return openapi.Schema(type=openapi.TYPE_INTEGER, description=description)


def schema(type=openapi.TYPE_STRING, description=""):
    return openapi.Schema(type=type, description=description)

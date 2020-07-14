from utils.status import *
from rest_framework.response import Response
from rest_framework import status as _status


def response(code=_status.HTTP_201_CREATED, status=None, headers=None, **data):
    data['code'] = code
    if status:
        data['status'] = status
    return Response(data, status=code, headers=headers)


def response_success_200(status=STATUS_200_SUCCESS, headers=None, **data):
    data['code'] = STATUS_200_SUCCESS
    data['status'] = status
    return Response(data, status=_status.HTTP_200_OK, headers=headers)


def response_error_400(status=None, headers=None, **data):
    data['code'] = STATUS_400_BAD_REQUEST
    if status:
        data['status'] = status
    return Response(data, status=_status.HTTP_400_BAD_REQUEST, headers=headers)


def response_error_500(status=STATUS_500_INTERNAL_SERVER_ERROR, headers=None, **data):
    data['code'] = STATUS_500_INTERNAL_SERVER_ERROR
    data['status'] = status
    return Response(data, status=_status.HTTP_500_INTERNAL_SERVER_ERROR, headers=headers)

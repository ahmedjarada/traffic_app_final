from rest_framework.response import Response


def json_response(status_data, data, errors, status_http, msg):
    return Response({'status': status_data, 'data': data, 'errors': errors, 'msg': msg}, status=status_http)


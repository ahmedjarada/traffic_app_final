from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from static_methods.Json_Response import json_response
from .models import History
from .serializers import HistorySerializer


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def add(request):
    lat = None
    long = None
    title = None
    errors = []
    try:
        lat = float(request.data["lat"])
    except KeyError as e:
        errors.append(e.args[0])
    try:
        long = float(request.data["long"])
    except KeyError as e:
        errors.append(e.args[0])
    try:
        title = request.data["title"]
    except KeyError as e:
        errors.append(e.args[0])
    if len(errors) > 0:
        return json_response(status_data=False, data=None, errors=[{err: "This field is required!"} for err in errors],
                             status_http=403, msg="Please fill all required fields")
    else:
        _id = request.user.id
        record = History.objects.create(long=long, lat=lat, title=title, user_id=_id)
        record.save()

        return json_response(status_data=True, data=HistorySerializer(record, many=False).data, errors=None,
                             status_http=201, msg="Success add this location")


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def ls(request):
    records = History.objects.filter(user_id=request.user.id)

    return json_response(status_data=True, data=HistorySerializer(records, many=True).data, errors=None,
                         status_http=200, msg="Success get list of locations")


@permission_classes([IsAuthenticated])
@api_view(['DELETE'])
def delete(request, _id):
    try:
        record = History.objects.get(pk=_id)
    except History.DoesNotExist:
        return json_response(status_data=False, data=None, errors=['not_found'],
                             status_http=404, msg="This record is not found")
    if record.user_id == request.user.id:
        record.delete()
        return json_response(status_data=False, data=None, errors=None,
                             status_http=200, msg="The record has been deleted")
    else:
        return json_response(status_data=False, data=None, errors=None,
                             status_http=401, msg="You cannot delete this record")

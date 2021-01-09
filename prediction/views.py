from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from static_methods.Json_Response import json_response


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




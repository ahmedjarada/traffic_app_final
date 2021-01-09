from django.contrib.auth import login
from django.core.exceptions import ObjectDoesNotExist
from knox.models import AuthToken
from passlib.hash import django_pbkdf2_sha256
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from Auth.AuthSerializer import AuthTokenSerializer
from Auth.knox_view import LoginView as KnoxLoginView
from client.models import ClientResetCode as clientReset
from client.models import ClientToken as client
from client.models import ClientVerificationCode as clientPIN
from static_methods.Json_Response import json_response
from static_methods.generatePINcode import rand_PINCode
from static_methods.sentMail import *
from static_methods.upload import upload_img
from .serializers import *


# Define check account information method
@api_view(["POST"])  # POST method only allowed
@permission_classes([AllowAny])  # Required user login by api
def email_check_validation(request):
    username = None
    email = None
    password = None
    first_name = None
    last_name = None
    state = None
    gender = None
    errors = []
    flag = False
    try:
        username = request.data["username"]
        flag = True
    except KeyError as e:
        errors.append(e.args[0])
    try:
        email = request.data["email"]
        flag = True
    except KeyError as e:
        errors.append(e.args[0])
    try:
        password = request.data["password"]
        flag = True
    except KeyError as e:
        errors.append(e.args[0])

    try:
        first_name = request.data["first_name"]
        flag = True
    except KeyError as e:
        errors.append(e.args[0])
    try:
        last_name = request.data["last_name"]
        flag = True
    except KeyError as e:
        errors.append(e.args[0])
    # try:
    #     state = request.data["state"]
    #     flag = True
    # except KeyError as e:
    #     errors.append(e.args[0])
    try:
        gender = request.data["gender"]
    except KeyError as e:
        pass
    print(errors)
    if len(errors) > 0:
        return json_response(status_data=False, data={}, errors=[{e: "This field is required"} for e in errors],
                             status_http=200,
                             msg='Please fill all required fields')

    if flag:
        if len(User.objects.filter(username=username)) > 0 and len(User.objects.filter(email=email)) > 0:
            return json_response(status_data=False, data={},
                                 errors=[{"email": "This email has already registered!"},
                                         {"username": "This username has already registered!"}], status_http=403,
                                 msg="The account is already exist")
        elif len(User.objects.filter(username=username)) > 0:
            return json_response(status_data=False, data={},
                                 errors=[{"email": "This email has already registered!"}], status_http=403,
                                 msg="The account is already exist")
        elif len(User.objects.filter(email=email)) > 0:
            return json_response(status_data=False, data={},
                                 errors=[{"username": "This username has already registered!"}], status_http=403,
                                 msg="The account is already exist")
        else:
            return json_response(status_data=True, data={},
                                 errors=[], status_http=200,
                                 msg="Pass check info")


class RegisterUserAPI(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    # Serializer :model :  user
    serializer_class = RegisterUserSerializer

    # Define POST Method view of Registration

    def post(self, request, *args, **kwargs):
        username = None
        email = None
        password = None
        first_name = None
        last_name = None
        state = None
        gender = None
        errors = []
        flag = False
        try:
            username = request.data["username"]
            flag = True
        except KeyError as e:
            errors.append(e.args[0])
        try:
            email = request.data["email"]
            flag = True
        except KeyError as e:
            errors.append(e.args[0])
        try:
            password = request.data["password"]
            flag = True
        except KeyError as e:
            errors.append(e.args[0])

        try:
            first_name = request.data["first_name"]
            flag = True
        except KeyError as e:
            errors.append(e.args[0])
        try:
            last_name = request.data["last_name"]
            flag = True
        except KeyError as e:
            errors.append(e.args[0])
        # try:
        #     state = request.data["state"]
        #     flag = True
        # except KeyError as e:
        #     errors.append(e.args[0])
        try:
            gender = request.data["gender"]
        except KeyError as e:
            pass

        if len(errors) > 0:
            return json_response(status_data=False, data={}, errors=[{e: "This field is required"} for e in errors],
                                 status_http=403,
                                 msg='Please fill all required fields')
        if flag:
            if len(User.objects.filter(username=username)) > 0 and len(User.objects.filter(email=email)) > 0:
                return json_response(status_data=False, data={},
                                     errors=[{"email": "This email has already registered!"},
                                             {"username": "This username has already registered!"}], status_http=403,
                                     msg="The account is already exist")
            elif len(User.objects.filter(username=username)) > 0:
                return json_response(status_data=False, data={},
                                     errors=[{"email": "This email has already registered!"}], status_http=403,
                                     msg="The account is already exist")
            elif len(User.objects.filter(email=email)) > 0:
                return json_response(status_data=False, data={},
                                     errors=[{"username": "This username has already registered!"}], status_http=403,
                                     msg="The account is already exist")
            else:
                serializer = self.get_serializer(data=request.data)
                if serializer.is_valid():
                    user = serializer.save()
                    token = AuthToken.objects.create(user)[1]
                    client_token = client.objects.create(token=token, user_id=user)
                    client_token.save()
                    pin = rand_PINCode(4)
                    client_pin = clientPIN.objects.create(user_id=user, reset_by='E', PIN=pin)
                    client_pin.save()
                    login(request, user)
                    send_verification_email = send_verificationPIN_bymail(to_email=user.email, PIN=pin)
                    return json_response(status_data=True, data={
                        "user": UserSerializer(user, many=False).data,
                        "token": token,
                        "email_is_sent": send_verification_email,
                    }, errors=[],
                                         msg='The account has been created successfully', status_http=200)
                else:
                    errors = list(serializer.errors.values())
                    _errors = []
                    for e in errors:
                        _errors.append(e[0])
                    try:
                        return json_response(status_data=False, data={},
                                             errors=_errors, status_http=403,
                                             msg=f"Unable to create this account, {_errors[0].lower()}")
                    except KeyError:
                        return json_response(status_data=False, data={}, errors=['Error Key'], status_http=403,
                                             msg='Error Key')


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):

        try:
            serializer = AuthTokenSerializer(data=request.data)
        except ObjectDoesNotExist:
            return json_response(data={}, status_http=403, msg='The email or password you\'ve entered is incorrect',
                                 status_data=False, errors=['ObjectDoesNotExist', 'Error auth'])

        if serializer.is_valid():
            user = serializer.validated_data['user']
            try:
                login(request, user)
            except ObjectDoesNotExist:
                return json_response(data={}, status_http=403, msg='The email or password you\'ve entered is incorrect',
                                     status_data=False, errors=['ObjectDoesNotExist', 'Error login'])

            return super(LoginAPI, self).post(request, format=None)

        else:

            errors = list(serializer.errors)
            try:
                return json_response(status_data=False, data={},
                                     errors=[{key: serializer.errors[key][0] for key in errors}], status_http=403,
                                     msg='failed to login with this email and password, please try again')

            except KeyError:
                return json_response(status_data=False, data={}, errors=['Error Key'], status_http=403,
                                     msg='Error Key')


# Define request verification method
@api_view(["POST"])  # POST method only allowed
@permission_classes([IsAuthenticated])  # Required user login by api
def request_verification(request):
    if request.method == 'POST':
        # Initialize
        reg_pin = None
        user = None
        # Processes
        try:
            user = User.objects.get(pk=request.user.id)
            reg_pin = clientPIN.objects.get(user_id_id=request.user.id)
        except ObjectDoesNotExist:
            pin = rand_PINCode(4)
            new_pin = clientPIN.objects.create(PIN=pin, user_id=user, reset_by='E')
            new_pin.save()
            flag = send_verificationPIN_bymail(to_email=user.mobile_no, PIN=pin)

            # Return method
            if flag:
                return json_response(status_data=True, data={}, errors=[],
                                     msg='The email message verification has been sent', status_http=200)
        if user.is_verified:
            return json_response(status_data=False, data={}, errors=[],
                                 msg='Your account already verified', status_http=200)
        else:
            if reg_pin.PIN and not reg_pin.is_opened:
                flag = send_verificationPIN_bymail(to_email=user.mobile_no, PIN=reg_pin.PIN)
                if flag:
                    return json_response(status_data=True, data={}, errors=[],
                                         msg='The email message verification has been sent', status_http=200)

                else:
                    return json_response(status_data=False, data={}, errors=['INTERNAL_SERVER_ERROR'],
                                         msg='The message verification has not sent', status_http=403)
            else:
                pin = rand_PINCode(4)
                new_pin = clientPIN.objects.create(PIN=pin, user_id=user, reset_by='E')
                new_pin.save()
                flag = send_verificationPIN_bymail(to_email=user.mobile_no, PIN=pin)
                if flag:
                    return json_response(status_data=True, data={}, errors=[],
                                         msg='The message verification has been sent', status_http=200)
                else:
                    return json_response(status_data=False, data={}, errors=['INTERNAL_SERVER_ERROR'],
                                         msg='Invalid Internal Server Error', status_http=403)


@api_view(["POST"])  # POST method only allowed
@permission_classes([IsAuthenticated])  # Required user login by api
def confirm_verification(request):
    if request.method == 'POST':
        try:
            pin = request.data["pin"]

        except KeyError as e:
            return json_response(status_data=False, data={}, errors=[{f"{e.args[0]}": "This field is required"}],
                                 status_http=403,
                                 msg=f'{e.args[0]} field is required')
        try:
            reg_pin = clientPIN.objects.get(user_id_id=request.user.id)
        except ObjectDoesNotExist:
            return json_response(status_data=False, data={}, errors=['ObjectDoesNotExist'], status_http=403,
                                 msg='Invalid pin')
        try:
            user = User.objects.get(pk=request.user.id)
        except ObjectDoesNotExist:
            return json_response(status_data=False, data={}, errors=['ObjectDoesNotExist'], status_http=403,
                                 msg='Invalid user')
        if reg_pin.PIN == pin:
            if user.is_verified:
                return json_response(status_data=False,
                                     data=UserSerializer(User.objects.get(pk=request.user.id), many=False).data,
                                     errors=[], status_http=200,
                                     msg='Your account already verified')
            else:
                user.is_verified = True
                reg_pin.is_opened = True
                reg_pin.save()
                user.save()
                return json_response(status_data=True,
                                     data=UserSerializer(User.objects.get(pk=request.user.id), many=False).data,
                                     errors=[], status_http=200,
                                     msg='Success verification')
        else:
            return json_response(status_data=False, data={}, errors=['BAD_REQUEST'], status_http=403,
                                 msg='PIN you\'ve entered is incorrect')


# Define get account "current user"
@api_view(["GET"])  # Get method only allowed
@permission_classes([IsAuthenticated])  # Required user login by api
def get_current_account(request):
    # Initialize variables
    me_id = request.user.id
    serializer = None

    # Processes
    try:
        serializer = UserSerializer(User.objects.get(pk=request.user.id), many=False).data
    except ObjectDoesNotExist:
        return json_response(status_data=False, data={}, errors=['ObjectDoesNotExist'], status_http=403,
                             msg='Account not found')
    # Return method
    if serializer is not None:
        return json_response(status_data=True, data=serializer, errors=[], status_http=200,
                             msg='Success get account')
    else:
        return json_response(status_data=False, data={}, errors=['Value Error'], status_http=403,
                             msg='Account not found')


# Define reset password for normal user
@api_view(["POST"])  # POST method only allowed
@permission_classes([AllowAny])  # No token required to access to this method
def forgot_password_request(request):
    # Processes
    try:
        email = request.data['email']
    except Exception:
        return json_response(status_data=False, data={}, errors=['Key Error'], status_http=403,
                             msg='Invalid input')
    try:
        find_ = User.objects.get(email=email)
        registered_email = find_.email
    except Exception:
        return json_response(status_data=False, data={}, errors=['Value Error'], status_http=403,
                             msg='Sorry, no user registered for this email')

    if registered_email == email:
        pin = rand_PINCode(4)
        reset_client = clientReset.objects.create(user_id=find_, reset_for='E', code=pin)
        reset_client.save()

        # Return method
        if send_resetpassword_bymail(find_.email, pin):
            return json_response(status_data=True, data={}, errors=[], status_http=200,
                                 msg='Your reset email message has been sent')
        else:
            return json_response(status_data=False, data={}, errors=[], status_http=403,
                                 msg='Invalid Internal Server Error')

    else:
        return json_response(status_data=False, data={}, errors=[], status_http=403,
                             msg='Sorry, no user registered for this email')


# Define pin that be sent to normal user
@api_view(["POST"])  # POST method only allowed
@permission_classes([AllowAny])  # No token required to access to this method
def forgot_password_check_pin(request):
    # Initialize variables
    pin = None

    # Processes
    try:
        pin = request.data['pin']
    except KeyError as e:
        return json_response(status_data=False, data={}, errors=['Key Error'], status_http=403,
                             msg='No PIN Entered')

    # Return method
    if pin is not None:
        client_reset = clientReset.objects.get(code=pin)
        if not client_reset.is_opened:
            if bool(client_reset):
                return json_response(status_data=True, data={}, errors=[], status_http=200,
                                     msg='Success confirm PIN')

        else:
            return json_response(status_data=False, data={}, errors=['FORBIDDEN'], status_http=403,
                                 msg='Invalid PIN entered')

    else:
        return json_response(status_data=False, data={}, errors=['NOT_FOUND'], status_http=403,
                             msg='No PIN found')


# Define confirm reset password for normal user
@api_view(["POST"])  # POST method only allowed
@permission_classes([AllowAny])  # No token required to access to this method
def forgot_password_confirm(request):
    # Initialize
    pin = None

    # Processes
    try:
        pin = request.data['pin']
        password = request.data['password']
        confirm_password = request.data['confirm_password']
    except KeyError as e:
        return json_response(status_data=False, data={}, errors=['NOT_FOUND'], status_http=403,
                             msg='All fields must be fill')

    if pin is not None:
        client_get_user = clientReset.objects.get(code=pin)
        if not client_get_user.is_opened:
            client_get_user.is_opened = True
            client_get_user.save()
            user = client_get_user.user_id
            if password == confirm_password:
                user.set_password(raw_password=password)
                user.save()
                client_token = client.objects.filter(user_id_id=user.id).delete()

                # Return Method
                return json_response(status_data=True, data={}, errors=[], status_http=200,
                                     msg='Success reset the password, you can login with new password now')
            else:
                return json_response(status_data=False, data={}, errors=['FORBIDDEN'], status_http=403,
                                     msg='Passwords you have entered not matched')
        else:
            return json_response(status_data=False, data={}, errors=['FORBIDDEN'], status_http=403,
                                 msg='Invalid PIN')

    else:
        return json_response(status_data=False, data={}, errors=['NOT_FOUND'], status_http=403,
                             msg='All fields must be fill')


@api_view(["POST"])  # POST method only allowed
@permission_classes([IsAuthenticated])  # Required user login by api
def change_password(request):
    # Processes
    try:
        old_password = request.data['old_password']
        new_password = request.data['new_password']
        con_new_password = request.data['confirm_password']
    except Exception:
        # Exception Return response
        return json_response(status_data=False, data={}, errors=['BAD_REQUEST'], status_http=403,
                             msg='Invalid input')
    try:
        user = User.objects.get(pk=request.user.id)
    except ObjectDoesNotExist:
        return json_response(status_data=False, data={}, errors=['BAD_REQUEST'], status_http=403,
                             msg='Invalid user')
    # Return method
    if old_password == new_password:
        return json_response(status_data=False, data={}, errors=['NOT_ACCEPTABLE'], status_http=403,
                             msg='You entered the same of old password, try another')
    else:
        if django_pbkdf2_sha256.verify(old_password, user.password):
            if con_new_password == new_password:
                try:
                    user.set_password(raw_password=new_password)
                    user.save()
                except Exception:
                    return json_response(status_data=False, data={}, errors=['NO_CONTENT'], status_http=403,
                                         msg='Your password has been not changed, please try again')
                return json_response(status_data=True, data={}, errors=[], status_http=200,
                                     msg='Your password has been changed')
            else:
                return json_response(status_data=False, data={}, errors=['RESET_CONTENT'], status_http=403,
                                     msg='Please try again enter new password and confirm password')
        else:
            return json_response(status_data=False, data={}, errors=['RESET_CONTENT'], status_http=403,
                                 msg='Your current password you\'ve entered is incorrect, please try again')


# @api_view(["POST"])  # POST method only allowed
# @permission_classes([IsAuthenticated])  # Required auth
# def upload_avatar(request):  # Upload avatar image of current user
#     try:
#         current_user = User.objects.get(pk=request.user.id)
#     except User.DoesNotExist as e:
#         return json_response(status_http=403, status_data=False, data={},
#                              errors=['not_found'],
#                              msg="Unable to found this user!")
#     img = upload_img(request, 'img')
#     if img is not None and current_user is not None:
#         current_user.avatar = img
#         current_user.save()
#         return json_response(status_http=200, status_data=True, data=UserSerializer(current_user, many=False).data,
#                              errors=[],
#                              msg="Your image has been added successfully!")


@api_view(["POST"])  # POST method only allowed
@permission_classes([IsAuthenticated])  # Required auth
def update_info(request):  # Upload avatar image of current user

    first_name = None
    last_name = None
    gender = None
    state = None
    try:
        first_name = request.data['first_name']
    except KeyError as e:
        pass
    try:
        last_name = request.data['last_name']
    except KeyError as e:
        pass
    try:
        gender = request.data['gender']
    except KeyError as e:
        pass
    try:
        state = request.data['state']
    except KeyError as e:
        pass
    try:
        current_user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist as e:
        return json_response(status_http=403, status_data=False, data={},
                             errors=['not_found'],
                             msg="Unable to found this user!")
    else:
        if 'img' in request.FILES:
            current_user.avatar = upload_img(request, 'img')
        if first_name is not None:
            current_user.first_name = first_name
        if last_name is not None:
            current_user.first_name = first_name
        if state is not None:
            current_user.state = state
        if gender is not None:
            current_user.first_name = gender
        current_user.save()
        return json_response(status_http=200, status_data=True, data=UserSerializer(current_user, many=False).data,
                             errors=[],
                             msg="Your image has been added successfully!")


@api_view(["POST"])  # POST method only allowed
@permission_classes([AllowAny])  # Accept Anonymous user
def delete_user(request):  # Delete method for any user by email, this endpoint for developers only
    user = None
    email = None
    try:
        email = request.data["email"]
    except KeyError as e:
        return json_response(status_http=403, status_data=False, data={},
                             errors=[{e.args[0]: "This field is required"}],
                             msg="Please fill the required field to do this process")
    if email is not None:
        try:
            user = User.objects.get(email=email)
        except Exception:
            return json_response(status_http=403, status_data=False, data={},
                                 errors=["Not_found"],
                                 msg=f"The user that related to email: {email} not found, please check it and try again")
    if user is not None:
        user.delete()
        try:
            user = User.objects.get(email=email)
        except Exception:
            return json_response(status_http=200, status_data=True, data={},
                                 errors=[],
                                 msg=f"The user that related to this email: {email} has been deleted, any data related to this user has been deleted also")
        return json_response(status_http=403, status_data=False, data={},
                             errors=["Unable", "internal_error"],
                             msg=f"Unable to delete the user that related to this email : {email}")

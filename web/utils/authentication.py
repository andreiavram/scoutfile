from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_sso import claims


def create_authorization_payload(session_token, user, account, **kwargs):
    print(user)
    return {
        claims.TOKEN: claims.TOKEN_AUTHORIZATION,
        claims.SESSION_ID: session_token.id,
        claims.USER_ID: user.email,
        'account': account.pk
    }


def authenticate_payload(payload, request):
    user_model = get_user_model()

    # TODO: refactor here
    try:
        print(claims.USER_ID)
        user = user_model.objects.get(email=claims.USER_ID)
        # service=payload.get(claims.ISSUER),
        # external_id=payload.get(claims.USER_ID)
    except user_model.DoesNotExist:
        raise AuthenticationFailed("User does not exist")

    if not user.is_active:
        raise AuthenticationFailed("User inactive or deleted")
    return user

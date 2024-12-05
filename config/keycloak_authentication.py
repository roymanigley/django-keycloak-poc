from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from jose import JWTError, jwt
import requests
from django.conf import settings
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import base64
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser


class KeycloakAuthentication(BaseAuthentication):

    def authenticate(self, request) -> tuple[AbstractUser, None]:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ")[1]
        try:
            decoded_token = verify_token(token)
            user = get_user_model().objects.filter(
                username=decoded_token['clientId']
            ).first()
            check_role(decoded_token)
            return (user, None)
        except JWTError as e:
            raise AuthenticationFailed(f"Invalid token: {token} - {str(e)}")


def base64url_decode(input_str: str) -> bytes:
    padding = "=" * ((4 - len(input_str) % 4) % 4)  # Add padding
    return base64.urlsafe_b64decode(input_str + padding)


def check_role(decoded_token: dict) -> None:
    """ raises AuthenticationFailed when the role from settings.APP_ROLE is not assigned to the token """
    required_role = settings.APP_ROLE
    roles = decoded_token.get('realm_access', {}).get('roles', [])
    if required_role not in roles:
        raise AuthenticationFailed(
            f"client does not have the role {required_role}"
        )


def get_keycloak_public_key() -> str:
    response = requests.get(
        f"{settings.KC_REALM_URL}/protocol/openid-connect/certs"
    )
    if response.status_code != 200:
        raise ValueError("Failed to fetch JWKS from Keycloak")

    jwks = response.json()
    if not jwks.get("keys"):
        raise ValueError("No keys found in JWKS")

    # probably we alo have to check for the other keys
    key = jwks["keys"][1]
    public_numbers = rsa.RSAPublicNumbers(
        e=int.from_bytes(base64url_decode(key["e"]), "big"),
        n=int.from_bytes(base64url_decode(key["n"]), "big")
    )
    public_key = public_numbers.public_key(default_backend())

    pem_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return pem_key.decode("utf-8")


def verify_token(token: str) -> dict:
    pem_key = get_keycloak_public_key()
    try:
        decoded_token = jwt.decode(
            token,
            pem_key,
            algorithms=["RS256"],
            audience='account',
            issuer=settings.KC_ISSUER
        )
        return decoded_token
    except jwt.JWTError as e:
        raise ValueError(f"Invalid token: {str(e)}")

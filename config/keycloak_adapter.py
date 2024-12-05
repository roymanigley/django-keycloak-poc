from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.http import HttpResponseForbidden
from config.keycloak_authentication import verify_token, check_role


class KeycloakRoleAdapter(DefaultSocialAccountAdapter):

    def pre_social_login(self, request, sociallogin) -> None:
        """ raises an ImmediateHttpResponse if the token can not be verified or does not have the role settings.APP_ROLE assigned """
        access_token = sociallogin.token.token
        try:
            decoded_token = verify_token(access_token)
            check_role(decoded_token)
        except Exception as e:
            raise ImmediateHttpResponse(
                HttpResponseForbidden(
                    e.__str__()
                )
            )

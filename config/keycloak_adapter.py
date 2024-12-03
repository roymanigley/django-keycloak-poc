from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.http import HttpResponseForbidden
import json


class KeycloakRoleAdapter(DefaultSocialAccountAdapter):
    REQUIRED_ROLE = "specific-role"  # Replace with your required Keycloak role

    def pre_social_login(self, request, sociallogin):
        # Extract Keycloak roles from the token
        access_token = sociallogin.token.token
        roles = self.get_keycloak_roles(access_token)
        print(roles)

        if self.REQUIRED_ROLE not in roles:
            # Deny login if the role is missing
            raise ImmediateHttpResponse(HttpResponseForbidden(
                "Access denied: missing required role."))

    def get_keycloak_roles(self, access_token):
        import jwt

        decoded_token = jwt.decode(access_token, options={
                                   "verify_signature": False})
        realm_access = decoded_token.get("realm_access", {})
        roles = []

        # Replace '<client-id>' with your Keycloak client ID
        client_roles = realm_access.get("roles", [])
        roles.extend(client_roles)

        return roles

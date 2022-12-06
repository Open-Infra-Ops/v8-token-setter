from django.http import JsonResponse
from rest_framework.generics import GenericAPIView
from token_setter.utils import connect_obs_client, get_metadata
from token_setter.permissions import QueryPermission


class TokenView(GenericAPIView):
    permission_classes = (QueryPermission,)

    def get(self, request, *args, **kwargs):
        obs_client = connect_obs_client()
        access_token, refresh_token = get_metadata(obs_client)
        return JsonResponse({'access_token': access_token})

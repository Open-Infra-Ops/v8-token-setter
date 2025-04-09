import os
import logging
import requests
import sys
from socket import gaierror
from obs import ObsClient
from django.conf import settings


logger = logging.getLogger('log')
Config = settings.CONFIG


def connect_obs_client():
    access_key_id = Config.get('ACCESS_KEY_ID', '')
    secret_access_key = Config.get('SECRET_ACCESS_KEY', '')
    endpoint = Config.get('OBS_ENDPOINT', '')
    obs_client = ObsClient(access_key_id=access_key_id,
                           secret_access_key=secret_access_key,
                           server='https://{}'.format(endpoint))
    return obs_client


def refresh(obs_client, refresh_token):
    url = 'https://gitee.com/oauth/token?grant_type=refresh_token&refresh_token={}'.format(refresh_token)
    r = requests.post(url)
    if r.status_code != 200:
        logger.error('Fail to refresh token')
        logger.error(r.json())
        sys.exit(1)
    else:
        logger.info('Refresh token successfully.')
    new_access_token = r.json()['access_token']
    new_refresh_token = r.json()['refresh_token']
    if not set_metadata(obs_client, new_access_token, new_refresh_token):
        logger.error('Fail to update metadata in OBS.')
    else:
        logger.info('Update metadata after refreshing token.')


def get_metadata(obs_client):
    bucket_name = Config.get('OBS_BUCKETNAME', '')
    object_key = Config.get('OBS_OBJECT_KEY', '')
    access_token, refresh_token = '', ''
    try:
        metadata = obs_client.getObjectMetadata(bucket_name, object_key)
        if metadata['status'] != 200:
            logger.error('Fail to get metadata of the target file, please check the OBS bucketName and object_key.')
        for data in metadata['header']:
            if data[0] == 'access_token':
                access_token = data[1]
            if data[0] == 'refresh_token':
                refresh_token = data[1]
        if not access_token:
            logger.error('Metadata has a lack of access_token.')
        if not refresh_token:
            logger.error('Metadata has a lack of refresh_token.')
    except gaierror:
        logger.error('Fail to connect OBS client, please check environment variables.')
    return access_token, refresh_token


def set_metadata(obs_client, access_token, refresh_token):
    bucket_name = Config.get('OBS_BUCKETNAME', '')
    object_key = Config.get('OBS_OBJECT_KEY', '')
    metadata = {
        'access_token': access_token,
        'refresh_token': refresh_token
    }
    res = obs_client.setObjectMetadata(bucket_name, object_key, metadata)
    if res['status'] == 200:
        return True
    else:
        return False

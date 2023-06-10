import platform
import os

from specklepy.api.credentials import get_default_account
from specklepy.api.client import Account, SpeckleClient


def get_auth_speckle_client():
    operation_system = platform.system()
    if operation_system == 'Windows':
        account = get_default_account()
        client = SpeckleClient(host=account.serverInfo.url)
        client.authenticate_with_account(account)
        return client
    elif operation_system == 'Linux':
        token_path = os.path.join(os.path.expanduser('~'), '.speckle', 'token')
        host_path = os.path.join(os.path.expanduser('~'), '.speckle', 'host')
        token_file = open(token_path, "r")
        host_file = open(host_path, "r")
        token = token_file.read().replace('\n', '')
        host = host_file.read().replace('\n', '')
        client = SpeckleClient(host=host)
        account = Account.from_token(token, host)
        client.authenticate_with_account(account)
        return client



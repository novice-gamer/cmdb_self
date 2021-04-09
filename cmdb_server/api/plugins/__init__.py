import importlib
from django.conf import settings

def process_server_info(info,server_obj):
    """
    处理资产信息
    :param info:
    :param server_obj:
    :return:
    """

    for key,path in settings.CMDB_PLUGIN_DICT.items():
        pass
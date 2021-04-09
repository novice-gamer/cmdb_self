import traceback
from .base import BasePlugin
from lib.plugins.log import logger
from lib.plugins import respnose


class Memory(BasePlugin):

    def process(self, hostname, ssh_func):
        """
        执行命令，去获取内存信息
        :return:
        """
        info_obj = respnose.BaseResponse()
        try:
            content = ssh_func(hostname, 'sudo dmidecode  -q -t 17 2>/dev/null')
            data = self.parse(content)
            info_obj.data = data
        except Exception as e:
            msg = traceback.format_exc()
            logger.log(msg)
            info_obj.status = False
            info_obj.error = msg

        return info_obj.dict

    def parse(self, content):
        """
        解析shell命令返回结果
        :param content: shell 命令结果
        :return:解析后的结果
        """
        ram_dict = {}
        key_map = {
            'Size': 'capacity',
            'Locator': 'slot',
            'Type': 'model',
            'Speed': 'speed',
            'Manufacturer': 'manufacturer',
            'Serial Number': 'sn',

        }
        devices = content.split('Memory Device')
        for item in devices:
            item = item.strip()
            if not item:
                continue
            if item.startswith('#'):
                continue
            segment = {}
            lines = item.split('\n\t')
            for line in lines:
                if len(line.split(':')) > 1:
                    key, value = line.split(':')
                else:
                    key = line.split(':')[0]
                    value = ""
                if key in key_map:
                    if key == 'Size':
                        segment[key_map['Size']] = value
                    else:
                        segment[key_map[key.strip()]] = value.strip()
            ram_dict[segment['slot']] = segment

        return ram_dict

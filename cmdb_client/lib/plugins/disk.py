import re
import traceback
from .base import BasePlugin
from lib.plugins.log import logger
from lib.plugins import respnose


class Disk(BasePlugin):

    def process(self, hostname, ssh_func):
        """
        执行命令，去获取硬盘信息
        :return:
        """
        info_obj = respnose.BaseResponse()
        try:
            # content = ssh_func(hostname,'sudo MegaCli  -PDList -aALL')
            with open('../file/diskout.txt', mode='r') as f:
                content = f.read()
            result = self.parse(content)
            info_obj.data = result
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
        response = {}
        result = []
        for row_line in content.split("\n\n\n\n"):
            result.append(row_line)
        for item in result:
            temp_dict = {}
            for row in item.split('\n'):
                if not row.strip():
                    continue
                if len(row.split(':')) != 2:
                    continue
                key, value = row.split(':')
                name = self.mega_patter_match(key)
                if name:
                    if key == 'Raw Size':
                        raw_size = re.search('(\d+\.\d+)', value.strip())
                        if raw_size:
                            temp_dict[name] = raw_size.group()
                        else:
                            raw_size = '0'
                    else:
                        temp_dict[name] = value.strip()
            if temp_dict:
                response[temp_dict['slot']] = temp_dict
        return response

    @staticmethod
    def mega_patter_match(needle):
        grep_pattern = {'Slot': 'slot', 'Raw Size': 'capacity', 'Inquiry': 'model', 'PD Type': 'pd_type'}
        for key, value in grep_pattern.items():
            if needle.startswith(key):
                return value
        return False

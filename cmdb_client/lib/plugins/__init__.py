from settings.settings import PLUGIN_DICT

def get_server_info(hostname,ssh_func):
    """

    :param hostname: 要远程操作的主机名
    :param ssh_func: 执行远程操作的方法
    :return:
    """
    info_dict = {}

    for key, path in PLUGIN_DICT.items():
        module_path, class_name = path.rsplit('.', maxsplit=1)

        # 1. 根据字符串的形式去导入模块 "lib.plugins.board"
        import importlib
        try:
            module = importlib.import_module(module_path)
        except Exception as e:
            print(e)

        # 2.去模块找到类
        cls = getattr(module, class_name)

        # 3. 对类型实例化
        obj = cls()

        # 4. 执行对象的process方法
        result = obj.process(hostname,ssh_func)

        info_dict[key] = result

    return info_dict






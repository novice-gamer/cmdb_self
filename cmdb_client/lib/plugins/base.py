class BasePlugin(object):
    def process(self,hostname,ssh_func):
        raise NotImplementedError("子类%s必须实现process方法" %self.__class__.__name__)
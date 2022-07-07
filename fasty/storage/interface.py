from abc import ABCMeta, abstractmethod


class IFileStorage:
    """
    Interface dùng để lưu trữ file
    """
    __metaclass__ = ABCMeta

    @classmethod
    def version(self):
        """
        Lấy version
        :return:
        """
        return "1.0"

    @abstractmethod
    def show(self): raise NotImplementedError

    @abstractmethod
    def show(self): raise NotImplementedError
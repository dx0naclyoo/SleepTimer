import os
from abc import ABC, abstractmethod


class SleepService(ABC):
    @classmethod
    @abstractmethod
    def fake_shutdown(cls, _time: int = 3600):
        pass

    @classmethod
    @abstractmethod
    def shutdown(cls, _time: int = 3600):
        pass

    @classmethod
    @abstractmethod
    def cancel_shutdown(cls):
        pass


class SleepServiceWindows(SleepService):  # for Windows
    _shutdown_active = False

    @classmethod
    def fake_shutdown(cls, _time: int = 3600):
        print("shutdown called with time", _time)

    @classmethod
    def shutdown(cls, _time: int = 3600):
        if not cls._shutdown_active:
            cls._shutdown_active = True
            os.system(f"shutdown -s -t {_time}")
        else:
            cls.cancel_shutdown()
            cls.shutdown(_time)

    @classmethod
    def cancel_shutdown(cls):
        print("shutdown cancelled")
        if cls._shutdown_active:
            os_response = os.system("shutdown -a")
            if os_response == 0:
                cls._shutdown_active = False


class SleepServiceLinux:
    pass


class SleepServiceMacOS:
    pass

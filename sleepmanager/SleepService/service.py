import os


class ShutdownService:
    _shutdown_active = False

    @classmethod
    def fake_shutdown(cls, _time: int = None):
        print("shutdown called")

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
        if cls._shutdown_active:
            os_response = os.system("shutdown -a")
            if os_response == 0:
                cls._shutdown_active = False

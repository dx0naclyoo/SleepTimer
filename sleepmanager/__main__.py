import sys
import platform

from sleepmanager.SleepService.service import SleepServiceWindows, SleepServiceMacOS, SleepServiceLinux
from sleepmanager.UI.window import GUIApp, MainWindow

if __name__ == '__main__':
    system = platform.system()

    match system:
        case "Windows":
            sleep_service = SleepServiceWindows()
        case "Linux":
            sleep_service = SleepServiceLinux()
        case "Darwin":
            sleep_service = SleepServiceMacOS()
        case _:
            print("Unknown system")
            sys.exit(1)

    print(sleep_service)
    app = GUIApp(sys.argv)
    main = MainWindow(sleep_service)

    app.init_widgets([main])

    app.exec()
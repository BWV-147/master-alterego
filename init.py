import ctypes
import platform
import sys

# initiate only once
_initiated = False


def initial():
    """
    Initiation must be called at the startup of program. Otherwise, some settings may take no sense.
    :return:
    """
    global _initiated
    if _initiated:
        return
    # 1st-DPI
    set_dpi_awareness()
    # 2nd-pyautogui, must import after setting DPI
    import pyautogui
    pyautogui.FAILSAFE = False

    _initiated = True


def set_dpi_awareness():
    """ Windows: set DPI aware to capture full screen on Hi-DPI monitors. """
    if platform.system().lower() == 'windows':
        version = sys.getwindowsversion()[:2]  # pylint: disable=no-member
        if version >= (6, 3):
            # Windows 8.1+
            # Here 2 = PROCESS_PER_MONITOR_DPI_AWARE, which means:
            #     per monitor DPI aware. This app checks for the DPI when it is
            #     created and adjusts the scale factor whenever the DPI changes.
            #     These applications are not automatically scaled by the system.
            res = ctypes.windll.shcore.SetProcessDpiAwareness(2)

        elif (6, 0) <= version < (6, 3):
            # Windows Vista, 7, 8 and Server 2012
            res = ctypes.WinDLL('user32').SetProcessDPIAware()
        else:
            res = f'unknown windows version "{sys.getwindowsversion()}"'
        print('Set DPI awareness:', res)

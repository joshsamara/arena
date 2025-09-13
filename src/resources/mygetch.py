"""Read single characer at a time from stdin."""


class _GetchUnix:

    """
    Class to track individual stdin characters.

    Taken from http://stackoverflow.com/questions/1052107/reading-a-single-char
    acter-getch-style-in-python-is-not-working-in-unix

    """

    def __init__(self):
        import tty
        import sys

    def __call__(self):
        import sys
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


getch = _GetchUnix()

import os


def clear_screen():
    clear = 'cls' if os.name == 'nt' else 'clear' # 윈도우는 nt, mac은 clear
    os.system(clear)

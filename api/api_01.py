import ctypes

user32 = ctypes.windll.LoadLibrary('user32.dll')
user32.MessageBoxA(0, str.encode('Ctypes is so smart!'), str.encode('Ctypes'), 0)

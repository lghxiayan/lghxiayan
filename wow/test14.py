import win32process

win32process.CreateProcess('c:\\windows\\system32\\notepad.exe', '', None, None, 0, win32process.CREATE_NO_WINDOW, None,
                           None, win32process.STARTUPINFO())

pip install -r requirements.txt

pyinstaller main.py --name="ValorantRPC" --onefile --hidden-import 'pystray._win32' --hidden-import plyer.platforms.win.notification --icon=favicon.ico 

pause
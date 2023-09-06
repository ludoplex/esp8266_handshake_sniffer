# Made by @xdavidhu (github.com/xdavidhu, https://xdavidhu.me/)

import serial
import io
import os
import subprocess
import signal
import time

try:
    serialportInput = input("[?] Select a serial port (default '/dev/ttyUSB0'): ")
    serialport = "/dev/ttyUSB0" if serialportInput == "" else serialportInput
except KeyboardInterrupt:
    print("\n[+] Exiting...")
    exit()

try:
    canBreak = False
    while not canBreak:
        boardRateInput = input("[?] Select a baudrate (default '115200'): ")
        if boardRateInput == "":
            boardRate = 115200
        else:
            try:
                boardRate = int(boardRateInput)
            except KeyboardInterrupt:
                print("\n[+] Exiting...")
                exit()
            except Exception as e:
                print("[!] Please enter a number!")
                continue
        canBreak = True
except KeyboardInterrupt:
    print("\n[+] Exiting...")
    exit()

try:
    filenameInput = input("[?] Select a filename (default 'capture.pcap'): ")
    filename = "capture.pcap" if filenameInput == "" else filenameInput
except KeyboardInterrupt:
    print("\n[+] Exiting...")
    exit()

canBreak = False
while not canBreak:
    try:
        ser = serial.Serial(serialport, boardRate)
        canBreak = True
    except KeyboardInterrupt:
        print("\n[+] Exiting...")
        exit()
    except:
        print("[!] Serial connection failed... Retrying...")
        time.sleep(2)
        continue

print(f"[+] Serial connected. Name: {ser.name}")
counter = 0
with open(filename,'wb') as f:
    check = 0
    while check == 0:
        line = ser.readline()
        check=1
    print("[+] Starting up wireshark...")
    cmd = f"tail -f -c +0 {filename} | wireshark -k -i -"
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                           shell=True, preexec_fn=os.setsid)

    try:
        while True:
            ch = ser.read()
            f.write(ch)
            f.flush()
    except KeyboardInterrupt:
        print("[+] Stopping...")
        os.killpg(os.getpgid(p.pid), signal.SIGTERM)

ser.close()
print("[+] Done.")

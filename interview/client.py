import socket
import sys
from collections import deque

HOST, PORT = "localhost", 9999

files_found = 0
# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))

    path_frontier = deque(["/"])
    while len(path_frontier) > 0:
        dir_to_list = path_frontier.popleft()
        sock.sendall(bytes("DIRLIST " + dir_to_list + "\r\n", "utf-8"))

        received = str(sock.recv(1024), "utf-8")
        print("received: " + received)
        received_lines = received.split("\r\n")
        for i in range(1, len(received_lines)-1):
            received_line = received_lines[i]
            if (names_in_path[-1] == "/"): #we found a directory
                path_frontier.append(dir_to_list+received_line)
            else: #we found a file
                files_found += 1
                print('{:,}'.format(files_found) + " file(s) found so far.")

print('{:,}'.format(files_found) + " file(s) found.")

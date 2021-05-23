import queue
import select
import socket
import sys
import threading

from collections import deque

HOST = "localhost"
PORT = 9999

prepared_requests = queue.Queue()
server_responses = queue.Queue()
directory_frontier = queue.Queue()

def manage_requests():
    while True:
        request = prepared_requests.get(block=True)
        _, ready_to_send, _ = select.select([], [sock], [], 60)
        if sock in ready_to_send:
            sock.sendall(request)
            #print("sent" + str(request))

def manage_responses():
    unfinished_response = ""
    while True:
        ready_to_read, _, _ = select.select([sock], [], [], 60)
        if sock in ready_to_read:
            response_data = sock.recv(1024)
            decoded_response = unfinished_response + str(response_data, "utf-8")
            split_responses = decoded_response.split(f"END\r\n")
            unfinished_response = split_responses[-1]
            for response in split_responses[:-1]:
                server_responses.put(response)

def manage_exploration():
    unanswered_dirlists = deque()
    files_found = 0
    responses_processed = 0

    def enqueue_request(dir_to_list):
        unanswered_dirlists.append(dir_to_list)
        request = bytes(f"DIRLIST " + dir_to_list + f"\r\n", "utf-8")
        prepared_requests.put(request)

    enqueue_request("/")
    
    while True:
        if not server_responses.empty():
            received = server_responses.get()
            responses_processed += 1
            received_lines = received.split(f"\r\n")
            parent_dirs = unanswered_dirlists.popleft()
            if (responses_processed%857==0):
                print(parent_dirs, len(received_lines), received_lines[-2])
            for i in range(1, len(received_lines)-1):
                received_line = received_lines[i].lstrip()
                if (received_line[-1] == "/"): #we found a directory
                    dir_to_list = parent_dirs+received_line
                    enqueue_request(dir_to_list)
                else: #we found a file
                    files_found += 1

            #print(responses_processed)
            if (responses_processed%1000==0):
                print(responses_processed, len(received_lines), files_found)

    return files_found
                

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    sock.setblocking(False)

    request_thread = threading.Thread(target=manage_requests)
    request_thread.start()

    response_thread = threading.Thread(target=manage_responses)
    response_thread.start()

    files_found = manage_exploration()
    print('{:,}'.format(files_found) + " file(s) found.")

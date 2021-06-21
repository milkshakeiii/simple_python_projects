import queue
import select
import socket
import threading

from collections import deque


class ChallengeClient:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.prepared_requests = queue.Queue()
        self.server_responses = queue.Queue()

    def run(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.host, self.port))
            sock.setblocking(False)

            exit_event = threading.Event()

            request_thread = threading.Thread(
                target=self.send_requests, args=(sock, exit_event)
            )
            request_thread.start()

            response_thread = threading.Thread(
                target=self.receive_responses, args=(sock, exit_event)
            )
            response_thread.start()

            files_found = self.do_scan(exit_event)
            print("{:,}".format(files_found) + " file(s) found.")

            exit_event.set()

    def send_requests(self, sock: socket.socket, exit_event: threading.Event) -> None:
        leftover_unsent_data = bytes()
        while not exit_event.is_set():
            request = self.prepared_requests.get(block=True)
            _, ready_to_send, _ = select.select([], [sock], [], 60)
            if sock in ready_to_send and sock:
                send_me = leftover_unsent_data + request
                sent = sock.send(send_me)
                leftover_unsent_data = send_me[sent:]

    def receive_responses(
        self, sock: socket.socket, exit_event: threading.Event
    ) -> None:
        unfinished_response = ""
        while not exit_event.is_set():
            ready_to_read, _, _ = select.select([sock], [], [], 60)
            if sock in ready_to_read:
                response_data = sock.recv(1024)
                decoded_data = str(response_data, "utf-8")
                if decoded_data == "":
                    break
                if "ERROR" in decoded_data:
                    print(decoded_data)
                    exit_event.set()
                decoded_response = unfinished_response + decoded_data
                split_responses = decoded_response.split(f"END\r\n")
                unfinished_response = split_responses[-1]
                for response in split_responses[:-1]:
                    self.server_responses.put(response)

    def do_scan(self, exit_event: threading.Event) -> int:
        unanswered_dirlists = deque()
        files_found = 0
        responses_processed = 0

        def enqueue_request(dir_to_list):
            unanswered_dirlists.append(dir_to_list)
            request = bytes(f"DIRLIST " + dir_to_list + f"\r\n", "utf-8")

            ### The prepared_requests size could be limited here,
            ### but due to an undiagnosed problem doing so causes the
            ### program's runtime to increase more than tenfold.
            ### I was therefore unable to fulfill this part of the
            ### challenge requirement
            ### while(prepared_requests.qsize() > 20): #for example
            ###     pass
            self.prepared_requests.put(request)

        enqueue_request("/")

        while len(unanswered_dirlists) > 0 and not exit_event.is_set():
            if not self.server_responses.empty():
                received = self.server_responses.get()
                responses_processed += 1
                received_lines = received.split(f"\r\n")
                parent_dirs = unanswered_dirlists.popleft()
                for i in range(1, len(received_lines) - 1):
                    received_line = received_lines[i].lstrip()
                    if received_line[-1] == "/":  # we found a directory
                        dir_to_list = parent_dirs + received_line
                        enqueue_request(dir_to_list)
                    else:  # we found a file
                        files_found += 1

                if (
                    responses_processed in [10, 1000]
                    or responses_processed % 10000 == 0
                ):
                    print(str(responses_processed) + " responses processed so far")
                    print(str(self.prepared_requests.qsize()) + " requests in queue")
                    print(str(files_found) + " files found so far")

        return files_found


if __name__ == "__main__":
    client = ChallengeClient("localhost", 9999)
    client.run()

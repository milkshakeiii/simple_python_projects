import select
import socket
import socketserver

from collections import deque


def simulated_dirlist(full_path: str) -> list:
    """
    Returns a list of directory names that would be at the path provided.

    Returns an empty list for paths not found in our filesystem.
    """
    full_path = full_path.strip("/")
    names_in_path = full_path.split("/")
    for name in names_in_path:
        if name == "":
            continue
        if name[0:4] != "dir_":
            return []
        for dir_num in name[5:-1]:
            if not dir_num.isdigit():
                return []
    if len(names_in_path) > 4:
        return []
    elif len(names_in_path) == 3:
        return ["file_00", "file_01", "file_02"]
    else:
        return ["dir_%02d/" % (i,) for i in range(100)]


class ChallengeTCPHandler(socketserver.BaseRequestHandler):
    """
    This is expected to override handle.

    It is instantiated for each connection and then handle() is called.

    The socket is closed when handle() finishes.
    """

    leftover_received_data = ""
    leftover_unsent_data = bytes()
    disconnect = False

    def receive_requests(self) -> list:
        received_data = self.request.recv(1024)
        decoded_data = received_data.decode("utf-8")
        completed_data = self.leftover_received_data + decoded_data
        data_parts = completed_data.split(f"\r\n")
        self.leftover_received_data = data_parts[-1]
        return data_parts[:-1]

    def respond_to_request(self, request: str) -> None:
        request_parts = request.split()
        if request_parts[0] == f"DIRLIST":
            if len(request_parts) > 2:
                self.error_and_close("Invalid syntax, expected DIRLIST /dirname/")
            if request_parts[1][0] != "/" or request_parts[1][-1] != "/":
                self.error_and_close(
                    "Directory must start and end with a '/' character."
                )
            names_listed = simulated_dirlist(request_parts[1])
            if len(names_listed) == 0:
                self.error_and_close(
                    "No directory exists named: " + str(request_parts[1])
                )
            response = f"BEGIN\r\n"
            for name in names_listed:
                response += " " + name + f"\r\n"
            response += f"END\r\n"
            if not self.disconnect:
                send_me = self.leftover_unsent_data + bytes(response, "utf-8")
                sent = self.request.send(send_me)
                self.leftover_unsent_data = send_me[sent:]
        else:
            self.error_and_close("Unrecognized request: " + request_parts[0])

    def error_and_close(self, error_message: str) -> None:
        error_bytes = bytes("ERROR " + error_message, "utf-8" + f"\r\n")
        self.request.sendall(error_bytes)
        self.disconnect = True

    def handle(self) -> None:
        print("a new client connected")

        self.request.setblocking(False)

        unanswered_requests = deque()
        responses_sent = 0

        while not self.disconnect:

            ready_to_read, _, _ = select.select([self.request], [], [], 60)
            if self.request in ready_to_read:  # receive requests
                requests = self.receive_requests()
                if len(requests) == 0:
                    self.disconnect = True
                for request in requests:
                    unanswered_requests.append(request)

            while len(unanswered_requests) > 0:  # respond to all requests
                _, ready_to_send, _ = select.select([], [self.request], [], 60)
                if self.request in ready_to_send:
                    request = unanswered_requests.popleft()
                    responses_sent += 1
                    if (responses_sent % 5000) == 0:
                        print(str(responses_sent) + " responses sent to this client")
                    self.respond_to_request(request)

        print("client disconnected, cleaning up")


if __name__ == "__main__":
    with socketserver.TCPServer(("localhost", 9999), ChallengeTCPHandler) as server:
        server.serve_forever()

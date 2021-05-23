import queue
import select
import socketserver
import time

HOST = "localhost"
PORT = 9999
TIMEOUT = 10

def simulated_dirlist(full_path):
    full_path = full_path.strip("/")
    names_in_path = full_path.split("/")
    if len(names_in_path) == 3:
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

    def receive_requests(self):
        received_data = self.request.recv(1024)
        #print(received_data)
        #time.sleep(1)
        last_communication = time.time()
        decoded_data = received_data.decode("utf-8")
        completed_data = self.leftover_received_data + decoded_data
        data_parts = completed_data.split(f"\r\n")
        self.leftover_received_data = data_parts[-1]
        return data_parts[:-1]

    def respond_to_request(self, request):
        request_parts = request.split()
        if request_parts[0] == f"DIRLIST":
            names_listed = simulated_dirlist(request_parts[1])
            response = f"BEGIN\r\n"
            for name in names_listed:
                response += " " + name + f"\r\n"
            response += f"END\r\n"
            send_me = self.leftover_unsent_data + bytes(response, "utf-8")
            sent = self.request.send(send_me)
            self.leftover_unsent_data = send_me[sent:]
            

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.request.setblocking(False)
        time.sleep(1)

        #prepared_responses = queue.Queue()
        client_requests = queue.Queue()
        
        client_disconnected = False
        while not client_disconnected:
            ready_to_read, _, _ = select.select([self.request], [], [], 60)
            if self.request in ready_to_read:
                requests = self.receive_requests()
                if len(requests)==0:
                    client_disconnected = True
                for request in requests:
                    client_requests.put(request)

            _, ready_to_send, _ = select.select([], [self.request], [], 60)
            if not client_requests.empty() and self.request in ready_to_send:
                request = client_requests.get()
                self.respond_to_request(request)
            
        print("client disconnected, cleaning up")

if __name__ == "__main__":
    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), ChallengeTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()

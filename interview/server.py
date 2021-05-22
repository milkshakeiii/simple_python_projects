import socketserver

def simulated_dirlist(full_path):
    full_path = full_path.strip("/")
    names_in_path = directory.split("/")
    if len(directories_in_path) == 3:
        return ["file_00", "file_01", "file_02"]
    else:
        return ["dir_%02d" % (i,) for i in range(100)]

class ChallengeTCPHandler(socketserver.BaseRequestHandler):
    """
    This is expected to override handle.

    It is instantiated for each request and then handle() is called.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        received_data = self.request.recv(1024)
        stripped_data = str(received_data).rstrip("\r\n")
        request_parts = received_data.split()
        if request_parts[0] == "DIRLIST":
            names_listed = simulated_dirlist(request_parts[1])
            respose = "BEGIN\r\n"
            for name in names_listed:
                response += " " + name + "\r\n"
            response += "END\r\n"
            print("response: " + response)
            self.request.sendall(response)

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), ChallengeTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()

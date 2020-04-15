"""The server side of a chat service.

Author: Alexnader Waters
Class: CSI-275-01/02
Assignment: Final
Due Date: April 24th

Certification of Authenticity:
I certify that this is entirely my own work, except where I have given
fully-documented references to the work of others. I understand the definition
and consequences of plagiarism and acknowledge that the assessor of this
assignment may, for the purpose of assessing this assignment:
- Reproduce this assignment and provide a copy to another member of academic
- staff; and/or Communicate a copy of this assignment to a plagiarism checking
- service (which may then retain a copy of this assignment on its database for
- the purpose of future plagiarism checking)
"""

import socket
import threading
import json
import global_var


class chatServer():
    def __init__(self):
        # dict of connectd users
        # {username : socket, (ip, port)}
        self.connectedUsers = {}

        # variables from config
        self.host = global_var.HOST
        self.write_port = global_var.SERVER_WRITE_PORT
        self.read_port = global_var.SERVER_READ_PORT

    def broadcast(self, message, user):
        '''Send messages to all connected users'''
        # add user header to message
        message_to_send = user + ": " + message

        # create a boradcast message
        data_to_send = self.create_message(message_to_send, 'b')

        # send to all users
        for username in self.connectedUsers.keys():
            self.connectedUsers[username][0].sendall(data_to_send)

    def create_message(self, string, type):
        """takes string & type of message and formats it into sendable data."""
        data_list = [type, string]
        json_data = json.dumps(data_list)
        data_to_send = len(json_data).to_bytes(4, 'big') \
            + json_data.encode("utf-8")
        return data_to_send

    def create_writeing_socket(self):
        """creates a socket for adding users to connected users"""
        self.write_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.write_sock.bind((self.host, self.write_port))
        self.write_sock.listen(20)

        # start listening for users
        self.client_recv_wait_start()

    def create_reading_socket(self):
        """creates a socket for creating threads for connected users"""
        self.read_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.read_sock.bind((self.host, self.read_port))
        self.read_sock.listen(20)

        # wait for users to connect to server
        self.monitor_user()

    def client_recv_wait(self):
        '''adds user to connected users var'''
        while True:
            client_sock, addr = self.write_sock.accept()

            data = self.recv_message(client_sock)

            if data[0] == "s":
                # if its a start message
                username = data[1]
                self.connectedUsers[username] = (client_sock, addr)
                # tell server another person joined
                self.broadcast(username + " has joined the Server", "Server")
                print(addr, username, "Joined")

    def client_recv_wait_start(self):
        ''' fail safe for client_recv_wait'''
        try:
            self.client_recv_wait()
        except EOFError:
            print('Client socket has closed')
        except ConnectionResetError as e:
            print('Connection reset')
        finally:
            self.write_sock.close()

    def monitor_messages(self, sock, addr):
        ''' for each user wait for thier messages'''
        while True:
            # recieve the message the user sent
            message = self.recv_message(sock)
            # get user name based on ip
            user = message[2]

            if message[0] == 'b':
                # if it is a broadcast message
                self.broadcast(message[1], user)
            elif message[0] == 'p':
                # if it is a personal messages
                try:
                    # try to split the message after @name
                    TO, message_data = message[1].split(' ', 1)
                    message_data = user + " <Private>:" + message_data
                    # include private tag

                    message_to_send = self.create_message(message_data, 'p')

                    private_socket = self.connectedUsers.get(TO[1::])[0]
                    # get socket to send too

                    private_socket.sendall(message_to_send)
                    # send data to socket

                except (ValueError, TypeError):
                    # if failed to split message or find user
                    # send message to ourselvs

                    message_data = "server" + " <Private>: " + "INVALID FORMAT"
                    # add private tag
                    message_to_send = self.create_message(message_data, 'p')
                    # create private message
                    private_socket = self.connectedUsers.get(user)[0].sendall(
                        message_to_send)
                    # send to ourself
            else:
                # the user has '!exit'
                self.broadcast(message[2] + " Has left the server", 'Server')
                # tell everyone
                sock.close()
                self.connectedUsers[user][0].close()
                # close sockets
                print(addr, user, "Left")
                del self.connectedUsers[user]
                # remove them from connected users
                break
                # end thread

    def monitor_user(self):
        ''' check for users connecting and if they do add new thread'''
        while True:
            client_sock, addr = self.read_sock.accept()
            if client_sock:
                # create a thread to handel user
                threading.Thread(target=self.monitor_messages,
                                 args=(client_sock, addr)).start()

    def recv_message(self, sock):
        '''recve message from socket'''
        message_length = int.from_bytes(sock.recv(4), 'big')
        message = self.recv_len(sock, message_length).decode('utf-8')
        data = json.loads(message)
        return data

    def recv_len(self, sock, length):
        """takes in a socket and data length and returns all data"""
        data = b''
        while len(data) < length:
            more = sock.recv(length - len(data))
            if more == b'':
                # if the byte string is empty
                sock.sendall(ERROR)
                break
            data += more
        return data

    def start(self):
        '''create treads to deal with recving and sending data'''
        read_thread = threading.Thread(target=self.create_reading_socket,
                                       args=())
        read_thread.start()

        write_thread = threading.Thread(target=self.create_writeing_socket,
                                        args=())
        write_thread.start()

        read_thread.join()
        write_thread.join()


if __name__ == '__main__':
    server = chatServer()
    server.start()

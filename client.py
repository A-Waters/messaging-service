"""The client and user side for the chat server

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
import threading
import socket
import json
import global_var


class client():
    def __init__(self):
        # get username from peron
        self.username = input("What is your username? : ")

        # validate username
        while not self.username.isalnum():
            print("invalid username")
            self.username = input("What is your username? : ")

        # sets host and port based off of global values
        self.host = global_var.HOST
        self.send_port = global_var.SERVER_READ_PORT
        self.recv_port = global_var.SERVER_WRITE_PORT

        # start threads
        self.start_threads()

    def create_message(self, string, type, sender=""):
        """takes string & type of message and formats it into sendable data."""
        if sender != "":
            data_list = [type, string, sender]
        else:
            data_list = [type, string]
        json_data = json.dumps(data_list)
        data_to_send = len(json_data).to_bytes(4, 'big') \
            + json_data.encode("utf-8")
        return data_to_send

    def create_send_socket(self):
        """creats a socket to send data with"""
        self.send_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.send_sock.connect((self.host, self.send_port))

        try:
            # move into sending data from user
            self.user_messaging()
        except EOFError:
            print('Client socket has closed')
        except ConnectionResetError as e:
            print('Connection lost')
        finally:
            self.send_sock.close()

    def create_recv_socket(self):
        '''Creates a socket to take in data from server'''

        self.recv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.recv_sock.connect((self.host, self.recv_port))

        # get server ready for client
        self.send_start()

        try:
            # start recieving messages
            self.recv_messaging()
        except EOFError:
            print('Client socket has closed')
        except ConnectionResetError as e:
            print('Connection lost')
        except ValueError:
            print("Exited")
        finally:
            self.recv_sock.close()

    def start_threads(self):
        """Start threads that deal with sending and reciving data."""
        # create a thread to send data
        send_thread = threading.Thread(target=self.create_send_socket, args=())
        send_thread.start()

        # create a thread to recieve data
        recv_thread = threading.Thread(target=self.create_recv_socket, args=())
        recv_thread.start()

        send_thread.join()
        recv_thread.join()

    def send_start(self):
        """Tell server to get ready for client."""
        data_to_send = self.create_message(self.username, 's')
        self.recv_sock.sendall(data_to_send)

    def recv_message(self, sock):
        '''recve message from socket'''
        message_length = int.from_bytes(sock.recv(4), 'big')
        message = self.recv_len(sock, message_length).decode('utf-8')
        data = json.loads(message)
        return data

    # receve message from sock based on how long the len is
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

    def recv_messaging(self):
        '''displays messsages as the come from server'''
        while True:
            message = self.recv_message(self.recv_sock)
            print("> " + message[1])

    def user_messaging(self):
        '''Wait for user input and send messages to server'''
        while True:
            message = input("")

            if not message == "":
                # if the messages isnt empty
                type = 'b'
                # defaulty its a broadcast
                if message.startswith('@'):
                    # if they @ someone its private
                    type = 'p'
                elif message == '!exit':
                    # if they exit
                    type = 'e'

                # create messages
                data = self.create_message(message, type, self.username)

                # send data to server
                self.send_sock.sendall(data)

                if (type == 'e'):
                    # exit
                    break


if __name__ == '__main__':
    user = client()

#######################################################################
# File:             server.py
# Name:             Ziping Huang
# Student ID:       916155583
# Github:           myreplica
# Python version:   python 3.81
# Purpose:          CSC645 Assigment #1 TCP socket programming
# Description:      Template server class. You are free to modify this
#                   file to meet your own needs. Additionally, you are
#                   free to drop this client class, and add yours instead.
# Running:          Python 2: python server.py
#                   Python 3: python3 server.py
#                   Note: Must run the server before the client.
########################################################################

from builtins import object
import socket
import pickle
import client_handler
import threading

class Server(object):

    MAX_NUM_CONN = 10

    def __init__(self, ip_address='127.0.0.1', port=5000):
        """
        Class constructor
        :param ip_address:
        :param port:
        """
        # create an INET, STREAMing socket
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # self.clients = {} # dictionary of clients handlers objects handling clients. format {clientid:client_handler_object}
        self.userlist = []
        self.clientobject_list = []
        self.client_id_list = []
        self.host = ip_address
        self.port = port
        # self.threadCount = 0
        self.sockets_list = [self.serversocket]
        self.connections = []
     


    def _listen(self):
        """
        Private method that puts the server in listening mode
        If successful, prints the string "Listening at <ip>/<port>"
        i.e "Listening at 127.0.0.1/10000"
        :return: VOID
        """
        #TODO: your code here
        try:
            # TODO: bind the socket to a public host, and a well-known port
            self.serversocket.bind((self.host,self.port))
            self.serversocket.listen(self.MAX_NUM_CONN)
            message = "Server listening on: " + str(self.host) + " ip/ " + str(self.port) + " port"
            print(message)

        except:
            print("Error listening on server")
            self.serversocket.close()

    def _accept_clients(self):
        """
        Accept new clients
        :return: VOID
        """

        while True:
            try:
                #TODO: Accept a client
                clientsocket, addr = self.serversocket.accept()
                #TODO: Create a thread of this client using the client_handler_threaded class
              
                clientThread = threading.Thread(target=self.client_handler_thread, args=(clientsocket,addr)) # client thread started 
                clientThread.daemon = True
                clientThread.start()
                self.connections.append(clientsocket)
                # print("list of client's connections: ")
                # print(self.connections)

               
                # self.threadCount += 1
                # print('Thread count: ' + str(self.threadCount))
          

            except KeyboardInterrupt as e:
                print("Shutting down server: ", e)
                break

            except socket.error as msg:
                print ("Socket Error: " , msg)
                return False
        
            

    def send(self, clientsocket, data):
        """
        TODO: Serializes the data with pickle, and sends using the accepted client socket.
        :param clientsocket:
        :param data:
        :return:
        """
        serialezed_data = pickle.dumps(data)
        clientsocket.send(serialezed_data)
      


    def receive(self, clientsocket, MAX_BUFFER_SIZE=4096):
        """
        TODO: Deserializes the data with pickle
        :param clientsocket:
        :param MAX_BUFFER_SIZE:
        :return: the deserialized data
        """
         # server receives data
        data_from_client = clientsocket.recv(MAX_BUFFER_SIZE)
        # deserializes the data received
        serialized_data = pickle.loads(data_from_client)
        return serialized_data

    def send_client_id(self, clientsocket, id):
        """
        Already implemented for you
        :param clientsocket:
        :return:
        """
        clientid = {'clientid': id}
        self.send(clientsocket, clientid)


    def client_handler_thread(self, clientsocket, address):
        """
        Sends the client id assigned to this clientsocket and
        Creates a new ClientHandler object
        See also ClientHandler Class
        :param clientsocket:
        :param address:
        :return: a client handler object.
        """
        client_id = address[1]

        #TODO: create a new client handler object and return it
        #send client_id to the client
        self.clienthandler = client_handler.ClientHandler(self, clientsocket, address)
        # self.clienthandler.__init__(self, clientsocket, address)
        
        #initial receive and receiving client name from client
        data = self.receive(clientsocket)
        print(data)
        self.client_name = data['name']

        print("Client: " + self.client_name + ":" + str(client_id) + " has been connected to the server!")
        #sending an acknowledge to the client by sending back  the menu
        self.clienthandler._sendMenu()
        data = self.receive(clientsocket)
        print(data)
        
        # #list of users
        self.users = self.client_name + ":" + str(client_id)
        self.userlist.append(self.users)
        print(self.userlist)

        #list of client objects
        self.clientobject_list.append(self.clienthandler)
        print(self.clientobject_list)


        for self.clienthandler in self.clientobject_list:
            # print(clienthandler.client_id)
            self.client_id_list.append(self.clienthandler.client_id)
            print("Here is a list of client id from clienthandler object: ")
            print(self.client_id_list)


        #processing client's options in clienthandler
        self.clienthandler.process_options()


        #Testing purposes for receving client's data
        # while True:
        #     clientdata = self.receive(clientsocket)
        #     print(clientdata)
        #     for clientsocket in self.connections:
        #         if clientdata:
        #             message = "[" + str(client_id) + ":" + self.client_name + "]: " + clientdata
        #             self.send(clientsocket, message)
        #         if not clientdata:
        #             break


    def run(self):
        """
        Already implemented for you. Runs this client
        :return: VOID
        """
        self._listen()
        self._accept_clients()


if __name__ == '__main__':
    server = Server()
    server.run()



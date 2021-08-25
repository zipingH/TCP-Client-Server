#######################################################################
# File:             client.py
# Name:             Ziping Huang
# Github:           zipingH
# Python version:   python 3.81
# Purpose:          CSC645 Assigment #1 TCP socket programming
# Description:      Template client class. You are free to modify this
#                   file to meet your own needs. Additionally, you are 
#                   free to drop this client class, and add yours instead. 
# Running:          Python 2: python client.py 
#                   Python 3: python3 client.py
#
########################################################################
import socket
import pickle
import sys
import menu



class Client(object):
    """
    The client class provides the following functionality:
    1. Connects to a TCP server 
    2. Send serialized data to the server by requests
    3. Retrieves and deserialize data from a TCP server
    """

    def __init__(self):
        """
        Class constractpr
        """
        # Creates the client socket
        # AF_INET refers to the address family ipv4.
        # The SOCK_STREAM means connection oriented TCP protocol.
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientid = 0
        self.isConnected = True
        self.menuObject = menu.Menu(self)

        

    def set_client(self):
        """
        Sets the client id assigned by the server to this client after a succesfull connection
        :return:
        """
        data = self.receive() # deserialized data
        client_id = data['clientid'] # extracts client id from data
        self.clientid = client_id # sets the client id to this client
        # print("Client ID: " + str(self.clientid))

        inputname = input("Enter your name: ")
        self.clientname = inputname
        print("Your client info is: ")
        print("Client ID: " + str(self.clientid))
        print("Client Name: "+ self.clientname + "\n")
        data = {'name': self.clientname}
        self.send(data)
    
    def connect(self, host="127.0.0.1", port=12000):
        """
        TODO: Connects to a server. Implements exception handler if connection is resetted. 
	    Then retrieves the cliend id assigned from server, and sets
        :param host: 
        :param port: 
        :return: VOID
        """
        self.clientsocket.connect((host,port))
        self.set_client()

        menudata = self.receive()
        if menudata:
            printmenu = menudata['menu']
            # print(printmenu)
            self.send("Client got the menu!")

        
        while self.isConnected: # client is put in listening mode to retrieve data from server.
            try:    
                print(printmenu)
                self.menuObject.printProcess()

            except socket.error as msg:
               print(msg)
               self.close()
               break


	
    def send(self, data):
        """
        TODO: Serializes and then sends data to server
        :param data:
        :return:
        """
        data = pickle.dumps(data) # serialized data
        self.clientsocket.send(data)

    def receive(self, MAX_BUFFER_SIZE=4096):
        """
        TODO: Desearializes the data received by the server
        :param MAX_BUFFER_SIZE: Max allowed allocated memory for this data
        :return: the deserialized data.
        """
        raw_data = self.clientsocket.recv(MAX_BUFFER_SIZE) # deserializes the data from server
        return pickle.loads(raw_data)
        

    def close(self):
        """
        TODO: close the client socket
        :return: VOID
        """
        self.clientsocket.close()

		

if __name__ == '__main__':
    client = Client()
    client.connect()

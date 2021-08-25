#######################################################################
# File:             client_handler.py
# Name:             Ziping Huang
# Github:           zipingH
# Python version:   python 3.81
# Purpose:          CSC645 Assigment #1 TCP socket programming
# Description:      Template ClientHandler class. You are free to modify this
#                   file to meet your own needs. Additionally, you are
#                   free to drop this client handler class, and use a version of yours instead.
# Running:          Python 2: python server.py
#                   Python 3: python3 server.py
#                   Note: Must run the server before the client.
# 
# Important:        Need to change and append sys.path to the path of the client folder
########################################################################
import server
import pickle
import threading
import menu

class ClientHandler(object):
    """
    The ClientHandler class provides methods to meet the functionality and services provided
    by a server. Examples of this are sending the menu options to the client when it connects,
    or processing the data sent by a specific client to the server.
    """
    def __init__(self, server_instance, clientsocket, addr):
        """
        Class constructor already implemented for you
        :param server_instance: normally passed as self from server object
        :param clientsocket: the socket representing the client accepted in server side
        :param addr: addr[0] = <server ip address> and addr[1] = <client id>
        """
        self.server_ip = addr[0]
        self.client_id = addr[1]
        self.server = server_instance
        self.clientsocket = clientsocket
        self.server.send_client_id(self.clientsocket, self.client_id)
        self.unreaded_messages = []
        self.send_clientData = None
        self.address = addr
        self.room_id = None
        self.connections = self.server.connections
       
       


    def print_lock(self):
        write_lock = threading.Lock()
        return write_lock
    


    def _sendMenu(self):
        """
        Already implemented for you.
        sends the menu options to the client after the handshake between client and server is done.
        :return: VOID
        """
        self.menu = menu.Menu(self)
        data = {'menu': self.menu.get_menu()}
        # data = self.menu.get_menu()
        self.server.send(self.clientsocket, data)
        # self.clientsocket.send(pickle.dumps(data))
        
        
    

    def process_options(self):
        """
        Process the option selected by the user and the data sent by the client related to that
        option. Note that validation of the option selected must be done in client and server.
        In this method, I already implemented the server validation of the option selected.
        :return:
        """
        print_lock = self.print_lock()
        # print(self.server.clientdata)
        # data = self.server.clientdata
        # print(data)
        while True:
            data = self.server.receive(self.clientsocket)
            print_lock.acquire()
            print("Data received from the client: " + str(data))
            if 'option' in data.keys() and 1 <= data['option'] <= 6: # validates a valid option selected
                option = data['option']
                if option == 1:
                    self._send_user_list()

                elif option == 2:
                    recipient_id = data['recipient_id']
                    message = data['message']
                    self._save_message(recipient_id, message)

                elif option == 3:
                    self._send_messages()

                elif option == 4:
                    self.room_id = data['room_id']
                    self._create_chat(self.room_id)

                elif option == 5:
                    room_id = data['room_id']
                    self._join_chat(room_id)

                elif option == 6:
                    disconnect_message = data['disconnect']
                    self._disconnect_from_server(disconnect_message)

            print_lock.release()



    def _send_user_list(self):
        """
        TODO: send the list of users (clients ids) that are connected to this server.
        :return: VOID
        """
        userlist = self.server.userlist
        users = "Users in server: " + ', '.join(userlist)
        sendusers = {'users': users}
        self.server.send(self.clientsocket, sendusers) #server sending client some data
    
      

    def _save_message(self, recipient_id, message):
        """
        TODO: link and save the message received to the correct recipient. handle the error if recipient was not found
        :param recipient_id:
        :param message:
        :return: VOID
        """
        # print(message)
        # print(recipient_id)
        message = message + " (from: " + "client_id: "+ str(self.client_id )+ ")"
        send_message = None

        clientobject_list = self.server.clientobject_list
        clienthandler = self.server.clienthandler

        if int(recipient_id) in self.server.client_id_list:
            send_message = "Message sent!"
            #check if the clienthandler object's client_id matches to the recipient_id 
            #Then append messages to the list of unread messages in that object
            for clienthandler in clientobject_list:
                print(clienthandler.client_id)
                if int(recipient_id) == clienthandler.client_id:
                    print("Appending the messages to id: " + str(clienthandler.client_id))
                    clienthandler.unreaded_messages.append(message)

            
            acknowledges = {'send_message':send_message}
            self.server.send(self.clientsocket, acknowledges)
            self.unreaded_messages.append(message)
            print("Message sent")
        
           
        else:
            send_message = "Recipient id not found!"
            print("Recipient id not found!")
            # error = "Recipient id not found!"
            acknowledges = {'send_message': send_message}
            self.server.send(self.clientsocket, acknowledges)
          
            
    

    def _send_messages(self):
        """
        TODO: send all the unreaded messages of this client. if non unread messages found, send an empty list.
        TODO: make sure to delete the messages from list once the client acknowledges that they were read.
        :return: VOID
        """
        unreaded_messages = None
        # print("Client with id: "+ str(self.client_id)+ " message: " + '\n'.join(self.unreaded_messages))
        if self.unreaded_messages == []:
            unreaded_messages = "No unreaded messages"
            send_message = {'unreaded_message': unreaded_messages}
            self.server.send(self.clientsocket, send_message)
            # return "No unreaded messages"
            # self.send_clientData = "No unreaded messages"
           
        
        else:
            unreaded_messages = "My messages: \n" + '\n'.join(self.unreaded_messages)
            send_message = {'unreaded_message': unreaded_messages}
            self.server.send(self.clientsocket, send_message)
            #clear the list of unreaded messages once read
            self.unreaded_messages.clear()

       

    def _create_chat(self, room_id):
        """
        TODO: Creates a new chat in this server where two or more users can share messages in real time.
        :param room_id:
        :return: VOID
        """
        room_message = "----------------------- Chat Room " + str(room_id) + "------------------------ \n \n"
        exit_message = "Type 'bye' to exit this chat room \n"
        chatowner = "Chat room created by: " + "[" + "client:" + str(self.client_id) + "] \n"
        # print(chatowner)
        waiting = "Waiting for other users to join... \n"
        send_room_message = room_message + exit_message + chatowner + waiting
        send_room = {'send_room': send_room_message}
        self.server.send(self.clientsocket, send_room)
        


    def _join_chat(self, room_id):
        """
        TODO: join a chat in a existing room
        :param room_id:
        :return: VOID
        """
        room_message = "----------------------- Chat Room " + str(room_id) + "------------------------ \n \n"
        exit_message = "Type 'bye' to exit this chat room \n"
        send_room_message = room_message + exit_message

        clienthandler = self.server.clienthandler
        clientobject_list = self.server.clientobject_list
        
        isTrue = True
        if isTrue:
            for clienthandler in clientobject_list:
                if clienthandler.room_id == room_id:
                    send_room = {'send_room': send_room_message}
                    self.server.send(self.clientsocket, send_room)

                    while isTrue:
                        chatData = self.server.receive(self.clientsocket)
                        print(chatData)
                       
                        for self.clientsocket in self.connections:
                            if chatData:
                                # client_name = chatData['client_name']
                                chatMsg = chatData['chatMsg']
                                message = chatData
                                self.server.send(self.clientsocket, message)  

                            if chatMsg == "bye":
                                print("Bye chat") 
                                isTrue = False
                                break

                else:
                    send_room = {'send_room': "No existing room id"}
                    self.server.send(self.clientsocket, send_room)
                    isTrue = False
                    break
        

    def delete_client_data(self):
        """
        TODO: delete all the data related to this client from the server.
        :return: VOID
        """
        self.server.userlist.remove(self.server.users)
        # del self.client_id
        # del self.server.clientname
        self.server.clientobject_list.remove(self)
        self.server.client_id_list.remove(self.client_id)
        self.server.connections.remove(self.clientsocket)
        print("list of users after disconnect: ")
        print(self.server.userlist)
        print("list of clientobjects after disconnect: ")
        print(self.server.clientobject_list)
        print("list of client_id after disconnect: ")
        print(self.server.client_id_list)
        print("list of connections after disconnect: ")
        print(self.server.connections)

    def _disconnect_from_server(self, message):
        """
        TODO: call delete_client_data() method, and then, disconnect this client from the server.
        :return: VOID
        """
        disconnect_message = {'disconnected': "You have been disconnected from the server!"}
        print("Client with id " + str(self.client_id) + message)
        self.server.send(self.clientsocket, disconnect_message)
        self.delete_client_data()
        















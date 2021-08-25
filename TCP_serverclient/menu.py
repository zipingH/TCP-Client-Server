#######################################################################################
# File:             menu.py
# Name:             Ziping Huang
# Github:           zipingH
# Python version:   python 3.81
# Purpose:          CSC645 Assigment #1 TCP socket programming
# Description:      Template Menu class. You are free to modify this
#                   file to meet your own needs. Additionally, you are
#                   free to drop this Menu class, and use a version of yours instead.
# Important:        The server sends a object of this class to the client, so the client is
#                   in charge of handling the menu. This behaivor is strictly necesary since
#                   the client does not know which services the server provides until the
#                   clients creates a connection.
# Running:          This class is dependent of other classes.
# Usage :           menu = Menu() # creates object
#
########################################################################################
# import server
import pickle
import socket
import client
from datetime import datetime
import threading



class Menu(object):
    """
    This class handles all the actions related to the user menu.
    An object of this class is serialized ans sent to the client side
    then, the client sets to itself as owner of this menu to handle all
    the available options.
    Note that user interactions are only done between client and user.
    The server or client_handler are only in charge of processing the
    data sent by the client, and send responses back.
    """

    def __init__(self, client):
        """
        Class constractor
        :param client: the client object on client side
        """
        self.client = client
        self.sameid = True
        

    def set_client(self, client):
        self.client = client

    def show_menu(self):
        """
        TODO: 1. send a request to server requesting the menu.
        TODO: 2. receive and process the response from server (menu object) and set the menu object to self.menu
        TODO: 3. print the menu in client console.
        :return: VOID
        """
        self.process_user_data()
        
        
        
    def process_user_data(self):
        """
        TODO: according to the option selected by the user, prepare the data that will be sent to the server.
        :param option:
        :return: VOID
        """
        
        data = {}
        option = self.option_selected()
        if 1 <= option <= 6: # validates a valid option
           # TODO: implement your code here
           # (i,e  algo: if option == 1, then data = self.menu.option1, then. send request to server with the data)
            if option == 1:
                data = self.option1()

            elif option == 2:
                data = self.option2()

            elif option == 3:
                data = self.option3()

            elif option == 4:
                data = self.option4()
              

            elif option == 5:
                data = self.option5()
           

            elif option == 6:
                data = self.option6()
            

        else: 
            print("Incorrect option number!")

        return data

            

    def option_selected(self):
        """
        TODO: takes the option selected by the user in the menu
        :return: the option selected.
        """
        option = 0
        # TODO: your code here.
        option = input("Your option <enter a number>: ")
        return int(option)

    def get_menu(self):
        """
        TODO: Inplement the following menu
        ****** TCP CHAT ******
        -----------------------
        Options Available:
        1. Get user list
        2. Sent a message
        3. Get my messages
        4. Create a new channel
        5. Chat in a channel with your friends
        6. Disconnect from server
        :return: a string representing the above menu.
        """

        # TODO: implement your code here
        tcpChat = "****** TCP CHAT ****** \n"
        dashes = "----------------------- \n"
        option1 = "1. Get user list \n"
        option2 = "2. Sent a message \n"
        option3 = "3. Get my messages \n"
        option4 = "4. Create a new channel \n"
        option5 = "5. Chat in a channel with your friends \n"
        option6 = "6. Disconnect from server \n"

        menu = tcpChat + dashes + option1 + option2 + option3 + option4 + option5 + option6

        return menu

    def option1(self):
        """
        TODO: Prepare the user input data for option 1 in the menu
        :param option:
        :return: a python dictionary with all the data needed from user in option 1.
        """
        data = {}
        data['option'] = 1
        # Your code here.
        return data

    def option2(self):
        """
        TODO: Prepare the user input data for option 2 in the menu
        :param option:
        :return: a python dictionary with all the data needed from user in option 2.
        """
        data = {}
        date = datetime.now()
        date_string = date.strftime("%Y-%m-%d %H:%M")
        # data['option'] = 2
        # Your code here.
        # fromMessage = "(from: " + self.client.clientname + ")"
        message = input("Enter your message: ")
        message_date = date_string + ": " + message
        recipient_id = input("Enter recipent id: ")
        data = {'option': 2, 'message': message_date, 'recipient_id': recipient_id}
        return data

    def option3(self):
        """
        TODO: Prepare the user input data for option 3 in the menu
        :param option:
        :return: a python dictionary with all the data needed from user in option 3.
        """
        data = {}
        data['option'] = 3
        # Your code here.
        return data

    def option4(self):
        """
        TODO: Prepare the user input data for option 4 in the menu
        :param option:
        :return: a python dictionary with all the data needed from user in option 4.
        """
        data = {}
        # data['option'] = 4
        # Your code here.
        room_id = input("Enter new room id: ")
        data = {'option': 4, 'room_id': room_id}
        return data

    def option5(self):
        """
        TODO: Prepare the user input data for option 5 in the menu
        :param option:
        :return: a python dictionary with all the data needed from user in option 5.
        """
        data = {}

        room_id = input("Enter chat room id to join: ")
        data = {'option': 5, 'room_id': room_id}
        # Your code here.
        return data

    def option6(self):
        """
        TODO: Prepare the user input data for option 6 in the menu
        :param option:
        :return: a python dictionary with all the data needed from user in option 6.
        """
        data = {}
        data = {'option': 6, 'disconnect': " has been disconnected! "}
        return data

    def sendMsg(self):
        while True:
            msg = input(self.client.clientname + "> ")
            sendChatmessage = {'client_name': self.client.clientname, 'chatMsg': msg}
            self.client.send(sendChatmessage)
            # self.client.send(msg)



    def printProcess(self):
        processData = self.process_user_data()
        self.client.send(processData)

        serverData = self.client.receive()

        if not serverData:
            self.client.close()
            self.client.isConnected = False

        if processData.get('option') == 1:
            userlist = serverData['users']
            print(userlist)
            # print(serverData)
                    
        if processData.get('option') == 2:
            send_message = serverData['send_message']
            print(send_message)
                    
        if processData.get('option') == 3:
            unreaded_message = serverData['unreaded_message']
            print(unreaded_message)
                    
        if processData.get('option') == 4:
            send_room = serverData['send_room']
            print(send_room)
                    
        if processData.get('option') == 5:
            send_room = serverData['send_room']
            print(send_room)
            # self.sendChatmessage()

            if send_room != "No existing room id":
                ithread = threading.Thread(target=self.sendMsg)
                ithread.daemon = True
                ithread.start()

                while True:
                    chatData = self.client.receive()

                    client_name = chatData['client_name']
                    chatMsg = chatData['chatMsg']
                    message = client_name + "> " + chatMsg
                    print(message)

                    # print(chatData)

                    if chatMsg == 'bye':
                        print(client_name + " has disconnected.")
                        break
                
                    if not chatData:
                        break
                



        if processData.get('option') == 6:
            disconnected_message = serverData['disconnected']
            print(disconnected_message)
            self.client.close()
            self.client.isConnected = False
           

    
   
    
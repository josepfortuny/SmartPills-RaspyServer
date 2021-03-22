#!/usr/bin/python3

"""
Note: This code has been design for run in a Raspberry Pi,
may there are dependencies that doesn't work in others enviroments.
Change the first line if your Python3 installation is in a alternative PATH
This code check if an image represents the correct pill box 
to be taken according to the data from Firebase DB.
"""
from time import sleep
from ui import userInput
from cloud import cloudManagment
from neuralnetwork import neuralnetwork
import datetime
import sys
import warnings
import threading
warnings.simplefilter("ignore")

### Constants pins ####
PIN_BUTTON = 5
PIN_LED_RED = 19
PIN_LED_GREEN = 26
FIREBASE_URL = 'https://roboticagrupo08-dee61.firebaseio.com/'
SERVER_KEY = "AAAAOssh_o0:APA91bGjz1HLoKbkbDHPVPwkyJJ9aCNySdn_qt1mEwv-FiSInyuPAwGRS6w5Ugc1c57y4vZ-oQggx6dfTGh4ODXDEP979nwhk0mSclEDXrBUGhrfSIHvwhFInd1HUSeVHJo-SapNGB-C"
PATH_TRAIN = "/home/pi/Desktop/Grupo08/neuralnetwork/datasets/"
TRAIN_NEURAL_NETWORK = f"""Do you want to train the code [Y/N] ?"""

email_exists = False
button_pressed = False
current_day = datetime.datetime.today().weekday()

"""
Main runtime of the code. 
Ask for user's mail if it's not registered.
Print the UI with all the instances specified:

If the user has pills planned for the current day and the image of the 
pill box is correct according to the neurla network set LED to green.

Pass to the following day

Print the user's calendar (Pills: day)

Train the neural network 

Leave the App
"""
try:
    user = userInput.userInput(PIN_BUTTON,PIN_LED_RED,PIN_LED_GREEN)
    cm = cloudManagment.firebaseManagment(FIREBASE_URL,SERVER_KEY)
    nn = neuralnetwork.NeuralNetwork(PATH_TRAIN)
    user.welcome_user()
    while not email_exists:
        email=user.check_email_contains(input("Please enter your email address : "))
        email_exists=cm.check_email_exists(email)
    cm.get_pills_calendar()
    while True:
        option = user.get_menu_answer()
        if (option == 1):
            if(cm.print_planned_pills(current_day)):
                if (nn.is_trained()):
                    pill_predicted = nn.predict_image()
                    if (cm.is_pill_planned(pill_predicted,current_day)):
                        # Set green LED HIGH
                        x = threading.Thread(target=user.turn_on_led, args=("green",))
                        x.start()
                        user.turn_on_led("green")

                    else:
                        print ("pill choosen ", pill_predicted ," wasn't planned !!")
                        x = threading.Thread(target=user.turn_on_led, args=("red",))
                        x.start()
                    cm.post_pill_taken(current_day,pill_predicted)
                    current_day = cm.next_day(current_day)
                else:
                    print ("The NeuralNetwork is not trained, please first train it")
            else:
                print("There are not pills planned for today, whait untill tomorrow :D")
        elif( option == 2 ):
            print ("Please Click next day Button")
            while not button_pressed:
                if (user.check_button()):
                    current_day = cm.next_day(current_day)
                    cm.print_planned_pills(current_day)
                    button_pressed = True
            button_pressed = False
        elif (option == 3):
            cm.print_calendar()
        elif (option == 4):
            print("Warning !!! This Process will take aprox 3 hours")
            if (user.ask_user(TRAIN_NEURAL_NETWORK)):
                nn.train_neural_network()
        else:
            print("Leaving the application")
            sys.exit(0)
            user.cleanup()
except KeyboardInterrupt:
    user.cleanup()
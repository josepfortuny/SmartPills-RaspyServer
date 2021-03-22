"""
Code that implements de User Interface
"""

import RPi.GPIO as GPIO
import re
import time

class userInput():
    MENU = f"""You can choose between this options:
    1: Take a pill
    2: Next day
    3: Show Calendar
    4: Train the algorithm
    5: Exit Program

What do you whant to do?"""
    WELCOME = f"""Welcome to Group08 Raspy program:
In order to access, we need to know who you are!!"""
    
    """
    Construct of user inputs
    :param pin_button: identification of the button
    :param pin_led_red: identification of red led pin
    :param pin_led_gree: identification of green led pin
    """
    def __init__(self,pin_button,pin_led_red,pin_led_green):
        self.pin_button = pin_button
        self.pin_led_red = pin_led_red
        self.pin_led_green = pin_led_green
        self.button_pressed = False
        self.regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        self.time_button_pressed = 0
        GPIO.setmode(GPIO.BCM)
        #  12 is equivalent to GPIO 26
        GPIO.setup(self.pin_button, GPIO.IN, pull_up_down = GPIO.PUD_UP )
        GPIO.setup(self.pin_led_red, GPIO.OUT, initial = GPIO.LOW )
        GPIO.setup(self.pin_led_green, GPIO.OUT, initial = GPIO.LOW )
        GPIO.add_event_detect(self.pin_button,GPIO.FALLING,callback=self.button_action,bouncetime=900)
    
    # Here gpio is initialized
    def button_action(self,channel):
        self.button_pressed = True
       
    
    # Valid email checker
    def check_email_contains(self,email_address, min_length=6):
        while True:
            if len(email_address) <= min_length:
                email_address = input("Your email address is too short\nPlease write your email address again: ")
            elif (re.search(self.regex,email_address)):
                return email_address
            else:
                email_address = input("Your email address is not valid\nPlease write your email address again: ")
    
    # Button status checker
    def check_button(self):
        if (self.button_pressed):
            self.button_pressed = False
            return True
        return False
    
    # Answers filter
    def ask_user(self,question):
        valid = {"yes": True, "y": True, "ye": True,
            "no": False, "n": False}
        while True:
            print(question)
            choise = input().lower()
            if choise in valid:
                return valid[choise]
            else:
                print ("You didn't write a correct choise")
    
    # Print the welcome message 
    def welcome_user(self):
        print (self.WELCOME)
    
    # Wait till it get a correct answer fro the user
    def get_menu_answer(self):
        while True:
            try:
                number = int(input(self.MENU))
            except ValueError:
                print("Its not a valid answer ... try it again: ")
            else:
                if number >= 1 and number <= 5:
                   return number
                else:
                    print("Its not a valid answer ... try it again:")
    # Set LED HIGH
    def turn_on_led(self,led):
        port_led = self.pin_led_green
        if (led == "red"):
            port_led = self.pin_led_red
        GPIO.output(port_led,GPIO.HIGH)
        time.sleep(2)
        GPIO.output(port_led,GPIO.LOW)
    
    # Clean up GPIO
    def cleanup(self):
        GPIO.cleanup();
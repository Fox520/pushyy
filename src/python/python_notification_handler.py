import time
import requests
import pushyy

def my_background_callback(data: dict) -> None:
    # ..your code goes here..
    """
    One of the things you can do here: Mark a chat message
    as delivered by making a request to your server
    """
    print("2222222222", data)
    requests.post("http://192.168.0.171:5000/ac", json = data)

if __name__ == '__main__':
    while True:
        try:
            pushyy.process_background_messages(my_background_callback)
            # break;
        except Exception as e:
            # Meh, run the loop again xD
            print(e)
        time.sleep(0.1)

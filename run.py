from flask import Flask
import walletTracker as wt
import time

app = Flask(__name__)


@app.route('/')
def main():
    print("Server is running...")
    wt.test()
    while True:
        print("Checking...")
        wt.start()
        #wt.test()
        time.sleep(60)
    return 'Server Stopped.'

import queue
import threading
import time


class BinanceThread(threading.Thread):
    def __init__(self, hostQueue):
        threading.Thread.__init__(self)
        self.hostQueue = hostQueue
        self.key_api = None
        self.key_secret = None
        self.tik = 1
        self._load_keys()

    def run(self):
        while True:
            time.sleep(self.tik)

    def _load_keys(self):
        with open("data/binance_api.txt") as file:
            self.key_api = file.readline()
        with open("data/binance_key.txt") as file:
            self.key_secret = file.readline()

    def change_tik(self, tik):
        self.tik = tik

    def get_balance(self):
        return str(123)


if __name__ == "__main__":
    print("start tests")
    hostQueue = queue.Queue()
    t = BinanceThread(hostQueue)
    t.setDaemon(True)
    t.start()

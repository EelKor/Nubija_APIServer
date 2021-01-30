from dbaccess import DBAccess
from time import sleep
import threading

def dbUpdater() :
    while True :
        db = DBAccess()
        db.update()
        db.close()

        sleep(10)

def test() :
    while True :
        print("This is fun Test")
        sleep(9)

if __name__ == '__main__':
    thread_updater = threading.Thread(target=dbUpdater)

    thread_updater.start()
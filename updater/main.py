from dbaccess import DBAccess
from time import sleep
import threading

# 데이터 베이스 업데이트 함수
def dbUpdater() :
    while True :
        db = DBAccess()
        db.update()
        db.close()

        sleep(300)

# 차후 추가할 함수
def test() :
    while True :
        print("This is fun Test")
        sleep(9)

# 스레딩을 이용해여 동시 실행
if __name__ == '__main__':
    thread_updater = threading.Thread(target=dbUpdater)

    thread_updater.start()
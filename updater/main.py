from dbaccess import DBAccess
from time import sleep
import datetime
import threading


# 데이터 베이스 업데이트 함수
def dbUpdater() :

    # 최근 업데이트 시간
    recent = 0
    print("recent")


    while True :
        now = datetime.datetime.now()

        # 누비자 이용시간이 지나면 업데이트 중지
        if now.hour >= 1 and now.hour < 4:
            recent = 0
            print("OOS")
            pass

        # 누비자 이용시간일때 업데이트 시작
        else:

            # 첫 업데이트
            if recent == 0:
                # 데이터베이스 완전 초기화후 재생성
                db = DBAccess()
                db.initupload()
                db.close()
                recent = datetime.datetime.now()
                print("init update")
                print("recent: ", recent)
            
            # 업데이트 시작 시간과 현재시간의 차이가 10초 정도 이면 업데이트 시작
            # == 를 사용하변 밀리세컨드 단위까지 같아야 해서 업데이트가 안되는
            # 경우 발생
            elif (now - (recent + datetime.timedelta(minutes=5))).seconds < 10:
                db = DBAccess()
                db.update()
                db.close()
                recent = datetime.datetime.now()
                print("update")
                print("recent: ", recent)

            else:
                pass



        

# 차후 추가할 함수
def test() :
    db = DBAccess()
    db.addcolumn()
    db.close()
    print("Done")

# 스레딩을 이용해여 동시 실행
if __name__ == '__main__':
    #thread_updater = threading.Thread(target=dbUpdater)
    thread_updater = threading.Thread(target=test)

    thread_updater.start()
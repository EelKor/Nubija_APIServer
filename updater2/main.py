from dbaccess import DBAccess
from time import sleep
from datetime import datetime, time, timedelta
from pytz import timezone
import threading

# 데이터 베이스 업데이트 함수
def dbUpdater() :

    while True :
        # 현재시간이 누비자 운영시간이면 프로그램 작동
        # 아니면 휴식
        now = datetime.now()
        now = now.hour
        if now >= 1 and now < 4:
            pass

        else:
            prev_TerminalInfo = []
            new_TerminalInfo = []
            result = []

            db = DBAccess()

            # 이전 데이터 불러오기
            prev_data = db.read(0)
            for oldData in prev_data:
                vno = int(oldData['Vno'])
                old_parkcnt = int(oldData['Parkcnt'])
                temp = [vno, old_parkcnt]
                prev_TerminalInfo.append(temp)

            # 데이터베이스 업데이트
            db.update()

            # 새로운 데이터 불러오기
            new_data = db.read(0)
            for newData in new_data:
                vno = int(newData['Vno'])
                new_parkcnt = int(newData['Parkcnt'])
                temp = [vno, new_parkcnt]
                new_TerminalInfo.append(temp)

            # 차이값 계산
            if len(new_TerminalInfo) == len(prev_TerminalInfo):
                for i in range(len(new_TerminalInfo)-1):
                    date = datetime.now(timezone('Asia/Seoul'))
                    date = date.strftime("%Y-%m-%d %H:%M:%S")
                    vno = new_TerminalInfo[i][0]
                    diff = new_TerminalInfo[i][1] - prev_TerminalInfo[i][1]
                    result.append([date, vno, diff])

                db.stationLogInsert(result)



            db.close()
            print(result)
            sleep(300)

# 스레딩을 이용해여 동시 실행
if __name__ == '__main__':
    thread_updater = threading.Thread(target=dbUpdater)

    thread_updater.start()
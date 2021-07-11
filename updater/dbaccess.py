import pymysql
from public_data import nubija
import datetime


class DBAccess(nubija.NubijaData):

    def __init__(self):

        # __db_login은 보안을 위해 privite
        self.__db_login = pymysql.connect(
            #user='publicdata',
            #passwd='1q2w3e4r',
            #host='127.0.0.1',
            #port=3316,
            #db='public_data',
            #charset='utf8'
#
            # 원격 접속때 이용
            user='publicdata',
            passwd='1q2w3e4r',
            host='db.lessnas.me',
            port=33306,
            db='public_data',
            charset='utf8'

        )
        # pymysql 을 사용하기 위한 기본 설정
        self.cursor = self.__db_login.cursor(pymysql.cursors.DictCursor)






    ##### 메소드 updateall 설명 ######
    # 데이터베이스를 업데이트 하는 것으로 데이터베이스내 모든 데이터를 최신화
    def initupload(self):
        self.__initsql = "truncate nubijaInfo"
        self.__sql = "INSERT INTO nubijaInfo (Vno, Emptycnt, Parkcnt) " \
                     "VALUES(%s, %s, %s)"

        # 데이터 베이스 초기화 실시
        self.cursor.execute(self.__initsql)
        self.__db_login.commit()


        # 새로운 누비자 데이터를 불러오기
        super().__init__()
        data = []

        # excutemany 를 활용하기 위해 이차원 리스트 형식으로 변환
        # 반복문으로 하나씩 excute 보다 훨씬 빠른 성능
        # 반복문의 len(self.rawdata)-1 은 길이를 의미
        for i in range(len(self.rawdata) - 1):
            dict_raw = dict(self.rawdata[i])

            dict_d = []
            dict_d.append(int(dict_raw['Vno']))
            dict_d.append(dict_raw['Emptycnt'])
            dict_d.append(dict_raw["Parkcnt"])

            data.append(dict_d)

        self.cursor.executemany(self.__sql, data)
        self.__db_login.commit()
        print(self.cursor.rowcount, "recored inserted")






    # update 메소드 설명
    # MySQL 서버의 NubijaData테이블 업데이트 메소드
    # 현재 소요시간이 많이 걸리는데 반복문 분석해 최적화 실시할것
    # 지금 코드는 누비자 서버로 부터 데이터 수신후 바로 Mysql에 업로드 하는 것인데
    # 먼저 Mysql에서 데이터를 수신받고, 이 데이터를 누비자 서버로 부터 받은 데이터와
    # 비교한후, 변동사항이 있는 것만 업로드 할 수있도록 코드 작성예정.

    def update(self):
        __updatesql = "UPDATE nubijaInfo SET  Emptycnt=%s, Parkcnt=%s WHERE Vno=%s"
        __readsql = "SELECT * FROM nubijaInfo"
        __insertStationlogs = ""
        super().__init__()
        data = []
        delta = []

        # 새로운 데이터 가져오기
        for i in range(len(self.rawdata) - 1):
            dict_raw = dict(self.rawdata[i])
            dict_d = [dict_raw['Emptycnt'], dict_raw['Parkcnt'], int(dict_raw['Vno'])]
            data.append(dict_d)


        # 기존 데이터 불러오기
        self.cursor.execute(__readsql)
        oldraw = self.cursor.fetchall()

        now = datetime.datetime.now()
        delta.append(now.strftime('%Y-%m-%d %H:%M:%S'))
       
        # 각 정류장의 변화량 계산
        for i in range(len(oldraw) - 1):
        
            old_raw = dict(oldraw[i])
            old = [old_raw['Emptycnt'], old_raw['Parkcnt'], old_raw['Vno']]
            new_empty = data[i]
            delta.append([int(new_empty[0]) - int(old[0]), int(old[2])])


            
        print(delta)

        #print(data)
        #self.cursor.executemany(__updatesql, data)
        #self.__db_login.commit()
        print(self.cursor.rowcount, "record inserted")






    def read(self, vno):

        if not type(vno) == type(int):
            vno = int(vno)

        if vno == 0:

            __readsql = "SELECT Emptycnt, Parkcnt, Vno FROM public_data.nubijaInfo"

            self.cursor.execute(__readsql)
            return self.cursor.fetchall()

        else:
            __readsql = "SELECT Emptycnt, Parkcnt FROM public_data.nubijaInfo WHERE Vno=%s"
            self.cursor.execute(__readsql, vno)
            return self.cursor.fetchall()

    # 284개의 테이블 컬럼 생성
    def addcolumn(self):
        __sql = """ALTER TABLE StationLogs ADD COLUMN %s char(10)"""
        for i in range(1,285):
            self.cursor.execute(__sql,(i))

        self.__db_login.commit()   




    def close(self):
        self.cursor.close()

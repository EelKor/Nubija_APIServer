import pymysql
from public_data import nubija

class DBAccess(nubija.NubijaData):

    def __init__(self):

        # __db_login은 보안을 위해 privite
        self.__db_login = pymysql.connect(
            #user='publicdata',
            #passwd='1q2w3e4r',
            #host='localhost',
            #port=33306,
            #db='public_data',
            #charset='utf8'

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
        self.__sql = "INSERT INTO NubijaData (Emptycnt, Parkcnt, Tmname, Rankcnt, Latitude, Longitude, Vno) " \
                     "VALUES(%s, %s, %s, %s, %s, %s, %s)"

        # 새로운 누비자 데이터를 불러오기
        super().__init__()
        data = []

        # excutemany 를 활용하기 위해 이차원 리스트 형식으로 변환
        # 반복문으로 하나씩 excute 보다 훨씬 빠른 성능
        # 반복문의 len(self.rawdata)-1 은 길이를 의미
        for i in range(len(self.rawdata)-1):
            dict_d = list(dict(self.rawdata[i]).values())
            dict_d[6] = int(dict_d[6])
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
        __updatesql = "UPDATE NubijaData SET  Emptycnt=%s, Parkcnt=%s WHERE Vno=%s"
        super().__init__()
        data = []

        for i in range(len(self.rawdata)-1):
            dict_d = list(dict(self.rawdata[i]).values())
            del dict_d[2:6]
            data.append(dict_d)

        self.cursor.executemany(__updatesql, data)
        self.__db_login.commit()
        print(self.cursor.rowcount, "record inserted")

    def read(self, vno):
        if not type(vno)==type(int):
            vno = int(vno)

        if vno == 0:
            __readsql = "SELECT Emptycnt, Parkcnt, Vno FROM public_data.NubijaData"
            self.cursor.execute(__readsql)
            return self.cursor.fetchall()

        else:
            __readsql = "SELECT Emptycnt, Parkcnt FROM public_data.NubijaData WHERE Vno=%s"
            self.cursor.execute(__readsql, vno)
            return self.cursor.fetchall()


    def close(self):
        self.cursor.close()








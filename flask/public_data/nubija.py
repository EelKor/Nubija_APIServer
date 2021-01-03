import requests

class NubijaData:
    rawdata = None                                 # 누비자 데이터 dict형식

    def __init__(self):

        # 최초실행코드
        raw = requests.get("http://api.nubija.com:1577/ubike/nubijaInfoApi.do?apikey=aMEEZeshtbWikWmkRmXD")
        dict_data = raw.json()
        list_data = dict_data['TerminalInfo']
        self.rawdata = list_data                               # 클래스 변수 초기화

    def terminalinfo(self, id):
        if not type(id) == int:
            raise ValueError("입력값이 int형이 아닙니다")
        if id < 0:
            raise ValueError("입력값이 양수가 아닙니다")

        self.id = id
        return dict(self.rawdata[self.id-1])

    def showdata(self):
        print(self.rawdata)


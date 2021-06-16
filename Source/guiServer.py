from socket import *
import threading
import datetime

stop = True

class chatRoom: # 채팅방에 관한 설정을 하는 클래스이다
    def __init__(self): # __init__메서드로 변수들을 초기화 한다
        self.clients = [] # 각 클라이언트을 담을 리스트 변수이다
        self.allChat = None # 모든 대화기록들을 저장할 변수이다

    def sendMessageAll(self, message): # 채팅방에 있는 모든 클라이언트에게 메시지를 전송한다
        for i in self.clients: # 리스트안에 있는 클라이언트의 수 만큼 반복한다
            print(i)
            i.sendMessage(message)

    def addClient(self, t): # 리스트에 새 클라이언트를 추가하는 메서드이다.
        self.clients.append(t)

    def delClient(self, t): # 리스트에서 해당 클라이언트를 삭제하는 메서드이다.
        self.clients.remove(t)

class chatClient: # 채팅의 송/수신을 담당하는 부분이다.
    def __init__(self, room, sock): # 사용할 변수들을 초기화해준다.
        self.room = room
        self.id = None
        self.sock = sock

    def readMessage(self):
        now = str(datetime.datetime.now().strftime("%A, %d. %I:%M %p"))  # 처음 접속하고 닉네임을 지정하는 시간 저장
        self.id = self.sock.recv(1024).decode() # 클리아언트로 부터 받은 id를 수신받는다
        message ='[' + now + '] ' +  self.id + '님이 입장하셨습니다.'
        self.room.sendMessageAll(message) # 모든 클라이언트에게 메시지를 전송

        while True:
            now = str(datetime.datetime.now().strftime("%A, %d. %I:%M %p"))  # 채팅 입력할 때마다 갱신하는 시간
            message = self.sock.recv(1024).decode() # 받은 데이터를 decode함수로 byte코드를 문자열로 변환한다
            # if message == "/종료":
            #     self.sock.sendall(message)
            #     self.room.delClient(self)
            #     stop = False
            #     break
            message = '[' + now + '] ' + self.id + ' : ' + message
            self.room.sendMessageAll(message)
        # self.room.sendMessageAll('[' + now + '] ' + self.id + '님이 퇴장하셨습니다')


    def sendMessage(self, message): #
        # print(type(message))
        self.sock.sendall(message.encode(encoding='utf-8')) # sendall함수는 모두 전송할 때까지 send함수를 호출한다

class chatSever: # 서버의 생성 및 설정을 담당
    ip = '127.0.0.1'
    port = 8080

    def __init__(self):
        self.server_sock = None
        self.room = chatRoom() # chatRoom클래스의 인스턴스 생성

    def open(self):
        self.server_sock = socket(AF_INET, SOCK_STREAM) # 서버 소켓 생성, AF_INET으로 IPv4인터넷 프로토콜로 설정/SOCK_STREAM으로 TCP프로토콜을 사용
        self.server_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # setsockopt로 소켓 옵션을 설정한다
        # 프로그램을 강제 종료하고나서, 커널단에서 해당 소켓을 바인딩해서 사용하고 있어서 프로그램을 재실행하면 오류가발생하는데,
        # SO_REUSEADDR 옵션을 주면 기존에 바인디된 주소를 다시 사용할 수 있게 할 수 있다.
        self.server_sock.bind((chatSever.ip,chatSever.port)) # 소켓을 ip와 포트 번호와 연결하는데 사용한다
        self.server_sock.listen() # 클라이언트 연결 대기상태

    def run(self): # 서버 가동 함수
        self.open()
        print('서버 가동')

        while True:
            client_sock, addr = self.server_sock.accept() # 클라이언트의 연결을 허용한다
            print(addr, '접속') # 연결을 허용한 클라이언트의 ip번호와 포트번호가 출력된다
            t = chatClient(self.room, client_sock) # 인스턴스 생성
            self.room.addClient(t) # 클라이언트 리스트에 새로 append한다
            print('클라이언트 : ', self.room.clients)
            th = threading.Thread(target=t.readMessage) # 스레드 생성
            # target=t.readMessage로 쓰레드가 실행할 함수를 선언한다.
            th.start() # 스레드 시작

            # if stop == False:
            #     self.server_sock.close()
            #     break


def main(): # 위의 모든 코드가 실행될 메인 부분
    cs = chatSever()
    cs.run()

main()
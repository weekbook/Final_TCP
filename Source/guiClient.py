import threading
from socket import *
from tkinter import *
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

class chatUi:
    ip = '127.0.0.1'
    port = 8080

    # ip = tkinter.StringVar()
    # port = tkinter.IntVar()

    def __init__(self): # 사용 할 변수들을 초기화한다
        # self.root = None
        self.conn_sock = None
        self.window2 = None
        self.window = None
        self.chatContent = None
        self.enterChat = None
        self.sendBtn = None
        self.allChat = ''
        # self.ip =''
        # self.port = None

        self.num1 = None
        self.num2 = None
        self.op = None
        self.result = None

    def connect(self): # 서버와의 연결을 담당하는 함수
        self.conn_sock = socket(AF_INET, SOCK_STREAM)
        self.conn_sock.connect((chatUi.ip, chatUi.port))

    # def connect(self):
    #     self.conn_sock = socket(AF_INET, SOCK_STREAM)
    #
    #     try:
    #         self.conn_sock.connect((self.ip, self.port))
    #     except Exception as e:
    #         print('Connect Error : ', e)
    #         return False
    #     else:
    #         th2 = threading.Thread(target=self.recvMessage)
    #         th2.start()
    #         print('연결')
    #
    #     return True

    def connetInfo(self):
        self.window2 = Tk()
        self.window2.title('주소정보입력')
        self.window2.geometry('220x50')
        self.ipInfo = tk.Label(self.window2, text='IP : ', textvariable=self.ip)
        self.portInfo = tk.Label(self.window2, text='Port : ', textvariable=self.port)
        self.ipEntry = tk.Entry(self.window2, width=30)
        self.portEntry = tk.Entry(self.window2, width=30)

        self.ipInfo.grid(row=0, column=0)
        self.portInfo.grid(row=1, column=0)
        self.ipEntry.grid(row=0, column=1)
        self.portEntry.grid(row=1, column=1)

        self.ipEntry.bind('<Return>', self.sendInfo)
        self.portEntry.bind('<Return>', self.sendInfo)

        self.window2.mainloop()

    def sendInfo(self, e):
        self.ip =self.ipEntry.get()
        self.port = self.portEntry.get()

        self.window2.destroy()

    def setWindow(self): # 채팅프로그램의 GUI
        self.window = Tk()
        self.window.title('인하챗2021')
        self.window.geometry('570x520')
        self.chatContent = tk.Label(self.window, borderwidth=4, relief="sunken",bg='white', width=60, height=30, text='닉네임을 입력하세요')
        self.joinUser = tk.Label(self.window, borderwidth=2, relief="sunken",bg='white', width=15, height=4,text='접속한 서버 정보' + '\n' + chatUi.ip + '\t' + str(chatUi.port))
        self.enterChat = tk.Entry(self.window, borderwidth=3, relief="sunken",width=54)
        self.sendBtn = tk.Button(self.window, borderwidth=4,width=10, text="보내기", command=self.sendMessage)
        self.exitBtn = tk.Button(self.window, borderwidth=4,width=10, text="종료", command=self.exitChat)
        self.cal = tk.Button(self.window, borderwidth=4, width=10, text='계산기', command=self.CalculatorUI)
        self.refresh = tk.Button(self.window, borderwidth=4, width=10, text='지우기', command=self.chatClear)

        # scroll = tk.Scrollbar(self.window, orient="vertical")
        # scroll.grid(row=0, column=1, sticky='ns',padx=10)
        # self.window.configure()
        # self.scrollbar = tk.Scrollbar(self.window)

        self.chatContent.grid(row=0, column=0) # 대화기록이 출력되는 창
        self.joinUser.grid(row=0, column=1, padx=10, sticky='n') # 접속정보가 출력되는 창
        self.enterChat.grid(row=1, column=0, ipadx=20) # 대화내용을 입력하는 창
        self.sendBtn.grid(row=1, column=1) # 대화내용을 전송하는 버튼
        self.exitBtn.grid(row=0, column=1,sticky='s',pady=60) # 통신 종료 버튼
        self.cal.grid(row=0, column=1,sticky='s',pady=15) # 계산기 버튼
        self.refresh.grid(row=0,column=1, sticky='s', pady=100) # 대화내용 초기화 버튼
        # self.scrollbar.grid(row=0, column=1,sticky='ns')

        self.enterChat.bind('<Return>', self.sendMessage) # bind함수를 사용하여 Enter키를 누르면 채팅이 보내지도록 연결

    def chatClear(self): # 채팅초기화 함수
        self.chatContent.config(text='')


    def sendMessage(self, e): # 채팅 전송 함수
        message = self.enterChat.get() # 입력받은 문자열을 메시지 변수에 저장
        self.enterChat.delete(0, tk.END) # 채팅 전송 후 입력창을 초기화한다
        self.enterChat.config(text='')
        print(type(message))
        message = message.encode(encoding='utf-8') # encode함수로 문자열을 byte코드로 변환한다 변환을 해야 서버쪽에서 수신받을 수 있다
        print(self.conn_sock)
        self.conn_sock.sendall(message) # sendall함수를 통해 요청한 데이터의 모든 버퍼 내용을 모두 전송한다
        print('메시지를 전송하였습니다')

    def recvMessage(self): # 채팅 수신 함수
        while True:
            print('메시지를 수신하였습니다')
            message = self.conn_sock.recv(1024) # 서버로부터 1024바이트 크기만큼 수신
            print(message)
            message = message.decode() + '\n' # byte코드를 문자열로 변환 / 가독성을 위해 줄 바꿈을 추가한다
            self.allChat += message
            print('서버 : ', self.allChat)
            self.chatContent.config(text=self.allChat, justify='left') # 대화내용을 config함수로 출력한다 / justify는 문자열의 정렬방법을 설정한다

        #     if message == '/종료':
        #         self.conn_sock.close()
        #         print('종료되었습니다')
        #         break
        # self.conn_sock.close()

    def exitChat(self): # 통신 종료 함수
        # self.conn_sock.sendall('접속을 종료하였습니다.'.encode(encoding='utf-8'))
        print(self.allChat, file=self.fp) # 통신을 종료하면서 지금까지 대화한 내용들을 파일에 모두 저장
        self.chatContent.config(text='접속을 종료하였습니다' ,justify='left')
        self.conn_sock.close() # 소켓을 종료한다
        self.fp.close() # 파일을 닫아준다

    def run(self): # 가동 기능 담당 함수
        self.connetInfo()
        self.fp = open('chatHistory.txt', 'a') # 대화 내용을 기록할 파일을 연결한다, 'a'값을 줘서 기존내용에 이어쓰도록 설정
        self.connect() # 연결
        self.setWindow() # GUI창 띄우기

        th1 = threading.Thread(target=self.recvMessage) # 스레드 생성
        # target=t.recvMessage 쓰레드가 실행할 함수를 선언한다.
        th1.start()

        self.window.mainloop() # 윈도우에서 수행되는 마우스 클릭 같은 이벤트들이 발생하게끔 유지해주는 함수

    def CalculatorUI(self): # 계산기의 GUI 세팅 함수
        newWindow = tk.Toplevel(self.window) # Toplevel 함수를 사용하여 외부 위젯을 종료하지않고 별도의 창을 작동할 수 있다
        newWindow.title('계산기')

        self.resultWindow = tk.Label(newWindow, width=25) # 입력한 값이나 결과값이 출력되는 부분
        self.resultWindow.grid(row=0, column=0, columnspan=4)

        # 각 버튼들을 생성 및 배치
        self.b1 = tk.Button(newWindow, text='1', width=25, command=lambda: self.numBtn('1'))
        self.b1.grid(row=1, column=0)
        self.b2 = tk.Button(newWindow, text='2', width=25, command=lambda: self.numBtn('2'))
        self.b2.grid(row=1, column=1)
        self.b3 = tk.Button(newWindow, text='3', width=25, command=lambda: self.numBtn('3'))
        self.b3.grid(row=1, column=2)
        self.b4 = tk.Button(newWindow, text='+', width=25, command=lambda: self.opBtn('+'))
        self.b4.grid(row=1, column=3)
        self.b5 = tk.Button(newWindow, text='4', width=25, command=lambda: self.numBtn('4'))
        self.b5.grid(row=2, column=0)
        self.b6 = tk.Button(newWindow, text='5', width=25, command=lambda: self.numBtn('5'))
        self.b6.grid(row=2, column=1)
        self.b7 = tk.Button(newWindow, text='6', width=25, command=lambda: self.numBtn('6'))
        self.b7.grid(row=2, column=2)
        self.b8 = tk.Button(newWindow, text='-', width=25, command=lambda: self.opBtn('-'))
        self.b8.grid(row=2, column=3)
        self.b9 = tk.Button(newWindow, text='7', width=25, command=lambda: self.numBtn('7'))
        self.b9.grid(row=3, column=0)
        self.b10 = tk.Button(newWindow, text='8', width=25, command=lambda: self.numBtn('8'))
        self.b10.grid(row=3, column=1)
        self.b11 = tk.Button(newWindow, text='9', width=25, command=lambda: self.numBtn('9'))
        self.b11.grid(row=3, column=2)
        self.b12 = tk.Button(newWindow, text='*', width=25, command=lambda: self.opBtn('*'))
        self.b12.grid(row=3, column=3)
        self.b13 = tk.Button(newWindow, text='0', width=25, command=lambda: self.numBtn('0'))
        self.b13.grid(row=4, column=0)
        self.b14 = tk.Button(newWindow, text='C', width=25, command=lambda: self.clear())
        self.b14.grid(row=4, column=1)
        self.b15 = tk.Button(newWindow, text='=', width=25, command=lambda: self.resultBtn())
        self.b15.grid(row=4, column=2)
        self.b16 = tk.Button(newWindow, text='/', width=25, command=lambda: self.opBtn('/'))
        self.b16.grid(row=4, column=3)

    # C 클릭시 발생하는 함수 / 초기화 기능을 담당
    def clear(self):
        self.num1 = None
        self.num2 = None
        self.op = None
        self.resultWindow.config(text='')

    # 숫자 클릭시 발생하는 함수
    def numBtn(self, num):
        txt = self.resultWindow.cget('text')
        txt += num
        if self.op is None:
            self.num1 = txt
            self.resultWindow.config(text=self.num1)
        else:
            self.num2 = txt
            self.resultWindow.config(text=self.num2)

    # 연산자 클릭시 발생하는 함수
    def opBtn(self, op):
        self.op = op
        self.resultWindow.config(text='')

    # = 버튼 클릭시 발생하는 함수
    def resultBtn(self):
        if self.num1 is not None and self.num2 is not None:
            if self.op == '+':
                self.num1 = int(self.num1) + int(self.num2)
                self.num2= None
                self.resultWindow.config(text=self.num1)
            elif self.op == '-':
                self.num1 = int(self.num1) - int(self.num2)
                self.num2 = None
                self.resultWindow.config(text=self.num1)
            elif self.op == '*':
                self.num1 = int(self.num1) * int(self.num2)
                self.num2 = None
                self.resultWindow.config(text=self.num1)
            elif self.op == '/':
                self.num1 = int(self.num1) / int(self.num2)
                self.num2 = None
                self.resultWindow.config(text=self.num1)


def main():
    connect = chatUi()
    connect.run()

main()
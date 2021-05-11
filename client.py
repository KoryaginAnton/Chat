from PyQt6 import QtWidgets, QtCore
import requests
import clientDiz
from datetime import datetime


class ExampleApp(QtWidgets.QMainWindow, clientDiz.Ui_MainWindow):
    def __init__(self, server_url):
        super().__init__()
        self.setupUi(self)

        self.server_url = server_url
        self.pushButton.pressed.connect(self.send_message)
        self.after = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.get_messages)
        self.timer.start(1000)

    def print_message(self, message):
        dt = datetime.fromtimestamp(message['time'])
        dt_str = dt.strftime('%H:%M:%S')
        self.textBrowser.append(dt_str + ' ' + message['name'])
        self.textBrowser.append(message['text'])
        self.textBrowser.append('')

    def get_messages(self):
        try:
            response = requests.get(self.server_url + '/messages', params={'after': self.after})
        except:
            return
        messages = response.json()['messages']
        if messages:
            for message in messages:
                self.print_message(message)
            self.after = messages[-1]['time']

    def send_message(self):
        data = {
            'name': self.lineEdit.text(),
            'text': self.textEdit.toPlainText()
        }
        try:
            response = requests.post(self.server_url + '/send', json=data)
        except:
            self.textBrowser.append('Сервер не доступен')
            self.textBrowser.append('')
            return
        if response.status_code != 200:
            self.textBrowser.append('Ошибка валлидации')
            self.textBrowser.append('')
            return
        self.textEdit.clear()


app = QtWidgets.QApplication([])
window1 = ExampleApp(server_url='http://42050a27ba44.ngrok.io')
window1.show()
app.exec()

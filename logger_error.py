from datetime import datetime


class log_error:
    def __init__(self):
        self.now = datetime.now()
        self.date = self.now.date()
        self.current_time = self.now.strftime("%H:%M:%S")

    def dvc_logger(self, log_mess):
        f = open("log.txt", 'a+')
        f.write(str(self.date) + "/" + str(self.current_time) + "\t\t" + log_mess + "\n")

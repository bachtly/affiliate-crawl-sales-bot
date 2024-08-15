import threading
from datetime import datetime
from time import sleep

MAX_RETRIES = 3


class Scheduler:
    threadLocal = None

    def __init__(self, handler, getSchedules, applicationName):
        self.handler = handler
        self.getSchedules = getSchedules
        self.applicationName = None

    def Run(self):
        thread = threading.Thread(target=self.Execute)
        thread.start()

    def Execute(self):
        retries = 0
        while True:
            try:
                if [datetime.now().hour, datetime.now().minute] in self.getSchedules():
                    print('scheduler.run_at.started')
                    self.handler()
                    print('scheduler.run_at.success')
                    sleep(60)
            except Exception as e:
                print(str(e))
                print({"retries": retries})
                if retries >= MAX_RETRIES: raise e
                retries += 1

            sleep(1)

    def GetApplicationName(self):
        return self.applicationName

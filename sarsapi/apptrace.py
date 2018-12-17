import datetime

class AppTrace:

    def __init__(self, traceEnabled):
        self.traces = []
        self.traceEnabled = traceEnabled
       

    def log(self, methodName, message):
        logitem = {
                "datetime": datetime.datetime.now().strftime("%c"),
                "method": methodName,
                "message": message
        }

        print(logitem)
        if self.traceEnabled == True:
            self.traces.append(logitem)
           

        
    def get(self):
        return self.traces


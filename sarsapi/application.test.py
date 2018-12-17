import controller
import lookup
import indexer
import apptrace
import settings

setting = settings.Setting() 
debug = setting.debugMode
trx = apptrace.AppTrace(setting.debugMode)
indx = indexer.Indexer(trx, setting)
lp = lookup.Lookup(trx, setting)
ctrl = controller.Controller(lp, indx, trx, setting)


def stdout(listtoprint, title):
    print(title)
    for item in enumerate(listtoprint):
        print(item)
    print()


def starttest():
    ctrl.load()
    searchcity = "Pittsburgh"
    searchstate = "PA"
    query_parameters = {"text": "good pizza", "city": searchcity, "state": searchstate}
    sresults = []
    sresults.append(ctrl.Search(query_parameters))
    stdout(sresults, "Printing document by location")
    stdout(trx.get(), "Traces")


def loadlookuptest():
    lp.load()
    stdout(trx.get(), "Traces")


def loadindexertest():
    indx.load()        
    stdout(trx.get(), "Traces")


# execute
if __name__ == '__main__':
   # loadlookuptest()
   # loadindexertest()
    starttest()
    
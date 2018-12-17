import json
import sys, os

class Lookup:

    def __init__(self, trace, settings):
        self.trace = trace
        self.filepath = settings.lookupFilePath
        self.datasetKey = settings.datasetKey
        self.dataset = settings.dataset
        self.stopwords = ["yelp", "...", ".", "..", "n't", "ve", "'ve", "....", ".....", "......", ".......", "'", "'ll", "''"]
       

    def load(self):
        lookupdata = {}
        self.trace.log("Lookup.load", "Number of items before loading file: {}".format(len(lookupdata)))
        lookupPath = os.path.abspath(self.filepath)
        self.trace.log("Lookup.load", "Path to load file: {}".format(lookupPath))
        
        with open(lookupPath, encoding="utf8") as json_file:  
            lookupdata = json.load(json_file)
            self.trace.log("Lookup.load", "File loaded, number of items loaded: {}".format(len(lookupdata)))
        return lookupdata        
    
    def dedupe(self, topics):
        dedupes = []
        for item in topics:
            sitem = item.strip()
            if sitem not in self.stopwords and sitem not in dedupes:
                dedupes.append(sitem)
        return dedupes

    
    def documentLookup(self, qresults, lookupdata, max_results):
        lookupresult = []     
        count = 0
        for item in qresults:            
        # for item in lookupdata:
            resultItem = item[self.datasetKey]
            if resultItem in lookupdata:
                lookupItem = lookupdata[resultItem]  
                lookupItem[self.dataset] = self.dedupe(item[self.dataset][resultItem].split(","))             
                lookupresult.append(lookupItem)
                count = count + 1
                if count >= max_results:
                    break
        return lookupresult


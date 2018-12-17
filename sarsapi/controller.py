
import math
import sys
import time
import metapy
import pytoml


class Controller:

    def __init__(self, lookup, indexer, trace, setting):
        self.lookup = lookup
        self.indexer = indexer
        self.trace = trace
        self.unknown = "UNKNOWN"
        self.datasetKey = setting.datasetKey
        self.maxSearchResults = setting.maxSearchResults

    # begin private methods

    def __filterbyLocation__(self, searchResults, requestParams):
        results = []
        searchcity = requestParams["city"].lower()
        searchstate = requestParams["state"].lower()
        self.trace.log("Controller.__filterbyLocation__", "Location: City: {} State: {}".format(searchcity, searchstate))
        self.trace.log("Controller.__filterbyLocation__", "Number of items in original results: {}".format(len(searchResults)))
        for res in searchResults:
            if searchcity != self.unknown and searchstate != self.unknown and res['city'].lower() == searchcity and res['state'].lower() == searchstate:
                results.append(res)
        self.trace.log("Controller.__filterbyLocation__", "Number of items in after filter: {}".format(len(results)))
        return results

    def __reduceResult__(self, parentList, smallList):
        reduced = []
        for keyitem in parentList:
            found = False
            for item in smallList:
                if keyitem[self.datasetKey] == item[self.datasetKey]:
                    found = True
                    break
            if found == False:
                reduced.append(keyitem)
        return reduced

            

    def __extractRequestParams__(self, query_parameters):
        if 'text' in query_parameters:
            searchtext = query_parameters['text']
        else:
            return self.__errorNoSearchText__()

        if 'city' in query_parameters:
            searchcity = query_parameters['city']
        else:
            searchcity = self.unknown

        if 'state' in query_parameters:
            searchstate = query_parameters['state']
        else:
            searchstate = self.unknown
        
        if 'zip' in query_parameters:
            searchzip = query_parameters['zip']
        else:
            searchzip = self.unknown
        
        return {
            "text": searchtext,
            "city": searchcity,
            "state": searchstate,
            "zip": searchzip
        }

    def __bySentiment__(self, item):
        return float(item['sentiment'])


    def __errorNoSearchText__(self):
        error = {
                "errorCode": 400, 
                "message": "Search Text not provided in request."
                }
        return error

    # end private methods

    # begin public methods
    def Search(self, query_parameters):
        
        requestParams = self.__extractRequestParams__(query_parameters)
        if 'errorCode' in requestParams:
            return requestParams

        # lookup load
        self.trace.log("Controller.Search", "calling lookup.load()")
        lookupdata = self.lookup.load()
        # load indexer
        self.trace.log("Controller.Search", "calling indexer.load()")
        newidx = self.indexer.load()
        # call queryResults
        qresults = self.indexer.queryResults(requestParams['text'], newidx)
        # perform lookup
        self.trace.log("Controller.Search", "calling lookup.documentLookup() for {} items".format(self.maxSearchResults))
       
        resultdocs = self.lookup.documentLookup(qresults, lookupdata, self.maxSearchResults)
        # resultdocs = self.lookup.documentLookup({}, self.maxSearchResults)
        # filter on location
        resultsbylocation = self.__filterbyLocation__(resultdocs, requestParams)
        resultsNotbylocation = self.__reduceResult__(resultdocs, resultsbylocation)

        requestResults = {
            "searchResults": sorted(resultsbylocation, key=self.__bySentiment__, reverse=True),
            "recommendations": sorted(resultsNotbylocation, key=self.__bySentiment__, reverse=True) 
        }

        return requestResults


    def load(self):
        self.trace.log("Controller.load", "calling lookup.load()")
        self.lookup.load()
        self.trace.log("Controller.load", "calling indexer.load()")
        self.indexer.load()

    # end public methods


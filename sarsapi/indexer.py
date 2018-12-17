import metapy
import pytoml
import json
import sys, os

class Indexer:

        def __init__(self, trace, settings):                
                self.trace = trace
                self.num_results = settings.maxSearchResults
                self.cfg = settings.cfg
                self.k1 = settings.bm25_K1
                self.b = settings.bm25_b
                self.k3 = settings.bm25_k3
                self.usejsonExtraction = settings.useJsonExtraction
                self.datasetKey = settings.datasetKey
                self.dataset = settings.dataset
       

        def load(self):
                cfgpath = os.path.abspath(self.cfg)                
                self.trace.log("Indexer.load", "Indexing from : {}".format(cfgpath))
                index = metapy.index.make_inverted_index(cfgpath)
                self.trace.log("Indexer.load", "Number of docs : {}".format(index.num_docs()))
                self.trace.log("Indexer.load", "Number of unique terms : {}".format(index.unique_terms()))
                self.trace.log("Indexer.load", "Average document length : {}".format(index.avg_doc_length()))
                self.trace.log("Indexer.load", "Number of total corpus terms : {}".format(index.total_corpus_terms()))
                self.trace.log("Indexer.load", "Indexing complete")
                return index
                

        def queryResults(self, searchtext, index):
                
                self.trace.log("Indexer.queryResults", "Instantiating ranker with k1 {}, b {}, k3 {}".format(self.k1, self.b, self.k3))
                ranker = metapy.index.OkapiBM25(k1=self.k1, b=self.b, k3=self.k3) 
                self.trace.log("Indexer.queryResults", "Instantiating query for text {}".format(searchtext))
                query = metapy.index.Document()
                query.content(searchtext) 
                self.trace.log("Indexer.queryResults", "Getting top {} result".format(self.num_results))
                top_results = ranker.score(index, query, num_results = self.num_results)
                self.trace.log("Indexer.queryResults", "Found results {}".format(len(top_results)))
                resultContents = []
                for num, (d_id, _) in enumerate(top_results):
                        content = index.metadata(d_id).get('content')                        
                        if content is not None:
                                if self.usejsonExtraction == True:
                                        doc = json.loads(content)                                        
                                        for docId in doc:
                                                resultItem = {}
                                                resultItem[self.datasetKey] = docId
                                                resultItem[self.dataset] = doc                                                
                                                resultContents.append(resultItem)
                                else:
                                        docId = content.split()[0]
                                        resultItem = {}
                                        resultItem[self.datasetKey] = docId 
                                        resultItem[self.dataset] = content 
                                        resultContents.append(resultItem)
                                        

                return resultContents

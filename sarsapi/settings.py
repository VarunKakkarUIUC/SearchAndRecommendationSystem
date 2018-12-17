

class Setting:

    def __init__(self):
        self.debugMode = False
        self.lookupFilePath = 'data/yelp_pennsylvania_business_recommendation_dataset.json'
        self.maxSearchResults = 50
        self.cfg = 'config.toml'
        self.datasetKey = 'business_id'
        self.dataset = 'topics'
        self.bm25_K1 = 1.2
        self.bm25_b = 0.75
        self.bm25_k3 = 500
        self.useJsonExtraction = True

import pandas as pd

class Extraction:
    def loadData(filename):
        # Load the data into the memory and ignore the rows with corrupt data.
        header = ['business_id','name','city','state','categories','userId','reviewId','stars','reviewText','date']
        with open(filename, mode='r', errors='ignore') as f:
            return pd.read_table(f, sep='\t', names=header, lineterminator='\n', low_memory=False)
        
    def extractReviewData(filename):
        reviewdataTable = Extraction.loadData(filename)
        
        # Filter the data to create index for just the review data
        onlyReviewData = reviewdataTable[["business_id", "reviewText", "stars"]]
        # filter out rows with null values
        onlyReviewData = onlyReviewData.dropna()
        # sort the data for all the reviews of the same business together and ignore filter that were written N years ago.
        return onlyReviewData.sort_values(by=['business_id'], ascending = True).groupby('business_id').filter(lambda x: len(x) >= 3)
    
    def extractIndividualReviewData(filename):
        reviewdataTable = Extraction.loadData(filename)
        
        # Filter the data to create index for just the review data
        onlyReviewData = reviewdataTable[["business_id", "reviewText", "name", "city"]]
        # filter out rows with null values
        onlyReviewData = onlyReviewData.dropna()
        # sort the data for all the reviews of the same business together and ignore filter that were written N years ago.
        return onlyReviewData.sort_values(by=['business_id'], ascending = True).groupby('business_id').filter(lambda x: len(x) >= 3)
    
    def getBusinessReview(filename):        
        sortedResult = Extraction.extractReviewData(filename)
        
        # dictionary of businessId and the reviews associated with the business
        resultDict = {}
        # Merge all the reviews for the business in order to feed into Topic Modelling
        business_id = ''
        reviews = ''
        for index, row in sortedResult.iterrows():
            business_id = row['business_id']
            reviews = row['reviewText']
            resultDict[business_id] = reviews  
        
        return resultDict
        
    def getBusinessReviews(filename):        
        sortedResult = Extraction.extractReviewData(filename)
        
        # dictionary of businessId and the reviews associated with the business
        resultDict = {}
        # Merge all the reviews for the business in order to feed into Topic Modelling
        business_id = ''
        reviews = ''
        for index, row in sortedResult.iterrows():
            #TODO: Add logic to filter the review that were written N years ago.
                if row['business_id'] != business_id:
                    if business_id == '':
                        reviews = row['reviewText'] + ' '
                    else:
                        resultDict[business_id] = reviews
                        reviews = ''
                        reviews = str(row['reviewText']) + ' '
                    business_id = row['business_id']
                else:
                    reviews = reviews  + ' ' + str(row['reviewText']) + ' '
        
        resultDict[business_id] = reviews  
        
        return resultDict
            
    if __name__ == '__main__':    
        reviewdataTable = loadData('yelp_pennsylvania_businesswithreview_dataset.txt')      
    
    
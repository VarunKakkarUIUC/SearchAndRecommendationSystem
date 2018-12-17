import extraction
import json
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def sentimentScorer(reviewText):
    sentiment_analyzer = SentimentIntensityAnalyzer()
    score = 0.0
    try:
        score = sentiment_analyzer.polarity_scores(reviewText)['compound']
    except AttributeError as err:
        score = 0.0
    return score

def getUserRating(userRating):
    rating = 0.0
    try:
        rating = float(userRating)
    except ValueError as err:
        rating = 0.0
    return rating
             
    #TODO: Take rating in account while calculating the polarity

def reviewPointer(reviewText, polarity):
    reviewScore = {}
    reviewScore[reviewText] =  polarity 
    return reviewScore
    
def ReviewSentiment(business_Reviews):        
    sentimentResult= open("yelpReviewSentimentsScore.txt","w+")
    
    # Initialize the variables
    reviewSentiment = {}
    business_id = ''
    reviews = []
    sumPolarity = 0.0
    sumUserRating = 0.0
    sentimentCount = 1
    
    # get the compound sentiment polarity related to the reviews for the business
    # ranges from -1 to 1 (1 being the best)
    for index, row in business_Reviews.iterrows():
        if row['reviewText'] is not None:
            polarity = sentimentScorer(row['reviewText'])
            userRating = getUserRating(row['stars'])
            if row['business_id'] != business_id:
                if business_id == '':
                    sumPolarity = polarity
                    sumUserRating = userRating
                    reviews.append(reviewPointer(str(row['reviewText']), str(polarity)))
                else:
                    averagePolarity = sumPolarity/sentimentCount
                    averageUserRating = sumUserRating/sentimentCount
                    
                    #Add the average weighted score
                    #reviews.append(reviewPointer("WeightedScore", str(averagePolarity)))
                    reviewSentiment['business_id'] = business_id
                    reviewSentiment['averagePolarity'] = averagePolarity
                    reviewSentiment['reviewCount'] = sentimentCount
                    reviewSentiment['averageUserRating'] = averageUserRating
                    sentimentResult.write(json.dumps(reviewSentiment))
                    sentimentResult.write('\n')
                    
                    # Start - Reinitialize the variables
                    reviews = []
                    sumPolarity = polarity
                    sumUserRating = userRating
                    sentimentCount = 1
                    # End - Reinitialize the variables
                    
                    reviews.append(reviewPointer(str(row['reviewText']), str(polarity)))
                business_id = row['business_id']
            else:
                sumPolarity = sumPolarity + polarity
                sumUserRating = sumUserRating + userRating
                sentimentCount = sentimentCount + 1
                reviews.append(reviewPointer(str(row['reviewText']), str(polarity)))
    
    averagePolarity = sumPolarity/sentimentCount
    averageUserRating = sumUserRating/sentimentCount
    
    #Add the average weighted score
    #reviews.append(reviewPointer("WeightedScore", str(averagePolarity)))
    reviewSentiment['business_id'] = business_id
    reviewSentiment['averagePolarity'] = averagePolarity
    reviewSentiment['reviewCount'] = sentimentCount
    reviewSentiment['averageUserRating'] = averageUserRating
    
    sentimentResult.write(json.dumps(reviewSentiment))
        
if __name__ == '__main__':    
    business_Reviews = extraction.Extraction.extractReviewData('yelp_pennsylvania_businesswithreview_dataset.txt')  
    
    ReviewSentiment(business_Reviews)

            
        
        
import pandas as pd
import json
import extraction

from gensim import corpora, models
import gensim

#spacy
import spacy
from spacy import displacy

#load model (TODO: Check the embedded version)
nlp = spacy.load('en_core_web_sm', disable = ['ner'])
# Getting the issue with [E088] 
nlp.max_length = 1500000
spacy_stopwords = spacy.lang.en.stop_words.STOP_WORDS

def StopWordRemoval(business_Review):
        # tokenization of all the reviews for a business
        reviews = business_Review            
        reviews_upt = nlp(reviews)
        
        review_tokens = [token.text.lower() for token in reviews_upt]
        
        # remove stop words and words with length < 3
        stopword_cleaned_tokens = [review_token for review_token in review_tokens if not review_token in spacy_stopwords]
        cleaned_tokens = [review_token for review_token in stopword_cleaned_tokens if len(review_token) > 2]
        #TODO: Lemmitization
        
        return cleaned_tokens 
    
def ReviewsCorpusData(business_Reviews):
    # tokenization and cleanup of all the reviews for the business
    businessIds = []
    allReviews = []
    corpusReviewTokens = []
    name = []
    city = []
    for index, row in business_Reviews.iterrows():
        tokens = StopWordRemoval(row['reviewText'])
        corpusReviewTokens.append(tokens) 
        businessIds.append(row['business_id'])
        allReviews.append(row['reviewText'])
        name.append(row['name'])
        city.append(row['city'])
        
    return pd.DataFrame({
        'business_Id': businessIds,
        'reviews': allReviews,
        'reviewTokens': corpusReviewTokens,
        'name':name,
        'city':city
        })
        
    
def GenerateLDA(reviews_token_dictionary, review_bow):                
    NUM_TOPICS = 3
    NUM_PASSES = 10
    ldamodel = gensim.models.ldamodel.LdaModel(review_bow, 
                                               num_topics = NUM_TOPICS, 
                                               id2word=reviews_token_dictionary, 
                                               passes=NUM_PASSES,
                                               per_word_topics=True,
                                               random_state=100,
                                               update_every=1,
                                               chunksize=100,
                                               alpha='auto',)
    #ldamodel.save('model6.gensim')
    return ldamodel

def GenerateTopicModel(input_reviewTokens):
    reviews_token_dictionary = corpora.Dictionary([input_reviewTokens])       
    # Filter very frequent and very infrequent words
    #reviews_token_dictionary.filter_extremes(no_below=20, no_above=0.1) 
    
    if bool(reviews_token_dictionary):
        #creating bag of words
        review_bow = [reviews_token_dictionary.doc2bow(text) for text in [input_reviewTokens]]
        
        #Train the model
        lda_model = GenerateLDA(reviews_token_dictionary, review_bow)
        
        # Print the Keyword in the topics
        topics_list = lda_model.show_topic(0)
        return ', '.join([w[0] for w in topics_list])


def MergeAndPrintAllTopicsForBusiness(business_topics): 
        topicsResult= open("./IndexFiles/business_topicModels.json","w+")
        
        business_topics.sort_values(by=['business_Id'], ascending = True).groupby('business_Id')               
        # dictionary of businessId, name, city  and the reviewTokens associated with the business
        topicsDictionary = {}
        # Merge all the review token alongwith city and name for the business in order to create inverted index
        business_id = ''
        topics = ''
        name = ''
        city = ''
        for index, row in business_topics.iterrows():
                if row['business_Id'] != business_id:
                    if business_id == '':
                        if row['Business_Topics'] != None:
                            topics = row['Business_Topics'] + ','
                    else:
                        topicsDictionary[business_id] = topics + name + ',' + city
                        topicsResult.write(json.dumps(topicsDictionary))
                        topicsResult.write('\n')
                        
                        # Reinitialize the variables
                        topicsDictionary = {}
                        topics = ''
                        if row['Business_Topics'] != None:
                            topics = str(row['Business_Topics']) + ','
                    business_id = row['business_Id']
                    city = row['city']
                    name = row['name']
                else:
                    topics = topics + str(row['Business_Topics']) + ','
        
        topicsDictionary[business_id] = topics + name + ',' + city 
        topicsResult.write(json.dumps(topicsDictionary))
    
if __name__ == '__main__':    
    business_Reviews_training_set = extraction.Extraction.extractIndividualReviewData('yelp_pennsylvania_businesswithreview_dataset.txt')
    
    # Generating the tokens for the reviews
    business_topics = ReviewsCorpusData(business_Reviews_training_set) 
    business_topics['Business_Topics'] = business_topics['reviewTokens'].apply(GenerateTopicModel)
    
    MergeAndPrintAllTopicsForBusiness(business_topics)    
    

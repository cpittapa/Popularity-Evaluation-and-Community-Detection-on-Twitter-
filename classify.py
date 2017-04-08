import json
import re
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import os
from collections import Counter


file_nm='data/Train_selenagomez.txt'
file_nm_test='data/Test_selenagomez.txt'


'''
AFINN part of the code is only used if the celebrity name is changed and to help to label to training data.

funtions used for this activity are:
classification(texts)
sentiment_calculation(words,text):

'''
afinn_file = open('AFINN-111.txt')
afinn = dict()
for line in afinn_file:
    parts = line.strip().split()
    if len(parts) == 2:
        afinn[parts[0]] = int(parts[1])
def classification(texts):
    cnt=0
    unique_tweets = []
    for t in texts:
        if (t not in unique_tweets):
            cnt += 1
            unique_tweets.append(t)
    print("Number of tweets that are not repeated", cnt)

    pos = 0
    neg = 0
    neutral=0
    try:
        os.remove("data/pos.txt")
        os.remove("data/neg.txt")
        os.remove("data/neutral.txt")
    except OSError:
        pass
    file1 = "data/pos.txt"
    p = open(file1, "a",encoding="utf8")
    file2 = "data/neg.txt"
    n = open(file2, "a",encoding="utf8")
    file3 = "data/neutral.txt"
    o = open(file3, "a",encoding="utf8")

    for line in unique_tweets:
        line_processed = tokenize(line)
        sen_score = sentiment_calculation(line_processed, line)
        if (sen_score > 0):
            p.write(line+'\n')
            pos += 1
        elif (sen_score < 0):
            n.write(line)
            n.write('\n')
            neg += 1
        else :
            neutral+=1
            o.write(line)
            o.write('\n')
    p.close()
    n.close()
    o.close()
    print(pos, neg,neutral)

def sentiment_calculation(words,text):
    score={}
    sentiment_score = 0
    for word in words:
        if(word in afinn):
            sentiment_score += afinn.get(word)
    score.append({'score': sentiment_score,'text': text})
    return sentiment_score




def read_tweets():
    tweets=[]
    texts=[]
    for line in open(file_nm_test,encoding="utf8"):
      try:
        tweets.append(json.loads(line))
      except:
        pass
    i=0
    for tweet in tweets:
        if('text'in tweet.keys()):
            texts.append(tweet['text'])
        i+=1
    return texts,i




def tokenize(text):
    text = text.lower()
    text = re.sub('http\S+', 'THIS_IS_A_URL', text)
    text = re.sub('@\S+', 'THIS_IS_A_MENTION', text)
    text = re.sub('#\S+', 'THIS_IS_A_HashTag', text)
    stop = stopwords.words('english')
    tokens = re.sub('\W+', ' ', text.lower()).split()
    tokens = [x for x in tokens if ((x not in stop) and len(x) > 2)]
    tokens=' '.join(x for x in tokens)
    return tokens.split()






'''
Maching learning part of sentimental analysis starts here.

Description:logistic_regress method will read the labelled texts and use them to create the vectorizer using countvectorizer.
The new tweets created are transformed into the using the vectorizer and then used to predict the unknown labels.

'''

def logistic_regress():
    print("\n For countvectorizer \n")
    twt = {}

    for line in open("data/pos.txt",encoding="utf8"):
        twt[line] = 1
    for line in open("data/neg.txt",encoding="utf8"):
        twt[line] = -1
    for line in open("data/neutral.txt",encoding="utf8"):
        twt[line] = 0
    test_set = []
    for line in open('data/Test_selenagomez.txt',encoding="utf8"):
        try:
            test_set.append(json.loads(line))
        except:
            pass
    texts = [tweet['text'] for tweet in test_set]
    vectorizer = CountVectorizer(min_df=1, ngram_range=(1, 1))
    X = vectorizer.fit_transform(twt.keys())
    y = [v for v in twt.values()]
    from sklearn.linear_model import LogisticRegression
    model = LogisticRegression()
    model.fit(X, y)
    X_test = vectorizer.transform(texts)
    res = model.predict(X_test)
    result = {}
    print("Model accuracy on traing set is :", model.score(X,y))
    vocab = np.array(vectorizer.get_feature_names())
    top_coefs(model, vocab)
    i = 0
    for t in texts:
        result[t] = res[i]
        i += 1
    return result

'''
Description:logistic_regress_tfidf method will read the labelled texts and use them to create the vectorizer using tfidfvectorizer.
The new tweets created are transformed into the using the vectorizer and then used to predict the unknown labels.

'''

def logistic_regress_tfidf():
    twt = {}
    print("\n For tfisdf-vectorizer \n")
    for line in open("data/pos.txt",encoding="utf8"):
        twt[line] = 1
    for line in open("data/neg.txt",encoding="utf8"):
        twt[line] = -1
    for line in open("data/neutral.txt",encoding="utf8"):
        twt[line] = 0
    test_set = []
    for line in open('data/Test_selenagomez.txt',encoding="utf8"):
        try:
            test_set.append(json.loads(line))
        except:
            pass
    texts = [tweet['text'] for tweet in test_set]
    vectorizer = TfidfVectorizer(min_df=1, ngram_range=(1, 1))
    X = vectorizer.fit_transform(twt.keys())
    y = [v for v in twt.values()]
    from sklearn.linear_model import LogisticRegression
    model = LogisticRegression()
    model.fit(X, y)
    X_test = vectorizer.transform(texts)
    res = model.predict(X_test)
    print("Model accuracy on traing set is :", model.score(X,y))
    i=0
    result={}

    vocab = np.array(vectorizer.get_feature_names())
    top_coefs(model,vocab)
    for t in texts:
        result[t]=res[i]
        i+=1
    return result


'''
Description : write_summary will take the result of results of the predicted tweets print the results.
Also write the results into a summary_classfication.txt
'''

def write_summary(res1,res2,count_tweets):
    cnts=Counter(res1.values())


    print("\n Using Logistic Regressing (Countvectorizer)")
    print("Number of positive tweets are :", cnts.get(1))
    print("Number of negative tweets are :", cnts.get(-1))
    print("Number of neutral tweets are :", cnts.get(0))

    file1 = "data/summary_classfication.txt"

    try:
        os.remove(file1)
    except OSError:
        pass
    f1= open(file1, "a",encoding="utf8")
    f1.write("\n\n CLASSIFICATION - SENTIMENTAL ANALYSIS  \n\n")
    f1.write("\n Number of tweets collected for training: 1263")
    f1.write("\n Number of tweets collected for testing:  "+str(count_tweets))
    f1.write("\n\n Using Logistic Regressing (Countvectorizer) \n")
    f1.write("\n Number of instances per class found: ")
    f1.write("\n Number of positive tweets are :" + str(cnts.get(1)))
    f1.write("\n Number of negative tweets are :"+ str(cnts.get(-1)))
    f1.write("\n Number of neutral tweets are :"+ str(cnts.get(0)))
    f1.write("\n\n One example from each class: \n\n")
    i = 0
    pos = False
    neu = False
    neg = False
    for t, v in res1.items():
        if (pos == False or neg == False or neu == False):
            if (v == 1 and pos == False):
                f1.write("\n Positive case :" + t)
                pos = True
            elif (v == 0 and neu == False):
                f1.write("\n Neutral case :" + t)
                neu = True
            elif (v == -1 and neg == False):
                f1.write("\n Negative case :" + t)
                neg = True

    print("\n Using Logistic Regressing (Tfidf vectorizer)")

    cnts = Counter(res2.values())
    print("Number of positive tweets are :"+ str(cnts.get(1)))
    print("Number of negative tweets are :"+ str(cnts.get(-1)))
    print("Number of neutral tweets are :"+ str(cnts.get(0)))

    f1.write("\n\n  Using Logistic Regressing (Tfidf vectorizer) \n\n ")
    f1.write("\n Number of instances per class found: ")
    f1.write("\n Number of positive tweets are :"+ str(cnts.get(1)))
    f1.write("\n Number of negative tweets are :"+ str(cnts.get(-1)))
    f1.write("\n Number of neutral tweets are :"+ str(cnts.get(0)))


    f1.write("\n\n One example from each class: \n\n" )
    pos = False
    neu = False
    neg = False
    for t, v in res2.items():
        if (pos == False or neg == False or neu == False):
            if (v == 1 and pos == False):
                f1.write("\n Positive case :" + t)
                pos = True
            elif (v == 0 and neu == False):
                f1.write("\n Neutral case :" + t)
                neu = True
            elif (v == -1 and neg == False):
                f1.write("\n Negative case :" + t)
                neg = True


def top_coefs(model,vocab):
    coef = model.coef_[2]
    top_coef_ind = np.argsort(coef)[::-1][:10]
    top_coef_terms = vocab[top_coef_ind]
    top_coef = coef[top_coef_ind]
    print('top weighted terms for positive class:')
    print([x for x in zip(top_coef_terms, top_coef)])
    coef = model.coef_[0]
    top_coef_ind = np.argsort(coef)[::-1][:10]
    top_coef_terms = vocab[top_coef_ind]
    top_coef = coef[top_coef_ind]
    print('top weighted terms for negative class:')
    print([x for x in zip(top_coef_terms, top_coef)])

'''
Main method
'''
if __name__ == '__main__':
    texts,count_tweets=read_tweets()
    result1=logistic_regress()
    result2=logistic_regress_tfidf()
    write_summary(result1,result2,count_tweets)

import csv
import re
import math
from positivewords import positivewords
from negativewords import negativewords

def extract_tweets(path,tweets):
    with open(path, newline='',encoding="utf-8") as csvfile:
         lines = (line.rstrip() for line in csvfile) 
         lines = list(line for line in lines if line)
         data = csv.DictReader(lines)
         for item in data:
             t=item['tweet']
             t = re.sub(r'https?:\/\/\S*', '', t, flags=re.MULTILINE)
             t= re.sub('\U0001F600-\U0001F64F','',t)
             t=t.lower()
             tweets.append(t)


def sentiment_analysis(tweets):
    List=[]
    for t in tweets:
            sentimentcount=0
            match=[]
            words = t.split()
            for word in words:
                if word in positivewords:
                    sentimentcount+=1
                    if word not in match:
                        match.append(word)
                elif word in negativewords:
                    sentimentcount+=-1
                    if word not in match:
                        match.append(word)
            if sentimentcount>0:
                result = "positive"
            elif sentimentcount==0:
                result = "neutral"
            else:
                result = "negative"
            newdata={"Tweet": t,"Match": match,"Polarity": result}
            List.append(newdata)
    
    header_list = ["Tweet","Match","Polarity"]
    with open("SentimentAnalysis.csv", 'w',encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header_list)
        writer.writeheader()
        for data in List:
            writer.writerow(data)
        print("Sentiment Analysis generated ")


def semantic_analysis(tweets,search_query,N):
    List=[]
    for query in search_query:
        df=0
        for tweet in tweets:
            words=tweet.split()
            if query in words:
                df+=1
        Ndf = N//df
        logNdf = math.log10(Ndf)
        newdata={"Search Query": query,"Document containing term(df)": df,"Total Documents(N)/ number of documents term appeared(df)": Ndf,"Log10(N/df)": logNdf}
        List.append(newdata)


    header_list = ["Search Query","Document containing term(df)","Total Documents(N)/ number of documents term appeared(df)","Log10(N/df)"]
    with open("SemanticAnalysis1.csv", 'w',encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header_list)
        writer.writeheader()
        for data in List:
            writer.writerow(data)
        print("SemanticAnalysis1 generated")

    List2=[]
    maxfrequency = 0
    article=0
    for tweet in tweets:
        article+=1
        Article = "Article"+str(article)
        words=tweet.split()
        totalwords = len(words)
        frequency = 0
        for word in words:
            if word== "cold":
                frequency+=1
        try:
            hf = frequency/totalwords
        except:
            hf=0
        if hf > maxfrequency:
            max= Article
            maxfrequency = hf
        newdata2={"Articles": Article,"Total Words": totalwords,"Frequency": frequency}
        List2.append(newdata2)

    print(max+"has highest frequency of cold")

    header_list = ["Articles","Total Words","Frequency"]
    with open("SemanticAnalysis2.csv", 'w',encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header_list)
        writer.writeheader()
        for data in List2:
            writer.writerow(data)
        print("SemanticAnalysis2 generated")



if __name__ == "__main__":
    tweets=[]
    for i in range(1,31):
        f="tweets"+str(i)+".csv"
        extract_tweets(f,tweets)
    sentiment_analysis(tweets)
    search_query=["flu","snow","cold"]
    N=len(tweets)
    semantic_analysis(tweets,search_query,N)

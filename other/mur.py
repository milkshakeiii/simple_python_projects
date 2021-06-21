import requests



number_positive = 0
number_negative = 0
number_neutral = 0
positive_probability = 0
negative_pobability = 0
neutral_probability = 0




def GetSentimentStrength(articleText):
    payload = {
        "text" : articleText
        }
    response = requests.post("http://text-processing.com/api/sentiment/", payload)
    return response.json()





article = ""
article_count = 0
keep_going = ""
while (keep_going != "n"):
    line = ""
    article = ""
    while (line != "end article"):
        line = input("a l: ")
        article = article + line
        
    article_count = article_count + 1
    sentiment = GetSentimentStrength(article)
    if (sentiment["label"] == "pos"):
        print ("---This article was with greatest probability postive")
        number_positive = number_positive + 1
    elif (sentiment["label"] == "neg"):
        print ("---This article was with greatest probability negative")
        number_negative = number_negative + 1
    else:
        print ("---This article was with greatest probability neutral")
        number_neutral = number_neutral + 1
    
    positive_probability = positive_probability + sentiment["probability"]["pos"]
    negative_pobability = negative_pobability + sentiment["probability"]["neg"]
    neutral_probability = neutral_probability + sentiment["probability"]["neutral"]


    keep_going = input ("should I keep going? (y/n)")




print("Here are the results for this candidate:")
print("average positive sentiment strength: ", positive_probability / article_count)
print("average negative sentiment strength: ", negative_pobability / article_count)
print("average neutral sentiment strength: ", neutral_probability / article_count)
print("number positive: ", number_positive)
print("number negative: ", number_negative)
print("number neutral: ", number_neutral)

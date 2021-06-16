# pyspark
# import argparse

from pyspark.sql import SparkSession
# from pyspark.ml.feature import Tokenizer, StopWordsRemover
# from pyspark.sql.functions import array_contains

# sentiment analysis
from textblob import TextBlob
from pyspark.sql.functions import udf

# standard modules
import pandas as pd



# function to run sentiment analysis
#def sentiment_analysis(input_loc, output_loc):

    # save output as csv
    #df_clean.write.csv(output_loc)


if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--input', type=str,
    #                     help='HDFS input', default='/twitter')
    # parser.add_argument('--output', type=str,
    #                     help='HDFS output', default='/output')
    # args = parser.parse_args()
    spark = SparkSession.builder.appName('SentimentAnalysis').getOrCreate()

    def apply_blob(sentence):
        temp = TextBlob(sentence).sentiment[0]
        if temp == 0.0:
            return 0.0 # Neutral
        elif temp >= 0.0:
            return 1.0 # Positive
        else:
            return 2.0 # Negative

    #def sentiment_analysis(**kwargs):
    # function to set up sentiment analysis logic

    # tweets = ['this is not so cool', 'this is actually very cool', 'this is the coolest thing I have ever seen']
    # df_raw = pd.DataFrame (tweets,columns=['tweets'])

    # read input
    #df_raw = spark.read.option('header', True).csv('s3://london-housing-webapp/twitter_output.csv')

    columns = ["tweets","users_count"]
    tweets = [("Java is sooo cool!", "20000"), ("Python is okay", "100000"), ("Scala is solid", "3000")]
    df_raw = spark.createDataFrame(tweets).toDF(*columns)

    # assign sentiment function as user defined function
    sentiment = udf(apply_blob)

    # apply sentiment function to all tweets
    df_clean = df_raw.withColumn('sentiment', sentiment(df_raw['tweets']))

    print(df_clean.sentiment[1])
    #sentiment_analysis(input_loc=args.input, output_loc=args.output)
    #sentiment_analysis()
    spark.stop()

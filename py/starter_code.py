"""
Please use Python version 3.7+
"""

import csv
from typing import List, Tuple
from collections import deque

AND = 1
OR = 2

class TweetIndex:
    # Starter code--please override
    def __init__(self):
        self.list_of_tweets = {}
        self.word_index = {}
        self.valid_tweet_timestamp_set = set()

    # Starter code--please override
    def create_word_index(self, tweet, timestamp) -> dict():
        for word in tweet.split(" "):
            word = word.lower()
            if word in self.word_index:
                self.word_index[word].add(timestamp)
            else:
                self.word_index[word] = {timestamp}


    def process_tweets(self, list_of_timestamps_and_tweets: List[Tuple[str, int]]) -> None:
        """
        process_tweets processes a list of tweets and initializes any data structures needed for
        searching over them.

        :param list_of_timestamps_and_tweets: A list of tuples consisting of a timestamp and a tweet.
        """
        for row in list_of_timestamps_and_tweets:
            timestamp = int(row[0])
            tweet = str(row[1])
            self.valid_tweet_timestamp_set.add(timestamp)
            self.list_of_tweets[timestamp] = tweet
            self.create_word_index(tweet, timestamp)

    def get_tweet_list(self, timestamps: list) -> List[Tuple[str, int]]:
        tweet_list = []
        for timestamp in timestamps:
            tweet = self.list_of_tweets[timestamp]
            tweet_list.append([tweet, timestamp])

        return tweet_list


    def evaluate_word(self, word: str, operator: int) -> None:
        if word in self.word_index:
            if operator == AND:
                self.valid_tweet_timestamp_set = self.valid_tweet_timestamp_set.intersection(self.word_index[word])
            elif operator == OR:
                self.valid_tweet_timestamp_set = self.valid_tweet_timestamp_set.union(self.word_index[word])

    # Starter code--please override
    def search(self, query: str) -> List[Tuple[str, int]]:
        """
        NOTE: Please update this docstring to reflect the updated specification of your search function

        search looks for the most recent tweet (highest timestamp) that contains all words in query.

        :param query: the given query string
        :return: a list of tuples of the form (tweet text, tweet timestamp), ordered by highest timestamp tweets first. 
        If no such tweet exists, returns empty list.
        """
        q = deque()
        for word in query.split(" "):
            q.append(word)

        operators = ['&', '|']
        while q:
            curr_word = q.popleft()
            if curr_word not in operators:
                self.evaluate_word(curr_word, AND)

        tweet_list = self.get_tweet_list(list(self.valid_tweet_timestamp_set))
        return tweet_list

        """
        for tweet, timestamp in self.list_of_tweets:
            words_in_tweet = tweet.split(" ")
            tweet_contains_query = True
            for word in list_of_words:
                if word not in words_in_tweet:
                    tweet_contains_query = False
                    break
            if tweet_contains_query and timestamp > result_timestamp:
                result_tweet, result_timestamp = tweet, timestamp
        return [(result_tweet, result_timestamp)] if result_timestamp != -1 else []
        """
        

if __name__ == "__main__":
    # A full list of tweets is available in data/tweets.csv for your use.
    tweet_csv_filename = "../data/small.csv"
    list_of_tweets = []
    with open(tweet_csv_filename, "r") as f:
        csv_reader = csv.reader(f, delimiter=",")
        for i, row in enumerate(csv_reader):
            if i == 0:
                # header
                continue
            timestamp = int(row[0])
            tweet = str(row[1])
            list_of_tweets.append((timestamp, tweet))

    ti = TweetIndex()
    ti.process_tweets(list_of_tweets)
    print(ti.search('hello neeva'))
    #print(ti.search('hello & neeva'))
    #print(ti.search("hello"))
    #print(ti.search("hello me"))
    #print(ti.search("hello bye"))
    #assert ti.search("hello") == ('hello this is also neeva', 15)
    #assert ti.search("hello me") == ('hello not me', 14)
    #assert ti.search("hello bye") == ('hello bye', 3)
    #assert ti.search("hello this bob") == ('hello neeva this is bob', 11)
    #assert ti.search("notinanytweets") == ('', -1)
    #print("Success!")

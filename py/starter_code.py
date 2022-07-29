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

    def eval_word(self, word) -> set():
        word_set = set()
        if word in self.word_index:
            word_set.update(self.word_index[word])
        return word_set
            
    def eval_expression(self, queries_queue: deque, curr_word: str) -> set():
        operators = {'&': AND, '|': OR}
        valid_sets = []
        operator = 0

        if curr_word[0] == '(':
            valid_sets.append(self.eval_expression(queries_queue, curr_word[1:]))
        else:
            valid_sets.append(self.eval_word(curr_word))

        while queries_queue:
            close_parenthesis_flag = 0
            curr_word = queries_queue.popleft()
            if curr_word[0] == '(':
                valid_sets.append(self.eval_expression(queries_queue, curr_word[1:]))
            elif curr_word[-1] == ')':
                valid_sets.append(self.eval_word(curr_word[:-1]))
                close_parenthesis_flag = 1
            elif curr_word not in operators:
                valid_sets.append(self.eval_word(curr_word))
            elif curr_word in operators:
                operator = operators[curr_word]
            else:
                print("error lol")

            if len(valid_sets) > 1:
                if operator == AND:
                    new_valid_set = valid_sets.pop().intersection(valid_sets.pop())
                    valid_sets.append(new_valid_set)
                elif operator == OR:
                    new_valid_set = valid_sets.pop().union(valid_sets.pop())
                    valid_sets.append(new_valid_set)
                
                if close_parenthesis_flag:
                    break

        
        if len(valid_sets) == 1:
            return valid_sets.pop()
        else:
            print(f"error at the end: {valid_sets}")
            return None
                

    # Starter code--please override
    def search(self, query: str) -> List[Tuple[str, int]]:
        """
        NOTE: Please update this docstring to reflect the updated specification of your search function

        search looks for the most recent tweet (highest timestamp) that contains all words in query.

        :param query: the given query string
        :return: a list of tuples of the form (tweet text, tweet timestamp), ordered by highest timestamp tweets first. 
        If no such tweet exists, returns empty list.
        """
        queries_queue = deque()
        for word in query.split(" "):
            queries_queue.append(word)

        tweet_set = self.eval_expression(queries_queue, queries_queue.popleft())
        return self.get_tweet_list(list(tweet_set))

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
    print(ti.search('hello & (google | neeva) & (bob | jack)'))
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

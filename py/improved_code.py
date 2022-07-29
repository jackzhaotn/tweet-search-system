"""
Please use Python version 3.7+
"""

import time
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
        self.initial_tweet_id_set = set()

    # Starter code--please override
    def create_word_index(self, tweet, timestamp) -> dict():
        """
        create_word_index: creates a hashmap data structure that acts like a word index. Creates a dictionary with 
        word->tweet(timestamp) associations

        :param tweet, timestamp: tweet text string and its timestamp
        """
        for word in tweet.split(" "):
            word = word.lower()
            if word in self.word_index:
                self.word_index[word].add(timestamp)
            else:
                self.word_index[word] = {timestamp}


    def process_tweets(self, list_of_timestamps_and_tweets: List[Tuple[str, int]]) -> None:
        """
        process_tweets processes a list of tweets and initializes a tweet and word index (hashmaps) that support word->tweet timestamps 
        and timestamp->tweet lookups, respectively 

        :param list_of_timestamps_and_tweets: A list of tuples consisting of a timestamp and a tweet.
        """
        for row in list_of_timestamps_and_tweets:
            timestamp = int(row[0])
            tweet = str(row[1])
            self.initial_tweet_id_set.add(timestamp)
            self.list_of_tweets[timestamp] = tweet
            self.create_word_index(tweet, timestamp)

    def get_tweet_list(self, timestamps: list) -> List[Tuple[str, int]]:
        """
        get_tweet_list gets a list of tweet text based on their timestamp and returns them in the format of:
        [(tweet, timestamp), ..., (tweet, timestamp)]

        :param timestamps: list of tweet timestamps
        :return: a list of tuples of tweet and timestamp
        """
        tweet_list = []
        timestamps.sort(reverse=True)
        for timestamp in timestamps[0:5]: #returns the 5 most recent tweets in in the list
            tweet = self.list_of_tweets[timestamp]
            tweet_list.append((tweet, timestamp))

        return tweet_list

    def eval_word(self, word) -> set():
        """
        eval_word evaluates a query word by looking it up in the word index. The function maintains a new set that is updated to the
        correlating set of valid tweets (timestamps) that satisfy the individual word query. This function also handles ! operator

        :param word: the query word
        :return: set of valid tweets (timestamps) that satisify the word
        """
        word_set = set()
        word = word.lower() #handles case insensentivity 
        if word in self.word_index:
            word_set.update(self.word_index[word])
        elif word[0] == '!':
            word = word[1:]
            if word in self.word_index:
                word_set.update(self.initial_tweet_id_set.difference(self.word_index[word])) 
            else:
                word_set.update(self.initial_tweet_id_set)
        return word_set
            
    def eval_expression(self, queries_queue: deque, curr_word: str) -> set():
        """
        eval_expression evaluates a query expression by parsing each query element and further evaluates each element based on its 
        classification of operand or operator. This class also maintains a stack of valid tweets (timestamps) after each query
        element evaluation. This function can also handles parenthesis groups by treating them like individual expression, and evaluates
        them recursively

        :param queries_queue: deque of all query elements in FIFO order
        :return: the final set of valid tweets (timestamps) that satisify the given expression
        """
        operators = {'&': AND, '|': OR}
        valid_sets = []
        operator = 0

        if curr_word[0] == '(': #start of parenthesis group, start recursion
            valid_sets.append(self.eval_expression(queries_queue, curr_word[1:]))
        else:
            valid_sets.append(self.eval_word(curr_word))

        while queries_queue:
            close_parenthesis_flag = 0
            curr_word = queries_queue.popleft()
            if curr_word[0] == '(':
                valid_sets.append(self.eval_expression(queries_queue, curr_word[1:]))
            elif curr_word[-1] == ')': #end of parenthesis group, enable clost flag
                while curr_word[-1] == ')':
                    curr_word = curr_word[:-1]
                valid_sets.append(self.eval_word(curr_word))
                close_parenthesis_flag = 1
            elif curr_word not in operators: #query operands
                valid_sets.append(self.eval_word(curr_word))
            elif curr_word in operators: #query operators
                operator = operators[curr_word]
            else:
                print("Error: invalid query element")

            if len(valid_sets) > 1: #once the stack more than one , we can apply the previous operator to those (two) valid sets
                if operator == AND:
                    new_valid_set = valid_sets.pop().intersection(valid_sets.pop())
                    valid_sets.append(new_valid_set)
                elif operator == OR:
                    new_valid_set = valid_sets.pop().union(valid_sets.pop())
                    valid_sets.append(new_valid_set)
                
                if close_parenthesis_flag: #break recursion here
                    break 

        
        if len(valid_sets) == 1: #one valid set should be left after all query elements are evaluated
            return valid_sets.pop()
        else:
            return None
                

    def search(self, query: str) -> List[Tuple[str, int]]:
        """
        search looks for the 5 most recent tweet (highest timestamp) that satisfies the query elements

        :param query: the given query string
        :return: a list of tuples of the form (tweet text, tweet timestamp), ordered by highest timestamp tweets first. 
        If no such tweet exists, returns [('', -1)].
        """
        #creates a queue for all query elements, FIFO order
        queries_queue = deque()
        for word in query.split(" "): 
            queries_queue.append(word)

        tweet_set = self.eval_expression(queries_queue, queries_queue.popleft())
        tweet_list = self.get_tweet_list(list(tweet_set))
        if tweet_list:
            return tweet_list
        else: #no valid tweet that satisfies query
            return [('', -1)]


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

    start = time.time()
    print(ti.search("neeva"))
    print(ti.search("hello & (me | neeva)"))
    print(ti.search("hello & (!me | neeva)"))
    print(ti.search("neeva & (jack | (hello & bob))"))
    print(ti.search("neeva & (hi | (jack & bob))"))
    print(ti.search("neeva & (hello & (jack | bob))"))
    print(ti.search("neeva & (hello & (bob | jack))"))
    print(ti.search("hello & this & !bob"))
    print(ti.search("bob | bye | me"))
    print(ti.search("bob | bye | me | stuff"))
    print(ti.search("notinanytweets"))
    print(ti.search("!notinanytweets"))
    print(ti.search("neeva & worl"))

    end = time.time()

    print(f"Success! Completed in {end-start}")

    
    #print("Success!")

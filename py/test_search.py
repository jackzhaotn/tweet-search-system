import unittest
import time
import csv
from improved_code import TweetIndex
from starter_code import TweetIndexStarter

class TestSearch(unittest.TestCase):

    def test_1_speed_large_dataset(self):
        tweet_csv_filename = "../data/tweets.csv"
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

        ti_starter = TweetIndexStarter()
        ti_starter.process_tweets(list_of_tweets)

        print("---Starting tweet searches on large dataset---")
        start = time.time()
        ti.search("neeva")
        ti.search("neeva & me")
        ti.search("neeva & one")
        ti.search("neeva & one & me")
        ti.search("notinanytweets")
        end = time.time()
        ti_time = end-start

        start = time.time()
        ti_starter.search("neeva")
        ti_starter.search("neeva me")
        ti_starter.search("neeva one")
        ti_starter.search("neeva one me")
        ti_starter.search("notinanytweets")
        end = time.time()
        ti_starter_time = end-start
        print(f"Starter search time: {ti_starter_time} vs. improved search time{ti_time}")

        if ti_time < ti_starter_time:
            print(f"Improved Noovi TI search is {ti_starter_time/ti_time} times faster than starter Noovi TI search!")
        else:
            print(f"Starter Noovi TI search is {ti_time/ti_starter_time} times faster than improved Noovi TI search :(")

    def test_2_basic_searches(self):
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
        print(f"\n---Starting basic test cases---")
        assert ti.search("neeva") == [('hello this is also neeva', 15), ('hello neeva this is bob', 11), ('hello neeva this is neeva', 10), ('neeva', 7), ('hello neeva me', 5)]
        assert ti.search("nEeVa") == ti.search("neeva")
        assert ti.search("hello & me") == [('hello not me', 14), ('hello me', 13), ('hello this is me', 6), ('hello neeva me', 5)]
        assert ti.search("hello & bye") == [('hello bye', 3)]
        assert ti.search("hello & this & bob") == [('hello neeva this is bob', 11)]
        assert ti.search("notinanytweets") == [('', -1)]
        print(f"Success! Basic search test cases passed!")

        


    def test_3_advanced_searches(self):
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

        print(f"\n---Starting advanced test cases---")
        assert ti.search("neeva") == [('hello this is also neeva', 15), ('hello neeva this is bob', 11), ('hello neeva this is neeva', 10), ('neeva', 7), ('hello neeva me', 5)]
        assert ti.search("hello & (me | neeva)") == [('hello this is also neeva', 15), ('hello not me', 14), ('hello me', 13), ('hello neeva this is bob', 11), ('hello neeva this is neeva', 10)]
        assert ti.search("hello & (!me | neeva)") == [('hello this is also neeva', 15), ('hello stuff', 12), ('hello neeva this is bob', 11), ('hello neeva this is neeva', 10), ('hello hello', 9)]
        assert ti.search("neeva & (jack | (hello & bob))") == [('hello neeva this is bob', 11)]
        assert ti.search("neeva & (hi | (jack & bob))") == [('', -1)]
        assert ti.search("neeva & (hello & (jack | bob))") == [('hello neeva this is bob', 11)]
        assert ti.search("neeva & (hello & (bob | jack))") == ti.search("neeva & (hello & (jack | bob))")
        assert ti.search("hello & this & !bob") == [('hello this is also neeva', 15), ('hello neeva this is neeva', 10), ('hello this is me', 6), ('hello this is neeva', 4)]
        assert ti.search("bob | bye | me") == [('hello not me', 14), ('hello me', 13), ('hello neeva this is bob', 11), ('hello this is me', 6), ('hello neeva me', 5)]
        assert ti.search("bob | bye | me | stuff") == [('hello not me', 14), ('hello me', 13), ('hello stuff', 12), ('hello neeva this is bob', 11), ('hello this is me', 6)]
        assert ti.search("notinanytweets") == [('', -1)]
        assert ti.search("!notinanytweets") == [('hello this is also neeva', 15), ('hello not me', 14), ('hello me', 13), ('hello stuff', 12), ('hello neeva this is bob', 11)]
        assert ti.search("neeva & worl") == [('', -1)]

        print(f"Success! Advanced search test cases passed!")



if __name__ == '__main__':
    unittest.main()

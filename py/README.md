# [Backend Project] Searching Tweets

## TweetIndex 
- Run with `$ python3 improved_code.py`
- Update main in improved_code with your own data tweet dataset and search query
    - `process_tweets()` processes a csv file of timestamps and tweets
    - `search()` takes in a query string and searches for the 5 most recent tweets that satisfies the query
- Run testing script with `$ python3 test_search.py`

## Approach to the problem
How do we improve the speed when searching in a large dataset?
- I approached this first problem by thinking about that time limiting factor when searching through large datasets. Each query word is evaluated against every tweet in the dataset. This is the bottleneck when the size of the dataset increases. Iterating through every word in every tweet to match every query word is redundant, so I started thinking about useful data structures. A hashmap (dictionary) seemed ideal because we can iterate through every word in the dataset once and store those words as keys with their corresponding tweets (timestamps) as a set of values. This way, we can match query words with a simple lookup instead of iterating through the entire dataset again.

How do we return the top 5 most recent tweets instead of just the most recent?
- Well this objective is inheriently, we just maintain a list of the 5 most recent tweets instead of just a single value, probably with a priority queue.
- However, thinking back to my word index data structure approach, I realized we can just maintain a set of valid tweets after each logical operator. Because this method already cuts down on the dataset iteration to 1, we can just maintain the entire valid set without any significant tradeoff to speed. After all queries are finished, we can simply update the set by sorting and taking the top 5 greatest values.

How do we implement logical operators like '&', '|', '!', and '()'?
- I approached this by thinking about how we can differientate between operands (the query words) and the operators. And how can we maintain the order since parenthesis group are involved now. I came to the conclusion that the query elements can be evaluated in order, FIFO, and parenthesis groups can be evaluated separately. With this approach, I knew to use a queue (deque) to maintain the query elements in order and then I knew we can somehow recursively evaluate parenthesis groups. With this method, we just evaluate the elements in order by parsing and classify the queries by operands and operators, and perform operations after two clauses (either singular word or parenthesis group) have been evaluated. 
- Because I approached the problem by maintaining a set of valid tweets, I realized that we can just use Set operations to perform the logical operations. '&' is equivalent to intersection of two sets. '|' is equivalent to the union of two sets. '!x' is the set difference of the whole set and x set.

## Considerations
# Design Decisions
Instead of matching word to tweet, we can view this problem in terms of sets. We can maintain sets of tweets (by their timestamps) that relate to each word. In addition, we maintain a set of valid tweets that still satisifies the queries as we perform the logical operations. This way, we can also perform logical operations in terms of set operations. This is also efficient because after each operation, the size of the valid tweet sets is always decreasing (or stays the same).

# Time complexity comparisons
Starter code:
- `process_tweets()`: for N tweets, O(N)
- `search()`: for N tweets, Q query words, O(NQ)

Improved code:
- `process_tweets()`: for N tweets, O(N) for original indexing + O(N) for word indexing = overall O(N)
- `search()`: for Q query words, O(Q) for query evaluation * O(1) for word index lookup for each query = overall O(Q)

# Tradeoffs
By creating a word index (huge hashmap), we are sacrificing a lot of memory for speed. This speed increase is very significant though, we go from O(NQ) to O(Q). This is especially useful with large datasets and N. 

# Assumptions
We are assuming that timestamps will stay globally unique, every query is in valid form in terms of spacing, corect 'operand operator operand' format, and valid parenthesis grouping.


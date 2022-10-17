# S&P 500 Ranking/Trading
A very simple example of ranking and buying equities in the S&amp;P 500.

1. Scrapes all symbols in S&P 500.
2. Retrieves the historical data for each symbol.
3. Scores each symbol based on an algorithm that uses the historical data. In this case, it is the prebuilt Linear Regression model in Sci-Kit Learn.
4. Adds all scores to a pandas dataframe.
5. Sorts the dataframe by score in descending order.
6. Executes buy orders for the stocks with the 50 highest scores.

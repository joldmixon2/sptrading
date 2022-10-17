from Features.Features import getData, rankPortfolio, getSpSymbols, buyOrder

symbols = getSpSymbols().table
data = getData(symbols).table
ranks = rankPortfolio(data).table
symbols = ranks['symbol']

for symbol in symbols[:50]:
    buyOrder(symbol)
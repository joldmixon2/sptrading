from Features import getData, rankPortfolio, getSpSymbols, trade, stop
import datetime
import schedule
import time as tt


def start():
    symbols = getSpSymbols().table
    data = getData(symbols).table
    ranks = rankPortfolio(data).table
    ranks = ranks[:50]
    for symbol,score in zip(ranks['symbol'],ranks['scores']):            
        trade(symbol,score)

while True:
    now = datetime.datetime.now()
    time = (str(now.hour) + ':' + str(now.minute))
    if time == '9:24':
        start()
    elif time == '15:55':
        stop()
    else:
        print(str(time)+':'+str(now.second))
        tt.sleep(1)

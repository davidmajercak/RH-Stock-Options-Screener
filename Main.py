import robin_stocks as rh
import matplotlib.pyplot as plt
import datetime as dt

username = ""; #Put your username here
password = ""; #Put your password here
rh.login(username, password);

# my_stocks = rh.build_holdings()
# for key, value in my_stocks.items():
#     print(key, value)

# stockList = ['F', 'GE', 'AAL', 'DAL', 'SNAP', 'PLUG']
stockList = ['KR']
expirationDates = ['2020-07-17']
maxAdjustedMarkPrice = .30  # .25 = $25 price per 100 (only less than or equal to will be shown)
maxChangeNeededPercent = 100  # 50 = 50% increase up or down needed for stock to reach strike price
minimumVolume = 20  # minimum volume needed
minimumOpenInterest = 10
minimumVolumePlusOpenInterest = minimumVolume + minimumOpenInterest
historicalDays = 35  # number of days to show historical data (max 365)
for stock in stockList:

    stockPrice = rh.stocks.get_latest_price(stock)

    for date in expirationDates:
        print('stock price -', stockPrice, ' symbol - ', stock)
        print('DATE - ', date)
        optionData = rh.find_options_for_list_of_stocks_by_expiration_date(stock, date,
                                                                           optionType='both')
        for item in optionData:
            index = 0
            if (float(item['volume']) + float(item['open_interest'])) >= minimumVolumePlusOpenInterest:
                changeInCost = float(item['adjusted_mark_price']) - float(item['previous_close_price'])
                changeInCostPercent = -100 + float(item['adjusted_mark_price']) / float(item['previous_close_price']) * 100
                changeNeeded = (float(item['break_even_price']) - float(stockPrice[index]))
                changeNeededPercent = changeNeeded / float(stockPrice[index]) * 100
                # intrinsicValue = float(item['strike_price']) - stockPrice
                # not doing anything with this yet
                # maybe have extrinsic value as well
                # if changeInCost >= .01 and (changeInCostPercent > .1 or changeInCostPercent < 0):
                if float(item['adjusted_mark_price']) <= maxAdjustedMarkPrice \
                        and abs(changeNeededPercent) <= maxChangeNeededPercent:
                    if item['delta'] is not None:
                        delta = round(float(item['delta']), 3)
                    else:
                        delta = 'none'
                    if item['theta'] is not None:
                        theta = round(float(item['theta']), 3)
                    else:
                        theta = 'none'
                    if item['vega'] is not None:
                        vega = round(float(item['vega']), 3)
                    else:
                        vega = 'none'

                    if item['implied_volatility'] is not None:
                        impliedVolatility = round(float(item['implied_volatility']) * 100, 2)
                        impliedVolatility = str(impliedVolatility) + '%'
                    else:
                        impliedVolatility = 'none'
                    if item['high_price'] is not None:
                        highPrice = round(float(item['high_price']), 3)
                    else:
                        highPrice = 'none'
                    if item['low_price'] is not None:
                        lowPrice = round(float(item['low_price']), 3)
                    else:
                        lowPrice = 'none'

                    adjustedMarkPrice = str(round(float(item['adjusted_mark_price']), 3))

                    print(stock.upper(), round(float(item['strike_price']), 3), item['type'].upper(),
                          ' adjusted.. $', adjustedMarkPrice,
                          ' exp.. ', item['expiration_date'],
                          ' \n\tdelta.. ', delta,
                          ' theta.. ', theta,
                          ' vega.. ', vega,
                          ' \n\tbid.. $', round(float(item['bid_price']), 3),
                          ' ask.. $', round(float(item['ask_price']), 3),
                          ' adjusted.. $', round(float(item['adjusted_mark_price']), 3),
                          ' break even.. $', round(float(item['break_even_price']), 3),
                          ' current.. $', round(float(stockPrice[0])),
                          ' change needed.. $', round(changeNeeded, 3),
                          ' % change needed.. ', round(changeNeededPercent, 3), "%",
                          ' \n\t\tprevious close.. $', round(float(item['previous_close_price']), 3),
                          ' change.. $', round(changeInCost, 3),
                          ' percent change.. ', round(changeInCostPercent, 3), "%"
                                                                               ' \n\t\t\timplied volatility.. ',
                          impliedVolatility,
                          ' volume.. ', item['volume'],
                          ' open interest.. ', item['open_interest'],
                          ' \n\t\t\thigh price.. ', highPrice,
                          ' low price.. ', lowPrice,
                          )

                    historicalData = rh.get_option_historicals(stock, date, item['strike_price'], item['type'], 'year')
                    dates = []
                    closingPrices = []
                    openPrices = []

                    for thing in historicalData['data_points']:
                        dates.append(thing['begins_at'])
                        closingPrices.append(float(thing['close_price']))
                        openPrices.append(float(thing['open_price']))


                    # Getting data to graph
                    dates = dates[-historicalDays:]
                    closingPrices = closingPrices[-historicalDays:]
                    openPrices = openPrices[-historicalDays:]
                    #

                    # change the dates into a format that matplotlib can recognize.
                    x = [dt.datetime.strptime(d, '%Y-%m-%dT%H:%M:%SZ') for d in dates]

                    strikePrice = str(round(float(item['strike_price']), 3))
                    # plots the data.

                    plt.plot(x, openPrices, '.b-')
                    plt.plot(x, closingPrices, '.r-')
                    plotTitle = (stock + " " + strikePrice + " " + item['type'].upper() + " " + "adj " +
                                 adjustedMarkPrice + " cur " + str(round(float(stockPrice[index]), 3)) + " "
                                 + str(date) + " over last " + str(historicalDays) + " days")
                    plt.title(plotTitle)
                    plt.xlabel("Dates")
                    plt.ylabel("Price")
                    plt.show()
                    print('\n')
            index = index + 1

"""
#!!! fill out the specific option information
strike = "1"
date = "2020-05-08"
stock = "ACB"
optionType = "call" #or "put"
#!!!

instrument_Data = rh.get_option_instrument_data(stock,date,strike,optionType)
market_Data = rh.get_option_market_data(stock,date,strike,optionType)

for key, value in instrument_Data.items():
    print("key: {:<25} value: {}".format(key, value))

for key, value in market_Data.items():
    print("key: {:<25} value: {}".format(key, value))
"""

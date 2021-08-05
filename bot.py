import pandas as pd


def bot_answer(stock_code):
	try:
		data = pd.read_csv("https://stooq.com/q/l/?s={}&f=sd2t2ohlcv&h&e=csv".format(stock_code))
		stock_name = data['Symbol'][0]
		stock_price = float(data['Close'][0])
		if stock_price:
			bot_message = "{} quote is ${} per share".format(stock_name, stock_price)
			return bot_message
	except:
		return "Stock does not found."
		
if __name__ == '__main__':
	stock_code = 'AAPL.US'
	print(bot_answer(stock_code))

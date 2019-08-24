# Import libraries
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import math

# Set the URL you want to webscrape from
url = 'https://www.nasdaq.com/symbol/real-time'
available_fund = 10000
#stores: {stock_name: (total_shares, average_price_per_share)}
# my_stocks = {'ZM': [10, 94], 'BABA': [10, 175]}

my_stocks = {}
# menu view
def show_menu ():
  menu = ['1.Check current performance', '2.Buy stock', '3.Sell stock', '4.Get current price of stock']
  print('Menu')
  for i in menu:
    print(i)
  user_option = False
  while user_option != '1' and user_option != '2' and user_option != '3' and user_option != '4':
    user_option = input('Please choose 1-4 from the menu: ')
  if user_option == '1':
    check_current_performance()
  elif user_option == '2':
    buy_stock()
  elif user_option == '3':
    sell_stock()
  else:
    get_current_stock_price(my_stocks)
  user_input = input('Press 5 to see menu ')
  if user_input == '5':
    show_menu()
  else:
    print('Thanks for using the app! ')
    
#option 1, check current performance
def check_current_performance ():
  #total value: calculate total price of stocks at hand + available_fund
  total_price = 0
  global available_fund 
  for key in my_stocks:
    stock_shares = my_stocks[key][0]
    print('***************************')
    print('Here is your stock list: ')
    # try: 
    stock_current_price = get_stock_price(url, key)
    stock_current_price = float(stock_current_price.replace('$', ''))
    total_price += int(stock_shares) * stock_current_price
    print(key + ': ' + str(stock_shares) + ' shares ' + 'Average Cost: ' + str(my_stocks[key][1]) + ' Current Price: $' +str(stock_current_price))
    # except:
    #   print('Something goes wrong ')
    #   print('stock_current_price', stock_current_price)
    #   return
  #total cost is the original fund: $10,000
  #total value - total cost = performance
  print('***************************')
  performance = round((total_price + float(available_fund)) - 10000, 2)
  available_fund = round(float(available_fund),2)
  if performance > 0:
    print('So far, you gained $' + str(performance))
    
  elif performance == 0:
    print('So far, you\'re break even! ')
  else: 
    performance = - performance
    print('So far, you lost $' + str(performance) + '! ')
  print('Your available fund is $' + str(available_fund))
#option 4, get current prices of your stocks
def get_current_stock_price(my_stocks):
  my_stock_performce = {}
  if len(my_stocks) == 0:
    print('You don\'t have any stocks ')
  else:
    for i in my_stocks:
      stock_symbol = i
      stock_price = get_stock_price (url, stock_symbol)
      # time.sleep(1)
      print(i + ': ' + str(stock_price))
      my_stock_performce.update({i: stock_price})
  return my_stock_performce
# prompt the user to enter the stock symbol
def enter_symbol():
  stock_symbol = input("Please enter stock symbol: ")
  return stock_symbol

# Connect to the URL to get the real time price of the stock
def get_stock_price (url, stock_symbol):
  new_url = url.split('/')
  new_url.insert(4,stock_symbol.upper())
  new_url = '/'.join(new_url)
  try:
    response = requests.get(new_url)
  # Parse HTML and save to BeautifulSoup object¶
    soup = BeautifulSoup(response.text, "html.parser")
    stock_price = soup.find (id = "qwidget_lastsale").getText()
    return stock_price
  except:
    print ('The stock symbol you entered is not found. ')
    return False
# ask the user to enter shares
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def enter_shares ():
  shares = input('How many shares? ')
  try:
    val = int(shares)
  except ValueError:
    print("That's not a number!")
    return enter_shares()
  return str(val)
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# calculate the total price
def calculate_price (stock_price, shares):
  if stock_price:
    stock_price = stock_price.replace('$', '')
  total_price = float(stock_price) * int(shares)
  # print only the first 2 digits after the point, total_price is str
  total_price = ('%.2f' % total_price)
  return total_price

# check the available fund
# compare the cost and the available fund
#check if the shares entered is within the limit
def check_buying_power (stock_cost):
  if (float(available_fund) < float(stock_cost)):
    shortage = float(stock_cost) - float(available_fund)
    print('Sorry, your are $' + str(shortage) + ' short!' )
    return False
  else:
    return True
# Condition 1: buying power is True
  # ask the user to confirm
  # if yes, submit the order; if not, show menu view

# ask the user to confirm 
def ask_to_confirm (buy_or_sell):
  confirm = input('Do you still want to ' + buy_or_sell + '? Yes or No? ')
  if confirm == 'y' or confirm == 'Y' or confirm == 'yes' or confirm == 'YES':
    return (buy_or_sell, True) 
  elif confirm == 'n' or confirm == 'N' or confirm == 'no' or confirm == 'NO':
    return (buy_or_sell, False)
  else: 
    return ask_to_confirm (buy_or_sell)

def place_order_for_buy (total_price, stock_shares, stock_price, stock_symbol):
  global available_fund
  available_fund = float(available_fund) - float(total_price)
  available_fund = ('%.2f' % available_fund)
  # check to see if the stock already exists:
  #if yes, push to the array as a new entry
  if stock_symbol.upper() in my_stocks:
    # calculate total_shares, ave_price
    for i in my_stocks:
      each_stock_shares = my_stocks[i][0] 
      each_stock_ave_price = my_stocks[i][1]
      total_shares = each_stock_shares + int(stock_shares)
      ave_price = (each_stock_shares * each_stock_ave_price + float(total_price)) / total_shares
      my_stocks[i][0] = total_shares
      my_stocks[i][1] = ave_price

  #if no, update the dictionary
  else:
    my_stocks.update({stock_symbol.upper(): [stock_shares, stock_price]})  
  print ('Your order is submitted!' + ' Your available fund is $' + str(available_fund))

#option 2, buy stock flow
def buy_stock():
  # enter stock_symbol
  stock_symbol = enter_symbol()
  stock_price = get_stock_price (url, stock_symbol)
  print('The current price for ' + stock_symbol.upper() + ' is ' + stock_price)
  if stock_price == False:
    show_menu()
  # enter stock_shares
  shares = enter_shares()
  # calculate total
  total_price = calculate_price (stock_price, shares)
  buying_power = check_buying_power (total_price)
   # if the cost is within the available fund, ask the user to confirm
  if buying_power:
    print ('Your total cost is $' + str(total_price))
    confirm = ask_to_confirm ('buy')[1]
    # if yes, place the order
    if confirm:
      place_order_for_buy(total_price, shares, stock_price, stock_symbol)
     # if not, exit
   # if the cost exceeds the available fund, re_enter shares OR exit
    else:
      user_input = input('Select 1 to re-start; Select 2 to go back to Menu: ')
      while user_input != '1' and user_input != '2':
        user_input = input('Select 1 to re-start; Select 2 to go back to Menu: ')
      if user_input == '1':
        buy_stock()
      elif user_input == '2':
        show_menu()
      else:
        return
     
#option 3, sell stock flow
def sell_stock():
  # enter stock_symbol
  stock_symbol = enter_symbol().upper()
  # if the symbol is not in my_stock list, please enter a valid symbol
  while stock_symbol not in my_stocks:
    # show my_stocks: for example, ZM: 100 shares; CRM: 200 shares;
    print('Here is your stock list: ')
    for i in my_stocks:
      print(i + ': ' + str(my_stocks[i][0]) + ' shares' )
    stock_symbol = input('Please enter a valid symbol: ')
    stock_symbol = stock_symbol.upper()
   # else: 1. show current stock price; 2. enter shares
  stock_price = get_stock_price(url, stock_symbol)
  print('The current price for ' + stock_symbol.upper() + ' is ' + stock_price)
  if stock_price:
    shares = enter_shares()
    my_shares = my_stocks[stock_symbol][0]
    # check shares within limit:
    # if exceeds limit: ask the user to re-enter;
    while int(shares) > int(my_shares):
      print('You can\'t sell more than ' + str(my_shares) + ' shares!')
      shares = enter_shares()
    # if within the limit: calculate the total price;
    # ask the user to confirm
    confirm = ask_to_confirm ('sell')
    # if yes, sell the stock: 
    if confirm[1]:
      global available_fund
      # 1. reduce the shares from my_stocks; 
      #  if the shares becomes 0, delete the stock from my list;
      total_shares = int(my_shares) - int(shares)
      try:
        my_stocks[stock_symbol][0] = total_shares
        if total_shares == 0:
          del my_stocks[stock_symbol]
      except KeyError:
        print('something goes wrong...')
      # 2. add available_fund
      most_recent_stock_price = get_stock_price(url, stock_symbol)
      total_price = calculate_price (most_recent_stock_price, shares)
      available_fund = float(available_fund)+ float(total_price)
      # back to menu
      print('Order submitted! Total price is ' + most_recent_stock_price + ' * ' + str(shares) + ' shares' + ' = $' + str(total_price))
    # if not, back to menu
    else:
      return



if __name__ == '__main__':
  show_menu()


  
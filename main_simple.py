#Created by Alex Comer-Crook for Vogogo
#28 July 2014
#alexcmrcrk@gmail.com
#+1 403 483 4759 
import sys, ast, decimal
 
#f'n is called only if discount information exists for item. It calculates if a discount is available and/or if the customer is eligable for a better price/free item
def calcDiscount (itemHash):
	if itemHash['TotalAmount'] % itemHash['DiscountAmount'] == 0 and itemHash['TotalAmount'] == itemHash['DiscountAmount']:
		itemHash['TakeFree'] = 0
		itemHash['TotalPrice'] += itemHash['DiscountPrice'] - itemHash['TotalPrice']
	elif itemHash['TotalAmount'] % itemHash['DiscountAmount'] == 0 and itemHash['TotalAmount'] > itemHash['DiscountAmount']:
		itemHash['TakeFree'] = 0
		itemHash['TotalPrice'] += itemHash['DiscountPrice'] - ((itemHash['DiscountAmount']-1)*itemHash['ItemPrice'])
	else:
		itemHash['TotalPrice'] += itemHash['ItemPrice']
		totalPossible = (itemHash['TotalPrice'] - (itemHash['TotalPrice'] % itemHash['DiscountPrice'])) / itemHash['DiscountPrice'] * itemHash['DiscountAmount']
		if totalPossible > itemHash['TotalAmount']:
			itemHash['TakeFree'] = totalPossible - itemHash['TotalAmount']
	return itemHash

#main f'n: reads in grocery items from list and builds hash according to their availability, price and discount information (if applicable)
def main (inputList,shoppingBag):
	for item in inputList:
		#keeping track of items in user list. Please see note below at decleration of var as to why I did this instead of keeping everything in one hash.
		itemsBought[item] = 1
        #since we still add the item to the hash if there is no stock, need to add extra check to see if a price exists for the item
		if item in shoppingBag and 'ItemPrice' in shoppingBag[item]:
			shoppingBag[item]['InStock'] = 1
			shoppingBag[item]['TotalAmount'] += 1
			if 'DiscountAmount' in shoppingBag[item] and 'DiscountPrice' in shoppingBag[item]:
				shoppingBag[item] = calcDiscount(shoppingBag[item])
			else:
				shoppingBag[item]['TotalPrice'] += shoppingBag[item]['ItemPrice']
		#here we still add the item to the hash so that we can store the fact that it is not in stock/no price information was received for it
		else:
			if item not in shoppingBag:
				shoppingBag[item] = {'InStock':0}
	return shoppingBag

#function that prints receipt
def printReceipt(itemsBought,shoppingBag):
	total = 0
	for key,value in itemsBought.iteritems():
		if shoppingBag[key]['InStock'] == 1:
			total += shoppingBag[key]['TotalPrice']
			if 'DiscountAmount' in shoppingBag[key] and 'DiscountPrice' in shoppingBag[key]:
				print "Item: " + str(key) + ", Unit Price: $" + str(decimal.Decimal(shoppingBag[key]['ItemPrice'])/100) + ", Quantity: " + str(shoppingBag[key]['TotalAmount']) + ", Discount: " + str(shoppingBag[key]['DiscountAmount']) + " for $" + str(decimal.Decimal(shoppingBag[key]['DiscountPrice'])/100) + ", Sub-Total: $" + str(decimal.Decimal(shoppingBag[key]['TotalPrice'])/100)
			else:
				print "Item: " + str(key) + ", Unit Price: $" + str(decimal.Decimal(shoppingBag[key]['ItemPrice'])/100) + ", Quantity: " + str(shoppingBag[key]['TotalAmount']) + ", Sub-Total: $" + str(decimal.Decimal(shoppingBag[key]['TotalPrice'])/100)
			if 'TakeFree' in shoppingBag[key] and 'DiscountAmount' in shoppingBag[key] and 'DiscountPrice' in shoppingBag[key] and shoppingBag[key]['TakeFree'] > 0:
				difference = shoppingBag[key]['TotalPrice'] - (((shoppingBag[key]['TakeFree'] + shoppingBag[key]['TotalAmount']) / shoppingBag[key]['DiscountAmount']) * shoppingBag[key]['DiscountPrice'])
				if difference > 0:
					print "You are eligible for a better deal. Take another " + str(shoppingBag[key]['TakeFree']) + " " + str(key) + "(s). You will save $" + str(decimal.Decimal(difference)/100)
				else:
					print "You are eligible for a better deal. Take another " + str(shoppingBag[key]['TakeFree']) + " " + str(key) + "(s) for the same price."
		else:
			print "Item " + str(key) + " is not in stock/for sale. Please put it back!"
	print "\nTOTAL: $" + str(decimal.Decimal(total)/100)

#create hash of CML arguments
arg_names = ['command', 'x', 'y', 'operation', 'option']
args = dict(zip(arg_names, sys.argv))

#if/else below so that there is at least a test case if no list is passed in
if 'y' in args:
	inputList = ast.literal_eval(args['y'])
else:
	inputList = ['apple','apple','apple','apple','apple','orange', 'berry',  'salad', 'steak', 'eggs', 'orange', 'eggs', 'eggs', 'oil', 'flour']

#I wanted to keep this code specifically cleaner for ease of reading/marking, so I just created another hash to keep track of bought items instead of splitting the other hash
#into "store" items and "customer" items.
itemsBought = {}

#putting price data into hash from txt file
shoppingBag = {}
with open(sys.argv[1]) as inputFile:
	for line in inputFile:
		shoppingBag[line.split()[0]] = {'ItemPrice': int(line.split()[1]), 'TotalAmount': 0, 'TotalPrice': 0}
		if len(line.split()) > 2:
			shoppingBag[line.split()[0]]['DiscountAmount'] = int(line.split()[2])
			shoppingBag[line.split()[0]]['DiscountPrice'] = int(line.split()[3])
			shoppingBag[line.split()[0]]['TakeFree'] = 0

#run main function and build main hash, then print receipt
shoppingBag = main(inputList,shoppingBag)
printReceipt(itemsBought,shoppingBag)

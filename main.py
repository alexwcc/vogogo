#Created by Alex Comer-Crook for Vogogo
#28 July 2014
#alexcmrcrk@gmail.com
#+1 403 483 4759
import sys, ast, decimal
 
#f'n is called only if discount information exists for item. It calculates the highest possible discount based on the number of items
def calcDiscount (itemHash, tempAmount, itemPrice):
	for key in sorted(itemHash,reverse=True):
		if tempAmount < key:
			if min(itemHash, key=itemHash.get) == key:
				return (itemPrice * tempAmount)
			else:
				continue	
		else:
			return itemHash[key] + calcDiscount(itemHash,tempAmount-key,itemPrice)

#f'n is called only if discount information exists for item. It calculates of there are any free items available without increasing the price
def calcFree(itemHash,totalAmount,totalPrice):
	tempTotal = 0
	for key in sorted(itemHash):
		if itemHash[key] <= totalPrice:
			totalPossible = (totalPrice - (totalPrice % itemHash[key])) / itemHash[key] * key
			if totalPossible > totalAmount and totalPossible > tempTotal:
				tempTotal = totalPossible
		else:
			break
	return tempTotal - totalAmount

#main f'n: reads in grocery items from list and builds hash
def main (inputList, shoppingBag):
	for item in inputList:
		#keeping track of items in user list. Please see note below at decleration of var as to why I did this instead of keeping everything in one hash.
		itemsBought[item] = 1
        #since we still add the item to the hash if there is no stock, need to add extra check to see if a price exists for the item
		if item in shoppingBag and 'ItemPrice' in shoppingBag[item]:
			shoppingBag[item]['InStock'] = 1
			shoppingBag[item]['TotalAmount'] += 1
		#here we still add the item to the hash so that we can store the fact that it is not in stock/no price information was received for it
		else:
			if item not in shoppingBag:
				shoppingBag[item] = {'InStock':0}
	return shoppingBag

#function that prints receipt and calls discount/free f'n only if discount information exists
def printReceipt(itemsBought,shoppingBag):
	total = 0
	for key,value in sorted(itemsBought.iteritems()):
		if shoppingBag[key]['InStock'] == 1:
			if 'DiscountInfo' in shoppingBag[key]:
				shoppingBag[key]['TotalPrice'] = calcDiscount(shoppingBag[key]['DiscountInfo'],shoppingBag[key]['TotalAmount'],shoppingBag[key]['ItemPrice'])
				shoppingBag[key]['TakeFree'] = calcFree(shoppingBag[key]['DiscountInfo'],shoppingBag[key]['TotalAmount'],shoppingBag[key]['TotalPrice'])
				if shoppingBag[key]['TakeFree'] > 0:
					print "Item: " + str(key) + ", Unit Price: $" + str(decimal.Decimal(shoppingBag[key]['ItemPrice'])/100) + ", Quantity: " + str(shoppingBag[key]['TotalAmount']) + ", Sub-Total: $" + str(decimal.Decimal(shoppingBag[key]['TotalPrice'])/100)
					print "You are eligible for a better deal. Take another " + str(shoppingBag[key]['TakeFree']) + " " + str(key) + "(s)." 
				else:
					print "Item: " + str(key) + ", Unit Price: $" + str(decimal.Decimal(shoppingBag[key]['ItemPrice'])/100) + ", Quantity: " + str(shoppingBag[key]['TotalAmount']) + ", Sub-Total: $" + str(decimal.Decimal(shoppingBag[key]['TotalPrice'])/100)
			else:
				shoppingBag[key]['TotalPrice'] = shoppingBag[key]['ItemPrice'] * shoppingBag[key]['TotalAmount']
				print "Item: " + str(key) + ", Unit Price: $" + str(decimal.Decimal(shoppingBag[key]['ItemPrice'])/100) + ", Quantity: " + str(shoppingBag[key]['TotalAmount']) + ", Sub-Total: $" + str(decimal.Decimal(shoppingBag[key]['TotalPrice'])/100)
			total += shoppingBag[key]['TotalPrice']
		else:
			print "Item " + str(key) + " is not in stock/for sale. Please put it back!"
	print "\nTOTAL: $" + str(decimal.Decimal(total)/100)

#create hash of CML arguments - just find this structure easier to work with
arg_names = ['command', 'x', 'y', 'operation', 'option']
args = dict(zip(arg_names, sys.argv))

#if/else below so that there is at least a test case if no list is passed in
if 'y' in args:
	inputList = ast.literal_eval(args['y'])
else:
	inputList = ['apple','apple','apple','apple','apple','orange', 'berry',  'salad', 'steak', 'eggs', 'orange', 'eggs', 'eggs', 'oil', 'flour']
	#inputList = ['apple','apple','apple','orange']

#I wanted to keep this code specifically cleaner for ease of reading/marking, so I just created another hash to keep track of bought items instead of splitting the other hash
#into "store" items and "customer" items.
itemsBought = {}

#putting price data into hash from txt file
shoppingBag = {}
with open(sys.argv[1]) as inputFile:
	for line in inputFile:
		shoppingBag[line.split()[0]] = {'ItemPrice': int(line.split()[1]), 'TotalAmount': 0, 'TotalPrice': 0}
		if len(line.split()) > 2:
			shoppingBag[line.split()[0]]['TakeFree'] = 0
			shoppingBag[line.split()[0]]['DiscountInfo'] = {}
			index = 2
			while index < len(line.split()):
				shoppingBag[line.split()[0]]['DiscountInfo'][int(line.split()[index])] = int(line.split()[index+1])
				index += 2
			

#run main function and build main hash, then print receipt
shoppingBag = main(inputList,shoppingBag)
printReceipt(itemsBought,shoppingBag)

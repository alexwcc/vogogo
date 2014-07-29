Thanks for taking the time to review my code!

Example command:
python main.py input.txt "['apple','apple','apple','apple','apple','orange', 'berry',  'salad', 'steak', 'eggs', 'orange', 'eggs', 'eggs', 'oil', 'flour']"

I have included two copies - I made one initially and then decided to add the extra feature to the later one. The later one is my final copy,
but I included the "main_simple.py" file so that you could see my initial thought process.

calcDiscount and calcFree are the main functions. The other code mostly reads in data and outputs content to the console. The data is input in the
following way: 
1) The store items and pricing rules are read in from a txt file. I included a sample in "input.txt"
2) The customer items are then input via a list as a CML argument, as requested. If no list is passed in, there is also a sample one for testing
purposes.
3) The items and pricing rules are set up in the folowing way, per line. All prices are in cents. All "tokens" are seperated by a space:
	a) The first token is the item name
	b) The second token is the price for 1 unit of the item
	c) All remaining pairs of tokens are discount/pricing information. The first token of the pair is the number of items and the second token is the price for that number of items.

Using the examples in the question, the following could be pricing for those examples:
1) Apples are normally $0.50, but buy three and get them for $1.30:
	apple 50 3 130
2) Buy one, get another half off
	ITEMNAME 300 2 450
3) Half off oranges
  orange 50 1 25

The extra feature that I added after my first draft was the ability to have multiple pricing rules. The format to input the pricing is the same, for example:
1) Apples are $0.50 each. Buy 3 for $1.25 or buy 5 for $2:
	apple 50 3 125 5 200

I also added the functionality to tell the user when they can get a better deal. For example: If apples are $0.50 each and the special is 4 for $1, but the user 
buys 3, it will tell charge them $1.50 but let them know that they can get a better deal by adding one more apple. Lastly, if there is an item in the customer list but not in the store list, it will tell the user to put the item back as it is out of stock.

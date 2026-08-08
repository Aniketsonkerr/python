#problem 1:
# take prices of the 3 products
# make bill
# and find out average price
# product1_price = float(input("enter the price for product 1: "))
# product2_price = float(input("enter the price for product 2: "))
# product3_price = float(input("enter the price for product 3: "))

# bill = float(product1_price + product2_price + product3_price)
# print("your total bill :",bill)

# average_rate=(bill/3)
# print("average rate of the product :",average_rate)

#problem 2:
#take input a superhero name and check if the name starts with "S"/"s" or not

superhero_name=input("enter your superhero name: ");
print("S" in superhero_name or "s" in superhero_name)
print(superhero_name.find("S") or superhero_name.find("s"))

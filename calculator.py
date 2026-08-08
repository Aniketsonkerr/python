#calculator 
a=float(input("enter first digit: "))

operation=input("enter the operation you want to perform: ")

b=float(input("enter first digit: "))

match operation:
  case "+" :
    print(a+b)
  case "-":
    print(a-b)
  case "*":
    print(a*b)
  case "/":
    print(a/b)
  case "%":
    print(a%b)
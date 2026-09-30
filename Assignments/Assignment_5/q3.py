def check_number(num):
    if num % 2 == 0:
        return "even"
    else:
        return "odd"

userinput = int(input("Enter a number: "))
print(f"{userinput} is an {check_number(userinput)} number.")
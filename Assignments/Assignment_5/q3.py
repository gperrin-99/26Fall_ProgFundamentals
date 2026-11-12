def check_number(num):
    if num % 2 == 0:
        return "even"
    else:
        return "odd"
#function to check if a number is even or odd
userinput = int(input("Enter a number: "))
#input to store the number with a prompt
print(f"{userinput} is an {check_number(userinput)} number.")
#print statement to display whether the input number is even or odd

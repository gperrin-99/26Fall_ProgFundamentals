def area(length, width):
    return length * width

def perimeter(length, width):
    return 2 * length + 2 * width

userinput = input("Enter length and width separated by a space: ")
length, width = map(float, userinput.split())
print(f"Area: {area(length, width)}")
print(f"Perimeter: {perimeter(length, width)}")
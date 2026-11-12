def area(length, width):
    return length * width
#function to calculate the area of a rectangle
def perimeter(length, width):
    return 2 * length + 2 * width
#function to calculate the perimeter of a rectangle

userinput = input("Enter length and width separated by a space: ")
#input to store the length and width separated by a space with a prompt
length, width = map(float, userinput.split())
#convert the input values to float and store them in length and width variables
print(f"Area: {area(length, width)}")

print(f"Perimeter: {perimeter(length, width)}")
#print statements to display the area and perimeter of the rectangle
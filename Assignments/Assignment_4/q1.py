#question 1
name="Bob"
age=20
height=6

print(f"{name} is {age} years old and {height} feet tall.")

#question 2

length=12.5
width=4
perimeter= length*2 + width*2
area=length*width


print(f"The area is {area}")
print(f"The perimiter is {perimeter}")

#question 3

mark1=90.00
mark2=75.00
mark3=83.00
marktotal=mark1+mark2+mark3
markavg=marktotal/3

print(f"Total: {marktotal:.2f} out of 300")
print(f"Average: {markavg:.2f}%") 

#question 4

item="Banana"
price=1
quant=7

subtotal=price*quant
tax=subtotal*0.005
finaltotal=subtotal+tax

print(f"Subtotal: {subtotal:.2f}")
print(f"Tax: {tax:.2f}")
print(f"Final Total: {finaltotal:.2f}")



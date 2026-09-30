userinput=input("Please choose from the following options: T - Temperature. H - Humidity. 0 - Both")

def temp():
    print("hi")

#     import time
# from hs3003 import HS3003
# sensor = HS3003()
# t, h = sensor.read()
# print("Temperature is: {:.1f} C".format(t))
# exit
#     
def humid():
    import time
from hs3003 import HS3003

sensor = HS3003()

while True:
    t,h = sensor.read()
    print("Humidity is: {:.1f} %".format(h))

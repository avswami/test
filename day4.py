#1
class ItrDemo:
 def __init__(self):
  self.inp=[]
 def Itr(self,InputString):
  print(InputString)
  self.inp= InputString
  it=iter(self.inp)
  try:
   for x in range(len(InputString)):
     print(next(it))
     next(it)
  except StopIteration:
    pass
  finally:
   print("Iteration is done")
o1 = ItrDemo()
o1.Itr("Hello")


#2
import csv
with open('expr.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)
with open('expr.csv', 'a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Name",23])
with open('expr.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)


#4
import glob
for python in glob.iglob('**\*.py', recursive=True):
    print(python)


#5
import sys
print(f"Aguments: {sys.argv}")


#6
import random
guess=random.randint(1,15)
num=int(input("Enter the number"))
count=1
while guess!=num :
    try:
        if(count==3):
            raise Exception
        if(num<guess):
            print("your guess value is lower than the real value")
            num=int(input("Enter the number"))
            count=count+1
        else:
            print("your guess value is higher than the real value")
            num=int(input("Enter the number"))
            count=count+1
    except Exception:
        print(f"You Lost\n\n")
        break
if(guess==num):
    print(f"you won\n\n")


#7 Value Error
import math
num=int(input("Enter the number"))
try:
    res=math.sqrt(num)
    print(res)
except ValueError:
    print("The value of num should be greater than 0")   # if num = -1


# Type Error
import math
num=input("Enter the number")
try:
    res=math.sqrt(num)
    print(res)   
except TypeError:
    print("The type of num should be an integer")    #if num='a'


 #8.KeyError
details={"abc":1,"xyz":2,"uv":3}
try:
    print(details["abcd"])
    print(details["st"])
except KeyError:
    print("Enter the correct key")


#indexError
array=[10,12,13]
try:
    print(array[1])
    print(array[5])
except IndexError:
    print("Index out of bound")
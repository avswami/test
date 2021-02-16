#task 1
import random
x=random.randint(1,20)
count = 0
while count < 3:
    count +=1
    guess=int(input("Guess a number:- "))
    if x == guess:
        print("Congratulations you did it in ",
              count, " try")
        break
    elif x > guess:
        print("You guessed too small!")
    elif x < guess:
        print("You Guessed too high!")
if (count >= 3 and x != guess):
    print("\nThe number is %d" % x)
    print("\tBetter Luck Next time!")

#task 2
for (i, v) in enumerate(["a", "b", "c", "d"]):
     print(i,":", v)


#task 3
a_dict = {'flavor': 'strawberry', 'chocolate': 'cadbury', 'car': 'nissan','price' : 100}
for key, value in a_dict.items():
   print(value , ' belongs to ', key)


#task 4
#else  invoked 
i = 1
while i < 3:
    print(i)
    i += 1
else:
    print("The number cannot be less than 2")
#else not being invoked
i = 1
while i < 2:
    print(i)
    i += 1
    if i == 2:
      break
else:
    print("The number cannot be less than 2")


#task5
def mul(num1: int, num2: int) -> int:
    '''Takes two values and prints their product'''
    mul = num1 * num2
    return mul
print(mul(1, 5))
print(mul(5, 10))
a = int(input("Enter first number: "))
b = int(input("Enter second number: "))
print(mul.__doc__)
print(mul(a, b))


#task6
def args(*args):
    for item in args:
        print(item)
args(10,20,30,40,50)


#task7
def kwargs1(**kwargs):
    count=0
    for key, value in kwargs.items():
     print(value , ' -> ', key)
     print(" you passed ",count, "args ")
     count +=1
kwargs1(FirstName="AV",LastName="SW",Greeting="Hello!")


#task8
def combo(*args, **kwargs):
    print(len(args) + len(kwargs))
combo(10,20,30, FirstName="AV",LastName="SW",Greeting="Hello!")  

#task9
List = [1, 3, 3, 4, 5, 6]
Result = [i*i for i in List if i%2 == 1]
for Square in Result:
	print(Square)


#task10
total=int(input("Enter the total : "))
count=int(input("Enter the count : "))
avg = lambda total, count : total /count
print("Average  = ", avg(total,count))


#task11 - bonus1
b_dict = {'flavor': 'strawberry', 'chocolate': 'cadbury', 'car': 'nissan','price' : 100}
b_list = [key for key,value in b_dict.items() if len(key)>=4]
print(b_list)

#task12- bonus 2
colors = [['Red', 'Orange', 'Green'], ['Blue', 'Purple', 'Lavendar'], ['Grey', 'Black', 'Brown']]   
combined_colors = []  
for sublist in colors: 
    for colors in sublist:          
        if len(colors) < 6: 
            combined_colors.append(colors)           
print(combined_colors) 

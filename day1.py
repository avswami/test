#task 1.2
names = ['john', 'jake', 'jack', 'jack','george', 'jenny', 'jason']
unique=set(names)
print("unique names:",unique)
for name in unique:
    if((len(name)<5) and ('e' not in name)):
         print(name)


#task 2
string ="python"
print('c'+string[1:])


#task 3
new={"name": "python", "ext": "py", "creator": "guido"}
keys=list(new.keys())
value=list(new.values())
both=list(new.items())
print("keys:",keys)
print("values:",value)
print("both:",both)


#task 4 fizzbuzz
for num in range(1,51):
    if num % 3 == 0 and num % 5 == 0:
        print("fizzbuzz")
    elif num % 3 == 0:
        print("fizz")
    elif num % 5 == 0:
        print("buzz")
    else:
        print("nothing")




#task 5
import random
guess=random.randint(1,20)
num=int(input("Enter the number : "))
while(guess!=num):
    if(num<guess):
        print("your guess value is lower than the real value")
        num=int(input("Enter the number : "))
    elif(num>guess):
        print("your guess value is higher than the real value")
        num=int(input("Enter the number : "))
print("correct answer")
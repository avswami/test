#task 1
nums = [1, 2, 3]
dict_comp = {x: x**2 for x in nums}
print (dict_comp)
list1 = list(dict_comp.values())
print(list1)


#task 2
list2 = [1, 2, 5, 2, 3, 1, 4, 5]
set1 = set(x**2 for x in list2)
print(set1)

#task 3
balance_list = [("Guido", 2000, 500), ("Raymond", -52, 1000), ("Jack", 900, 1000), ("Brandon", 2000, 0)]
dict1 = {}
for i in balance_list:  
    if i[1] > i[2] :
     dict1.setdefault(i[0],i[1])
print(dict1)

bal = set()
for i in balance_list: 
         bal.add(i[1])
print(bal)

acc_holder = []
for i in balance_list:
  acc_holder.append(i[0])
print (acc_holder)

dict2 = {}
for i in balance_list:  
    if i[1] < i[2] :
       # i[1] = i[2] - i[1]
        dict2.setdefault(i[0],i[2]-i[1])
print(dict2)

new_Bal = []
for a in balance_list:
     if a[1] > 0 :
       new_Bal.append(a[0:2])
print (new_Bal)


#task 4
class Developer :

     def __init__(self, languages):
         self.languages=["C","C++","Java","Python","JS","JSON"]
     def code(self,language): 
            if(language in self.languages): 
                 print("code in : ", language) 
            else:
                 print("code not in list")
     def resume(self):
        print(self.languages)           
language = input("Enter a coding language: ")
print(language.__str__())
print(language.__repr__())
s = Developer("")
s.code(language)
s.resume()

class SrDeveloper(Developer):
    def __init__(self):
        self.reviews = []
        Developer.__init__(self)
    def review(self,review):            
        if(len(self.reviews)<len(self.languages)):
            self.reviews.append(languages)    

class TechLead(SrDeveloper):
    def __init__(self):
        SrDeveloper.__init__(self)
    def design(self):                       
        print("Design function in TechLead Class")

#task5
from math import factorial
class Factorial:
    def __init__(self):
        self.result = []
    def computeFactorial(self,numbers):
        for number in numbers:
            self.result.append(factorial(number))
        return self.result
newObject = Factorial()
print(newObject.computeFactorial([3,2]))

#task6
from importModule import firstFunction
firstFunction()

#task7
from importModule import nextFunction as importedModule
importedModule()


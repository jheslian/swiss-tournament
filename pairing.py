import itertools
list = ["A", "B", "C", "D", "E", "F", "G", "H"]
play_with = ["B", "C"]
pairs = []
l = "A"
new_list = []
not_played = []
for pair in itertools.combinations(list,2):
   e = [l]
   if (pair[1] not in play_with):
      e.append(pair[1]) 
   if len(e) != 1 :   
      not_played.append(e)   
new_list.append(not_played[0])   
#print(not_played)


d_list = []
p_with = []
# for j, pair in enumerate(itertools.combinations(list,2)):
#    print(pair)
for i, p in enumerate(list):
   print("lettre",p)
   for j, pair in enumerate(itertools.combinations(list,2)):
      print("R", )
      
      if p == pair[0] and d_list != [] and p not in d_list[-1]:
         print(pair)
         d_list.append(pair)
      
      else:
         if j == 0 and i == 0:
            print(pair)
            d_list.append(pair)
         
      
      j += 1
   i += 1   

print(d_list)     
   #
   # for i in range(len(list)):
   #    #if i in pair and pair == 0:

   #    print(i)
# b = []     
# a = [[1, 2],[3,4]]  
# print( 2 in a[0], 3 not in a[1])
import random
print(random.choice(["W", "B"]))



o = {

"players": {
        "1": {
            "last_name": "Rr",
            "first_name": "rr",
            "birth_date": "r",
            "gender": "r",
            "rank": "r",
            "score": 0
        },
        "2": {
            "last_name": "A",
            "first_name": "a",
            "birth_date": "a",
            "gender": "a",
            "rank": "a",
            "score": 0
        },
        "3": {
            "last_name": "y",
            "first_name": "y",
            "birth_date": "y",
            "gender": "y",
            "rank": "",
            "score": 0
        }
    }
}
print(o["players"]["1"])
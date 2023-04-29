import re
import json

content = {
    'csrfmiddlewaretoken': ['driieKXoVAH54qA5qcfyZXLXCCXaxrOgXTtuQuinTDxQw9lGmmm6BIgUe5txvfUB'], 'questions': ['', ''], 
    'question3': ['who was the earthly father of Jesus'], 
    'choice3': ['True'], 
    'question1': ['how old was Jesus when he began his earthly ministry?'], 'choice1': ['False']}

content2 = {
    'csrfmiddlewaretoken': ['x4EjMXi6ARVlGvKqyw303MnjszGRsHnzhwPvoHD5yUL68ev1uGayFxSg42ceqvtU'],
    'question3': ['who was the earthly father of Jesus'], 
    'choice3': ['False,8'], 
    'question2': ['how old was Jesus when He died'], 
    'choice2': ['True,5']}

content3 ={
    'csrfmiddlewaretoken': ['Gf4i5oOok2bOgX3OIfhtGy4Yxp1J8WGDqHfuH89ni51zIGOpEpo1ijzV9Sx66KMY'], 'question3': ['3'], 
    'choice3': ['8'], 
    'question2': ['2'], 
    'choice2': ['5']}

question_answer_pair ={}
for key,value in content3.items():
    if re.search(r'^question',key):
        print(f'questions are {key + ":" + value[0] }')

# json formatting
# json_data = json.dumps(content2, indent=2)
# print (json_data)
# q =json_data["question3"]
# print(f'question3 is: {type(json_data)}')
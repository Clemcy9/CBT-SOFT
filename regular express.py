import re

# regex below matches 1 to infinix *(1000) digit at the end of a string
id = re.compile(r'[0-9]{1,}$')
text = 'hello how are you doing 45, and2 mummy 13'
res =id.findall(text) #returns a list

# print(id.search(text).group())
# print(res)


def match_question_with_choice(querydict):
    print(querydict)
    question_answer_pair ={} #diction of quest_id:choice_id pair
    found_key=''
    found_choice=' '
    for key,value in querydict.items():
        if re.search(r'^question',key):
            # print(f'questions are {key + ":" + value[0] }')
            found_key = value[0]
        if re.search(r'^choice',key):
            # print(f'choices are: {key + ":" + value[0] }')
            found_choice = value[0]
        try :
            id.search(found_key).group() == id.search(found_choice).group()
            question_answer_pair[found_key] = found_choice
            # print(f'found key:{querydict(found_key)}')
        except:
            print('no match found')
    return question_answer_pair

# testing
content3 ={
    'csrfmiddlewaretoken': ['JsL0S1OoeGKJlomeW27jg4orwLM0v57etUWcuL9ncJAuN77PSceRSPTo8eintTdz'], 'question2': ['2'], 
    'choice2': ['4'], 
    'question1': ['1'], 
    'choice1': ['2'], 
    'question3': ['3'], 
    'choice3': ['9']
    }

print(f'testing {match_question_with_choice(content3)}')

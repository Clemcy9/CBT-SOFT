from openpyxl import load_workbook
from openpyxl.worksheet import worksheet as wss
from threading import Thread
from cbt_app.models import Question,Choice,Topic

def xl2db(url,course,title):
    wb = load_workbook(url)
    ws = wb.active
    print(f'reading from the file: {ws["A2"].value}')
    inner = 0
    outer = 0
    for row in wss.Worksheet.iter_rows(ws,min_row=3,max_col=6,max_row=100):
        print(f'this is outer counter {outer}')
        # print(f'outer values{row[outer].value, row[outer], row[outer].col_idx}')

        # if cell is empty or no question
        # if row[outer].value == None:
        #     print('question has finished')
        #     break
        
        for cell in row:
            print(f'this inner counter {inner}')
            inner = inner +1
            # topic col
            if cell.col_idx ==1:
                # t=Topic.objects.create(name=cell.value)
                global t
                if cell.value == None:
                    print('no topic identified')
                    t=Topic.objects.get_or_create(name='no topic',courses = course)[0]
                else:
                    t=Topic.objects.get_or_create(name=cell.value,courses = course)[0]
            
            # question text col
            elif cell.col_idx ==2:
                # stop operation if question col is empty
                if cell.value == None:
                    print('no question found, exiting...')
                    return 1

                # if question already in db, move to another question
                try: 
                    q =Question.objects.get(content=cell.value)
                    print(f'question already in db... now adding title and questionid ={q.id}')
                    q.upload_title=title
                    q.save()
                except:
                    print(f'question does not exit, creating question')
                    print(cell.value, cell, cell.col_idx)
                    break
                    # print(f'this is t in question block: {t}')
                    global quest
                    # quest = Question.objects.get_or_create(content=cell.value,upload_title=title)[0]
                    quest =Question.objects.create(content=cell.value,upload_title=title)
                    print(f'this is quest id = {quest.id}')

                    try:
                        quest.topic.add(t)
                        print('topic has paired with question')
                    except:
                        print('couldnt pair question to topic')
            # options col
            elif cell.col_idx==3:
                if cell.value:
                    c1 = Choice.objects.create(content=cell.value,question=quest)
                    
            elif cell.col_idx==4:
                if cell.value:
                    c2 = Choice.objects.create(content=cell.value,question=quest)
            elif cell.col_idx==5:
                if cell.value:
                    c3 = Choice.objects.create(content=cell.value,question=quest)
            elif cell.col_idx==6:
                if cell.value:
                    a = Choice.objects.create(content=cell.value,question=quest, is_answer=True)
            
        outer = outer +1
            
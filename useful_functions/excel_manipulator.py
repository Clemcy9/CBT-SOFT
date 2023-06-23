from openpyxl import load_workbook
from openpyxl.worksheet import worksheet as wss
from threading import Thread
from cbt_app.models import Question,Choice,Topic

def xl2db(url,course,title):
    wb = load_workbook(url)
    ws = wb.active
    print(f'reading from the file: {ws["A2"].value}')

    for row in wss.Worksheet.iter_rows(ws,min_row=3,max_col=6,max_row=8):
        for cell in row:
            # if cell.value == None:
            #     print('question has finished')
            #     break
            print(cell.value, cell, cell.col_idx)
        
            # topic col
            if cell.col_idx ==1:
                # t=Topic.objects.create(name=cell.value)
                global t
                if cell.value == None:
                    print('no topic identified')
                    t=Topic.objects.get_or_create(name='no topic',courses = course)[0]
                t=Topic.objects.get_or_create(name=cell.value,courses = course)[0]
            # question text col
            elif cell.col_idx ==2:
                # stop operation if question col is empty
                if cell.value == None:
                    print('question has finished')
                    break
                print(f'this is t in question block: {t}')
                global q
                q = Question.objects.get_or_create(content=cell.value, upload_title=title)[0]
                try:
                    q.topic.add(t)
                    print('topic has paired with question')
                except:
                    print('couldnt pair question to topic')
            # options col
            elif cell.col_idx==3:
                if cell.value:
                    c1 = Choice.objects.create(content=cell.value,question=q)
                    
            elif cell.col_idx==4:
                if cell.value:
                    c2 = Choice.objects.create(content=cell.value,question=q)
            elif cell.col_idx==5:
                if cell.value:
                    c3 = Choice.objects.create(content=cell.value,question=q)
            elif cell.col_idx==6:
                if cell.value:
                    a = Choice.objects.create(content=cell.value,question=q, is_answer=True)
            
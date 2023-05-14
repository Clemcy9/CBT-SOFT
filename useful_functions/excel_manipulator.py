from openpyxl import load_workbook
from openpyxl.worksheet import worksheet as wss
from threading import Thread

def xl2db(url):
    wb = load_workbook(url)
    ws = wb.active
    print(f'reading from the file: {ws["A2"].value}')


 # using thread to achieve async file processing (saving excel to db)
# t1 =Thread(target=xl2db,args=[str(form.instance.excel_file.name),])
# t1.start()

wb = load_workbook(r'C:\Programming\Backend\CBT SOFT\static\uploads\Maths_ss1_template for cbt.xlsx')
ws = wb.active


'''
for x in ws['a3':'a8']:
     print(x[0].value)   
     if x[0].value ==None:
             print('no more questions')
             break
'''

for row in wss.Worksheet.iter_rows(ws,min_row=3,max_col=6,max_row=8):
    for cell in row:
        if cell.value == None:
            print('question has finished')
            break
        print(cell.value, cell, cell.col_idx)
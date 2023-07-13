 this document shows the intended design for the custom made paginated quiz

# requirements / features
 * get questions and options from db 
 * display questions in chuncks (paginate question)
 * provide next and prev button to navigate the quiz (save state of quiz)
 * calculate result i.e score
 * send result, time taken and question choice pair to db (backend)

# method
 * receive question/options as a dict, store it in jscript object as questions
 * create question-choice object to store user progress
 * create an empty form tag
 * generate elements for form tag based on the chunck-question from questions object
 * create a function { change_content(page_number) } that toggles displayed element based on prev/next button or page id (page number)
 * onclick of the change_content() user choice gets appended to question-choice object
 * on serving the last set of question from questions object, a submit button should appear
 * onclicking on the submit button, result, time taken and question-choice get sent to db
 * if time elapse, previous step should be carried out.

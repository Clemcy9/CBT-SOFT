export function send_data(){
    alert('a different loading')
}
// fetch post and get request
export async function makeRequest(url, method, data){
    let response = {}
    let headers ={
        // 'X-Requested-With':'XMLHttpRequest',
        // 'Content-Type':'multipart/form-data'
    }

    if(method == "POST"){
        const csrf = document.querySelector('[name = csrfmiddlewaretoken]').value
        headers['X-CSRFToken'] = csrf
        response= await fetch(url,{
           method:method,
           headers:headers,
           body:data
        })
    }
    else{
        response= await fetch(url)
    }

    return response.json()
} 

  // load all questions
export function load_questions(questions,quizBox){
    // variable for question numbering
    let q_num =0
    questions.forEach(q => {
        let question_div = document.createElement('div')
        question_div.classList.add('questions','inactive')
        quizBox.appendChild(question_div)
        // Object.entries is similar to dict.items in python that returns key,value
        for (const [question,options] of Object.entries(q)){
            q_num++
            // console.log('question= ',question)
            question_div.innerHTML = `
                <input type='radio' onclick="decorator(${q_num},3)" class='flag'>flag</>
                <hr class="ques" >
                <div class="mb-2 ques" >
                    <b>${q_num}.${question}</b>
                </div>
            `
            for (const option of options){
                question_div.innerHTML += `
                    <div>
                        <input type="radio" onclick="decorator(${q_num},1)" class="ans"  id="choice${option[1]}" name="${option[2]}" value="${option[1]}">
                        <label for="${option[2]}"  class="answer">${option[0]}</label>
                    </div>
            
                    `
            }
        }
    }); 
}

 // function to record user attempt
// gather_report create an array of objects contain question_id: choice_id
// [{question_id : choice_id}]
function gather_report(choices,no_question){
    // array for all user response
    let user_response = []
    // step through all the choices and get question_id with user choice
    for (let choice of choices){
        // variable for user response
        if(choice.checked){
            let q_id = choice.name
            let user_question_choice = new Object()
            user_question_choice[q_id] =choice.value
            user_response.push(user_question_choice)
        }else{
            // if not option not checked, check if question_id of choice is already registered
            // in user_response array, if not, add question id with null as choice_id
            console.log('runnig else block')
            
        }
    }
    console.log(user_response)
}

export function countDown(timeLeft,min_left,sec_left,submit_btn) {
    let min = 0;
    let secs = 0;
    setInterval(function () {
        if (timeLeft > 0) {
            timeLeft--;
            // let post =
            min = Math.floor(timeLeft/60) // minute only half of the countdown
            secs= Math.round(((timeLeft/60)-min)*60) // seconds only half of the countdown
            min_left.innerHTML = min
            sec_left.innerHTML = secs
        }
        if (timeLeft <= 0) {
            // submit.attr("disabled", true);
            clearInterval()
            timeLeft = 0
            submit_btn.click()
        }
    }, 1000)
}
// export default send_data
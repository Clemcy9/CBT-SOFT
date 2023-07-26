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

// export default send_data
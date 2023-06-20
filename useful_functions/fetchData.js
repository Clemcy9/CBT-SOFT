async function makeRequest(url, method, body){
    let headers ={
        'X-Requested-With':'XMLHttpRequest',
        'Content-Type':'application/json'
    }

    if(method == 'post'){
        const csrf = document.querySelector('[name = csrfmiddlewaretoken]').value
        headers['X-CSRFToken'] = csrf
    }

    let response = await fetch(url,{
        method:method,
        headers:headers,
        body:body
    })

    return await response.statusText()
} 

// javascript request (get) data async: frontend

// x = await fetch('http://127.0.0.1:8000/quiz/api/')
// y = await x.json()
// console.log(y)


// posting data
let data = JSON.stringify('hello world')
let post =  await makeRequest('http://127.0.0.1:8000/quiz/api/','post',data)
export function send_data(){
    alert('a different loading')
}
// fetch post and get request
export async function makeRequest(url, method, data){
    alert('loaded js successfully')
    let headers ={
        // 'X-Requested-With':'XMLHttpRequest',
        // 'Content-Type':'multipart/form-data'
    }

    if(method == "POST"){
        const csrf = document.querySelector('[name = csrfmiddlewaretoken]').value
        headers['X-CSRFToken'] = csrf
    }

    let response = await fetch(url,{
        method:method,
        headers:headers,
        body:data
    })

    return await response.json()
} 

// export default send_data
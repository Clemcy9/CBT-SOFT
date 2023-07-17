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

// export default send_data
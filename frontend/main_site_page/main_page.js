const YoutubeToMp3 = document.getElementById('first-button')
const Mp4ToMp3 = document.getElementById('second-button')
function first_button(event){
    event.preventDefault()
    alert("Sorry, this feature is currently under development")
}
function second_button(event){
    event.preventDefault()
    // window.location.replace("http://localhost:8000/upload")
    // history.pushState({}, null, "http://localhost:8000/upload")
    window.location.href = 'http://localhost:8000/upload'
    /*
    fetch('http://localhost:8000/upload')
    .then((response) => {
      return response.text();
    })
    .then((html) => {
      document.body.innerHTML = html     
    })
    document.getElementsByTagName('title')[0].innerHTML = 'Mp4 to mp3 converter'
    if (window.history.replaceState) {
        window.history.replaceState({}, '', "/upload")
    }
    */
}
YoutubeToMp3.addEventListener('click', first_button)
Mp4ToMp3.addEventListener('click', second_button)
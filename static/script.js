let lang = document. getElementById("language");
let start = document.getElementById("start");
let stop = document.getElementById("stop");
let text = document.getElementById("text");

let SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
let recognition = new SpeechRecognition();
recognition.continuous = false;
recognition.lang = 'en-US';
recognition.interimResults = false;  
recognition.maxAlternatives = 1;

start.onclick=()=>{
  start.innerHTML = "Recording..."
  recognition.start();
  console.log("Ready to receive a command.");
  }
recognition.onspeechend=()=>{
  start.innerHTML = "Start Recording"
  recognition.stop();
  console.log("Stopped receiving commands.");
}
recognition.onresult=(event)=>{
  let transcript = event.results[0][0].transcript;
    console.log(transcript);
    text.value ="Generating code.... please wait"
  fetch('/process', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ speech:transcript  ,  language: lang.value })
  })
  
  .then(response => response.json())
  .then(data => {
    console.log(data.result);
    
    text.value = data.result+"\n";
  })
  // text.value += transcript+"\n";
}
stop.onclick=()=>{
  recognition.stop();
  console.log("Stopped receiving commands.");
  }

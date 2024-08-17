// const startBtn = document.getElementById('startBtn');
// const stopBtn = document.getElementById('stopBtn');
// const transcriptArea = document.getElementById('transcript');

// let recognition;

// function startRecognition() {
//     recognition = new webkitSpeechRecognition();
//     recognition.continuous = true;
//     recognition.interimResults = false;
//     recognition.lang = 'en-US';
//     recognition.maxAlternatives = 1;

//     recognition.start();

//     startBtn.disabled = true;
//     stopBtn.disabled = false;
// }

// function stopRecognition() {
//     recognition.stop();
//     startBtn.disabled = false;
//     stopBtn.disabled = true;
// }

// startBtn.addEventListener('click', startRecognition);
// stopBtn.addEventListener('click', stopRecognition);

// recognition.onresult = function(event) {
//     const transcript = Array.from(event.results)
//         .map(result => result[0])
//         .map(result => result.transcript)
//         .join('');

//     transcriptArea.value = transcript;
// };


//from medium article
//https://gopesh3652.medium.com/building-a-voice-to-text-app-with-javascript-a-step-by-step-guide-9042493bdd63
const startButton = document.getElementById('startButton');
const outputDiv = document.getElementById('output');

const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition || window.mozSpeechRecognition || window.msSpeechRecognition)();
recognition.lang = 'en-US';

recognition.onstart = () => {
    startButton.textContent = 'Listening...';
};

recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    outputDiv.textContent = transcript;
};

recognition.onend = () => {
    startButton.textContent = 'Start Voice Input';
};

startButton.addEventListener('click', () => {
    recognition.start();
});
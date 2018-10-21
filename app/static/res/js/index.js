// get navigation links
var allLinks = document.getElementsByTagName('a');
// get last word said element
var strongEl = document.getElementById('latest-word');

// new instance of speech recognition
var recognition = new webkitSpeechRecognition();
var recognizing = false;


// input for speech synthesis
var speechMsgInput = document.getElementById('speech-msg');
var voiceSelect = document.getElementById('voice');

// load voices
// Execute loadVoices.
loadVoices();
// Chrome loads voices asynchronously.
window.speechSynthesis.onvoiceschanged = function(e) {
  loadVoices();
};

// set params
recognition.continuous = true;
recognition.interimResults = true;
//recognition.start();

recognition.onresult = function(event){
  
  // delve into words detected results & get the latest
  // total results detected
  var resultsLength = event.results.length -1 ;
  // get length of latest results
  var ArrayLength = event.results[resultsLength].length -1;
  // get last word detected
  var saidWord = event.results[resultsLength][ArrayLength].transcript;
  
  // loop through links and match to word spoken
  for (i=0; i<allLinks.length; i++) {
    
    // get the word associated with the link
    var dataWord = allLinks[i].dataset.word;
    
    // if word matches chenge the colour of the link
    if (saidWord.toLowerCase().indexOf(dataWord) != -1) {
      allLinks[i].style.color = 'red';
    }
  }
  
  // append the last word to the bottom sentence
  strongEl.innerHTML = saidWord;

  speechMsgInput.value = saidWord;
}

// speech error handling
recognition.onerror = function(event){
  console.log('error?');
  console.log(event);
}

recognition.onend = function() {
    recognizing = false;
    begin.innerHTML = 'Start Recognition';
  
    if (speechMsgInput.value.length > 0) {
		  speak("I think you just said ")
      speak(speechMsgInput.value);
	  }
}

function startButton(event) {
  if (recognizing) {
    recognition.stop();
     for (i=0; i<allLinks.length; i++) {
       allLinks[i].style.color = 'blue';
     }
    return;
  }
  //final_transcript = '';
  //recognition.lang = select_dialect.value;
  recognizing = true;
  recognition.start();
  //ignore_onend = false;
  begin.innerHTML = 'Stop Recognition';
  //start_img.src = '/intl/en/chrome/assets/common/images/content/mic-slash.gif';
  //start_timestamp = event.timeStamp;
}


function speak(text) {
  // Create a new instance of SpeechSynthesisUtterance.
	var msg = new SpeechSynthesisUtterance();
  
  // Set the text.
	msg.text = text;
  
  // Set the attributes.
	msg.volume = 1; //parseFloat(volumeInput.value);
	msg.rate = 1; //parseFloat(rateInput.value);
	msg.pitch = 1;// parseFloat(pitchInput.value);
  
  // If a voice has been selected, find the voice and set the
  // utterance instance's voice attribute.
	if (voiceSelect.value) {
		msg.voice = speechSynthesis.getVoices().filter(function(voice) { return voice.name == voiceSelect.value; })[0];
	}
  
  // Queue this utterance.
	window.speechSynthesis.speak(msg);
}


function loadVoices() {
  // Fetch the available voices.
	var voices = speechSynthesis.getVoices();
  
  // Loop through each of the voices.
	voices.forEach(function(voice, i) {
    // Create a new option element.
		var option = document.createElement('option');
    
    // Set the options value and text.
		option.value = voice.name;
		option.innerHTML = voice.name;
		  
    // Add the option to the voice selector.
		voiceSelect.appendChild(option);
	});
}

function speakButton(event) {
	if (speechMsgInput.value.length > 0) {
		speak(speechMsgInput.value);
	}
}
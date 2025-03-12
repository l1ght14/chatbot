const msgerForm = get(".msger-inputarea");
const msgerInput = get(".msger-input");
const msgerChat = get(".msger-chat");

function getResponseFromServerBot(message){
    let msg = "This is Message";
  const xhttp = new XMLHttpRequest();
  xhttp.onload = function(msg) {
        msg =  this.responseText;
        botResponse(msg);
    }
  xhttp.open("GET", "/getResponse?msg="+message, true);
  xhttp.send();

}

// Icons made by Freepik from www.flaticon.com
const BOT_IMG = "https://cdn-icons-png.flaticon.com/512/6684/6684500.png";
const PERSON_IMG = "https://cdn-icons-png.flaticon.com/512/7838/7838354.png";
const BOT_NAME = "BOT";
const PERSON_NAME = "You";

msgerForm.addEventListener("submit", event => {
    event.preventDefault();
    const msgText = msgerInput.value;
    if (!msgText) return;

    //Appending the message
    appendMessage(PERSON_NAME, PERSON_IMG, "right", msgText);
    msgerInput.value = "";
    botReply = getResponseFromServerBot(msgText);

});

function appendMessage(name, img, side, text) {
  //   Simple solution for small apps
  const msgHTML = `
    <div class="msg ${side}-msg">
      <div class="msg-img" style="background-image: url(${img})"></div>

      <div class="msg-bubble">
        <div class="msg-info">
          <div class="msg-info-name">${name}</div>
          <div class="msg-info-time">${formatDate(new Date())}</div>
        </div>

        <div class="msg-text">${text}</div>
      </div>
    </div>
  `;

  msgerChat.insertAdjacentHTML("beforeend", msgHTML);
  msgerChat.scrollTop += 500;
}

function botResponse(botReply) {
    const delay = botReply.split(" ").length * 100;
//    log(botReply)
    setTimeout(() => {
        appendMessage(BOT_NAME, BOT_IMG, "left", botReply); //This appends the message to bot side
    }, 2000);
}

// Utils
function get(selector, root = document) {
  return root.querySelector(selector);
}

function formatDate(date) {
  const h = "0" + date.getHours();
  const m = "0" + date.getMinutes();

  return `${h.slice(-2)}:${m.slice(-2)}`;
}

function random(min, max) {
  return Math.floor(Math.random() * (max - min) + min);
}
function log(w){
    console.log(w);
}
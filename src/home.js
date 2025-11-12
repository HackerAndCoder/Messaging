function addMessage(text) {
  var messageBox = document.getElementById("messages");
  
  var messageClass = document.createElement("div");
  messageClass.classList.add("messageobject");
  
  var messageText = document.createElement("h4");
  messageText.classList.add("messagetext");
  
  if (Math.random() < 0.2) {
    messageText.classList.add("me");
  }
  
  messageText.innerText = text;
  
  messageClass.append(messageText);
  
  messageBox.appendChild(messageClass);
}

function addChat(name) {
  var chatList = document.getElementById("chatlist");
  
  var chatObject = document.createElement("div");
  chatObject.classList.add("chatobject")
  chatObject.innerText = "Chat " + name;
  
  chatList.appendChild(chatObject);
}

function sendPostRequest(path, json) {
  return fetch(backend + path, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(json)
  });
}

function sendMessageToServer(text) {
  sendPostRequest(
    "/send", {
      "message": text,
      "chat": 1
    })
    .then((response) => response.json())
    .then((json) => console.log(json));
}

const backend = "http://localhost:8000"
 
window.onload = function () {
  
  var form = document.getElementById("messagebox");
  form.addEventListener("submit", function (event) {
    event.preventDefault();
    
    var text = form.elements["text"].value;
    
    console.log(text);
    
    sendMessageToServer(text);
    
    form.elements["text"].value = "";
  })
  
  for (var i = 0; i < 200; i++) {
    addMessage("message " + i);
    addChat(i);
  }
  
  sendPostRequest("/chat", {"chat": 42})
    .then((response) => response.json())
    .then((json) => console.log(json));
}
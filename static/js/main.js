const chatMessages = document.getElementById("chat-messages");
const userInput = document.getElementById("user-input");
const sendButton = document.getElementById("send-button");
var dat;

function messageServer() {
    const url = '/main/mess'; // Replace with your server URL

    // Define the JSON data you want to send
    const jsonData = {
        'message': userInput.value.trim()
    };

    // Create the request options
    const requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(jsonData), // Stringify the JSON data
    };
    document.getElementById("gm").style.display = 'inherit'
    fetch(url, requestOptions)
        .then(response => response.json())
        .then(data => {
            // Handle the response data here
            console.log('Response:', data);
            dat = data;
            addMessage(data.response, 'server')
            document.getElementById("gm").style.display = 'none'
        })
        .catch(error => {
            // Handle any errors that occurred during the request
            console.error('Error:', error);
        });
}

function addMessage(message, uos) {
    const chatMessage = document.createElement("div");
    chatMessage.className = uos + "-message";
    chatMessage.innerHTML = message;

    // Append the message to the chat-messages container
    chatMessages.appendChild(chatMessage);

    // Clear the input field
    userInput.value = "";

    // Scroll to the bottom of the chat-messages container
    chatMessages.scrollTop = chatMessages.scrollHeight;
}
document.addEventListener("DOMContentLoaded", function() {


    sendButton.addEventListener("click", function() {
        const messageText = userInput.value.trim();

        if (messageText !== "") {
            messageServer();
            // Create a new chat message element
            addMessage(messageText, 'user')

        }
    });

    // Function to handle pressing the Enter key
    userInput.addEventListener("keydown", function(event) {
        if (event.key === "Enter") {
            event.preventDefault(); // Prevents a newline in the input field
            sendButton.click(); // Trigger a click on the send button
        }
    });
});
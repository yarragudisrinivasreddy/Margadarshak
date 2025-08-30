/* Time */
var deviceTime = document.querySelector('.status-bar .time');
var messageTime = document.querySelectorAll('.message .time');

deviceTime.innerHTML = moment().format('h:mm');
setInterval(function() {
    deviceTime.innerHTML = moment().format('h:mm');
}, 1000);

for (var i = 0; i < messageTime.length; i++) {
    messageTime[i].innerHTML = moment().format('h:mm A');
}

/* Message */
var form = document.querySelector('.conversation-compose');
var conversation = document.querySelector('.conversation-container');

form.addEventListener('submit', newMessage);

function newMessage(e) {
    e.preventDefault();
    var input = e.target.input;

    if (input.value) {
        // Append user message
        var message = buildMessage(input.value, "sent");
        conversation.appendChild(message);
        animateMessage(message);

        // Send to backend
        fetch("/chat", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({message: input.value})
        })
        .then(res => res.json())
        .then(data => {
			// Preserve line breaks from AI response
			let formattedReply = data.reply.replace(/\n/g, "<br>");

			// Append AI reply
			var reply = buildMessage(formattedReply, "received");
			conversation.appendChild(reply);
			animateMessage(reply);
			conversation.scrollTop = conversation.scrollHeight;
		})

        .catch(err => {
            var errorMsg = buildMessage("⚠️ Error contacting server", "received");
            conversation.appendChild(errorMsg);
        });
    }

    input.value = '';
    conversation.scrollTop = conversation.scrollHeight;
}

function buildMessage(text, type) {
    var element = document.createElement('div');
    element.classList.add('message', type);

    element.innerHTML = text +
        '<span class="metadata">' +
            '<span class="time">' + moment().format('h:mm A') + '</span>' +
        '</span>';

    return element;
}

function animateMessage(message) {
    setTimeout(function() {
        var tick = message.querySelector('.tick');
        if (tick) tick.classList.remove('tick-animation');
    }, 500);
}

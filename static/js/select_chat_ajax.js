let chats = document.getElementsByClassName("one_of_chats");
// set event on every chat
for (let i=0; i < chats.length; i++) { 
    let chat = chats[i];
    chat.addEventListener("click", () => {
        let chat_id = chat.id;
        // get selected chat data 
        $.ajax({
            url: "/chat/" + chat_id,
            type: "GET",
            dataType: "html",
            // display selected chat data 
            success: function(data) {
                $("div.messages").replaceWith(data);
            },
            // when displayed do this
            complete: function() {
                // change uri to match displayed chat
                window.history.replaceState({} , 'chat' + chat_id, '/home/' + chat_id);
                // scroll to the end of chat when displayed
                var msgs_field = document.getElementById("messages");
                msgs_field.scrollTop = msgs_field.scrollHeight;
            }
        });
    });
}
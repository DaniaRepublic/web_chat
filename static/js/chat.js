function check_input() {
    var msg = document.getElementById("message").value;
    if ((msg.replace(/ /g, '') != '') && msg) {
        return true;
    }
    return false;
}

$(document).ready(function () {
    $("form").submit(function (event) {
        
        event.preventDefault();
        
        if (check_input()) {
            $.ajax({
                type: "POST",
                url: window.location.pathname,
                data: $("#message").serialize(),
                success: function(data) {
                    $("div.messages").append(data);
                    var msgs_field = document.getElementById("messages");
                    msgs_field.scrollTop = msgs_field.scrollHeight;
                },
                complete: function() {
                    $("#message").val("");
                }
            });
        }
    
    });
  });
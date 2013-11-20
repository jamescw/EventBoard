var inbox = new ReconnectingWebSocket("ws://" + location.host + "/receive");

inbox.onmessage = function (message) {
    var data = JSON.parse(message.data);
    $("#events").append(
        "<div class='alert alert-"+ data.type +" alert-dismissable'>" +
            "<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;</button>" +
            "<strong>" + data.source + "</strong>: &nbsp;" + $('<span/>').text(data.message).html() +
        "</div>");
    $("#events").stop().animate({
        scrollTop: $('#events')[0].scrollHeight
    }, 800);
};

inbox.onclose = function () {
    console.log('inbox closed');
    this.inbox = new WebSocket(inbox.url);

};

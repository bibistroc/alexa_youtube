function gogo(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/log');

    var re = /(^.{24})([^ ]+)\s+(.*)$/gm
    //receive details from server
    socket.on('content', function(msg) {
        $('#log').append(msg.content.replace(re, '<div><date>$1</date><type>$2</type><message>$3</message></div>'));
    });

    setInterval(function(){
        console.log('get more');
        socket.emit('getMore');
    }, 3000);
}

$(function(){
    setTimeout(gogo, 3000)
});
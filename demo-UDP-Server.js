var PORT = 33333;
var HOST = '192.168.4.6';
var dgram = require('dgram');
var server = dgram.createSocket('udp4');
var logname = "/new_user/" + Date.now() + "log.txt"
var fs = require('fs');
var logger = fs.createWriteStream(logname, {
flags: 'a' // 'a'
});


server.on('listening', function () {
    var address = server.address();
    console.log('UDP Server listening on ' + address.address + ":" + address.port);
});

server.on('message', function (message, remote) {
    console.log(remote.address + ':' + remote.port +' - ' + message);
logger.write(Date.now() + "," + message +"\n")
});

server.bind(PORT, HOST);

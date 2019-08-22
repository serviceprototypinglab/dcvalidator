const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const webSocketsServerPort = 8000;
const webSocketServer = require('ws');
const http = require('http');
// Spinning the http server and the websocket server.
const server = http.createServer(app);
const port = process.env.PORT || 5000;
// server.listen(webSocketsServerPort);
const wsServer = new webSocketServer.Server({
  server
});
server.listen(webSocketsServerPort, () => {
  console.log(`Listening on port ${webSocketsServerPort}`)
  wsServer.on('request', request => {
    var userID = getUniqueID();
    console.log((new Date()) + ' Recieved a new connection from origin ' + request.origin + '.');
    // You can rewrite this part of the code to accept only the requests from allowed origin
    const connection = request.accept(null, request.origin);
    clients[userID] = connection
    console.log('connected: ' + userID + ' in ' + Object.getOwnPropertyNames(clients))
  });
});




app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.get('/api/hello', (req, res) => {
  res.send({ express: 'Hello From Express' });
  // wsServer.on('request', function(req) {
  //   var userID = getUniqueID();
  //   console.log((new Date()) + ' Recieved a new connection from origin ' + req.origin + '.');
  //   // You can rewrite this part of the code to accept only the requests from allowed origin
  //   const connection = req.accept(null, req.origin);
  //   clients[userID] = connection;
  //   console.log('connected: ' + userID + ' in ' + Object.getOwnPropertyNames(clients))
  // });
});

app.post('/api/world', (req, res) => {
  console.log(req.body); 
  res.send(
    `I received your POST request. This is what you sent me: ${req.body.post}`,
  );
});
app.post('/api/wsServer', (req, res) => { 
  // var request = req
  res.send(
    'got ya!'
  );
  console.log(req)
  //  wsServer.on('request', (request) => {
  //   var userID = getUniqueID();
  //   console.log('WASAAAAP!')
  //   console.log((new Date()) + ' Recieved a new connection from origin ' + request.origin + '.');
  //   // You can rewrite this part of the code to accept only the requests from allowed origin
  //   const connection = request.accept(null, request.origin);
  //   clients[userID] = connection;
  //   console.log('connected: ' + userID + ' in ' + Object.getOwnPropertyNames(clients))
  // });
});
// I'm maintaining all active connections in this object
const clients = {};

// This code generates unique userid for everyuser.
const getUniqueID = () => {
  const s4 = () => Math.floor((1 + Math.random()) * 0x10000).toString(16).substring(1);
  return s4() + s4() + '-' + s4();
};

wsServer.on('request', function(request) {
  var userID = getUniqueID();
  console.log((new Date()) + ' Recieved a new connection from origin ' + request.origin + '.');
  // You can rewrite this part of the code to accept only the requests from allowed origin
  const connection = request.accept(null, request.origin);
  clients[userID] = connection;
  console.log('connected: ' + userID + ' in ' + Object.getOwnPropertyNames(clients))
});

// app.listen(port, () => console.log(`Listening on port ${port}`));
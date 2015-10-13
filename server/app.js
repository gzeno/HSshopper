// Server scriptor Node.js

var express = require('express');
var cookieParser = require('cookie-parser');
//var bodyParser = require('body-parser');
var session = require('cookie-session');


var app = express();
	
//app.use(bodyParser.json());
app.use(cookieParser('somekindofkey'));
app.use(session({
	name: 'session',
	keys: ['key1', 'key2']
}));
app.use(express.static('res'));

// Functions

// get session name
function getName(req, res) {
	return
}


app.get('/', function(req,res){
	res.sendFile(__dirname+"/res/html/home.html");
});

app.listen(3000);

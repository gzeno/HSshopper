// Server scriptor Node.js

var express = require('express');
var cookieParser = require('cookie-parser');
//var bodyParser = require('body-parser');
var session = require('cookie-session');
var pg = require('pg');
var routes = require('./routes/index');

var app = express();


// Config
app.set('views', path.join(__dirname, '/res/views'));
app.set('view engine', 'jade');

app.use()
	
//app.use(bodyParser.json());
app.use(cookieParser('somekindofkey'));
app.use(session({
	name: 'session',
	keys: ['key1', 'key2']
}));
app.use(express.static('res'));
var cString = 'postgres://user:pass@localhost:5432/dbname';
/*
pg.connect(cString, function(err, client, done) {
	if (err) {
		return console.error('error fetching client from pool',err);
	}
	client.query('SELECT name from school WHERE numstudents > 1000', function(err, res) {
		done();

		if (err) {
			return console.error('error running query', err);
		}
		console.log(res);
	});
});
*/
// Functions

// get session name
function getName(req, res) {
	return
}

// Search results
function getSearchRes(req, res) {
	pg.connect(cString, function(err, client, done) {
		if (err) {
			return console.error('error fetching client from pool', err);
		}
		client.query('SELECT name from school WHERE name = '+req.params.query, function(err, resp) {
			done();
			if (err) {
				return console.error('error running query', err);
			}
			console.log(resp);
		});
	});
}


// ROUTES (See below or res/routes/index.js)

app.get('/', function(req,res){
	res.sendFile(__dirname+"/res/html/home.html");
});
app.get('/search-results/:query', function(req,res) {
	res.sendFile(__dirname+"/res/html/search-results.html");
});
app.get('/search/:query', function(req, res) {

});
app.post()

app.listen(3000);

// Javascript for home page to send 

$(document).ready(function(){
	$('#search-btn').on('click', function(event) {
		event.preventDefault();
		var searchQuery = $('#query').val();
		//console.log(searchQuery);
		// Parse search query
		var i;
		var sterm = "";
		var capNextLetter = false;
		for (i=0;i<searchQuery.length;i+=1) {
			if (searchQuery[i] === " "){
				capNextLetter = true;
			}
			else if (capNextLetter) {
				console.log(searchQuery.charAt(i).toUpperCase());
				sterm = sterm+ searchQuery.charAt(i).toUpperCase();
				capNextLetter = false;
			}
			else {
				sterm = sterm+ searchQuery.charAt(i);
			}

		}
		//console.log(sterm);
		window.location.href = window.location.hostname+"/search-results/" +sterm;

	});
});
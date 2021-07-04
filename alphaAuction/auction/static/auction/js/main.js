function setTimer(beg, end) {
	var x = setInterval(function() {
		var timer = $("#timer");
		var now = new Date().getTime();
		var diff = beg - now;
		var pref = "Starts in: ";
		if (diff < 0) {
			diff = end - now;
			pref = "Ends in: ";
			if (diff < 0) {
				clearInterval(x);
				timer.text("EXPIRED");
				return;
			}
		}
		
		// Time calculations for days, hours, minutes and seconds
		var day = Math.floor(diff / (1000 * 60 * 60 * 24));
		var hr = ("0" + Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))).slice(-2);
		var min = ("0" + Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60))).slice(-2);
		var sec = ("0" + Math.floor((diff % (1000 * 60)) / 1000)).slice(-2);
		
		timer.text(pref + (day > 0 ? day + " days, " : "") + hr + ":" + min + ":" + sec);
	}, 1000);
}

/*
// Old Image Slider:
	var slideIndex = 1;
	showDivs(slideIndex);

	function plusDivs(n) {
		showDivs(slideIndex += n);
	}

	function currentDiv(n) {
		showDivs(slideIndex = n);
	}

	function showDivs(n) {
		var i;
		var x = document.getElementsByClassName("mySlides");
		var dots = document.getElementsByClassName("demo");
		if (n > x.length) {slideIndex = 1}
		if (n < 1) {slideIndex = x.length}
		for (i = 0; i < x.length; i++) {
			x[i].style.display = "none";
		}
		for (i = 0; i < dots.length; i++) {
			dots[i].className = dots[i].className.replace(" red", "");
		}
		x[slideIndex-1].style.display = "block";
		dots[slideIndex-1].className += " red";
	}

// Old Grid Generator:
	// returns card div for item
	function itemCard(item, cols) {
		if (cols == 1) {
			return $('<div class="row no-gutters">\n' +
				'<div class="col-md-2">\n' +
				'<img src="' + item.ref + '" class="card-img my-3" alt="thumbnail">\n</div>\n' +
				'<div class="col-md">\n<div class="card-body">\n' +
				'<h5 class="card-title">' + item.title + '</h5>\n' +
				'<p class="card-text">' + item.desc + '</p>\n' +
				'<p class="card-text">' + item.cost + '</p>\n' +
				'<a href="#" class="btn btn-primary">Bid</a>\n' +
				'</div>\n</div>\n</div>');
		}
		else {
			return $('<img class="card-img-top pt-3" src="' + item.ref + '" alt="Card image">\n' +
			'<div class="card-body px-1 py-3">\n' +
			'<h5 class="card-title p-0">' + item.title + '</h5>\n' +
			(cols < 5 ? '<p class="card-text">' + item.desc + '</p>\n' : '') +
			'<p class="card-text">' + item.cost + '</p>\n' +
			'<a href="#" class="btn btn-primary">Bid</a>\n' +
			'</div>');
		}
		return card;
	}

	// adds item grid to main
	function addGrid(cols, total) {
		var main = $(".main");
		main.html("")
		for (var i = 0; i < total / cols; ++i) {
			var row = $('<div class="row"></div>');
			main.append(row);
			for (var j = 0; j < cols; ++j) {
				var col = $('<div class="col-sm card m-1"></div>');
				col.append(itemCard(new Sample(i * cols + j + 1), cols));
				row.append(col);
			}
		}
	}

Old Style:
	// Get the elements with class="column"
	var elements = document.getElementsByClassName("column");

	// Declare a loop variable
	var i;

	// List View
	function listView() {
		for (i = 0; i < elements.length; i++) {
			elements[i].style.width = "100%";
		}
	}

	// Grid View
	function gridView() {
		for (i = 0; i < elements.length; i++) {
			elements[i].style.width = "50%";
		}
	}

	// Optional: Add active class to the current button (highlight it)
	var container = document.getElementById("btnContainer");
	var btns = container.getElementsByClassName("btn");
	for (var i = 0; i < btns.length; i++) {
		btns[i].addEventListener("click", function() {
			var current = document.getElementsByClassName("active");
			current[0].className = current[0].className.replace(" active", "");
			this.className += " active";
		});
	}
	var x = setInterval(function() {
		var countDownDate = new Date("Feb 28, 2020 15:37:25").getTime();
		// Get today's date and time
		var now = new Date().getTime();

		// Find the distance between now and the count down date
		var distance = countDownDate - now;

		// Time calculations for days, hours, minutes and seconds
		var days = Math.floor(distance / (1000 * 60 * 60 * 24));
		var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
		var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
		var seconds = Math.floor((distance % (1000 * 60)) / 1000);

		// Output the result in an element with id="demo"
		document.getElementById("time").innerHTML = "Bid Time Remaining: " + days + "d " + hours + "h "
			+ minutes + "m " + seconds + "s ";

		// If the count down is over, write some text
		if (distance < 0) {
			clearInterval(x);
			document.getElementById("time").innerHTML = "EXPIRED";
		}
	}, 1000);
*/

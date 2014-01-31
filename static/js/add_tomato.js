String.prototype.format = String.prototype.f = function() {
    var s = this,
        i = arguments.length;

    while (i--) {
        s = s.replace(new RegExp('\\{' + i + '\\}', 'gm'), arguments[i]);
    }
    return s;
};

/*
  Author: Kai Kang
  *** This is all hardcode right now !!! */
var number_of_tomato = 0;

function preload(arrayOfImages) {
    $(arrayOfImages).each(function(){
	$("<img/>")[0].src = this;
	});
    }

var img0 = "static/img/0.png";
var img1 = "static/img/1.png";
var img2 = "static/img/2.png";
var img3 = "static/img/3.png";
var img4 = "static/img/4.png";
var img5 = "static/img/5.png";

preload([img0, img1, img2, img3, img4, img5]);

var changeImage = function(number_of_tomato) {
    switch(number_of_tomato){
    case 0:
	$("#image1 img")("src", img0);
	break;
    case 1:
	$("#image1 img").attr("src", img1);
	break;
    case 2:
	$("#image1 img").attr("src", img2);
	break;
    case 3:
	$("#image1 img").attr("src", img3);
	break;
    case 4:
	$("#image1 img").attr("src", img4);
	break;
    case 5:
	$("#image1 img").attr("src", img5);
	break;
    default:
	break;
    }}

var addTomato = function() {
    if (number_of_tomato != 5) {
	number_of_tomato += 1;}
    changeImage(number_of_tomato);
}

var minusTomato = function() {
    if (number_of_tomato != 0) {
	number_of_tomato -= 1;}
    changeImage(number_of_tomato);
}

var addNode = function() {
    number = 0;
    var task_html = '<li>\
      <form class="navbar-form navbar-left" role="search">\
	<div id="image{0}" class="panel panel-danger">\
	  <div class="panel-heading"><h3 class="panel-title">Fundamentals of Cooking</h3></div>\
	  <div class="panel-body">\
	  <img src="static/img/{0}.png" />\
	  <span id="add_tomato" class="btn-group">\
	    <button type="button" class="btn btn-default" >+</button>\
	  </span>\
	  <span id="minus_tomato">\
	    <button type="button" class="btn btn-default" >-</button>\
	  </span>\
	  <span id="task_text">\
	    Specify Task Content:\
	  </span>\
	  <input type="text"></input>\
	  </div>\
	</div>\
      </form>\
    </li>'.format(number);
    var task = $(task_html);
    $(".space").append(task);
}

$(document).ready( function() {
    $("#image1 button").first().on('click', addTomato);
    $("#image1 button").last().on('click', minusTomato);
})

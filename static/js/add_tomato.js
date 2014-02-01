/*
  Author: Kai Kang
  *** This is all hardcode right now !!! */

String.prototype.format = String.prototype.f = function() {
    var s = this,
        i = arguments.length;

    while (i--) {
        s = s.replace(new RegExp('\\{' + i + '\\}', 'gm'), arguments[i]);
    }
    return s;
};

function addNumberOfNodes(){
    number_of_nodes += 1;
}

function preload(arrayOfImages) {
    $(arrayOfImages).each(function(){
	$("<img/>")[0].src = this;
	});
    }

var number_of_tomato = [];
var number_of_nodes = 0;
var img0 = "static/img/0.png";
var img1 = "static/img/1.png";
var img2 = "static/img/2.png";
var img3 = "static/img/3.png";
var img4 = "static/img/4.png";
var img5 = "static/img/5.png";
var colors = ["primary", "danger", "success", "warning"]; //Hongyu will update this
// Preload all the images
preload([img0, img1, img2, img3, img4, img5]);

var changeImage = function(number_of_tomato, order_of_task) {
    var objToChange = "#image{0} img".format(order_of_task)
    switch(number_of_tomato[order_of_task]){
    case 0:
	$(objToChange).attr("src", img0);
	break;
    case 1:
	$(objToChange).attr("src", img1);
	break;
    case 2:
	$(objToChange).attr("src", img2);
	break;
    case 3:
	$(objToChange).attr("src", img3);
	break;
    case 4:
	$(objToChange).attr("src", img4);
	break;
    case 5:
	$(objToChange).attr("src", img5);
	break;
    default:
	break;
    }}

var addTomato = function(event) {
    if (number_of_tomato[event.data.number] != 5) {
	number_of_tomato[event.data.number] += 1;}
    changeImage(number_of_tomato, event.data.number);
}

var minusTomato = function(event) {
    if (number_of_tomato[event.data.number] != 0) {
	number_of_tomato[event.data.number] -= 1;}
    changeImage(number_of_tomato, event.data.number);
}

var addNode = function(number) {
    var task_html = '<li>\
      <form class="navbar-form navbar-left" role="search">\
	<div id="image{0}" class="panel {1}">\
	  <div class="panel-heading"><h3 class="panel-title">Fundamentals of Cooking</h3></div>\
	  <div class="panel-body">\
	  <img src="static/img/0.png" />\
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
    </li>'.format(number, "panel-"+colors[number%colors.length]);
    var task = $(task_html);
    $(".space").append(task);
}

var detectClick = function(order_of_task) {
    // order_of_task can be 0 - 5
    var a = "#image{0} button".format(order_of_task);
    $(a).first().on('click', {number:order_of_task}, addTomato);
    $(a).last().on('click', {number:order_of_task}, minusTomato);
}

$(document).ready( function() {
    for (var i =0; i < number_of_nodes; i++) {
	detectClick(i);
	number_of_tomato.push(0);
    }
})

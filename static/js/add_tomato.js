/*
  Author: Kai Kang */
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

var number_of_tomato = []; // stores as a 2-D list
var name_of_nodes = [];
var all_subtasks = [];  // stores as a 2-D list
var number_of_nodes = 0;  // number of tasks
var img0 = "static/img/0.png";
var img1 = "static/img/1.png";
var img2 = "static/img/2.png";
var img3 = "static/img/3.png";
var img4 = "static/img/4.png";
var img5 = "static/img/5.png";
var colors = ["blue", "red", "green", "yellow", "lightblue"]; //Hongyu will update this
// Preload all the images
preload([img0, img1, img2, img3, img4, img5]);

var addName = function(name){
    name_of_nodes.push(name);
}

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
	<div id="image{0}" class="panel {1}">\
	  <div class="panel-heading"><h3 class="panel-title" id="title{0}">{2}</h3></div>\
	  <div class="panel-body">\
	  <img src="static/img/0.png" />\
	  <span id="add_tomato" class="btn-group">\
	    <button type="button" class="btn btn-default" >+</button>\
	  </span>\
	  <span id="minus_tomato">\
	    <button type="button" class="btn btn-default" >-</button>\
	  </span>\
	  <span id="task_text">\
	    Specify Subtask Content:\
	  </span>\
	  <input type="text"></input>\
	  </div>\
	</div>\
    </li>'.format(number, "panel-"+colors[number%colors.length], name_of_nodes[number]);
    var task = $(task_html);
    $(".space").append(task);
}

var changeTitle= function(number, new_title) {
    // change the title to something
    var text = "#title{0}".format(number);
    $(text).html(new_title);
}

var addSubtask = function(event) {
    // add subtask to all_subtasks
    var task_content_text = "#image{0} input".format(event.data.number);
    var task_content = $(task_content_text).val()
    all_subtasks[event.data.number].push(task_content);
    $(task_content_text).val("");
}

var minusSubtask = function(event) {
    // pop subtask to all_subtasks
    all_subtasks[event.data.number].pop()
}

var detectClick = function(order_of_task) { // when a button is clicked
    // order_of_task can be 0 - 5
    var a = "#image{0} button".format(order_of_task);
    $(a).first().on('click', {number:order_of_task}, addTomato);
    $(a).first().on('click', {number:order_of_task}, addSubtask);
    $(a).last().on('click', {number:order_of_task}, minusTomato);
    $(a).last().on('click', {number:order_of_task}, minusSubtask)
}

var storeData = function(){
    localStorage.number_of_tomato = JSON.stringify( number_of_tomato );
    localStorage.all_subtasks = JSON.stringify( all_subtasks );
    localStorage.names = JSON.stringify( name_of_nodes );
}

$(document).ready( function() {
    for (var i =0; i < number_of_nodes; i++) {
	detectClick(i);
	all_subtasks.push([]);
	number_of_tomato.push(0);
	changeTitle(i, name_of_nodes[i]);
    }
    $("#show").on('click', storeData);
})

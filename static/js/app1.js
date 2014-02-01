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

var number_of_tomato;
var all_subtasks;
var name_of_nodes;
var current_task = 0;
var current_subtask = 0;
var clock;
var current_status = 1; // 1 is working; 0 is taking a break

var work_duration = 5; // in seconds
var rest_duration = 3;


var process = function(l, indices) {
    var result = [];
    for (var i =0; i< indices.length; i++) {
	result.push(l[indices[i]]);
    }
    return result;
}

var getData = function() {
    // get only non-empty data
    var nonEmptyIndices = [];
    pre_number_of_tomato = JSON.parse(localStorage.number_of_tomato);
    for (var i=0; i<pre_number_of_tomato.length; i++) {
	if (pre_number_of_tomato[i] != 0) {
	    nonEmptyIndices.push(i);
	}
    }
    number_of_tomato = process(pre_number_of_tomato, nonEmptyIndices);
    pre_name_of_nodes = JSON.parse(localStorage.names);
    name_of_nodes = process(pre_name_of_nodes, nonEmptyIndices); // keep non-empty
    pre_all_subtasks = JSON.parse(localStorage.all_subtasks);
    all_subtasks = process(pre_all_subtasks, nonEmptyIndices);
}

var create_list_group_item = function() {
    // create the list of the left
    var a = 0;
    for (var i =0; i<number_of_tomato.length; i++) {
	if ( number_of_tomato[i] != 0) {
	    var text_1 = '<a class="list-group-item" id="task{0}">'.format(a);

	    var text_2 = '<span class="badge pull-right">{0}</span>'.format(number_of_tomato[i]);
	    var text_3 = '{0}</a>'.format(name_of_nodes[i]);
	    a += 1;
	    $('#list_group').append($(text_1+text_2+text_3));}
    }
}

var activate = function(task_number){
    var task_to_act_text = '#task{0}'.format(task_number);
    $(task_to_act_text).attr('class', 'list-group-item active');
}

var deactivate = function(task_number){
    var task_to_act_text = '#task{0}'.format(task_number);
    $(task_to_act_text).attr('class', 'list-group-item');
}

var create_mainLabel = function(task_number, subtask_number) {
    var label_text = "{0}-{1}".format(name_of_nodes[task_number], subtask_number+1);
    // var obj_text = '<div class="panel-heading" style="font-size:30px;">{0}</div>'.format(label_text);
    $(".panel-heading").html(label_text);
}

var create_description = function(task_number, subtask_number) {
    var description = all_subtasks[task_number][subtask_number];
    if (description.length > 0) {
	$("h4").html(description);
    }
}

var labelViaRest = function() {
    var label_text = "You can take a break";
    $(".panel-heading").html(label_text);
}

var descriptionViaRest = function() {
    $("h4").html(" ");
}

var make_finish_button = function() {
    $("#button-group a").first().attr("class", "btn btn-success");
    $("#button-group a").first().attr("href", "/finish");
    $("#button-group a").first().html("Finish");
    $("#button-group a").last().remove();
}

var next_task_button = function() {
    //TODO
    var max_possible_subtasks = all_subtasks[current_task].length;
    if ( current_subtask < max_possible_subtasks-1 ) {
	current_subtask += 1;
    }
    else { // finished the current task
	if (current_task < name_of_nodes.length-1) {
	    current_task += 1;
	    current_subtask = 0;
	    activate(current_task);
	    if (current_task != 0) { deactivate(current_task-1);}
	}
    }
    create_mainLabel(current_task, current_subtask);
    create_description(current_task, current_subtask);
    if (current_task == name_of_nodes.length-1) {
	// the last task
	// test if the current sub task is the last sub task
	var max = all_subtasks[current_task].length;
	if (current_subtask == max-1) {
	    make_finish_button();
	}
    }
}

var give_up_button = function() {
    1+1;
}

var clock_stop = function(){
    if (current_task == name_of_nodes.length-1) {
	var max = all_subtasks[current_task].length;
	if (current_subtask == max-1) {
	    clock.stop();
	}
    }
    current_status = 1- current_status; // change status
    activate(current_task);
    if (current_task != 0) { deactivate(current_task-1);}
    if ( current_status == 0 ) {
	// taking a break
	clock.setTime(rest_duration);
	clock.start();
	labelViaRest();
	descriptionViaRest();
    }
    else {
	clock.setTime(work_duration);
	clock.start();
	next_task_button();
    }
}

$(document).ready( function() {
    getData();
    create_list_group_item();
    activate(0);
    create_mainLabel(current_task, current_subtask);
    // next-task button
    $("#button-group a").first().on('click', next_task_button);
    // Give up button
    $("#button-group a").last().on('click', give_up_button);
    clock = $(".clock").FlipClock(5, {
		clockFace: 'MinuteCounter',
		countdown: true,
		callbacks: {
		stop: function() {
		    clock_stop();
		}
		}
		});
})

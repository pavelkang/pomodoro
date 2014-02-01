var number_of_tomato;
var all_subtasks;

var getData = function() {
    number_of_tomato = JSON.parse(localStorage.number_of_tomato);
    all_subtasks = JSON.parse(localStorage.all_subtasks);
}

$(document).ready( function() {
    getData();
})

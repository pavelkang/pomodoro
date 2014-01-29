$(document).ready(
)
function add_number() {
    var adder1 = parseInt($("#add1").val());
    var adder2 = parseInt($("#add2").val());
    $("h2").text((adder1+adder2).toString());
};

function alert_hello() {
	alert('Hello world');
};

function changeText() {
    $("h2").text("This is the new text");
    }

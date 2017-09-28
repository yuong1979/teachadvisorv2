// function showflashMessage(message) {
// 	var template = "<div class='container container-alert-flash'>" +
// 	"<div class='col-sm-3 col-sm-offset-8'>" + 
// 	"<div class='alert alert-success alert-dismissible' role='alert'>" + 
// 	"<button type='button' class='close' data-dismiss='alert' aria-label='Close'>" +
// 	"<span aria-hidden='true'>&times;</span></button>" + 
// 	+ message + "</div></div></div>"
// 	$("body").append(template);
// 	setTimeout(function(){
// 		$("container-alert-flash").fadeIn();	
// 	}, 1)
// }


function showFlashMessage(message) {
	// var template = "{% include 'alert.html' with message='" + message + "' %}"
	var template = "<div class='container container-alert-flash'>" + 
	"<div class='col-sm-3 col-sm-offset-8'> " + 
	"<div class='alert alert-success alert-dismissible' role='alert'>" + 
	"<button type='button' class='close' data-dismiss='alert' aria-label='Close'>" +
	"<span aria-hidden='true'>&times;</span></button>" 
	+ message + "</div></div></div>"
	$("body").append(template);
	$(".container-alert-flash").fadeIn();
	setTimeout(function(){ 
		$(".container-alert-flash").fadeOut();
	}, 1800);

}


$(document).ready(function () {

     $('#navbar.navbar-collapse').on('show.bs.collapse', function () {
         $("html, body").addClass('no-scroll');
         $("#navbar-button .icon-bar").addClass('hidden');
         $("#navbar-button span.close-btn").removeClass('hidden');
         $("#navbar-button").blur();
     });

     $('#navbar.navbar-collapse').on('hide.bs.collapse', function () {
         $("html, body").removeClass('no-scroll');
         $("#navbar-button .icon-bar").removeClass('hidden');
         $("#navbar-button span.close-btn").addClass('hidden');
         $("#navbar-button").blur();
     });


});
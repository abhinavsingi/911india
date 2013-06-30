jQuery(document).ready(function($) {
	
	$("#add-experience").hide();
	$("#add-education").hide();

	$("#add-experience-trigger").bind('mousedown', function(event) {
		$("#add-experience").slideDown("slow");
		$("#add-experience-trigger").hide();
	});
	
	$("#add-education-trigger").bind('mousedown', function(event) {
		$("#add-education").slideDown("slow");
		$("#add-education-trigger").hide();
	});

	$("#add-experience-trigger2").bind('mousedown', function(event) {
		$("#add-experience").slideUp("slow");
		$("#add-experience-trigger").show();
	});

	$("#add-education-trigger2").bind('mousedown', function(event) {
		$("#add-education").slideUp("slow");
		$("#add-education-trigger").show();
	});
});

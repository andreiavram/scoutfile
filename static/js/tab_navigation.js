/**
 * 	Javascript for handling bootstrap tabs and ajax calls to their urls 
 * 	Andrei AVRAM, FITX
 * 
 */


jQuery("document").ready(function () {
	jQuery("#nav-menu li a").click(function (event) {
		event.preventDefault();

		var tab_id = jQuery(this).attr("href");
		var target = jQuery(this).attr("tab-link");
		
		jQuery.get(target, function(data) {
			jQuery(tab_id).html(data);
		});
		
		
		jQuery(this).tab('show');
	});
	
	//	First tab - active on page show, triggering manually
	
	var tab_id = jQuery("#nav-menu li.active a").attr("href");
	var target = jQuery("#nav-menu li.active a").attr("tab-link");
	
	jQuery.get(target, function(data) {
		jQuery(tab_id).html(data);
	});
	
	jQuery("#nav-menu li.active a").tab('show');
	
});

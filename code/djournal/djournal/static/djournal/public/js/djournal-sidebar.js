jQuery(function(){
	jQuery('.date-sidebar-year').click(function() {
		jQuery(this).next().slideToggle();
		jQuery(this).toggleClass("date-sidebar-year-collapsed").toggleClass("date-sidebar-year-expanded");
		return false;
	});
});

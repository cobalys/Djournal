jQuery(function() {
	jQuery("#id_title").bind("keyup", function(event) {
	    if(event.keyCode === jQuery.ui.keyCode.TAB && jQuery(this).data("autocomplete").menu.active) {
	        event.preventDefault();
	    }
		jQuery("#id_slug").val(URLify(jQuery("#id_title").val(), 100));
	});
});
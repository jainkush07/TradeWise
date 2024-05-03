(function($){
	$(window).on("load",function(){
		$(".customScroller").mCustomScrollbar({
			theme:"minimal",
			mouseWheel:{
				enable: true,
			}
		});
	});
})(jQuery);
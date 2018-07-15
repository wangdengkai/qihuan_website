$(function(){
	$('.embedShow').delegate('li','mouseover',function(){
		$(this).children('ul').css('display','block');

	})
	$('.embedShow').delegate('li','mouseout',function(){
		$(this).children('ul').css('display','none');

	})
})
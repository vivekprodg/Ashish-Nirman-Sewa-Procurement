var rid = $('#rid').val();
if(rid != 0){
	$('#reservesel').val('/reserviour-session/'+rid+'/');
}

$('.detailbtn').click(function(){
	$('.edit_popupbanner').fadeIn();
	$('#edit_popup').css({"transform": "scale(1)", "opacity": "1"});
});
$('#closep_pop').click(function(){
	$('#edit_popup').css({"transform": "scale(.2)", "opacity": "0"});
	$('.edit_popupbanner').fadeOut();
});
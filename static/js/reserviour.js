$(document).on("wheel", "input[type=number]", function (e) {
    $(this).blur();
});
$('form input').on('keypress', function(e) {
    return e.which !== 13;
});

$(window).on('load', function(){
	if($('.msgon').length>0){
		var msg = $('.msgon').first().val();
		if(msg=='done'){
			$('.success_ban').show('slide', {direction: 'right'}, 500);
			setTimeout(function(){
				$('.success_ban').hide('slide', {direction: 'right'}, 500);
			}, 5000);
		}
		if(msg=='error'){
			$('.error_ban').show('slide', {direction: 'right'}, 500);
			setTimeout(function(){
				$('.error_ban').hide('slide', {direction: 'right'}, 500);
			}, 5000);
		}
	}
});

$('.inputs').click(function(){
	$(this).removeClass('errorcolor');
});
function url(){
  var name = $('#name').val();
  $('#url').val(name);
  var mat_url = $('#url').val().toLowerCase();
  var result = mat_url.replace(/[^a-z0-9\s]/gi, '').replace(/[_\s]/g, '');
  $('#url').val(result);
}
$('#name').on('keyup', function(){
	url();
});

$('#ReserviourForm').on('submit', function(){
	var error = 0;
	$('#spinner1').show();
	var name = $('input[name=name]').val();
	var site = $('#site option:selected').val();
	var location = $('#location').val();
	var opening = $('#opening').val();
	var capacity = $('input[name=capacity]').val();
	if(name==''){
		error = 1;
		$('#name').addClass('errorcolor');
	}
	if(site==''){
		error = 1;
		$('#site').addClass('errorcolor');
	}
	if(opening == ''){
		error = 1;
		$('#opening').addClass('errorcolor');
	}
	if(capacity == ''){
		error = 1;
		$('#capacity').addClass('errorcolor');
	}
	if(error==0){
		document.ReserviourForm.submit();
	}else{
		$('#spinner1').hide();
	}
	event.preventDefault();
});




//=========edit part--------------------
$('.sup_edit').click(function(){
	$('.edit_popupbanner').fadeIn();
	var idstr = $(this).attr("data");
	var name = $('#name'+idstr).val();
	var url = $('#url'+idstr).val();
	var location = $('#location'+idstr).val();
	var capacity = $('#capacity'+idstr).val();
	var opening = $('#opening'+idstr).val();
	var site = $('#site'+idstr).val();
	var stock = $('#stock'+idstr).val();
	$('#suid').val(idstr);
	$('#name').val(name);
	$('#url').val(url);
	if(location!='' && location!='None'){
		$('#location').val(location);
	}
	if(site!='' && site!='None'){
		$('#site').val(site);
	}
	$('#capacity').val(capacity);
	$('#opening').val(opening);
	$('#dopening').val(opening);
	$('#dstock').val(stock);
	$('#edit_popup').css({"transform": "scale(1)", "-webkit-transform": "scale(1)", "-moz-transform": "scale(1)"});
});
$('#close_edit').click(function(){
	$('#suid').val('');
	$('#name').val('');
	$('#url').val('');
	$('#location').val('');
	$('#opening').val('');
	$('#capacity').val('');
	$('#site').val('');
	$('#edit_popup').css({"transform": "scale(.1)", "-webkit-transform": "scale(.1)", "-moz-transform": "scale(.1)"});
	$('.edit_popupbanner').fadeOut();
});
$('.sup_delete').click(function(){
	$('.del_popupbanner').fadeIn();
	var idstr = $(this).attr("data");
	$('#sid').val(idstr);
	$('#del_popup').css({"transform": "scale(1)", "-webkit-transform": "scale(1)", "-moz-transform": "scale(1)"});
});
$('#cancel_btn').on('click', function(){
	$('#sid').val('');
	$('#del_popup').css({"transform": "scale(.1)", "-webkit-transform": "scale(.1)", "-moz-transform": "scale(.1)"});
	$('.del_popupbanner').fadeOut();
});

$('#ReserveEditForm').on('submit', function(){
	var error = 0;
	$('#spinner1').show();
	var name = $('input[name=name]').val();
	var site = $('#site option:selected').val();
	var location = $('#location').val();
	var opening = $('#opening').val();
	var capacity = $('input[name=capacity]').val();
	if(name==''){
		error = 1;
		$('#name').addClass('errorcolor');
	}
	if(site==''){
		error = 1;
		$('#site').addClass('errorcolor');
	}
	if(opening == ''){
		error = 1;
		$('#opening').addClass('errorcolor');
	}
	if(capacity == ''){
		error = 1;
		$('#capacity').addClass('errorcolor');
	}
	if(error==0){
		document.ReserveEditForm.submit();
	}else{
		$('#spinner1').hide();
	}
	event.preventDefault();
});

//===========================================
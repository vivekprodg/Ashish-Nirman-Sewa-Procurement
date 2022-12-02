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

$('#adcheck').click(function(){
	if($(this).prop("checked") == true){
		$('#admin_sta').val("admin");
	}else{
		$('#admin_sta').val("staff");
	}
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

$('#SiteForm').on('submit', function(){
	var error = 0;
	$('#spinner1').show();
	var name = $('input[name=name]').val();
	var url = $('input[name=url]').val();
	var address = $('input[name=address]').val();
	var pan = $('input[name=pan]').val();
	var contact = $('input[name=contact]').val();
	if(name=='' || url == ''){
		error = 1;
		$('#name').addClass('errorcolor');
	}
	if(address==''){
		error = 1;
		$('#address').addClass('errorcolor');
	}
	if(pan==''){
		error = 1;
		$('#pan').addClass('errorcolor');
	}
	if(contact == ''){
		error = 1;
		$('#contact').addClass('errorcolor');
	}
	if(error==0){
		document.SiteForm.submit();
	}else{
		$('#spinner1').hide();
	}
	event.preventDefault();
});
$('.sup_edit').click(function(){
	$('.edit_popupbanner').fadeIn();
	var idstr = $(this).attr("data");
	var name = $('#name'+idstr).val();
	var url = $('#url'+idstr).val();
	var address = $('#address'+idstr).val();
	var pan = $('#pan'+idstr).val();
	var contact = $('#contact'+idstr).val();
	var role = $('#role'+idstr).val();
	$('#suid').val(idstr);
	$('#name').val(name);
	$('#dname').val(name);
	$('#url').val(url);
	$('#address').val(address);
	$('#pan').val(pan);
	$('#contact').val(contact);
	$('#admin_sta').val(role);
	if(role == 'admin'){
		$('#adcheck').prop("checked", true);
	}
	if(role == 'staff'){
		$('#adcheck').prop("checked", false);
	}
	$('#edit_popup').css({"transform": "scale(1)", "-webkit-transform": "scale(1)", "-moz-transform": "scale(1)"});
});
$('#close_edit').click(function(){
	$('#suid').val('');
	$('#name').val('');
	$('#dname').val('');
	$('#url').val('');
	$('#address').val('');
	$('#contact').val('');
	$('#pan').val('');
	$('#admin_sta').val('');
	$('#adcheck').prop("checked", false);
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
$('.usup_delete').click(function(){
	$('.udel_popupbanner').fadeIn();
	var idstr = $(this).attr("data");
	$('#ssid').val(idstr);
	$('#udel_popup').css({"transform": "scale(1)", "-webkit-transform": "scale(1)", "-moz-transform": "scale(1)"});
});
$('#ucancel_btn').on('click', function(){
	$('#ssid').val('');
	$('#udel_popup').css({"transform": "scale(.1)", "-webkit-transform": "scale(.1)", "-moz-transform": "scale(.1)"});
	$('.udel_popupbanner').fadeOut();
});

$('#SiteEditForm').on('submit', function(){
	var error = 0;
	$('#spinner1').show();
	var name = $('#name').val();
	var url = $('#url').val();
	var address = $('#address').val();
	var pan = $('#pan').val();
	var role = $('#admin_sta').val();
	if(name=='' || url == ''){
		error = 1;
		$('#name').addClass('errorcolor');
	}
	if(address==''){
		error = 1;
		$('#address').addClass('errorcolor');
	}
	if(pan==''){
		error = 1;
		$('#pan').addClass('errorcolor');
	}
	if(contact==''){
		error = 1;
		$('#contact').addClass('errorcolor');
	}
	if(error==0){
		document.SiteEditForm.submit();
	}else{
		$('#spinner1').hide();
	}
	event.preventDefault();
});
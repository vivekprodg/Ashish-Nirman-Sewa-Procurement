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

$('#UserForm').on('submit', function(){
	var error = 0;
	$('#spinner1').show();
	var user_name = $('input[name=user_name]').val();
	var first_name = $('input[name=first_name]').val();
	var last_name = $('input[name=last_name]').val();
	var email = $('input[name=email]').val();
	var password1 = $('input[name=password1]').val();
	var password2 = $('input[name=password2]').val();
	var site = $('#site option:selected').val();
	var role = $('#role option:selected').val();
	if(user_name==''){
		error = 1;
		$('#user_name').addClass('errorcolor');
	}
	if(first_name==''){
		error = 1;
		$('#first_name').addClass('errorcolor');
	}
	if(last_name==''){
		error = 1;
		$('#last_name').addClass('errorcolor');
	}
	if(email == ''){
		error = 1;
		$('#email').addClass('errorcolor');
	}
	if(!IsEmail(email)){
		error = 1;
		$('#email').addClass('errorcolor');
	}
	if(site == ''){
		error = 1;
		$('#site').addClass('errorcolor');
	}
	if(role == ''){
		error = 1;
		$('#role').addClass('errorcolor');
	}
	if(password1 == ''){
		error = 1;
		$('#password1').addClass('errorcolor');
	}
	if(password2 == ''){
		error = 1;
		$('#password2').addClass('errorcolor');
	}
	if(password1 != password2){
		error = 1;
		$('#password1').addClass('errorcolor');
		$('#password2').addClass('errorcolor');
	}
	if(error==0){
		document.UserForm.submit();
	}else{
		$('#spinner1').hide();
	}
	event.preventDefault();
});

function isEmail(email) {
  var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
  return regex.test(email);
}

$('.sup_edit').click(function(){
	var idstr = $(this).attr("data");
	var user_name = $('#username'+idstr).val();
	var first_name = $('#first'+idstr).val();
	var last_name = $('#last'+idstr).val();
	var email = $('#email'+idstr).val();
	var site = $('#site'+idstr).val();
	var role = $('#role'+idstr).val();
	var user_id = $('#userid'+idstr).val();
	$('#user_name').val(user_name);
	$('#first_name').val(first_name);
	$('#last_name').val(last_name);
	$('#email').val(email);
	$('#site').val(site);
	$('#role').val(role);
	$('#user_id').val(user_id);
	$('#uid').val(idstr);
	$('.edit_popupbanner').fadeIn();
	$('#edit_popup').css({"transform": "scale(1)", "-webkit-transform": "scale(1)", "-moz-transform": "scale(1)"});
});
$('#close_edit').click(function(){
	$('#user_name').val('');
	$('#first_name').val('');
	$('#last_name').val('');
	$('#email').val('');
	$('#site').val('');
	$('#role').val('');
	$('#user_id').val('');
	$('#uid').val('');
	$('#edit_popup').css({"transform": "scale(.1)", "-webkit-transform": "scale(.1)", "-moz-transform": "scale(.1)"});
	$('.edit_popupbanner').fadeOut();
});
$('.sup_delete').click(function(){
	$('.del_popupbanner').fadeIn();
	var idstr = $(this).attr("data");
	$('#uid2').val(idstr);
	var user_id = $('#userid'+idstr).val();
	$('#user_id2').val(user_id);
	$('#del_popup').css({"transform": "scale(1)", "-webkit-transform": "scale(1)", "-moz-transform": "scale(1)"});
});
$('.usup_delete').click(function(){
	$('.udel_popupbanner').fadeIn();
	var idstr = $(this).attr("data");
	$('#uuid2').val(idstr);
	var user_id = $('#userid'+idstr).val();
	$('#uuser_id2').val(user_id);
	$('#udel_popup').css({"transform": "scale(1)", "-webkit-transform": "scale(1)", "-moz-transform": "scale(1)"});
});
$('#cancel_btn').on('click', function(){
	$('#uid2').val('');
	$('#user_id2').val('');
	$('#del_popup').css({"transform": "scale(.1)", "-webkit-transform": "scale(.1)", "-moz-transform": "scale(.1)"});
	$('.del_popupbanner').fadeOut();
});
$('#ucancel_btn').on('click', function(){
	$('#uuid2').val('');
	$('#uuser_id2').val('');
	$('#udel_popup').css({"transform": "scale(.1)", "-webkit-transform": "scale(.1)", "-moz-transform": "scale(.1)"});
	$('.udel_popupbanner').fadeOut();
});

$('#chng_pass').click(function(){
	$('.password_change').fadeIn();
	var idstr = $('#user_name').val();
	$('#user').val(idstr);
	$('.password_cover').css({"transform": "scale(1)", "-webkit-transform": "scale(1)", "-moz-transform": "scale(1)"});
});
$('#close_pass').click(function(){
	$('#user_id1').val('');
	$('.password_change').fadeOut();
	$('.password_cover').css({"transform": "scale(.1)", "-webkit-transform": "scale(.1)", "-moz-transform": "scale(.1)"});
});

$('#ChangePassword').on('submit', function(){
	$('#spinner1').show();
	var pwd1 = $('#password1').val();
	var pwd2 = $('#password2').val();
	if(pwd1 != '' && pwd2 != ''){
		if(pwd1==pwd2){
			document.ChangePassword.submit();
		}else{
			$('#spinner1').hide();
			$('#password2').addClass('errorcolor');
			$('#password1').addClass('errorcolor');
		}
	}else{
		$('#spinner1').hide();
		$('#password2').addClass('errorcolor');
		$('#password1').addClass('errorcolor');
	}
	event.preventDefault();
});

$('#UserEditForm').on('submit', function(){
	var error = 0;
	$('#spinner1').show();
	var user_name = $('input[name=user_name]').val();
	var first_name = $('input[name=first_name]').val();
	var last_name = $('input[name=last_name]').val();
	var email = $('input[name=email]').val();
	var site = $('#site option:selected').val();
	var role = $('#role option:selected').val();
	if(user_name==''){
		error = 1;
		$('#user_name').addClass('errorcolor');
	}
	if(first_name==''){
		error = 1;
		$('#first_name').addClass('errorcolor');
	}
	if(last_name==''){
		error = 1;
		$('#last_name').addClass('errorcolor');
	}
	if(email == ''){
		error = 1;
		$('#email').addClass('errorcolor');
	}
	if(!IsEmail(email)){
		error = 1;
		$('#email').addClass('errorcolor');
	}
	if(site == ''){
		error = 1;
		$('#site').addClass('errorcolor');
	}
	if(role == ''){
		error = 1;
		$('#role').addClass('errorcolor');
	}
	if(error==0){
		document.UserEditForm.submit();
	}else{
		$('#spinner1').hide();
	}
	event.preventDefault();
});
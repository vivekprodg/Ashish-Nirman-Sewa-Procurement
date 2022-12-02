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
  var name = $('#problem').val();
  $('#url').val(name);
  var mat_url = $('#url').val().toLowerCase();
  var result = mat_url.replace(/[^a-z0-9\s]/gi, '').replace(/[_\s]/g, '');
  $('#url').val(result);
}
$('#problem').on('keyup', function(){
	url();
});
$('#ProblemForm').on('submit', function(){
	var error = 0;
	$('#spinner1').show();
	var name = $('#problem').val();
	var url = $('#url').val();
	if(name==''){
		error = 1;
		$('#problem').addClass('errorcolor');
	}
	if(url==''){
		error = 1;
		$('#problem').addClass('errorcolor');
	}
	if(error==0){
		document.ProblemForm.submit();
	}else{
		$('#spinner1').hide();
	}
	event.preventDefault();
});

$('.sup_edit').click(function(){
	var idstr = $(this).attr("data");
	var name = $('#name'+idstr).val();
	var url = $('#url'+idstr).val();
	$('#luid').val(idstr);
	$('#editname').val(name);
	$('#default').val(name);
	$('#editurl').val(url);
	$('.edit_popupbanner').fadeIn();
	$('#edit_popup').css({"transform": "scale(1)", "-webkit-transform": "scale(1)", "-moz-transform": "scale(1)"});
});
$('#close_edit').click(function(){
	$('#editname').val('');
	$('#editurl').val('');
	$('#default').val('');
	$('#edit_popup').css({"transform": "scale(.1)", "-webkit-transform": "scale(.1)", "-moz-transform": "scale(.1)"});
	$('.edit_popupbanner').fadeOut();
});

$('.sup_delete').click(function(){
	$('.del_popupbanner').fadeIn();
	var idstr = $(this).attr("data");
	$('#lid').val(idstr);
	$('#del_popup').css({"transform": "scale(1)", "-webkit-transform": "scale(1)", "-moz-transform": "scale(1)"});
});
$('#cancel_btn').on('click', function(){
	$('#lid').val('');
	$('#del_popup').css({"transform": "scale(.1)", "-webkit-transform": "scale(.1)", "-moz-transform": "scale(.1)"});
	$('.del_popupbanner').fadeOut();
});

function editurl(){
  var name = $('#editname').val();
  $('#editurl').val(name);
  var mat_url = $('#editurl').val().toLowerCase();
  var result = mat_url.replace(/[^a-z0-9\s]/gi, '').replace(/[_\s]/g, '');
  $('#editurl').val(result);
}
$('#editname').on('keyup', function(){
	editurl();
});

$('#ProblemEditForm').on('submit', function(){
	var error = 0;
	$('#spinner2').show();
	var name = $('#editname').val();
	var url = $('#editurl').val();
	if(name==''){
		error = 1;
		$('#editname').addClass('errorcolor');
	}
	if(url==''){
		error = 1;
		$('#editname').addClass('errorcolor');
	}
	if(error==0){
		document.ProblemEditForm.submit();
	}else{
		$('#spinner2').hide();
	}
	event.preventDefault();
});
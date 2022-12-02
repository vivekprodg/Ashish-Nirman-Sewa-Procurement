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

$('form input').on('keypress', function(e) {
    return e.which !== 13;
});

var date = document.getElementById("date");
if(date!=null){
	date.nepaliDatePicker({
	    readOnlyInput: true
	});
}

$('.inputs').click(function(){
	$(this).removeClass('errorcolor');
});

$('#cqcheck').click(function(){
	$('#chq').prop('checked', true);
	$('#cash').prop('checked', false);
	$('#trans').val('cheque');
	$('.bank').show();
});

$('#cacheck').click(function(){
	$('#chq').prop('checked', false);
	$('#cash').prop('checked', true);
	$('#trans').val('cash');
	$('.bank').hide();
});

$('#CreditPayForm').on('submit', function(){
	var error = 0;
	$('#spinner1').show();
	var date = $('#date').val();
	var amount = $('#amount').val();
	if(date==''){
		error = 1;
		$('#name').addClass('errorcolor');
	}
	if(amount==''){
		error = 1;
		$('#address').addClass('errorcolor');
	}
	if(error==0){
		document.CreditPayForm.submit();
	}else{
		$('#spinner1').hide();
	}
	event.preventDefault();
});
$('#addpay').click(function(){
	$('.edit_popupbanner').fadeIn();
	$('#edit_popup').css({"transform": "scale(1)", "-webkit-transform": "scale(1)", "-moz-transform": "scale(1)"});
});
$('#close_edit').on('click', function(){
	$('#edit_popup').css({"transform": "scale(.1)", "-webkit-transform": "scale(.1)", "-moz-transform": "scale(.1)"});
	$('.edit_popupbanner').fadeOut();
});
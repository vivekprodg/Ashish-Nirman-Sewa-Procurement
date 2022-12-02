var date = document.getElementById("date");
if(date!=null){
	date.nepaliDatePicker({
	    readOnlyInput: true
	});
}
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

$('#FuelPurchase').on('submit', function(){
	var error = 0;
	$('#spinner1').show();
	var purchase_number = $('#purchase_number').val();
	var pon = $('#pon').val();
	var reserviour = $('#reserviour option:selected').val();
	var issue_site = $('#issue_site').val();
	var quantity = $('#quantity').val();
	var rate = $('input[name=rate]').val();
	var amount = $('input[name=amount]').val();
	var date = $('input[name=date]').val();
	var location = $('input[name=location]').val();
	var fuel_type = $('#fuel_type option:selected').val();
	if(purchase_number=='' || pon==''){
		error = 1;
		$('#purchase_number').addClass('errorcolor');
	}
	if(issue_site==''){
		error = 1;
		$('#issue_site').addClass('errorcolor');
	}
	if(reserviour==''){
		error = 1;
		$('#reserviour').addClass('errorcolor');
	}
	if(date==''){
		error = 1;
		$('#date').addClass('errorcolor');
	}
	if(fuel_type==''){
		error = 1;
		$('#fuel_type').addClass('errorcolor');
	}
	if(error==0){
		document.FuelPurchase.submit();
	}else{
		$('#spinner1').hide();
	}
	event.preventDefault();
});

$('#quantity').on('keyup', function(){
	var val = $(this).val();
	if(val != ''){
		if(val > 0){
			val = parseFloat(val);
			var rate = $('#rate').val();
			if(rate != ''){
				if(rate > 0){
					rate = parseFloat(rate);
					var total = val * rate;
					total = parseFloat(total);
					total = total.toFixed(2);
					$('#amount').val(total);
					$('#rate').removeClass('errorcolor');
					$(this).removeClass('errorcolor');
				}else{
					$('#rate').addClass('errorcolor');
				}
			}else{
				$('#rate').addClass('errorcolor');
			}
		}else{
			$(this).addClass('errorcolor');
		}
	}else{
		$(this).addClass('errorcolor');
	}
});

$('#rate').on('keyup', function(){
	var val = $(this).val();
	if(val != ''){
		if(val > 0){
			val = parseFloat(val);
			var qty = $('#quantity').val();
			if(qty != ''){
				if(qty > 0){
					qty = parseFloat(qty);
					var total = val * qty;
					total = parseFloat(total);
					total = total.toFixed(2);
					$('#amount').val(total);
					$('#quantity').removeClass('errorcolor');
					$(this).removeClass('errorcolor');
				}else{
					$('#quantity').addClass('errorcolor');
				}
			}else{
				$('#quantity').addClass('errorcolor');
			}
		}else{
			$(this).addClass('errorcolor');
		}
	}else{
		$(this).addClass('errorcolor');
	}
});


//edition part ======================

var dfuel = $('#dfuel').val();
var dreserve = $('#dreserve').val();

if(dfuel!='' && dfuel!='None'){
	$('#fuel_type').val(dfuel);
}
if(dreserve!='' && dreserve!='None'){
	$('#reserviour').val(dreserve);
}

$('#FuelPurchase').on('submit', function(){
	var error = 0;
	$('#spinner1').show();
	var purchase_number = $('#purchase_number').val();
	var reserviour = $('#reserviour option:selected').val();
	var issue_site = $('#issue_site').val();
	var quantity = $('#quantity').val();
	var rate = $('input[name=rate]').val();
	var amount = $('input[name=amount]').val();
	var date = $('input[name=date]').val();
	var location = $('input[name=location]').val();
	var fuel_type = $('#fuel_type option:selected').val();
	if(purchase_number=='' || pon==''){
		error = 1;
		$('#purchase_number').addClass('errorcolor');
	}
	if(issue_site==''){
		error = 1;
		$('#issue_site').addClass('errorcolor');
	}
	if(reserviour==''){
		error = 1;
		$('#reserviour').addClass('errorcolor');
	}
	if(date==''){
		error = 1;
		$('#date').addClass('errorcolor');
	}
	if(fuel_type==''){
		error = 1;
		$('#fuel_type').addClass('errorcolor');
	}
	if(location=='None'){
		$('input[name=location]').val('');
	}
	if(error==0){
		document.FuelPurchase.submit();
	}else{
		$('#spinner1').hide();
	}
	event.preventDefault();
});


//=========fuel purchase detail js--------------------

//===========================================
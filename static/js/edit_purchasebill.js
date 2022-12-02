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

var pur_on = $('#purchase_number').val();
$('.purchaseorder_cover').show();
$('#pcover'+pur_on).show();

var vatd = $('#vatd').val();
if(vatd!='' && vatd!='None' && vatd!=0){
	$('#vatc').prop("checked", true);
	$('.vatfield').show();
	$('#vatval').val('yes');
}

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
					if($('#vatc').prop("checked") == true){
						var vat = total * 13/100;
						vat = parseFloat(vat);
						var gtot = total + vat;
						gtot = parseFloat(gtot);
						gtot = gtot.toFixed(2);
						vat = vat.toFixed(2);
						$('#vat').val(vat);
						$('#amount').val(gtot);
						$('#rate').removeClass('errorcolor');
						$(this).removeClass('errorcolor');
					}else{
						total = total.toFixed(2);
						$('#amount').val(total);
					}
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
					if($('#vatc').prop("checked") == true){
						var vat = total * 13/100;
						vat = parseFloat(vat);
						var gtot = total + vat;
						gtot = parseFloat(gtot);
						gtot = gtot.toFixed(2);
						vat = vat.toFixed(2);
						$('#vat').val(vat);
						$('#amount').val(gtot);
						$('#quantity').removeClass('errorcolor');
						$(this).removeClass('errorcolor');
					}else{
						total = total.toFixed(2);
						$('#amount').val(total);
					}
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

$('.vatcheck').click(function(){
	if($('#vatc').prop("checked") == true){
		$('#vatc').prop("checked", false);
		$('.vatfield').hide();
		$('#vatval').val('no');
		var qty = $('#quantity').val();
		var rate = $('#rate').val();
		if(qty != '' && rate != ''){
			if(qty > 0 && rate > 0){
				qty = parseFloat(qty);
				rate = parseFloat(rate);
				var total = rate * qty;
				total = parseFloat(total);
				total = total.toFixed(2);
				$('#vat').val('');
				$('#amount').val(total);
			}
		}
	}else{
		$('#vatc').prop("checked", true);
		$('.vatfield').show();
		$('#vatval').val('yes');
		var qty = $('#quantity').val();
		var rate = $('#rate').val();
		if(qty != '' && rate != ''){
			if(qty > 0 && rate > 0){
				qty = parseFloat(qty);
				rate = parseFloat(rate);
				var total = rate * qty;
				total = parseFloat(total);
				var vat = total * 13/100;
				vat = parseFloat(vat);
				var gtot = total + vat;
				gtot = parseFloat(gtot);
				gtot = gtot.toFixed(2);
				vat = vat.toFixed(2);
				$('#vat').val(vat);
				$('#amount').val(gtot);
			}
		}
	}
});

$('#vatc').click(function(){
	if($(this).prop("checked") == true){
		$(this).prop("checked", false);
		$('.vatfield').hide();
		$('#vatval').val('no');
		var qty = $('#quantity').val();
		var rate = $('#rate').val();
		if(qty != '' && rate != ''){
			if(qty > 0 && rate > 0){
				qty = parseFloat(qty);
				rate = parseFloat(rate);
				var total = rate * qty;
				total = parseFloat(total);
				total = total.toFixed(2);
				$('#vat').val('');
				$('#amount').val(total);
			}
		}
	}else{
		$(this).prop("checked", true);
		$('.vatfield').show();
		$('#vatval').val('yes');
		var qty = $('#quantity').val();
		var rate = $('#rate').val();
		if(qty != '' && rate != ''){
			if(qty > 0 && rate > 0){
				qty = parseFloat(qty);
				rate = parseFloat(rate);
				var total = rate * qty;
				total = parseFloat(total);
				var vat = total * 13/100;
				vat = parseFloat(vat);
				var gtot = total + vat;
				gtot = parseFloat(gtot);
				gtot = gtot.toFixed(2);
				vat = vat.toFixed(2);
				$('#vat').val(vat);
				$('#amount').val(gtot);
			}
		}
	}
});

var porder = 0;
$('#purchase_number').on('keyup', function(){
	var val = $(this).val();
	val = val.toUpperCase();
	$('.purchaseorder_cover').show();
	$('.jobload').show();
	$('.jobload').empty();
	$('.purchaseorder_ban').hide();
	var mystr = 'Loading...';
	$('.jobload').append(mystr);
	$('#pon').val('');
	$('#quantity').val('');
	$('#rate').val('');
	$('#amount').val('');
	porder = 1;
	if($('#pcover'+val).length > 0){
		var sta = $('#postatus'+val).val();
		if(sta=='approved'){
			$('.jobload').hide();
			$('#pcover'+val).show();
			$('#pon').val(val);
			porder = 0;
			var qty = $('#poqty'+val).val();
			var rate = $('#porate'+val).val();
			var amt = $('#poamt'+val).val();
			if(qty != '' && rate != '' && amt != '' && qty != null && rate != null && amt != null){
				$('#quantity').val(qty);
				$('#rate').val(rate);
				$('#amount').val(amt);
			}
		}else{
			$('.jobload').empty();
			var mystr = 'Provided purchase order number "'+val+'" is not approved!';
			$('.jobload').append(mystr);
		}
	}
	if($('#pcover'+val).length == 0){
		$('.jobload').empty();
		var mystr = 'No match found';
		$('.jobload').append(mystr);
		$('#pon').val('');
	}

});

$('#PurchaseBillAdd').on('submit', function(){
	var error = 0;
	$('#spinner1').show();
	var date = $('input[name=date]').val();
	if(date==''){
		error=1;
		$('#date').addClass('errorcolor');
	}
	var ponnum = $('input[name=pon]').val();
	if(ponnum=='' && porder == 0){
		error=1;
		$('#purchase_number').addClass('errorcolor');
	}

	var qty = $('#quantity').val();
	if(qty=='' || qty < 0){
		error=1;
		$('#quantity').addClass('errorcolor');
	}
	var rate = $('#rate').val();
	if(rate=='' || rate < 0){
		error=1;
		$('#rate').addClass('errorcolor');
	}
	var amt = $('#amount').val();
	if(amt=='' || amt < 0){
		error=1;
		$('#amount').addClass('errorcolor');
	}

	if(error==0){
		document.PurchaseBillAdd.submit();
	}else{
		$('#spinner1').hide();
	}

	
	event.preventDefault();
});
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
$('#reserviour').on('change', function(){
	var idstr = $('#reserviour option:selected').val();
	var vname = $('#reserve'+idstr).val();
	$('#reserviour_name').val(vname);
});

$('#LickageForm').on('submit', function(){
	var error = 0;
	$('#spinner1').show();
	var consump_num = $('#consump_number').val();
	var pon = $('#pvn_count').val();
	var reserviour = $('#reserviour option:selected').val();
	var quantity = $('#quantity').val();
	var date = $('input[name=date]').val();
	var fuel_type = $('#fuel_type option:selected').val();
	if(consump_num=='' || pon==''){
		error = 1;
		$('#consump_number').addClass('errorcolor');
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
	if(quantity==''){
		error = 1;
		$('#quantity').addClass('errorcolor');
	}
	if(error==0){
		document.LickageForm.submit();
	}else{
		$('#spinner1').hide();
	}
	event.preventDefault();
});



//edition part ======================

var dfuel = $('#dftype').val();
var dreserve = $('#dreserve').val();

if(dfuel!='' && dfuel!='None'){
	$('#fuel_type').val(dfuel);
}
if(dreserve!='' && dreserve!='None'){
	$('#reserviour').val(dreserve);
}

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

$('#FuelTransfer').on('submit', function(){
	var error = 0;
	$('#spinner1').show();
	var fuel_number = $('#fuel_number').val();
	var pon = $('#pon').val();
	var freserviour = $('#freserviour option:selected').val();
	var treserviour = $('#treserviour option:selected').val();
	var quantity = $('#quantity').val();
	var fuel_type = $('#fuel_type option:selected').val();
	if(fuel_number=='' || pon==''){
		error = 1;
		$('#fuel_number').addClass('errorcolor');
	}
	if(freserviour==''){
		error = 1;
		$('#freserviour').addClass('errorcolor');
	}
	if(treserviour==''){
		error = 1;
		$('#treserviour').addClass('errorcolor');
	}
	if(treserviour==freserviour){
		error = 1;
		$('#treserviour').addClass('errorcolor');
		$('#freserviour').addClass('errorcolor');
	}
	if(date==''){
		error = 1;
		$('#date').addClass('errorcolor');
	}
	if(fuel_type==''){
		error = 1;
		$('#fuel_type').addClass('errorcolor');
	}
	if(quantity=='' || quantity==0 || quantity<0){
		error = 1;
		$('#quantity').addClass('errorcolor');
	}
	if(error==0){
		document.FuelTransfer.submit();
	}else{
		$('#spinner1').hide();
	}
	event.preventDefault();
});


//edition part ======================

var dfuel = $('#dfuel').val();
var dfreserve = $('#dfreserve').val();
var dtreserve = $('#dtreserve').val();

if(dfuel!='' && dfuel!='None'){
	$('#fuel_type').val(dfuel);
}
if(dfreserve!='' && dfreserve!='None'){
	$('#freserviour').val(dfreserve);
}
if(dtreserve!='' && dtreserve!='None'){
	$('#treserviour').val(dtreserve);
}



//=========fuel purchase detail js--------------------

//===========================================
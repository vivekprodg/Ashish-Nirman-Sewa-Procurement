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

function url(vehi_num){
  var mat_url = vehi_num.toLowerCase();
  var result = mat_url.replace(/[^a-z0-9\s]/gi, '').replace(/[_\s]/g, '');
  return result;
}

$('#vehicle_type').on('change', function(){
	var idstr = $('#vehicle_type option:selected').val();
	var vname = $('#vtypename'+idstr).val();
	$('#vehicle_type_name').val(vname);
	$('.vehicles').hide();
	if($('#chasis_check').prop("checked") == true){
		$('#vehitypechasisid'+idstr).show();
	}else if($('#engine_check').prop("checked") == true){
		$('#vehitypeengineid'+idstr).show();
	}else{
		$('#vehitypenumid'+idstr).show();
	}
});
$('#chasis_check').on('click', function(){
	$('.vehicles').hide();
	var idstr = $('#vehicle_type option:selected').val();
	if($('#chasis_check').prop("checked")==true){
		$('#engine_check').prop("checked",false);
		if(idstr!=''){
			var val = $('#vtypename'+idstr).val();
			$('#vehitypechasisid'+idstr).show();
		}
	}else{
		if(idstr!=''){
			var val = $('#vtypename'+idstr).val();
			$('#vehitypenumid'+idstr).show();
		}
	}
	
});
$('#engine_check').on('click', function(){
	$('.vehicles').hide();
	var idstr = $('#vehicle_type option:selected').val();
	if($('#engine_check').prop("checked")==true){
		$('#chasis_check').prop("checked",false);
		if(idstr!=''){
			var val = $('#vtypename'+idstr).val();
			$('#vehitypeengineid'+idstr).show();
		}
	}else{
		if(idstr!=''){
			var val = $('#vtypename'+idstr).val();
			$('#vehitypenumid'+idstr).show();
		}
	}
	
});
$('.vchoice').on('change', function(){
	var idstr = $(this).attr("id");
	var val = $('#'+idstr+' option:selected').val();
	$('.vehidet').show();
	var vnum = url(val);
	if($('#vh'+vnum).length>0){
		var vh = $('#vh'+vnum).val();
		var vhc = $('#vh'+vnum).attr("name");
		var vhe = $('#vh'+vnum).attr("data");
		$('#vehidetnum').text(vh);
		$('#vehidetchasis').text(vhc);
		$('#vehidetengine').text(vhe);
	}
	if($('#vhc'+vnum).length>0){
		var vh = $('#vhc'+vnum).attr("name");
		var vhc = $('#vhc'+vnum).val();
		var vhe = $('#vhc'+vnum).attr("data");
		$('#vehidetnum').text(vh);
		$('#vehidetchasis').text(vhc);
		$('#vehidetengine').text(vhe);
	}
	if($('#vhe'+vnum).length>0){
		var vh = $('#vhe'+vnum).attr("data");
		var vhc = $('#vhe'+vnum).attr("name");
		var vhe = $('#vhe'+vnum).val();
		$('#vehidetnum').text(vh);
		$('#vehidetchasis').text(vhc);
		$('#vehidetengine').text(vhe);
	}
});
$('#reserviour').on('change', function(){
	var idstr = $('#reserviour option:selected').val();
	var vname = $('#reserve'+idstr).val();
	$('#reserviour_name').val(vname);
});
var pbill = 0;
$('#coupon').blur(function(){
	var val = $(this).val();
	pbill = 0;
	$('.couponlist').each(function(){
		var cha = $(this).val();
		if(val == cha){
			pbill = 1;
			$('#coupon').addClass('errorcolor');
			$('.coupon_error').show();
		}
	});
});
$('#coupon').click(function(){
	$('.coupon_error').hide();
});

$('#FuelForm').on('submit', function(){
	var error = 0;
	$('#spinner1').show();
	var consump_num = $('#consump_number').val();
	var pon = $('#pvn_count').val();
	var reserviour = $('#reserviour option:selected').val();
	var coupon = $('#coupon').val();
	var quantity = $('#quantity').val();
	var vehicle_type = $('#vehicle_type option:selected').val();
	var kilometer = $('#kilometer').val();
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
	if(coupon=='' || pbill == 1){
		error = 1;
		$('#coupon').addClass('errorcolor');
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
	if(kilometer==''){
		error = 1;
		$('#kilometer').addClass('errorcolor');
	}
	var idstr = $('#vehicle_type option:selected').val();
	var vehicle = '';
	if($('#chasis_check').prop("checked") == true){
		var vehicle = $('#vehi_chasis'+idstr+' option:selected').val();
		if(vehicle==''){
			error = 1;
			$('#vehi_chasis'+idstr).addClass('errorcolor');
		}else{
			$('#vehicle_confirm').val(vehicle);
		}
		$('#num_type').val('chasis');
	}else if($('#engine_check').prop("checked") == true){
		var vehicle = $('#vehi_engine'+idstr+' option:selected').val();
		if(vehicle==''){
			error = 1;
			$('#vehi_engine'+idstr).addClass('errorcolor');
		}else{
			$('#vehicle_confirm').val(vehicle);
		}
		$('#num_type').val('engine');
	}else{
		var vehicle = $('#vehi_number'+idstr+' option:selected').val();
		if(vehicle==''){
			error = 1;
			$('#vehi_number'+idstr).addClass('errorcolor');
		}else{
			$('#vehicle_confirm').val(vehicle);
		}
		$('#num_type').val('vehicle');
	}
	if(error==0){
		document.FuelForm.submit();
	}else{
		$('#spinner1').hide();
	}
	event.preventDefault();
});



//edition part ======================

var dfuel = $('#dftype').val();
var dreserve = $('#dreserve').val();
var dvtype = $('#dvtype').val();
var dvtypeid = $('#dvtypeid').val();
var dvehi = $('#dvnum').val();
var dnumtype = $('#dnumtype').val();

if(dfuel!='' && dfuel!='None'){
	$('#fuel_type').val(dfuel);
}
if(dreserve!='' && dreserve!='None'){
	$('#reserviour').val(dreserve);
}
if(dvtypeid!='' && dvtypeid !='None'){
	$('#vehicle_type').val(dvtypeid);
}
if(dnumtype!='' && dnumtype != 'None'){
	$('.vehidet').show();
	var vnum = url(dvehi);
	if(dnumtype=='chasis'){
		$('#vehitypechasisid'+dvtypeid).show();
		$('#vehi_chasis'+dvtypeid).val(dvehi);
		$('#chasis_check').prop("checked", true);
		var vh = $('#vhc'+vnum).attr("name");
		var vhc = $('#vhc'+vnum).val();
		var vhe = $('#vhc'+vnum).attr("data");
		$('#vehidetnum').text(vh);
		$('#vehidetchasis').text(vhc);
		$('#vehidetengine').text(vhe);
	}
	if(dnumtype=='engine'){
		$('#vehitypeengineid'+dvtypeid).show();
		$('#vehi_engine'+dvtypeid).val(dvehi);
		$('#engine_check').prop("checked", true);
		var vh = $('#vhe'+vnum).attr("data");
		var vhc = $('#vhe'+vnum).attr("name");
		var vhe = $('#vhe'+vnum).val();
		$('#vehidetnum').text(vh);
		$('#vehidetchasis').text(vhc);
		$('#vehidetengine').text(vhe);
	}
	if(dnumtype=='vehicle'){
		$('#vehitypenumid').show();
		$('#vehi_number'+dvtypeid).val(dvehi);
		$('#chasis_check').prop("checked", false);
		$('#engine_check').prop("checked", false);
		var vh = $('#vh'+vnum).val();
		var vhc = $('#vh'+vnum).attr("name");
		var vhe = $('#vh'+vnum).attr("data");
		$('#vehidetnum').text(vh);
		$('#vehidetchasis').text(vhc);
		$('#vehidetengine').text(vhe);
	}
}

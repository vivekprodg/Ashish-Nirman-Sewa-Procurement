var date = document.getElementById("date");
if(date!=null){
	date.nepaliDatePicker({
	    readOnlyInput: true
	});
}
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
	var val = $('#vtypename'+idstr).val();
	$('.vehicles').hide();
	$('#vtype').val(val);
	$('#vtypeidd').val(idstr);
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

$('#VehicleForm').on('submit', function(){
	var error = 0;
	$('#spinner1').show();
	var froms = $('#issue_locate').val();
	var tos = $('#site option:selected').val();
	var mnum = $('#mid').val();

	if(mnum==''){
		error = 1;
		$('#mid').addClass('errorcolor');
	}
	if(froms==''){
		error = 1;
		$('#issue_locate').addClass('errorcolor');
	}
	if(tos==''){
		error = 1;
		$('#site').addClass('errorcolor');
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
		document.VehicleForm.submit();
	}else{
		$('#spinner1').hide();
	}
	event.preventDefault();
});

$('.sup_edit').click(function(){
	$('.edit_popupbanner').fadeIn();
	var idstr = $(this).attr("data");
	var vehi = $('#dvehinum'+idstr).val();
	var date = $('#ddate'+idstr).val();
	var fromsite = $('#dfsite'+idstr).val();
	var tosite = $('#dtsite'+idstr).val();
	var vtype = $('#vtype'+idstr).val();
	var vtypeid = $('#vtypeid'+idstr).val();
	var numtype = $('#dntype'+idstr).val();
	var mnum = $('#dfnum'+idstr).val();
	$('#suid').val(idstr);
	$('#date').val(date);
	$('#vtype').val(vtype);
	$('#vtypeidd').val(vtypeid);
	$('#vehicle_type').val(vtypeid);
	$('#vehicle_confirm').val(vehi);
	$('#num_type').val(numtype);
	$('#issue_locate').val(fromsite);
	$('#site').val(tosite);
	$('#mid').val(mnum);
	if(numtype=='engine'){
		$('#engine_check').prop("checked", true);
		$('#vehitypeengineid'+vtypeid).show();
		$('#vehi_engine'+vtypeid).val(vehi);
	}
	if(numtype=='chasis'){
		$('#chasis_check').prop("checked", true);
		$('#vehitypechasisid'+vtypeid).show();
		$('#vehi_chasis'+vtypeid).val(vehi);
	}
	if(numtype=='vehicle'){
		$('#chasis_check').prop("checked", false);
		$('#engine_check').prop("checked", false);
		$('#vehitypenumid'+vtypeid).show();
		$('#vehi_number'+vtypeid).val(vehi);
	}

	$('.vehidet').show();
	var vnum = url(vehi);
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
	
	$('#edit_popup').css({"transform": "scale(1)", "-webkit-transform": "scale(1)", "-moz-transform": "scale(1)"});
});
$('#close_edit').click(function(){
	$('#suid').val('');
	$('#date').val('');
	$('#vtype').val('');
	$('#vtypeidd').val('');
	$('#vehicle_type').val('');
	$('#vehicle_confirm').val('');
	$('#num_type').val('');
	$('#issue_locate').val('');
	$('#site').val('');
	$('#chasis_check').prop("checked", false);
	$('#engine_check').prop("checked", false);
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
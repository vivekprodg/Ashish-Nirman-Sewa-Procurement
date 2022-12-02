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
  var name = $('#vehicle_number').val();
  $('#vehi_url').val(name);
  var mat_url = $('#vehi_url').val().toLowerCase();
  var result = mat_url.replace(/[^a-z0-9\s]/gi, '').replace(/[_\s]/g, '');
  $('#vehi_url').val(result);
}
function chasis_url(){
  var name = $('#chasis_number').val();
  $('#chasis_url').val(name);
  var mat_url = $('#chasis_url').val().toLowerCase();
  var result = mat_url.replace(/[^a-z0-9\s]/gi, '').replace(/[_\s]/g, '');
  $('#chasis_url').val(result);
}
function engine_url(){
  var name = $('#engine_number').val();
  $('#engine_url').val(name);
  var mat_url = $('#engine_url').val().toLowerCase();
  var result = mat_url.replace(/[^a-z0-9\s]/gi, '').replace(/[_\s]/g, '');
  $('#engine_url').val(result);
}
$('#vehicle_number').on('keyup', function(){
	url();
});
$('#chasis_number').on('keyup', function(){
	chasis_url();
});
$('#engine_number').on('keyup', function(){
	engine_url();
});

$('#vehicle_type').on('change', function(){
	var idstr = $('#vehicle_type option:selected').val();
	var vname = $('#vttype'+idstr).val();
	$('#vehicle_type_name').val(vname);
});
$('.vtypeclass').on('change', function(){
	var idstr = $(this).attr("id");
	var ids = $(this).attr("data");
	var val = $('#'+idstr+' option:selected').val();
	var vname = $('#vttype'+val).val();
	$('#vtypename'+ids).val(vname);
});

$('#VehicleForm').on('submit', function(){
	var error = 0;
	$('#spinner1').show();
	var vehi_number = $('input[name=vehicle_number]').val();
	var chasis = $('input[name=chasis_number]').val();
	var engine = $('input[name=engine_number]').val();
	var vehicle_type = $('#vehicle_type option:selected').val();
	var vehicle_type_name = $('#vehicle_type_name').val();
	var owner = $('#owner_name').val();
	var driver = $('#driver_name').val();
	var helper = $('#helper_name').val();
	var capacity = $('#capacity').val();
	var contact = $('#contact1').val();
	if(vehi_number==''){
		error = 1;
		$('#vehicle_number').addClass('errorcolor');
	}
	if(chasis==''){
		error = 1;
		$('#chasis_number').addClass('errorcolor');
	}
	if(engine==''){
		error = 1;
		$('#engine_number').addClass('errorcolor');
	}
	if(contact == ''){
		error = 1;
		$('#contact1').addClass('errorcolor');
	}
	if(error==0){
		document.VehicleForm.submit();
	}else{
		$('#spinner1').hide();
	}
	event.preventDefault();
});

// $('#driver_select').on('change', function(){
// 	var val = $('#driver_select option:selected').val();
// 	var drive = $('#drive'+val).val();
// 	$('#driver_name').val(drive);
// });
// $('#helper_select').on('change', function(){
// 	var val = $('#helper_select option:selected').val();
// 	var help = $('#help'+val).val();
// 	$('#helper_name').val(help);
// });

$('.sup_edit').click(function(){
	$('.edit_popupbanner').fadeIn();
	var idstr = $(this).attr("data");
	var vehi = $('#dvehinum'+idstr).val();
	var url = $('#durl'+idstr).val();
	var chasis_url = $('#dchurl'+idstr).val();
	var engine_url = $('#denurl'+idstr).val();
	var engine = $('#dengine'+idstr).val();
	var chasis = $('#dchasis'+idstr).val();
	var capacity = $('#dcapa'+idstr).val();
	var owner = $('#downer'+idstr).val();
	var driver = $('#ddriver'+idstr).val();
	var helper = $('#dhelper'+idstr).val();
	var contact1 = $('#dcon1'+idstr).val();
	var contact2 = $('#dcon2'+idstr).val();
	var vtypeid = $('#vtypeid'+idstr).val();
	var vtype = $('#vtype'+idstr).val();
	$('#suid').val(idstr);
	$('#vehicle_number').val(vehi);
	$('#vehi_url').val(url);
	$('#chasis_url').val(chasis_url);
	$('#engine_url').val(engine_url);
	$('#chasis_number').val(chasis);
	$('#engine_number').val(engine);
	$('#contact1').val(contact1);
	$('#vehicle_type_name').val(vtype);
	$('#vehicle_type').val(vtypeid);
	$('#defaultvehi').val(vehi);
	$('#defaultchasis').val(chasis);
	$('#defaultengine').val(engine);
	if(owner!='' && owner != 'None'){
		$('#owner_name').val(owner);
	}
	if(driver!='' && driver != 'None'){
		$('#driver_name').val(driver);
	}
	if(helper!='' && helper != 'None'){
		$('#helper_name').val(helper);
	}
	if(capacity!='' && capacity != 'None'){
		$('#capacity').val(capacity);
	}
	if(contact2!='' && contact2 != 'None'){
		$('#contact2').val(contact2);
	}
	$('#edit_popup').css({"transform": "scale(1)", "-webkit-transform": "scale(1)", "-moz-transform": "scale(1)"});
});
$('#close_edit').click(function(){
	$('#suid').val('');
	$('#vehicle_number').val('');
	$('#vehi_url').val('');
	$('#chasis_number').val('');
	$('#engine_number').val('');
	$('#contact1').val('');
	$('#contact2').val('');
	$('#owner_name').val('');
	$('#driver_name').val('');
	$('#helper_name').val('');
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
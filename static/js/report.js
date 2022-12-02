if($('.fromdate').length > 0){
	$('.fromdate').nepaliDatePicker({
		readOnlyInput: true
	});
}
if($('.todate').length > 0){
	$('.todate').nepaliDatePicker({
		readOnlyInput: true
	});
}

$('.report_btn').click(function(){
	var idstr = $(this).attr("data");
	$('.edit_popupbanner').fadeIn();
	$('.rep').css({"transform": "scale(.1)", "-webkit-transform": "scale(.1)", "-moz-transform": "scale(.1)"});
	$('.rep').hide();
	$('#'+idstr).show();
	$('#'+idstr).css({"transform": "scale(1)", "-webkit-transform": "scale(1)", "-moz-transform": "scale(1)"});
});

$('.close_edit').click(function(){
	var idstr = $(this).attr("data");
	$('.rep').css({"transform": "scale(.1)", "-webkit-transform": "scale(.1)", "-moz-transform": "scale(.1)"});
	$('#'+idstr).css({"transform": "scale(.1)", "-webkit-transform": "scale(.1)", "-moz-transform": "scale(.1)"});
	$('.edit_popupbanner').fadeOut();
});

$("#report_csv").on("click",function(){
	var idstr = $('#reporttab').val();
    $("#"+idstr).tableHTMLExport({
      type:'csv',
      filename:idstr+'.csv'
    });
});
$("#sup").on("change",function(){
	var idstr = $('#sup option:selected').val();
	var name = $('#sup'+idstr).val();
	$('#supname').val(name);
});

$('#vehicle_typefuel').on('change', function(){
	var idstr = $('#vehicle_typefuel option:selected').val();
	var vname = $('#vtypenamefuel'+idstr).val();
	$('#vehicle_type_namefuel').val(vname);
	$('.vehicles').hide();
	if($('#chasis_checkfuel').prop("checked") == true){
		$('#vehitypechasisidfuel'+idstr).show();
	}else if($('#engine_checkfuel').prop("checked") == true){
		$('#vehitypeengineidfuel'+idstr).show();
	}else{
		$('#vehitypenumidfuel'+idstr).show();
	}
});
$('#chasis_checkfuel').on('click', function(){
	$('.vehicles').hide();
	var idstr = $('#vehicle_typefuel option:selected').val();
	if($('#chasis_checkfuel').prop("checked")==true){
		$('#engine_checkfuel').prop("checked",false);
		if(idstr!=''){
			var val = $('#vtypenamefuel'+idstr).val();
			$('#vehitypechasisidfuel'+idstr).show();
		}
	}else{
		if(idstr!=''){
			var val = $('#vtypenamefuel'+idstr).val();
			$('#vehitypenumidfuel'+idstr).show();
		}
	}
	
});
$('#engine_checkfuel').on('click', function(){
	$('.vehicles').hide();
	var idstr = $('#vehicle_typefuel option:selected').val();
	if($('#engine_checkfuel').prop("checked")==true){
		$('#chasis_checkfuel').prop("checked",false);
		if(idstr!=''){
			var val = $('#vtypenamefuel'+idstr).val();
			$('#vehitypeengineidfuel'+idstr).show();
		}
	}else{
		if(idstr!=''){
			var val = $('#vtypenamefuel'+idstr).val();
			$('#vehitypenumidfuel'+idstr).show();
		}
	}
	
});

$('#vehicle_typemain').on('change', function(){
	var idstr = $('#vehicle_typemain option:selected').val();
	var vname = $('#vtypenamemain'+idstr).val();
	$('#vehicle_type_namemain').val(vname);
	$('.vehicles').hide();
	if($('#chasis_checkmain').prop("checked") == true){
		$('#vehitypechasisidmain'+idstr).show();
	}else if($('#engine_checkmain').prop("checked") == true){
		$('#vehitypeengineidmain'+idstr).show();
	}else{
		$('#vehitypenumidmain'+idstr).show();
	}
});
$('#chasis_checkmain').on('click', function(){
	$('.vehicles').hide();
	var idstr = $('#vehicle_typemain option:selected').val();
	if($('#chasis_checkmain').prop("checked")==true){
		$('#engine_checkmain').prop("checked",false);
		if(idstr!=''){
			var val = $('#vtypenamemain'+idstr).val();
			$('#vehitypechasisidmain'+idstr).show();
		}
	}else{
		if(idstr!=''){
			var val = $('#vtypenamemain'+idstr).val();
			$('#vehitypenumidmain'+idstr).show();
		}
	}
	
});
$('#engine_checkmain').on('click', function(){
	$('.vehicles').hide();
	var idstr = $('#vehicle_typemain option:selected').val();
	if($('#engine_checkmain').prop("checked")==true){
		$('#chasis_checkmain').prop("checked",false);
		if(idstr!=''){
			var val = $('#vtypenamemain'+idstr).val();
			$('#vehitypeengineidmain'+idstr).show();
		}
	}else{
		if(idstr!=''){
			var val = $('#vtypenamemain'+idstr).val();
			$('#vehitypenumidfmain'+idstr).show();
		}
	}
	
});


$('#VFForm').on('submit', function(){
	var idstr = $('#vehicle_typefuel option:selected').val();
	var vehicle = '';
	if($('#chasis_checkfuel').prop("checked") == true){
		var vehicle = $('#vehi_chasisfuel'+idstr+' option:selected').val();
		if(vehicle!=''){
			$('#vehicle_confirmfuel').val(vehicle);
			$('#num_typefuel').val('chasis');
		}
	}else if($('#engine_checkfuel').prop("checked") == true){
		var vehicle = $('#vehi_enginefuel'+idstr+' option:selected').val();
		if(vehicle!=''){
			$('#vehicle_confirmfuel').val(vehicle);
			$('#num_typefuel').val('engine');
		}
	}else{
		var vehicle = $('#vehi_numberfuel'+idstr+' option:selected').val();
		if(vehicle!=''){
			$('#vehicle_confirmfuel').val(vehicle);
			$('#num_typefuel').val('vehicle');
		}
	}
	document.VFForm.submit();
	event.preventDefault();
});

$('#VMForm').on('submit', function(){
	var idstr = $('#vehicle_typemain option:selected').val();
	var vehicle = '';
	if($('#chasis_checkmain').prop("checked") == true){
		var vehicle = $('#vehi_chasismain'+idstr+' option:selected').val();
		if(vehicle!=''){
			$('#vehicle_confirmmain').val(vehicle);
			$('#num_typemain').val('chasis');
		}
	}else if($('#engine_checkmain').prop("checked") == true){
		var vehicle = $('#vehi_enginemain'+idstr+' option:selected').val();
		if(vehicle!=''){
			$('#vehicle_confirmmain').val(vehicle);
			$('#num_typemain').val('engine');
		}
	}else{
		var vehicle = $('#vehi_numbermain'+idstr+' option:selected').val();
		if(vehicle!=''){
			$('#vehicle_confirmmain').val(vehicle);
			$('#num_typemain').val('vehicle');
		}
	}
	document.VMForm.submit();
	event.preventDefault();
});

$('#vehicle_typemove').on('change', function(){
	var idstr = $('#vehicle_typemove option:selected').val();
	var vname = $('#vtypenamemove'+idstr).val();
	$('#vehicle_type_namemove').val(vname);
	$('.vehicles').hide();
	if($('#chasis_checkmove').prop("checked") == true){
		$('#vehitypechasisidmove'+idstr).show();
	}else if($('#engine_checkmove').prop("checked") == true){
		$('#vehitypeengineidmove'+idstr).show();
	}else{
		$('#vehitypenumidmove'+idstr).show();
	}
});
$('#chasis_checkmove').on('click', function(){
	$('.vehicles').hide();
	var idstr = $('#vehicle_typemove option:selected').val();
	if($('#chasis_checkmove').prop("checked")==true){
		$('#engine_checkmove').prop("checked",false);
		if(idstr!=''){
			var val = $('#vtypenamemove'+idstr).val();
			$('#vehitypechasisidmove'+idstr).show();
		}
	}else{
		if(idstr!=''){
			var val = $('#vtypenamemove'+idstr).val();
			$('#vehitypenumidmove'+idstr).show();
		}
	}
	
});
$('#engine_checkmove').on('click', function(){
	$('.vehicles').hide();
	var idstr = $('#vehicle_typemove option:selected').val();
	if($('#engine_checkmove').prop("checked")==true){
		$('#chasis_checkmove').prop("checked",false);
		if(idstr!=''){
			var val = $('#vtypenamemove'+idstr).val();
			$('#vehitypeengineidmove'+idstr).show();
		}
	}else{
		if(idstr!=''){
			var val = $('#vtypenamemove'+idstr).val();
			$('#vehitypenumidfmove'+idstr).show();
		}
	}
	
});

$('#MoveForm').on('submit', function(){
	var idstr = $('#vehicle_typemove option:selected').val();
	var vehicle = '';
	if($('#chasis_checkmove').prop("checked") == true){
		var vehicle = $('#vehi_chasismove'+idstr+' option:selected').val();
		if(vehicle!=''){
			$('#vehicle_confirmmove').val(vehicle);
			$('#num_typemove').val('chasis');
		}
	}else if($('#engine_checkmove').prop("checked") == true){
		var vehicle = $('#vehi_enginemove'+idstr+' option:selected').val();
		if(vehicle!=''){
			$('#vehicle_confirmmove').val(vehicle);
			$('#num_typemove').val('engine');
		}
	}else{
		var vehicle = $('#vehi_numbermove'+idstr+' option:selected').val();
		if(vehicle!=''){
			$('#vehicle_confirmmove').val(vehicle);
			$('#num_typemove').val('vehicle');
		}
	}
	document.MoveForm.submit();
	event.preventDefault();
});
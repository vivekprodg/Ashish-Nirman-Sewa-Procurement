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

/*-------default section============*/
var add = 0;
var itemadd = [];
$('.good_count').each(function(){
	var cha = $(this).val();
	add = add+1;
	itemadd.push(add);
});

var vtype = $('#dvtype').val();
var vtypeid = $('#dvtypeid').val();
var dnumtype = $('#dnumtype').val();
var vnum = $('#vnum').val();
var dnum = $('#dnum').val();
var dpo = $('#dpo').val();
if(dpo=='yes'){
	$('.vehirequire').show();
	$('#vehicle_type').val(vtypeid);
	if(dnumtype=='chasis'){
		$('#vehitypechasisid'+vtypeid).show();
		$('#vehi_chasis'+vtypeid).val(vnum);
		$('#chasis_check').prop("checked", true);
	}
	if(dnumtype=='engine'){
		$('#vehitypeengineid'+vtypeid).show();
		$('#vehi_engine'+vtypeid).val(vnum);
		$('#engine_check').prop("checked", true);
	}
	if(dnumtype=='vehicle'){
		$('#vehitypenumid').show();
		$('#vehi_number'+vtypeid).val(vnum);
		$('#chasis_check').prop("checked", false);
		$('#engine_check').prop("checked", false);
	}
}

/*===============*/

$('.inputs').click(function(){
	$(this).removeClass('errorcolor');
});
$('.goods').click(function(){
	$(this).removeClass('errorcolor');
});
$('#challan').click(function(){
	$('.challan_e').hide();
});
$('#bill').click(function(){
	$('.bill_e').hide();
});

$('#additem').click(function(){
	$('.edit_popupbanner').fadeIn();
	$('#edit_popup').css({"transform": "scale(1)", "-webkit-transform": "scale(1)", "-moz-transform": "scale(1)"});	$('#itemname').focus();
	$('#item').focus();
});
$('#close_edit').click(function(){
	$('#edit_popup').css({"transform": "scale(.1)", "-webkit-transform": "scale(.1)", "-moz-transform": "scale(.1)"});
	$('.edit_popupbanner').fadeOut();
});
$('#close_edit1').click(function(){
	$('#edit_popup1').css({"transform": "scale(.1)", "-webkit-transform": "scale(.1)", "-moz-transform": "scale(.1)"});
	$('.edit_popupbanner1').fadeOut();
});

$('#yjobcheck').click(function(){
	$('#yesjob').prop('checked', true);
	$('#nojob').prop('checked', false);
	$('#po').val('yes');
	$('.vehirequire').show();
});

$('#njobcheck').click(function(){
	$('#yesjob').prop('checked', false);
	$('#nojob').prop('checked', true);
	$('#po').val('no');
	$('.vehirequire').hide();
});

$('#vehicle_type').on('change', function(){
	var idstr = $('#vehicle_type option:selected').val();
	var val = $('#vtypename'+idstr).val();
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

$('#item').on('change', function(){
	var idstr = $('#item option:selected').val();
	var name = $('#ini'+idstr).val();
	var uom = $('#ini'+idstr).attr("data");
	var alias = $('#ini'+idstr).attr("name");
	$('#itemname').val(name);
	$('#uom').val(uom);
	$('#itemalias').val(alias);
});
$('#edititem').on('change', function(){
	var idstr = $('#edititem option:selected').val();
	var name = $('#eini'+idstr).val();
	var uom = $('#eini'+idstr).attr("data");
	var alias = $('#eini'+idstr).attr("name");
	$('#edititemname').val(name);
	$('#edituom').val(uom);
	$('#edititemalias').val(alias);
});

$('#additembtn').click(function(){
	var error = 0;
	$('#item').focus();
	var item = $('#item option:selected').val();
	var itemname = $('#itemname').val();
	var uom = $('#uom').val();
	var qty = $('#qty').val();
	var desc = $('#desc').val();
	var alias = $('#itemalias').val();
	if(itemname == '' || item == '' ){
		error = 1;
		$('#item').addClass('errorcolor');
	}
	if(uom == ''){
		error = 1;
		$('#uom').addClass('errorcolor');
	}
	if(qty=='' || qty < 0){
		error = 1;
		$('#qty').addClass('errorcolor');	
	}
	if(error == 0){
		add = add + 1;
		itemadd.push(add);
		// console.log(amount);
		// console.log(itemadd);
		$(".hidden_inputs").append('<input type="hidden" name="itemadd" id="itemad'+add+'" value="'+add+'">');
		$(".hidden_inputs").append('<input type="hidden" name="inameid'+add+'" id="inameid'+add+'" value="'+item+'">');
		$(".hidden_inputs").append('<input type="hidden" name="iname'+add+'" id="iname'+add+'" value="'+itemname+'">');
		$(".hidden_inputs").append('<input type="hidden" name="iuom'+add+'" id="iuom'+add+'" value="'+uom+'">');
		$(".hidden_inputs").append('<input type="hidden" name="iqty'+add+'" id="iqty'+add+'" value="'+qty+'">');
		$(".hidden_inputs").append('<input type="hidden" name="idesc'+add+'" id="idesc'+add+'" value="'+desc+'">');
		$(".hidden_inputs").append('<input type="hidden" name="ialias'+add+'" id="ialias'+add+'" value="'+alias+'">');
		$('#item').val('');
		$('#itemname').val('');
		$('#uom').val('');
		$('#qty').val('');
		$('#desc').val('');
		$("#ItemTable tbody").append('<tr id="itemrow'+add+'"><td><button type="button" class="edititem" id="eitem'+add+'" data="'+add+'"><i class="far fa-edit"></i></button><button type="button" class="delitem" id="ditem'+add+'" data="'+add+'"><i class="far fa-trash-alt"></i></button></td><td>'+itemname+'('+alias+')</td><td>'+uom+'</td><td>'+qty+'</td><td>'+desc+'</td></tr>');
		$('.tfoot2').hide();
		// $('.tfoot').show();
	}
});

$('#additemeditbtn').click(function(){
	$('#item').focus();
	var itemname = $('#edititemname').val();
	var item = $('#edititem option:selected').val();
	var qty = $('#editqty').val();
	var desc = $('#editdesc').val();
	var uom = $('#edituom').val();
	var alias = $('#edititemalias').val();
	var did = $('#dfaultid').val();
	if(itemname == '' || item == '' ){
		error = 1;
		$('#item').addClass('errorcolor');
	}
	if(uom == ''){
		error = 1;
		$('#uom').addClass('errorcolor');
	}
	if(qty=='' || qty < 0){
		error = 1;
		$('#qty').addClass('errorcolor');	
	}
	$('#inameid'+did).val(item);
	$('#iname'+did).val(itemname);
	$('#iuom'+did).val(uom);
	$('#iqty'+did).val(qty);
	$('#idesc'+did).val(desc);
	$('#ialias'+did).val(alias);
	$('#edititemname').val('');
	$('#edititem').val('');
	$('#editqty').val('');
	$('#editdesc').val('');
	$('#edituom').val('');
	$('#edititemalias').val('');
	$('#itemrow'+did).remove();
	$("#ItemTable tbody").append('<tr id="itemrow'+did+'"><td><button type="button" class="edititem" id="eitem'+did+'" data="'+did+'"><i class="far fa-edit"></i></button><button type="button" class="delitem" id="ditem'+did+'" data="'+did+'"><i class="far fa-trash-alt"></i></button></td><td>'+itemname+'('+alias+')</td><td>'+uom+'</td><td>'+qty+'</td><td>'+desc+'</td></tr>');
	$('#edit_popup1').css({"transform": "scale(.1)", "-webkit-transform": "scale(.1)", "-moz-transform": "scale(.1)"});
	$('.edit_popupbanner1').fadeOut();

});

$(document).on('click', '.edititem', function(){
	var idstr = $(this).attr("data");
	$('.edit_popupbanner1').fadeIn();
	$('#edit_popup1').css({"transform": "scale(1)", "-webkit-transform": "scale(1)", "-moz-transform": "scale(1)"});	$('#itemname').focus();
	$('#edititem').focus();
	var itemid = $('#inameid'+idstr).val();
	var name = $('#iname'+idstr).val();
	var uom = $('#iuom'+idstr).val();
	var qty = $('#iqty'+idstr).val();
	var desc = $('#idesc'+idstr).val();
	var alias = $('#ialias'+idstr).val();
	$('#edititem').val(itemid);
	$('#edititemname').val(name);
	$('#edituom').val(uom);
	$('#editqty').val(qty);
	$('#editdesc').val(desc);
	$('#edititemalias').val(alias);
	$('#dfaultid').val(idstr);
});

$(document).on('click', '.delitem', function(){
	var idstr = $(this).attr("data");
	$('#itemad'+idstr).remove();
	$('#iname'+idstr).remove();
	$('#inameid'+idstr).remove();
	$('#iqty'+idstr).remove();
	$('#iuom'+idstr).remove();
	$('#idesc'+idstr).remove();
	$('#ialias'+idstr).remove();
	itemadd = $.grep(itemadd, function(value) {
		return value != idstr;
	});
	$('#itemrow'+idstr).remove();
	if (itemadd.length === 0) {
		$('.tfoot2').show();
	    
	}
	
});

$('#GoodsForm').on('submit', function(){
	var error = 0;
	$('#spinner1').show();
	var date = $('input[name=date]').val();
	var pon = $('input[name=pon]').val();
	var issue_site = $('input[name=issue_site]').val();
	if(date==''){
		error = 1;
		$('#date').addClass('errorcolor');
	}
	if(pon==''){
		error = 1;
		$('#pon').addClass('errorcolor');
	}
	if(issue_site==''){
		error = 1;
		$('#issue_site').addClass('errorcolor');
	}

	if($('#yesjob').prop("checked") == false && $('#nojob').prop("checked") == false){
		error = 1;
		$('#checkblock').addClass('errorcolor');
	}

	if($('#yesjob').prop("checked") == true){
		var idstr = $('#vehicle_type option:selected').val();
		var val = $('#vtypename'+idstr).val();
		var vehicle = '';
		$('#vtype').val(val);
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
	}

	if(itemadd.length === 0) {
		error = 1;
	    $('.goods').addClass('errorcolor');
	}
	if(error==0){
		document.GoodsForm.submit();
	}else{
		$('#spinner1').hide();
	}
	event.preventDefault();
});
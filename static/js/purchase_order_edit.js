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

function url(vehi_num){
  var mat_url = vehi_num.toLowerCase();
  var result = mat_url.replace(/[^a-z0-9\s]/gi, '').replace(/[_\s]/g, '');
  return result;
}

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
	$('#yesjob').prop("checked", true);
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
if(dpo=='no'){
	$('#nojob').prop("checked", true);
}
$('.vehidet').show();
var vnumm = url(vnum);
if($('#vh'+vnumm).length>0){
	var vh = $('#vh'+vnumm).val();
	var vhc = $('#vh'+vnumm).attr("name");
	var vhe = $('#vh'+vnumm).attr("data");
	$('#vehidetnum').text(vh);
	$('#vehidetchasis').text(vhc);
	$('#vehidetengine').text(vhe);
}
if($('#vhc'+vnumm).length>0){
	var vh = $('#vhc'+vnumm).attr("name");
	var vhc = $('#vhc'+vnumm).val();
	var vhe = $('#vhc'+vnumm).attr("data");
	$('#vehidetnum').text(vh);
	$('#vehidetchasis').text(vhc);
	$('#vehidetengine').text(vhe);
}
if($('#vhe'+vnumm).length>0){
	var vh = $('#vhe'+vnumm).attr("data");
	var vhc = $('#vhe'+vnumm).attr("name");
	var vhe = $('#vhe'+vnumm).val();
	$('#vehidetnum').text(vh);
	$('#vehidetchasis').text(vhc);
	$('#vehidetengine').text(vhe);
}

/*===============*/

$('.inputs').click(function(){
	$(this).removeClass('errorcolor');
});
$('.goods').click(function(){
	$(this).removeClass('errorcolor');
});
$('#checkblock').click(function(){
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
	$('.editsubcatshow').hide();
	$('.edititemshow').hide();
	$('#edit_popup1').css({"transform": "scale(.1)", "-webkit-transform": "scale(.1)", "-moz-transform": "scale(.1)"});
	$('.edit_popupbanner1').fadeOut();
});

function search_url(val){
  var url = val.toLowerCase();
  var result = url.replace(/[^a-z0-9\s]/gi, '').replace(/[_\s]/g, '');
  return result;
}
$('#category').on('change', function(){
	var val = $('#category option:selected').val();
	var url = search_url(val);
	$('.subcatshow').hide();
	$('.subcategory').val('');
	if($('#subcatshow'+url).length>0){
		$('#subcatshow'+url).show();
		var sval = $('#subcategory'+url+' option:selected').val();
		$('#subcatval').val(sval);
	}else{
		$('#subcatval').val('');
	}
	$('.itemshow').hide();
});
$('.subcategory').on('change', function(){
	var idstr = $(this).attr("id");
	var val = $('#'+idstr+' option:selected').val();
	var catval = $('#category option:selected').val();
	var caturl = search_url(catval);
	var surl = search_url(val);
	var mainu = caturl+''+surl;
	$('.itemshow').hide();
	$('#itemshow'+mainu).show();
});
$('#editcategory').on('change', function(){
	var val = $('#editcategory option:selected').val();
	var url = search_url(val);
	$('.editsubcatshow').hide();
	$('.editsubcategory').val('');
	if($('#editsubcatshow'+url).length>0){
		$('#editsubcatshow'+url).show();
		var sval = $('#editsubcategory'+url+' option:selected').val();
		$('#editsubcatval').val(sval);
	}else{
		$('#editsubcatval').val('');
	}
	$('.edititemshow').hide();
});
$('.editsubcategory').on('change', function(){
	var idstr = $(this).attr("id");
	var val = $('#'+idstr+' option:selected').val();
	var catval = $('#editcategory option:selected').val();
	var caturl = search_url(catval);
	var surl = search_url(val);
	var mainu = caturl+''+surl;
	$('.edititemshow').hide();
	$('#edititemshow'+mainu).show();
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

$('.item').on('change', function(){
	var vdstr = $(this).attr("id");
	var idstr = $('#'+vdstr+' option:selected').val();
	var name = $('#ini'+idstr).val();
	var uom = $('#ini'+idstr).attr("data");
	var alias = $('#ini'+idstr).attr("name");
	$('#itemm').val(idstr);
	$('#itemname').val(name);
	$('#uom').val(uom);
	$('#itemalias').val(alias);
});
$('.edititemm').on('change', function(){
	var vdstr = $(this).attr("id");
	var idstr = $('#'+vdstr+' option:selected').val();
	var name = $('#eini'+idstr).val();
	var uom = $('#eini'+idstr).attr("data");
	var alias = $('#eini'+idstr).attr("name");
	$('#edititem').val(idstr);
	$('#edititemname').val(name);
	$('#edituom').val(uom);
	$('#edititemalias').val(alias);
});

$('#additembtn').click(function(){
	var error = 0;
	$('#item').focus();
	var item = $('#itemm').val();
	var itemname = $('#itemname').val();
	var uom = $('#uom').val();
	var qty = $('#qty').val();
	var desc = $('#desc').val();
	var alias = $('#itemalias').val();
	var cval = $('#category option:selected').val();
	var curl = search_url(cval);
	var sval = $('#subcategory'+curl+' option:selected').val();
	var surl = search_url(sval);
	var mainu = curl+''+surl;
	if($('#itemshow'+mainu).length>0){
		var ival = $('#item'+mainu+' option:selected').val();
		if(ival==''){
			error = 1;
			$('#item'+mainu).addClass('errorcolor');
		}else{
			if(item!=ival){
				error = 1;
				$('#item'+mainu).addClass('errorcolor');
				$('#category').addClass('errorcolor');
				$('#subcategory'+curl).addClass('errorcolor');
			}
		}
	}else{
		error = 1;
		$('#category').addClass('errorcolor');
	}
	if(itemname == '' || item == '' ){
		error = 1;
		$('#itemm').addClass('errorcolor');
	}
	if(uom == ''){
		error = 1;
		$('#uom').addClass('errorcolor');
	}
	if(qty=='' || qty < 0){
		error = 1;
		$('#qty').addClass('errorcolor');	
	}
	if($('.itamval'+item).length==0){
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
			$('#itemm').val('');
			$('#itemname').val('');
			$('#uom').val('');
			$('#qty').val('');
			$('#desc').val('');
			$('.item').val('');
			$('#category').val('');
			$('.subcatshow').hide();
			$('.itemshow').hide();
			$("#ItemTable tbody").append('<tr id="itemrow'+add+'" class="itamval'+item+'"><td><button type="button" class="edititem" id="eitem'+add+'" data="'+add+'" data-itm="itamval'+item+'"><i class="far fa-edit"></i></button><button type="button" class="delitem" id="ditem'+add+'" data="'+add+'"><i class="far fa-trash-alt"></i></button></td><td>'+itemname+'('+alias+')</td><td>'+uom+'</td><td>'+qty+'</td><td>'+desc+'</td></tr>');
			$('.tfoot2').hide();
			// $('.tfoot').show();
		}
	}
});

$('#additemeditbtn').click(function(){
	$('#item').focus();
	var error = 0;
	var itemname = $('#edititemname').val();
	var item = $('#edititemon').val();
	var qty = $('#editqty').val();
	var desc = $('#editdesc').val();
	var uom = $('#edituom').val();
	var alias = $('#edititemalias').val();
	var did = $('#dfaultid').val();
	var cval = $('#editcategory option:selected').val();
	if(cval!=''){
		var curl = search_url(cval);
		var sval = $('#editsubcategory'+curl+' option:selected').val();
		var surl = search_url(sval);
		var mainu = curl+''+surl;
		if($('#edititemshow'+mainu).length>0){
			var ival = $('#edititem'+mainu+' option:selected').val();
			if(ival==''){
				error = 1;
				$('#edititem'+mainu).addClass('errorcolor');
			}else{
				if(item!=ival){
					error = 1;
					$('#edititem'+mainu).addClass('errorcolor');
					$('#editcategory').addClass('errorcolor');
					$('#editsubcategory'+curl).addClass('errorcolor');
				}
			}
		}else{
			error = 1;
			$('#editcategory').addClass('errorcolor');
		}
	}
	if(itemname == '' || item == '' ){
		error = 1;
		$('#edititem').addClass('errorcolor');
	}
	if(uom == ''){
		error = 1;
		$('#edituom').addClass('errorcolor');
	}
	if(qty=='' || qty < 0){
		error = 1;
		$('#editqty').addClass('errorcolor');	
	}
	if(error == 0){
		$('#inameid'+did).val(item);
		$('#iname'+did).val(itemname);
		$('#iuom'+did).val(uom);
		$('#iqty'+did).val(qty);
		$('#idesc'+did).val(desc);
		$('#ialias'+did).val(alias);
		$('#edititemname').val('');
		$('#edititemon').val('');
		$('#editqty').val('');
		$('#editdesc').val('');
		$('#edituom').val('');
		$('#edititemalias').val('');
		$('.edititem').val('');
		$('#editcategory').val('');
		$('.editsubcatshow').hide();
		$('.edititemshow').hide();
		$('#itemrow'+did).remove();
		$("#ItemTable tbody").append('<tr id="itemrow'+did+'" class="itamval'+item+'"><td><button type="button" class="edititem" id="eitem'+did+'" data="'+did+'"><i class="far fa-edit"></i></button><button type="button" class="delitem" id="ditem'+did+'" data="'+did+'"><i class="far fa-trash-alt"></i></button></td><td>'+itemname+'('+alias+')</td><td>'+uom+'</td><td>'+qty+'</td><td>'+desc+'</td></tr>');
		$('#edit_popup1').css({"transform": "scale(.1)", "-webkit-transform": "scale(.1)", "-moz-transform": "scale(.1)"});
		$('.edit_popupbanner1').fadeOut();
	}
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
	$('#edititemon').val(itemid);
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
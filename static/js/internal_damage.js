var date = document.getElementById("date");
var indate = document.getElementById("invoice_date");
if(date!=null){
	date.nepaliDatePicker({
	    readOnlyInput: true
	});
}
if(indate!=null){
	indate.nepaliDatePicker({
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
$('.goods').click(function(){
	$(this).removeClass('errorcolor');
});
$('.pvnsel').click(function(){
	$('.pvnsel').removeClass('errorcolor');
});

$('#close_edit').click(function(){
	$('#edit_popup').css({"transform": "scale(.1)", "-webkit-transform": "scale(.1)", "-moz-transform": "scale(.1)"});
	$('.edit_popupbanner').fadeOut();
});
$('#close_edit1').click(function(){
	$('#edit_popup1').css({"transform": "scale(.1)", "-webkit-transform": "scale(.1)", "-moz-transform": "scale(.1)"});
	$('.edit_popupbanner1').fadeOut();
});

$('#jobnumber').click(function(){
	$('.porder_e').hide();
	$(this).removeClass('errorcolor');
});


var pch = 0;
var pbill = 0;
var porder = 0;
var ponum = [];
var rec = 0;
var add = 0;
var itemadd = [];
var amount = [];
// $('#jobnumber').blur(function(){
// 	var val = $(this).val();
// 	val = val.toUpperCase();
// 	if($('#po'+val).length == 0){
// 		porder = 1;
// 		$(this).addClass('errorcolor');
// 		$('.porder_e').show();
// 	}else{
// 		porder = 0;
// 	}
// });

// $('#jobnumber').on('keyup', function(){
// 	var val = $(this).val();
// 	val = val.toUpperCase();
// 	porder = 0;
// 	$('.pvnselban').hide();
// 	$(this).removeClass('errorcolor');
// 	$('.porder_e').hide();
// 	$('.goods').removeClass('errorcolor');
// 	if($('#yesjob').prop("checked")==true){
// 		if($('#po'+val).length == 0){
// 			porder = 1;
// 			$(this).addClass('errorcolor');
// 			$('.porder_e').show();
// 		}else{
// 			var vv = val.toLowerCase();
// 			if($('#pvnselban'+val).length == 0){
// 				if($('#pvnselban'+vv).length == 0){
// 					porder = 1;
// 					$(this).addClass('errorcolor');
// 					$('.porder_e').show();
// 				}else{
// 					$('#pvnselban'+vv).show();
// 				}
// 			}else{
// 				$('#pvnselban'+val).show();
// 			}
// 		}
// 	}
// });

$('#jobnumber').on('keypress', function(e){
	if(e.which===13){
		var idstr = $(this).val();
		$('.loading').slideDown();
		$('.goods').removeClass('errorcolor');
		$(this).removeClass('errorcolor');
		var val = idstr.toUpperCase();
		if($('.grd'+val).length == 0){
			if($('.pvnon'+val).length > 0){
				rec = rec + 1;
				var rus = val + rec;
				$(".hidden_inputs").append('<input type="hidden" name="pvnval" class="pvnval" id="pval'+val+'" value="'+val+'">');

				$(".grncol").append('<div class="coldiv grd'+val+'" id="colrec'+rus+'"><span class="coldes">'+val+'</span><button type="button" class="colbtn" name="'+val+'" data="'+rus+'"><i class="fa fa-times"></i></button></div>');
			}else{
				$(this).addClass('errorcolor');
			}
		}else{
			$(this).addClass('errorcolor');
		}
		$('.loading').slideUp();
		$(this).val('');
		$(this).focus();
	}
});

$(document).on('click', '.colbtn', function(e){
	var idstr = $(this).attr("data");
	var pval = $(this).attr("name");
	$('.loading').slideDown();
	
	$('#colrec'+idstr).remove();
	$('.pvnval').each(function(){
		var val = $(this).val();
		if(val==pval){
			$('#pval'+val).remove();
		}
	});
	if($('.itemrow'+pval).length>0){
		$('.itemrow'+pval).remove();
	}
	if($('.pvnitm'+pval).length>0){
		$('.pvnitm'+pval).each(function(){
			var val = $(this).val();
			$('#itemad'+val).remove();
			$('#iname'+val).remove();
			$('#inameid'+val).remove();
			$('#iqty'+val).remove();
			$('#iuom'+val).remove();
			$('#ialias'+val).remove();
			itemadd = $.grep(itemadd, function(value) {
				return value != val;
			});
		});
	}
	if (itemadd.length === 0) {
		$('.tfoot2').show();
	    
	}
	$('.loading').slideUp();

});

$('#additem').click(function(){
	if($('.pvnval').length>0){
		$('.edit_popupbanner').fadeIn();
		$('#edit_popup').css({"transform": "scale(1)", "-webkit-transform": "scale(1)", "-moz-transform": "scale(1)"});	$('#itemname').focus();
		$('#item').focus();
		$('.pvnval').each(function(){
			var cha = $(this).val();
			$('.pitm'+cha).each(function(){
				var itm_id = $(this).val();
				var itm = $(this).attr("data");
				if($("#item option[value='"+itm_id+"']").length===0){
					$('#item').append($('<option>', {
					    value: itm_id,
					    data_lab: cha,
					    text: itm
					}));
				}
				
			});
		});
	}else{
		$('#jobnumber').addClass('errorcolor');
	}

});

$('#item').on('change', function(){
	$('#rate').removeClass('errorcolor');
	var idstr = $('#item option:selected').val();
	var name = $('#ini'+idstr).val();
	var uom = $('#ini'+idstr).attr("data");
	var alias = $('#ini'+idstr).attr("name");
	$('#itemname').val(name);
	$('#uom').val(uom);
	$('#itemalias').val(alias);
});
$('#edititem').on('change', function(){
	$('#editrate').removeClass('errorcolor');
	var idstr = $('#edititem option:selected').val();
	var name = $('#eini'+idstr).val();
	var uom = $('#eini'+idstr).attr("data");
	var alias = $('#eini'+idstr).attr("name");
	$('#edititemname').val(name);
	$('#edituom').val(uom);
	$('#edititemalias').val(alias);
});

$('#additembtn').on('click',function(){
	diserror = 0;
	var error = 0;
	$('#item').focus();
	var item = $('#item option:selected').val();
	var label = $('#item option:selected').attr("data_lab");
	var itemname = $('#itemname').val();
	var uom = $('#uom').val();
	var alias = $('#itemalias').val();
	var qty = $('#qty').val();
	if(itemname == '' || item == '' ){
		error = 1;
		$('#item').addClass('errorcolor');
	}
	if(uom == ''){
		error = 1;
		$('#uom').addClass('errorcolor');
	}
	if(qty=='' || qty < 1){
		error = 1;
		$('#qty').addClass('errorcolor');	
	}
	if($('.irow'+label+'itm'+item).length==0){
		if(error == 0){
			add = add + 1;
			itemadd.push(add);
			var rstr = label + add;
			$(".hidden_inputs").append('<input type="hidden" name="pvnitm" class="pvnitm'+label+'" value="'+add+'">');
			$(".hidden_inputs").append('<input type="hidden" name="itemadd" id="itemad'+add+'" value="'+add+'">');
			$(".hidden_inputs").append('<input type="hidden" name="inameid'+rstr+'" id="inameid'+add+'" value="'+item+'">');
			$(".hidden_inputs").append('<input type="hidden" name="iname'+rstr+'" id="iname'+add+'" value="'+itemname+'">');
			$(".hidden_inputs").append('<input type="hidden" name="iuom'+rstr+'" id="iuom'+add+'" value="'+uom+'">');
			$(".hidden_inputs").append('<input type="hidden" name="iqty'+rstr+'" id="iqty'+add+'" value="'+qty+'">');
			$(".hidden_inputs").append('<input type="hidden" name="ialias'+rstr+'" id="ialias'+add+'" value="'+alias+'">');
			$('.tfoot2').hide();
			$("#MaintainanceTable tbody").append('<tr id="itemrow'+add+'" class="itemrow'+label+'"><td class="irow'+label+'itm'+item+'"><button type="button" class="edititem" id="eitem'+add+'" data="'+add+'"><i class="far fa-edit"></i></button><button type="button" class="delitem" id="ditem'+add+'" data="'+add+'"><i class="far fa-trash-alt"></i></button></td><td>'+itemname+'('+alias+')</td><td>'+uom+'</td><td>'+qty+'</td></tr>');
			$('.tfoot').show();

			$('#item').val('');
			$('#itemname').val('');
			$('#uom').val('');
			$('#itemalias').val('');
			$('#qty').val('');
		}
	}
});

$('#additemeditbtn').click(function(){
	diserror = 0;
	var error = 0;
	$('#edititem').focus();
	var item = $('#edititem option:selected').val();
	var label = $('#item option:selected').attr("data_lab");
	var itemname = $('#edititemname').val();
	var uom = $('#edituom').val();
	var qty = $('#editqty').val();
	var did = $('#dfaultid').val();
	var alias = $('#edititemalias').val();
	if(itemname == '' || item == '' ){
		error = 1;
		$('#edititem').addClass('errorcolor');
	}
	if(uom == ''){
		error = 1;
		$('#edituom').addClass('errorcolor');
	}
	if(qty=='' || qty < 1){
		error = 1;
		$('#editqty').addClass('errorcolor');	
	}
	if(error == 0){
		$('#inameid'+did).val(item);
		$('#iname'+did).val(itemname);
		$('#iuom'+did).val(uom);
		$('#iqty'+did).val(qty);
		$('#ialias'+did).val(alias);
		$('#edititemname').val('');
		$('#edititem').val('');
		$('#editqty').val('');
		$('#edituom').val('');
		$('#edititemalias').val('');
		$('#itemrow'+did).remove();
		$("#MaintainanceTable tbody").append('<tr id="itemrow'+did+'" class="itemrow'+label+'"><td class="irow'+label+'itm'+item+'"><button type="button" class="edititem" id="eitem'+did+'" data="'+did+'"><i class="far fa-edit"></i></button><button type="button" class="delitem" id="ditem'+did+'" data="'+did+'"><i class="far fa-trash-alt"></i></button></td><td>'+itemname+'('+alias+')</td><td>'+uom+'</td><td>'+qty+'</td></tr>');


		$('#edit_popup1').css({"transform": "scale(.1)", "-webkit-transform": "scale(.1)", "-moz-transform": "scale(.1)"});
		$('.edit_popupbanner1').fadeOut();
	}

});

$(document).on('click', '.edititem', function(){
	var idstr = $(this).attr("data");
	if($('.pvnval').length>0){
		$('.edit_popupbanner1').fadeIn();
		$('#edit_popup1').css({"transform": "scale(1)", "-webkit-transform": "scale(1)", "-moz-transform": "scale(1)"});	$('#itemname').focus();
		$('#edititem').focus();
		$('.pvnval').each(function(){
			var cha = $(this).val();
			$('.epitm'+cha).each(function(){
				var itm_id = $(this).val();
				var itm = $(this).attr("data");
				if($("#edititem option[value='"+itm_id+"']").length===0){
					$('#edititem').append($('<option>', {
					    value: itm_id,
					    data_lab: cha,
					    text: itm
					}));
				}
				
			});
		});
		var itemid = $('#inameid'+idstr).val();
		var name = $('#iname'+idstr).val();
		var uom = $('#iuom'+idstr).val();
		var qty = $('#iqty'+idstr).val();
		var alias = $('#ialias'+idstr).val();
		$('#edititem').val(itemid);
		$('#edititemname').val(name);
		$('#edituom').val(uom);
		$('#editqty').val(qty);
		$('#edititemalias').val(alias);
		$('#dfaultid').val(idstr);
	}else{
		$('#jobnumber').addClass('errorcolor');
	}
	
});

$(document).on('click', '.delitem', function(){
	var idstr = $(this).attr("data");
	$('#itemad'+idstr).remove();
	$('#iname'+idstr).remove();
	$('#inameid'+idstr).remove();
	$('#iqty'+idstr).remove();
	$('#iuom'+idstr).remove();
	$('#ialias'+idstr).remove();
	itemadd = $.grep(itemadd, function(value) {
		return value != idstr;
	});
	$('#itemrow'+idstr).remove();
	if (itemadd.length === 0) {
		$('.tfoot').hide();
		$('.tfoot2').show();
	    
	}
	
});

$('#DamageForm').on('submit', function(){
	var error = 0;
	$('#spinner1').show();
	var date = $('input[name=date]').val();
	var damage_number = $('input[name=damage_number]').val();
	if(date==''){
		error = 1;
		$('#date').addClass('errorcolor');
	}
	if(damage_number==''){
		error = 1;
		$('#damage_number').addClass('errorcolor');
	}
	if($('.pvnval').length==0){
		error = 1;
		$('#jobnumber').addClass('errorcolor');
	}
	if(itemadd.length === 0) {
		error = 1
	    $('.goods').addClass('errorcolor');
	}
	if(error==0){
		document.DamageForm.submit();
	}else{
		$('#spinner1').hide();
	}
	event.preventDefault();
});
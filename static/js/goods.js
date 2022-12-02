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
$('.goods').click(function(){
	$(this).removeClass('errorcolor');
});
$('#challan').click(function(){
	$('.challan_e').hide();
});
$('#bill').click(function(){
	$('.bill_e').hide();
});
$('#porder').click(function(){
	$('.porder_e').hide();
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

var gch = 0;
var gbill = 0;
$('#challan').blur(function(){
	var val = $(this).val();
	gch = 0;
	$('.gchallan').each(function(){
		var cha = $(this).val();
		if(val == cha){
			gch = 1;
			$('#challan').addClass('errorcolor');
			$('.challan_e').show();
		}
	});
});
$('#bill').blur(function(){
	var val = $(this).val();
	gbill = 0;
	$('.gbill').each(function(){
		var cha = $(this).val();
		if(val == cha){
			gbill = 1;
			$('#bill').addClass('errorcolor');
			$('.bill_e').show();
		}
	});
});

$('#item').on('change', function(){
	var idstr = $('#item option:selected').val();
	var name = $('#ini'+idstr).val();
	var uom = $('#ini'+idstr).attr("data");
	$('#itemname').val(name);
	$('#uom').val(uom);
});
$('#edititem').on('change', function(){
	var idstr = $('#edititem option:selected').val();
	var name = $('#eini'+idstr).val();
	var uom = $('#eini'+idstr).attr("data");
	$('#edititemname').val(name);
	$('#edituom').val(uom);
});

var add = 0;
var itemadd = [];
$('#additembtn').click(function(){
	var error = 0;
	$('#item').focus();
	var item = $('#item option:selected').val();
	var itemname = $('#itemname').val();
	var uom = $('#uom').val();
	var qty = $('#qty').val();
	var remark = $('#remark').val();
	if(remark==''){
		remark = 'none';
	}
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
		$(".hidden_inputs").append('<input type="hidden" name="iremark'+add+'" id="iremark'+add+'" value="'+remark+'">');
		$('#item').val('');
		$('#itemname').val('');
		$('#uom').val('');
		$('#qty').val('');
		$('#remark').val('');
		$("#ItemTable tbody").append('<tr id="itemrow'+add+'"><td><button type="button" class="edititem" id="eitem'+add+'" data="'+add+'"><i class="far fa-edit"></i></button><button type="button" class="delitem" id="ditem'+add+'" data="'+add+'"><i class="far fa-trash-alt"></i></button></td><td>'+itemname+'</td><td>'+uom+'</td><td>'+qty+'</td><td>'+remark+'</td></tr>');
		$('.tfoot2').hide();
		// $('.tfoot').show();
	}
});

$('#additemeditbtn').click(function(){
	$('#item').focus();
	var itemname = $('#edititemname').val();
	var item = $('#edititem option:selected').val();
	var qty = $('#editqty').val();
	var uom = $('#edituom').val();
	var remark = $('#editremark').val();
	var did = $('#dfaultid').val();
	if(remark==''){
		remark = 'none';
	}
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
	$('#iremark'+did).val(remark);
	$('#edititemname').val('');
	$('#edititem').val('');
	$('#editqty').val('');
	$('#edituom').val('');
	$('#editremark').val('');
	$('#itemrow'+did).remove();
	$("#ItemTable tbody").append('<tr id="itemrow'+did+'"><td><button type="button" class="edititem" id="eitem'+did+'" data="'+did+'"><i class="far fa-edit"></i></button><button type="button" class="delitem" id="ditem'+did+'" data="'+did+'"><i class="far fa-trash-alt"></i></button></td><td>'+itemname+'</td><td>'+uom+'</td><td>'+qty+'</td><td>'+remark+'</td></tr>');
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
	var remark = $('#iremark'+idstr).val();
	$('#edititem').val(itemid);
	$('#edititemname').val(name);
	$('#edituom').val(uom);
	$('#editqty').val(qty);
	$('#editremark').val(remark);
	$('#dfaultid').val(idstr);
});

$(document).on('click', '.delitem', function(){
	var idstr = $(this).attr("data");
	$('#itemad'+idstr).remove();
	$('#iname'+idstr).remove();
	$('#inameid'+idstr).remove();
	$('#iqty'+idstr).remove();
	$('#iuom'+idstr).remove();
	$('#iremark'+idstr).remove();
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
	var grn = $('input[name=grn]').val();
	var challan = $('input[name=challan]').val();
	var bill = $('#bill').val();
	// var location = $('#location option:selected').val();
	var supplier = $('#supplier option:selected').val();
	var vehicle = $('#vehicle').val();
	if(date==''){
		error = 1;
		$('#date').addClass('errorcolor');
	}
	if(grn==''){
		error = 1;
		$('#grn').addClass('errorcolor');
	}
	if(challan==''){
		error = 1;
		$('#challan').addClass('errorcolor');
	}
	if(bill==''){
		error = 1;
		$('#bill').addClass('errorcolor');
	}
	// if(location==''){
	// 	error = 1;
	// 	$('#location').addClass('errorcolor');
	// }
	if(supplier==''){
		error = 1;
		$('#supplier').addClass('errorcolor');
	}
	// if(vehicle==''){
	// 	error = 1;
	// 	$('#vehicle').addClass('errorcolor');
	// }
	if(gch==1){
		error = 1;
		$('#challan').addClass('errorcolor');
	}
	if(gbill==1){
		error = 1;
		$('#bill').addClass('errorcolor');
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
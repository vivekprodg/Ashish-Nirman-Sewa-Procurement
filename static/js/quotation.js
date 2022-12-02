var date = document.getElementById("date");
var valid_date = document.getElementById("valid_date");
if(date!=null){
	date.nepaliDatePicker({
	    readOnlyInput: true
	});
}
if(valid_date!=null){
	valid_date.nepaliDatePicker({
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
$('#supplier').blur(function(){
	var val = $(this).val();
	gch = 0;
	$('.qsup').each(function(){
		var cha = $(this).val();
		if(val == cha){
			gch = 1;
			$('#supplier').addClass('errorcolor');
			$('.challan_e').show();
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
	var rate = $('#rate').val();
	if(itemname == '' || item == '' ){
		error = 1;
		$('#item').addClass('errorcolor');
	}
	if(uom == ''){
		error = 1;
		$('#uom').addClass('errorcolor');
	}
	if(rate=='' || rate < 0){
		error = 1;
		$('#rate').addClass('errorcolor');	
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
		$(".hidden_inputs").append('<input type="hidden" name="irate'+add+'" id="iqty'+add+'" value="'+rate+'">');
		$('#item').val('');
		$('#itemname').val('');
		$('#uom').val('');
		$('#rate').val('');
		$("#ItemTable tbody").append('<tr id="itemrow'+add+'"><td><button type="button" class="edititem" id="eitem'+add+'" data="'+add+'"><i class="far fa-edit"></i></button><button type="button" class="delitem" id="ditem'+add+'" data="'+add+'"><i class="far fa-trash-alt"></i></button></td><td>'+itemname+'</td><td>'+uom+'</td><td>'+rate+'</td></tr>');
		$('.tfoot2').hide();
		// $('.tfoot').show();
	}
});

$('#additemeditbtn').click(function(){
	$('#item').focus();
	var itemname = $('#edititemname').val();
	var item = $('#edititem option:selected').val();
	var rate = $('#editrate').val();
	var uom = $('#edituom').val();
	var did = $('#dfaultid').val();
	if(itemname == '' || item == '' ){
		error = 1;
		$('#item').addClass('errorcolor');
	}
	if(uom == ''){
		error = 1;
		$('#uom').addClass('errorcolor');
	}
	if(rate=='' || rate < 0){
		error = 1;
		$('#rate').addClass('errorcolor');	
	}
	$('#inameid'+did).val(item);
	$('#iname'+did).val(itemname);
	$('#iuom'+did).val(uom);
	$('#irate'+did).val(qty);
	$('#iremark'+did).val(remark);
	$('#edititemname').val('');
	$('#edititem').val('');
	$('#editrate').val('');
	$('#edituom').val('');
	$('#itemrow'+did).remove();
	$("#ItemTable tbody").append('<tr id="itemrow'+did+'"><td><button type="button" class="edititem" id="eitem'+did+'" data="'+did+'"><i class="far fa-edit"></i></button><button type="button" class="delitem" id="ditem'+did+'" data="'+did+'"><i class="far fa-trash-alt"></i></button></td><td>'+itemname+'</td><td>'+uom+'</td><td>'+rate+'</td></tr>');
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
	var rate = $('#irate'+idstr).val();
	$('#edititem').val(itemid);
	$('#edititemname').val(name);
	$('#edituom').val(uom);
	$('#editrate').val(rate);
	$('#dfaultid').val(idstr);
});

$(document).on('click', '.delitem', function(){
	var idstr = $(this).attr("data");
	$('#itemad'+idstr).remove();
	$('#iname'+idstr).remove();
	$('#inameid'+idstr).remove();
	$('#irate'+idstr).remove();
	$('#iuom'+idstr).remove();
	itemadd = $.grep(itemadd, function(value) {
		return value != idstr;
	});
	$('#itemrow'+idstr).remove();
	if (itemadd.length === 0) {
		$('.tfoot2').show();
	    
	}
	
});

$('#QuotationForm').on('submit', function(){
	var error = 0;
	$('#spinner1').show();
	var date = $('input[name=date]').val();
	var valid_date = $('input[name=valid_date]').val();
	var supplier = $('#supplier option:selected').val();
	if(date==''){
		error = 1;
		$('#date').addClass('errorcolor');
	}
	if(valid_date==''){
		error = 1;
		$('#valid_date').addClass('errorcolor');
	}
	if(supplier==''){
		error = 1;
		$('#supplier').addClass('errorcolor');
	}
	if(gch==1){
		error = 1;
		$('#supplier').addClass('errorcolor');
	}
	if(itemadd.length === 0) {
		error = 1;
	    $('.goods').addClass('errorcolor');
	}
	if(error==0){
		document.QuotationForm.submit();
	}else{
		$('#spinner1').hide();
	}
	event.preventDefault();
});
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
var porder = 0;
var add = 0;
var itemadd = [];
var ponum = [];
var rec = 0;
$('.good_count').each(function(){
	var cha = $(this).val();
	add = add+1;
	itemadd.push(add);
});
$('.irecon').each(function(){
	var cha = $(this).val();
	rec = rec+1;
});

var jnum = $('#jnum').val();

jnumu = jnum.toUpperCase();
jnuml = jnum.toLowerCase();
if($('#pvnselban'+jnumu).length>0){
	$('#pvnselban'+jnumu).show();
}
if($('#pvnselban'+jnuml).length>0){
	$('#pvnselban'+jnuml).show();
}

/*===============*/

$('.inputs').click(function(){
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
$('.goods').click(function(){
	$(this).removeClass('errorcolor');
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

$('#jobnumber').on('keyup', function(){
	var val = $(this).val();
	val = val.toUpperCase();
	porder = 0;
	$('.pvnselban').hide();
	$(this).removeClass('errorcolor');
	$('.porder_e').hide();
	$('.goods').removeClass('errorcolor');
	if($('#po'+val).length == 0){
		porder = 1;
		$(this).addClass('errorcolor');
		$('.porder_e').show();
	}else{
		var vv = val.toLowerCase();
		if($('#pvnselban'+val).length == 0){
			if($('#pvnselban'+vv).length == 0){
				porder = 1;
				console.log('a');
				$(this).addClass('errorcolor');
				$('.porder_e').show();
			}else{
				$('#pvnselban'+vv).show();
			}
		}
	}
});

$('.pvnsel').on('change', function(){
	var idstr = $(this).attr("id");
	var val = $('#'+idstr+' option:selected').val();
	$('.loading').slideDown();
	$('.goods').removeClass('errorcolor');
	val = val.toUpperCase();
	var po = $('#jobnumber').val();
	console.log(po);
	if($('.grd'+val).length == 0){
		if($('.gooid'+val).length > 0){
			if(ponum.length===0){
				ponum.push(po);
			}
			if($.inArray(po, ponum)!=-1){
				rec = rec + 1;
				var rus = val + rec;
				// var tdisper = $('#puridper'+val).val();
				// var tdisamt = $('#puridamt'+val).val();
				// var tvat = $('#purivat'+val).val();
				$(".hidden_inputs").append('<input type="hidden" name="pvnval" class="pvnval" id="pval'+val+'" value="'+val+'">');
				// $(".hidden_inputs").append('<input type="hidden" class="tdisper" id="tdisper'+val+'" value="'+tdisper+'">');
				// $(".hidden_inputs").append('<input type="hidden" class="tdisamt" id="tdisamt'+val+'" value="'+tdisamt+'">');
				// $(".hidden_inputs").append('<input type="hidden" class="tvat" id="tvat'+val+'" value="'+tvat+'">');
				$('.gooid'+val).each(function(){
					var cha = $(this).val();
					var item = $('#item'+cha).val();
					var itemid = $('#itemid'+cha).val();
					var uom = $('#uom'+cha).val();
					var qty = $('#qty'+cha).val();
					var alias = $('#alias'+cha).val();

					add = add + 1;
					itemadd.push(add);
					var us = val+add;
					$(".hidden_inputs").append('<input type="hidden" class="irec'+rus+'" value="'+us+'" data="'+add+'">');
					$(".hidden_inputs").append('<input type="hidden" name="itemadd" id="itemad'+us+'" value="'+add+'">');
					$(".hidden_inputs").append('<input type="hidden" name="ipvn'+add+'" id="ipvn'+us+'" value="'+val+'">');
					$(".hidden_inputs").append('<input type="hidden" name="inameid'+add+'" id="inameid'+us+'" value="'+itemid+'">');
					$(".hidden_inputs").append('<input type="hidden" name="iname'+add+'" id="iname'+us+'" value="'+item+'">');
					$(".hidden_inputs").append('<input type="hidden" name="iuom'+add+'" id="iuom'+us+'" value="'+uom+'">');
					$(".hidden_inputs").append('<input type="hidden" name="iqty'+add+'" id="iqty'+us+'" value="'+qty+'">');
					$(".hidden_inputs").append('<input type="hidden" name="ialias'+add+'" id="ialias'+us+'" value="'+alias+'">');
					$('.tfoot2').hide();
					$("#ItemTable tbody").append('<tr id="itemrow'+us+'"><td></td><td>'+item+'('+alias+')</td><td>'+uom+'</td><td>'+qty+'</td></tr>');
					$('.tfoot').show();
				});
				$(".grncol").append('<div class="coldiv grd'+val+'" id="colrec'+rus+'"><span class="coldes">'+val+'</span><button type="button" class="colbtn" name="'+val+'" data="'+rus+'"><i class="fa fa-times"></i></button></div>');
			}
		}
	}
	$('.loading').slideUp();
	$(this).val('');
	$(this).focus();
});

$(document).on('click', '.colbtn', function(e){
	var idstr = $(this).attr("data");
	var pval = $(this).attr("name");
	diserror = 0;
	$('.loading').slideDown();
	$('.irec'+idstr).each(function(){
		var cha = $(this).val();
		var hac = $(this).attr("data");
		$('#itemad'+cha).remove();
		$('#ipvn'+cha).remove();
		$('#inameid'+cha).remove();
		$('#iname'+cha).remove();
		$('#iuom'+cha).remove();
		$('#iqty'+cha).remove();
		$('#ialias'+cha).remove();

		itemadd = $.grep(itemadd, function(value) {
			return value != hac;
		});
		$('#itemrow'+cha).remove();
		$('#colrec'+idstr).remove();
	});
	$('.pvnval').each(function(){
		var val = $(this).val();
		if(val==pval){
			$('#pval'+val).remove();
		}
	});
	if(itemadd.length === 0){
		ponum = []
		$('.tfoot').hide();
		$('.tfoot2').show();
	}
	$('.loading').slideUp();

});

$('#additembtn').click(function(){
	var error = 0;
	$('#item').focus();
	var item = $('#item option:selected').val();
	var itemname = $('#itemname').val();
	var uom = $('#uom').val();
	var qty = $('#qty').val();
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
		$(".hidden_inputs").append('<input type="hidden" name="itemadd" id="itemad'+add+'" value="'+add+'">');
		$(".hidden_inputs").append('<input type="hidden" name="iid'+add+'" id="inameid'+add+'" value="'+item+'">');
		$(".hidden_inputs").append('<input type="hidden" name="iname'+add+'" id="iname'+add+'" value="'+itemname+'">');
		$(".hidden_inputs").append('<input type="hidden" name="iuom'+add+'" id="iuom'+add+'" value="'+uom+'">');
		$(".hidden_inputs").append('<input type="hidden" name="iqty'+add+'" id="iqty'+add+'" value="'+qty+'">');
		$(".hidden_inputs").append('<input type="hidden" name="ialias'+add+'" id="ialias'+add+'" value="'+alias+'">');
		$('#item').val('');
		$('#itemname').val('');
		$('#uom').val('');
		$('#qty').val('');
		$("#ItemTable tbody").append('<tr id="itemrow'+add+'"><td><button type="button" class="edititem" id="eitem'+add+'" data="'+add+'"><i class="far fa-edit"></i></button><button type="button" class="delitem" id="ditem'+add+'" data="'+add+'"><i class="far fa-trash-alt"></i></button></td><td>'+itemname+'('+alias+')</td><td>'+uom+'</td><td>'+qty+'</td></tr>');
		$('.tfoot2').hide();
	}
});

$('#additemeditbtn').click(function(){
	$('#item').focus();
	var itemname = $('#edititemname').val();
	var item = $('#edititem option:selected').val();
	var qty = $('#editqty').val();
	var uom = $('#edituom').val();
	var did = $('#dfaultid').val();
	var alias = $('#edititemalias').val();
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
	$('#iid'+did).val(item);
	$('#iname'+did).val(itemname);
	$('#iuom'+did).val(uom);
	$('#iqty'+did).val(qty);
	$('#edititemname').val('');
	$('#edititem').val('');
	$('#editqty').val('');
	$('#edituom').val('');
	$('#edititemalias').val('');
	$('#itemrow'+did).remove();
	$("#ItemTable tbody").append('<tr id="itemrow'+did+'"><td><button type="button" class="edititem" id="eitem'+did+'" data="'+did+'"><i class="far fa-edit"></i></button><button type="button" class="delitem" id="ditem'+did+'" data="'+did+'"><i class="far fa-trash-alt"></i></button></td><td>'+itemname+'('+alias+')</td><td>'+uom+'</td><td>'+qty+'</td></tr>');
	$('#edit_popup1').css({"transform": "scale(.1)", "-webkit-transform": "scale(.1)", "-moz-transform": "scale(.1)"});
	$('.edit_popupbanner1').fadeOut();

});

$(document).on('click', '.edititem', function(){
	var idstr = $(this).attr("data");
	$('.edit_popupbanner1').fadeIn();
	$('#edit_popup1').css({"transform": "scale(1)", "-webkit-transform": "scale(1)", "-moz-transform": "scale(1)"});	$('#itemname').focus();
	$('#edititem').focus();
	var itemid = $('#iid'+idstr).val();
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
});

$(document).on('click', '.delitem', function(){
	var idstr = $(this).attr("data");
	$('#itemad'+idstr).remove();
	$('#iname'+idstr).remove();
	$('#iid'+idstr).remove();
	$('#iqty'+idstr).remove();
	$('#iuom'+idstr).remove();
	$('#ialias'+idstr).remove();
	itemadd = $.grep(itemadd, function(value) {
		return value != idstr;
	});
	$('#itemrow'+idstr).remove();
	if (itemadd.length === 0) {
		$('.tfoot2').show();
	    
	}
	
});

$('#MaterialIssueForm').on('submit', function(){
	var error = 0;
	$('#spinner1').show();
	var date = $('input[name=date]').val();
	// var issue_locate = $('input[name=issue_locate]').val();
	// var vehicle = $('input[name=vehicle]').val();
	// var receive_locate = $('input[name=receive_locate]').val();
	if(date==''){
		error = 1;
		$('#date').addClass('errorcolor');
	}
	// if(issue_locate==''){
	// 	error = 1;
	// 	$('#issue_locate').addClass('errorcolor');
	// }
	// if(vehicle==''){
	// 	error = 1;
	// 	$('#vehicle').addClass('errorcolor');
	// }
	var jobnumber = $('#jobnumber').val();
	if(jobnumber==''){
		error = 1;
		$('#jobnumber').addClass('errorcolor');
	}
	if(porder==1){
		error = 1;
		$('#jobnumber').addClass('errorcolor');
	}
	// if(receive_locate==''){
	// 	error = 1;
	// 	$('#receive_locate').addClass('errorcolor');
	// }
	if(itemadd.length === 0) {
		error = 1;
	    $('.goods').addClass('errorcolor');
	}
	if(error==0){
		document.MaterialIssueForm.submit();
	}else{
		$('#spinner1').hide();
	}
	event.preventDefault();
});
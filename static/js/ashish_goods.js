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
	$('.already_error').hide();
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

var gch = 0;
var gbill = 0;
var porder = 0;
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
$('#porder').blur(function(){
	var val = $(this).val();
	val = val.toUpperCase();
	if($('#po'+val).length == 0){
		porder = 1;
		$(this).addClass('errorcolor');
		$('.porder_e').show();
	}else{
		if($('#pinv'+val).length == 0){
			v = val.toLowerCase();
			if($('#pinv'+v).length == 0){
				porder = 1;
				$(this).addClass('errorcolor');
				$('.porder_e').show();
			}else{
				porder = 0;
				$('.pvntabshow').show();
				$('.pinvrec').hide();
				$('#pinvrec'+v).show();
			}
		}else{
			porder = 0;
			$('.pvntabshow').show();
			$('.pinvrec').hide();
			$('#pinvrec'+val).show();
		}
	}
});

var add = 0;
var rec = 0;
var itemadd = [];
var diserror = 0;
var ponum = [];
$('#pvn').on('keyup', function(){
	$(this).removeClass('errorcolor');
});
$('#pvn').on('keypress',function(e){
	if(e.which===13){
		diserror = 0;
		$('.goods').removeClass('errorcolor');
		$('.loading').slideDown();
		$('#pvn').removeClass('errorcolor');
		var val = $('#pvn').val();
		val = val.toUpperCase();
		var po = $('#porder').val();
		if(po != ''){
			pou = po.toUpperCase();
			pol = po.toLowerCase();
			if($('#pinv'+pou+'pvn'+val).length > 0 || $('#pinv'+pol+'pvn'+val).length > 0){
				if($('.grd'+val).length == 0){
					if($('.gooid'+val).length > 0){
						if(ponum.length===0){
							ponum.push(po);
						}
						if($.inArray(po, ponum)!=-1){
							rec = rec + 1;
							var rus = val+rec;
							$('.gooid'+val).each(function(){
								var cha = $(this).val();
								var item = $('#item'+cha).val();
								var itemid = $('#itemid'+cha). val();
								var uom = $('#uom'+cha). val();
								var qty = $('#qty'+cha). val();
								var alias = $('#alias'+cha). val();

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
								$("#ItemTable tbody").append('<tr id="itemrow'+us+'"><td>'+item+'('+alias+')</td><td>'+uom+'</td><td>'+qty+'</td></tr>');
								$('.tfoot').show();
								$('#pvn').val('');
								$('#pvn').focus();
							});
							$(".grncol").append('<div class="coldiv grd'+val+'" id="colrec'+rus+'"><span class="coldes">'+val+'</span><button type="button" class="colbtn" data="'+rus+'"><i class="fa fa-times"></i></button></div>');
						}else{
							$('#porder').addClass('errorcolor');
						}

					}else{
						$('#pvn').addClass('errorcolor');
					}
				}else{
					$('#pvn').addClass('errorcolor');
				}
			}else{
				$('#pvn').addClass('errorcolor');
			}
		}else{
			$('#porder').addClass('errorcolor');
		}
		$('.loading').slideUp();
	}
});

$(document).on('click', '.colbtn', function(e){
	var idstr = $(this).attr("data");
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
	});
	if(itemadd.length === 0){
		ponum = [];
		$('tfoot').hide();
		$('.tfoot2').show();
	}
	$('#colrec'+idstr).remove();
	$('.loading').slideUp();

});

$('#GoodsForm').on('submit', function(){
	var error = 0;
	$('#spinner1').show();
	var date = $('input[name=date]').val();
	var grn = $('input[name=grn]').val();
	var challan = $('input[name=challan]').val();
	var bill = $('#bill').val();
	var location = $('#location option:selected').val();
	var supplier = $('#supplier option:selected').val();
	var vehicle = $('#vehicle').val();
	var pod = $('#porder').val();
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
	if(location==''){
		error = 1;
		$('#location').addClass('errorcolor');
	}
	if(supplier==''){
		error = 1;
		$('#supplier').addClass('errorcolor');
	}
	if(vehicle==''){
		error = 1;
		$('#vehicle').addClass('errorcolor');
	}
	if(pod==''){
		error = 1;
		$('#porder').addClass('errorcolor');
	}
	if(gch==1){
		error = 1;
		$('#challan').addClass('errorcolor');
	}
	if(gbill==1){
		error = 1;
		$('#bill').addClass('errorcolor');
	}
	if(porder==1){
		error = 1;
		$('#porder').addClass('errorcolor');
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
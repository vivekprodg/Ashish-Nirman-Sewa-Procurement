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

/*---------edit part----------*/
$('.tfoot').show();
var add = 0;
var rec = 0;
var itemadd = [];
var amount = [];
var diserror = 0;
$('.inv_count').each(function(){
	var cha = $(this).val();
	itemadd.push(cha);
});
$('.inv_amt').each(function(){
	var cha = $(this).val();
	amount.push(cha);
	add = add+1;
});
$('.rec_count').each(function(){
	var cha = $(this).val();
	rec = rec+1;
});
var dsup = $('#dsup').val();
// var dloc = $('#dloc').val();
var dinvtype = $('#dinvtype').val();
$('#supplier').val(dsup);
// $('#location').val(dloc);
$('#invoice_type').val(dinvtype);


/*=========================*/

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

$('#challan').click(function(){
	$('.challan_e').hide();
});
$('#invoice').click(function(){
	$('.bill_e').hide();
});

var pch = 0;
var pbill = 0
$('#challan').blur(function(){
	var val = $(this).val();
	pch = 0;
	$('.pchallan').each(function(){
		var cha = $(this).val();
		if(val == cha){
			pch = 1;
			$('#challan').addClass('errorcolor');
			$('.challan_e').show();
		}
	});
});
$('#invoice').blur(function(){
	var val = $(this).val();
	pbill = 0;
	$('.pvoice').each(function(){
		var cha = $(this).val();
		if(val == cha){
			pbill = 1;
			$('#invoice').addClass('errorcolor');
			$('.bill_e').show();
		}
	});
});

$('#grn').on('keypress',function(e){
	if(e.which===13){
		diserror = 0;
		$('.goods').removeClass('errorcolor');
		$('.loading').slideDown();
		$('#grn').removeClass('errorcolor');
		var val = $('#grn').val();
		val = val.toUpperCase();
		if($('.grd'+val).length == 0){
			if($('.gooid'+val).length > 0){
				rec = rec + 1;
				var rus = val+rec;
				itemadd.push(val);
				$('.gooid'+val).each(function(){
					var cha = $(this).val();
					var item = $('#item'+cha).val();
					var itemid = $('#itemid'+cha). val();
					var uom = $('#uom'+cha). val();
					var qty = $('#qty'+cha). val();
					var rate = $('#st'+itemid).val();
					qty = parseFloat(qty);
					rate = parseFloat(rate);
					var amt = qty * rate;
					amt = parseFloat(amt);
					amt = amt.toFixed(2);

					add = add + 1;
					amount.push(amt);
					var us = val+add;
					$(".hidden_inputs").append('<input type="hidden" class="irec'+rus+'" value="'+us+'" data="'+val+'">');
					$(".hidden_inputs").append('<input type="hidden" name="itemadd" id="itemad'+us+'" value="'+us+'">');
					$(".hidden_inputs").append('<input type="hidden" name="igrn'+us+'" id="igrn'+us+'" value="'+val+'">');
					$(".hidden_inputs").append('<input type="hidden" name="inameid'+us+'" id="inameid'+us+'" value="'+itemid+'">');
					$(".hidden_inputs").append('<input type="hidden" name="iname'+us+'" id="iname'+us+'" value="'+item+'">');
					$(".hidden_inputs").append('<input type="hidden" name="iuom'+us+'" id="iuom'+us+'" value="'+uom+'">');
					$(".hidden_inputs").append('<input type="hidden" name="iqty'+us+'" id="iqty'+us+'" value="'+qty+'">');
					$(".hidden_inputs").append('<input type="hidden" name="irate'+us+'" id="irate'+us+'" value="'+rate+'">');
					$(".hidden_inputs").append('<input type="hidden" class="iamount" name="iamt'+us+'" id="iamt'+us+'" value="'+amt+'">');
					$('.tfoot2').hide();
					$("#ItemTable tbody").append('<tr id="itemrow'+us+'"><td>'+item+'</td><td>'+uom+'</td><td>'+qty+'</td><td>'+rate+'</td><td class="ltd">'+amt+'</td></tr>');
					$('.tfoot').show();
					$('#grn').val('');
					$('#grn').focus();
				});
				$(".grncol").append('<div class="coldiv grd'+val+'" id="colrec'+rus+'"><span class="coldes">'+val+'</span><button type="button" class="colbtn" name="'+val+'" data="'+rus+'"><i class="fa fa-times"></i></button></div>');

				var sumamount = 0;
				sumamount = parseFloat(sumamount);
				$.each(amount,function(){sumamount+=parseFloat(this) || 0;});
				var sumamoun = sumamount.toFixed(2);
				$('#subtotal').val(sumamoun);

				var disp = $('#discount1').val();
				if(disp != '' && disp > 0){
					var dis = sumamount * disp/100;
					var disv = dis.toFixed(2);
					$('#discount2').val(disv);
				}else{
					var dis = $('#discount2').val();
				}
				var intype = $('#invoice_type option:selected').val();
				var vat = 0;
				var total = 0;
				if(dis != '' && dis > 0){
					dis = parseFloat(dis);
					if(dis < sumamount){
						if(intype != ''){
							if(intype == 'VAT Bill'){
								var tot = sumamount - dis;
								tot = parseFloat(tot);
								vat = tot * 13/100;
								vat = parseFloat(vat);
								total = tot + vat;
								total = parseFloat(total);
								vat = vat.toFixed(2);
								total = total.toFixed(2);
							}else{
								var tot = sumamount - dis;
								tot = parseFloat(tot);
								total = tot;
								total = parseFloat(total);
								total = total.toFixed(2);
							}
						}else{
							$('#invoice_type').addClass('errorcolor');
						}
					}else{
						diserror = 1;
						$('#discount2').addClass('errorcolor');
						$('#discount1').addClass('errorcolor');
					}
				}else{
					if(intype != ''){
						if(intype == 'VAT Bill'){
							vat = sumamount * 13/100;
							vat = parseFloat(vat);
							total = sumamount + vat;
							total = parseFloat(total);
							vat = vat.toFixed(2);
							total = total.toFixed(2);
						}else{
							total = sumamoun;
						}
					}else{
						$('#invoice_type').addClass('errorcolor');
					}
				}

				$('#vat').val(vat);
				$('#total').val(total);

			}else{
				$('#grn').addClass('errorcolor');
			}
		}else{
			$('#grn').addClass('errorcolor');
		}
		$('.loading').slideUp();
	}
});

$(document).on('click', '.colbtn', function(e){
	var idstr = $(this).attr("data");
	var grr = $(this).attr("name");
	diserror = 0;
	$('.loading').slideDown();
	$('.irec'+idstr).each(function(){
		var cha = $(this).val();
		var hac = $(this).attr("data");
		$('#itemad'+cha).remove();
		$('#igrn'+cha).remove();
		$('#inameid'+cha).remove();
		$('#iname'+cha).remove();
		$('#iuom'+cha).remove();
		$('#iqty'+cha).remove();
		$('#irate'+cha).remove();
		$('#iamt'+cha).remove();

		$('#itemrow'+cha).remove();
	});
	itemadd = $.grep(itemadd, function(value) {
		return value != grr;
	});
	amount = [];
	if(itemadd.length === 0){
		$('#colrec'+idstr).remove();
		$('#subtotal').val(0);
		$('#discount1').val(0);
		$('#discount2').val(0);
		$('#vat').val(0);
		$('#total').val(0);
		$('tfoot').hide();
		$('.tfoot2').show();
	}else{
		$('.iamount').each(function(){
			var val = $(this).val();
			amount.push(val);
		});
		var sumamount = 0;
		sumamount = parseFloat(sumamount);
		$.each(amount,function(){sumamount+=parseFloat(this) || 0;});
		var sumamoun = sumamount.toFixed(2);
		$('#subtotal').val(sumamoun);
		$('#colrec'+idstr).remove();

		var disp = $('#discount1').val();
		var dis = sumamount * disp/100;
		var disv = dis.toFixed(2);
		$('#discount2').val(disv);
		var intype = $('#invoice_type option:selected').val();
		var vat = 0;
		var total = 0;
		if(dis != '' && dis > 0){
			dis = parseFloat(dis);
			if(dis < sumamount){
				if(intype != ''){
					if(intype == 'VAT Bill'){
						var tot = sumamount - dis;
						tot = parseFloat(tot);
						vat = tot * 13/100;
						vat = parseFloat(vat);
						total = tot + vat;
						total = parseFloat(total);
						vat = vat.toFixed(2);
						total = total.toFixed(2);
					}else{
						var tot = sumamount - dis;
						tot = parseFloat(tot);
						total = tot;
						total = parseFloat(total);
						total = total.toFixed(2);
					}
				}else{
					$('#invoice_type').addClass('errorcolor');
				}
			}else{
				diserror = 1;
				$('#discount2').addClass('errorcolor');
				$('#discount1').addClass('errorcolor');
			}
		}else{
			if(intype != ''){
				if(intype == 'VAT Bill'){
					vat = sumamount * 13/100;
					vat = parseFloat(vat);
					total = sumamount + vat;
					total = parseFloat(total);
					vat = vat.toFixed(2);
					total = total.toFixed(2);
				}else{
					total = sumamoun;
				}
			}else{
				$('#invoice_type').addClass('errorcolor');
			}
		}
		$('#vat').val(vat);
		$('#total').val(total);
	}
	$('.loading').slideUp();

});

$('#discount1').on('keyup', function(){
	diserror = 0;
	$(this).removeClass('errorcolor');
	$('#discount2').removeClass('errorcolor');
	var val = $(this).val();
	var intype = $('#invoice_type option:selected').val();
	var sub = $('#subtotal').val();
	var sumamount = parseFloat(sub);
	var	dis = 0;
	if(val != '' && val > 0){
		dis = sumamount * val/100;
		dis = parseFloat(dis);
		if(dis < sumamount){
			var total = 0;
			var vat = 0;
			if(intype != ''){
				if(intype == 'VAT Bill'){
					var tot = sumamount - dis;
					tot = parseFloat(tot);
					vat = tot * 13/100;
					vat = parseFloat(vat);
					total = tot + vat;
					total = parseFloat(total);
					vat = vat.toFixed(2);
					total = total.toFixed(2);
				}else{
					var tot = sumamount - dis;
					tot = parseFloat(tot);
					total = tot;
					total = parseFloat(total);
					total = total.toFixed(2);
				}
			}else{
				$('#invoice_type').addClass('errorcolor');
			}
			$('#vat').val(vat);
			$('#total').val(total);
		}else{
			diserror = 1;
			$(this).addClass('errorcolor');
			$('#discount2').addClass('errorcolor');
		}
	}else{
		var total = 0;
		var vat = 0;
		if(intype != ''){
			if(intype == 'VAT Bill'){
				vat = sumamount * 13/100;
				vat = parseFloat(vat);
				total = sumamount + vat;
				total = parseFloat(total);
				vat = vat.toFixed(2);
				total = total.toFixed(2);
			}else{
				total = sumamount.toFixed(2);
			}
		}else{
			$('#invoice_type').addClass('errorcolor');
		}
		$('#vat').val(vat);
		$('#total').val(total);
	}
	dis = dis.toFixed(2);
	$('#discount2').val(dis);

});

$('#discount2').on('keyup', function(){
	diserror = 0;
	$(this).removeClass('errorcolor');
	$('#discount1').removeClass('errorcolor');
	var intype = $('#invoice_type option:selected').val();
	var dis = $(this).val();
	var sub = $('#subtotal').val();
	var sumamount = parseFloat(sub);
	var	val = 0;
	if(dis != '' && dis > 0){
		dis = parseFloat(dis);
		if(dis < sumamount){
			val = dis * 100/sumamount;
			val = parseFloat(val);
			var total = 0;
			var vat = 0;
			if(intype != ''){
				if(intype == 'VAT Bill'){
					var tot = sumamount - dis;
					tot = parseFloat(tot);
					vat = tot * 13/100;
					vat = parseFloat(vat);
					total = tot + vat;
					total = parseFloat(total);
					vat = vat.toFixed(2);
					total = total.toFixed(2);
				}else{
					var tot = sumamount - dis;
					tot = parseFloat(tot);
					total = tot;
					total = parseFloat(total);
					total = total.toFixed(2);
				}
			}else{
				$('#invoice_type').addClass('errorcolor');
			}
			$('#vat').val(vat);
			$('#total').val(total);
		}else{
			diserror = 1;
			$(this).addClass('errorcolor');
			$('#discount1').addClass('errorcolor');
		}
	}else{
		var total = 0;
		var vat = 0;
		if(intype != ''){
			if(intype == 'VAT Bill'){
				vat = sumamount * 13/100;
				vat = parseFloat(vat);
				total = sumamount + vat;
				total = parseFloat(total);
				vat = vat.toFixed(2);
				total = total.toFixed(2);
			}else{
				total = sumamount.toFixed(2);
			}
		}else{
			$('#invoice_type').addClass('errorcolor');
		}
		$('#vat').val(vat);
		$('#total').val(total);
	}
	val = val.toFixed(2);
	$('#discount1').val(val);

});

$('#invoice_type').on('change', function(){
	diserror = 0;
	var intype = $('#invoice_type option:selected').val();
	var disp = $('#discount1').val();
	if(disp != '' && disp > 0){
		var dis = sumamount * disp/100;
		var disv = dis.toFixed(2);
		$('#discount2').val(disv);
	}else{
		var dis = $('#discount2').val();
	}
	var sub = $('#subtotal').val();
	var sumamount = 0;
	if(sub != ''){
		sumamount = parseFloat(sub);
	}
	var vat = 0;
	var total = 0;
	if(dis != '' && dis > 0){
		dis = parseFloat(dis);
		if(dis < sumamount){
			if(intype != ''){
				if(intype == 'VAT Bill'){
					var tot = sumamount - dis;
					tot = parseFloat(tot);
					vat = tot * 13/100;
					vat = parseFloat(vat);
					total = tot + vat;
					total = parseFloat(total);
					vat = vat.toFixed(2);
					total = total.toFixed(2);
				}else{
					var tot = sumamount - dis;
					tot = parseFloat(tot);
					total = tot;
					total = parseFloat(total);
					total = total.toFixed(2);
				}
			}else{
				$('#invoice_type').addClass('errorcolor');
			}
		}else{
			diserror = 1;
			$('#discount2').addClass('errorcolor');
			$('#discount1').addClass('errorcolor');
		}
	}else{
		if(intype != ''){
			if(intype == 'VAT Bill'){
				vat = sumamount * 13/100;
				vat = parseFloat(vat);
				total = sumamount + vat;
				total = parseFloat(total);
				vat = vat.toFixed(2);
				total = total.toFixed(2);
			}else{
				total = sumamount.toFixed(2);
			}
		}else{
			$('#invoice_type').addClass('errorcolor');
		}
	}
	$('#vat').val(vat);
	$('#total').val(total);
});

$('#InvoiceForm').on('submit', function(){
	var error = 0;
	$('#spinner1').show();
	var date = $('input[name=date]').val();
	var invoice_date = $('input[name=invoice_date]').val();
	var voucher_number = $('input[name=voucher_number]').val();
	var invoice = $('input[name=invoice]').val();
	var challan = $('input[name=challan]').val();
	var vehicle = $('input[name=vehicle]').val();
	// var location = $('input[name=location]').val();
	var invoice_type = $('#invoice_type option:selected').val();
	var supplier = $('#supplier option:selected').val();
	var discount = $('input[name=discount2]').val();
	var amount = $('input[name=total]').val();
	if(date==''){
		error = 1;
		$('#date').addClass('errorcolor');
	}
	if(invoice_date==''){
		error = 1;
		$('#invoice_date').addClass('errorcolor');
	}
	if(voucher_number==''){
		error = 1;
		$('#voucher_number').addClass('errorcolor');
	}
	if(challan==''){
		error = 1;
		$('#challan').addClass('errorcolor');
	}
	if(invoice==''){
		$('#invoice').val('none');
	}
	if(invoice_type==''){
		error = 1;
		$('#invoice_type').addClass('errorcolor');
	}
	if(supplier==''){
		error = 1;
		$('#supplier').addClass('errorcolor');
	}
	// if(vehicle==''){
	// 	error = 1;
	// 	$('#vehicle').addClass('errorcolor');
	// }
	if(amount=='' || amount < 0 || amount == 0){
		error = 1;
	}
	if(diserror==1){
		error = 1;
		$('#discount1').addClass('errorcolor');
		$('#discount2').addClass('errorcolor');
	}
	if(pch==1){
		error = 1;
		$('#challan').addClass('errorcolor');
	}
	if(pbill==1){
		error = 1;
		$('#invoice').addClass('errorcolor');
	}
	if(discount=='' || discount < 0){
		$('#discount1').val(0);
		$('#discount2').val(0);
	}
	if(itemadd.length === 0) {
		error = 1
	    $('.goods').addClass('errorcolor');
	}
	if(error==0){
		document.InvoiceForm.submit();
	}else{
		$('#spinner1').hide();
	}
	event.preventDefault();
});
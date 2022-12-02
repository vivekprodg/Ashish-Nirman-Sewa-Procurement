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
	add = add+1;
	itemadd.push(cha);
});
$('.inv_amount').each(function(){
	var cha = $(this).val();
	amount.push(cha);
});
var dsup = $('#dsup').val();
// var dloc = $('#dloc').val();
var dinvtype = $('#dinvtype').val();
$('#supplier').val(dsup);
// $('#location').val(dloc);
$('#invoice_type').val(dinvtype);
var dtran = $('#dtrans').val();
if(dtran=='credit'){
	$('#crejob').prop("checked", true);
	$('#payday').show();
}
if(dtran=='cash'){
	$('#cajob').prop("checked", true);
	$('#payday').hide();
}


/*=========================*/

// $('#additem').click(function(){
// 	$('.edit_popupbanner').fadeIn();
// 	$('#edit_popup').css({"transform": "scale(1)", "-webkit-transform": "scale(1)", "-moz-transform": "scale(1)"});	$('#itemname').focus();
// 	$('#item').focus();
// });
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
$('#porder').click(function(){
	$('.porder_e').hide();
});

$('#crcheck').click(function(){
	$('#crejob').prop('checked', true);
	$('#cajob').prop('checked', false);
	$('#trans').val('credit');
	$('#payday').show();
});

$('#cacheck').click(function(){
	$('#crejob').prop('checked', false);
	$('#cajob').prop('checked', true);
	$('#trans').val('cash');
	$('#payday').hide();
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
$('#porder').blur(function(){
	var val = $(this).val();
	val = val.toUpperCase();
	if($('#po'+val).length == 0){
		porder = 1;
		$(this).addClass('errorcolor');
		$('.porder_e').show();
	}else{
		porder = 0;
	}
});

$('#additem').click(function(){
	var pon = $('#porder').val();
	if(pon!=''){
		var val = $('#porder').val();
		val = val.toUpperCase();
		if($('#po'+val).length>0){
			$('.edit_popupbanner').fadeIn();
			$('#edit_popup').css({"transform": "scale(1)", "-webkit-transform": "scale(1)", "-moz-transform": "scale(1)"});	$('#itemname').focus();
			$('#item').focus();
			$('.pitm'+val).each(function(){
				var itm_id = $(this).val();
				var itm = $(this).attr("data");
				if($("#item option[value='"+itm_id+"']").length===0){
					$('#item').append($('<option>', {
					    value: itm_id,
					    text: itm
					}));
				}
				
			});
		}else{
			$('#porder').addClass('errorcolor');
		}
	}else{
		$('#porder').addClass('errorcolor');
	}

});

$('#item').on('change', function(){
	$('#rate').removeClass('errorcolor');
	var idstr = $('#item option:selected').val();
	var name = $('#ini'+idstr).val();
	var uom = $('#ini'+idstr).attr("data");
	var alias = $('#ini'+idstr).attr("name");
	// var rate = $('#ini'+idstr).attr("name");
	$('#itemname').val(name);
	$('#uom').val(uom);
	$('#itemalias').val(alias);
	// $('#rate').val(rate);
	// var rate = $('#rate').val();
	// var qty = $('#qty').val();
	// if(qty != '' && qty > 0 && rate != '' && rate == 0 || rate > 0){
	// 	qty = parseFloat(qty);
	// 	rate = parseFloat(rate);
	// 	var amt = qty * rate;
	// 	amt = parseFloat(amt);
	// 	amt = amt.toFixed(2);
	// 	$('#amount').val(amt);
	// }
});
$('#edititem').on('change', function(){
	$('#editrate').removeClass('errorcolor');
	var idstr = $('#edititem option:selected').val();
	var name = $('#eini'+idstr).val();
	var uom = $('#eini'+idstr).attr("data");
	var alias = $('#eini'+idstr).attr("name");
	// var rate = $('#eini'+idstr).attr("name");
	$('#edititemname').val(name);
	$('#edituom').val(uom);
	$('#edititemalias').val(alias);
	// $('#editrate').val(rate);
	// var rate = $('#editrate').val();
	// var qty = $('#editqty').val();
	// if(qty != '' && qty > 0 && rate != '' && rate == 0 || rate > 0){
	// 	qty = parseFloat(qty);
	// 	rate = parseFloat(rate);
	// 	var amt = qty * rate;
	// 	amt = parseFloat(amt);
	// 	amt = amt.toFixed(2);
	// 	$('#editamount').val(amt);
	// }
});

// $('#qty').on('keyup', function(){
// 	$(this).removeClass('errorcolor');
// 	var qty = $(this).val();
// 	if(qty != '' && qty > 0){
// 		qty = parseFloat(qty);
// 		var rate = $('#rate').val();
// 		if(rate != '' && rate > 0){
// 			rate = parseFloat(rate);
// 			var amt = qty * rate;
// 			amt =parseFloat(amt);
// 			amt = amt.toFixed(2);
// 			$('#amount').val(amt);
// 		}else{
// 			$('#rate').addClass('errorcolor');
// 		}
// 	}else{
// 		$('#qty').addClass('errorcolor');
// 	}
// });
// $('#rate').on('keyup', function(){
// 	$(this).removeClass('errorcolor');
// 	var rate = $(this).val();
// 	if(rate != '' && rate == 0 || rate > 0){
// 		rate = parseFloat(rate);
// 		var qty = $('#qty').val();
// 		if(qty != '' && qty > 0){
// 			qty = parseFloat(qty);
// 			var amt = qty * rate;
// 			amt =parseFloat(amt);
// 			amt = amt.toFixed(2);
// 			$('#amount').val(amt);
// 		}else{
// 			$('#qty').addClass('errorcolor');
// 		}
// 	}else{
// 		$('#rate').addClass('errorcolor');
// 	}
// });
// $('#editqty').on('keyup', function(){
// 	$(this).removeClass('errorcolor');
// 	var qty = $(this).val();
// 	if(qty != '' && qty > 0){
// 		qty = parseFloat(qty);
// 		var rate = $('#editrate').val();
// 		if(rate != '' && rate > 0){
// 			rate = parseFloat(rate);
// 			var amt = qty * rate;
// 			amt =parseFloat(amt);
// 			amt = amt.toFixed(2);
// 			$('#editamount').val(amt);
// 		}else{
// 			$('#editrate').addClass('errorcolor');
// 		}
// 	}else{
// 		$(this).addClass('errorcolor');
// 	}
// });
// $('#editrate').on('keyup', function(){
// 	$(this).removeClass('errorcolor');
// 	var rate = $(this).val();
// 	if(rate != '' && rate == 0 || rate > 0){
// 		rate = parseFloat(rate);
// 		var qty = $('#editqty').val();
// 		if(qty != '' && qty > 0){
// 			qty = parseFloat(qty);
// 			var amt = qty * rate;
// 			amt =parseFloat(amt);
// 			amt = amt.toFixed(2);
// 			$('#editamount').val(amt);
// 		}else{
// 			$('#editqty').addClass('errorcolor');
// 		}
// 	}else{
// 		$('#editrate').addClass('errorcolor');
// 	}
// });

$('#qty').on('keyup', function(){
	var val = $(this).val();
	if(val != ''){
		val =parseFloat(val);
		val = val.toFixed(2);
		if(val>0){
			var rt = $('#rate').val();
			if(rt!=''){
				if(rt>0){
					rt = parseFloat(rt);
					rt = rt.toFixed(2);
					var amt = val * rt;
					amt = parseFloat(amt);
					amt = amt.toFixed(2);
					$('#amount').val(amt);
					var dis_per = $('#discount_per').val();
					if(dis_per != '' && dis_per > 0){
						var dis = amt * dis_per/100;
						dis = parseFloat(dis);
						if(dis < amt){
							var total = amt - dis;
							total = parseFloat(total);
							total = total.toFixed(2);
							$('#amount').val(total);
							$('#discount_amt').removeClass('errorcolor');
							$('#discount_per').removeClass('errorcolor');
						}else{
							$(this).addClass('errorcolor');
							$('#discount_amt').addClass('errorcolor');
							$('#discount_per').addClass('errorcolor');
						}
						$('#discount_amt').val(dis);
					} 
				}else{
					$('#rate').addClass('errorcolor');
				}
			}else{
				$('#rate').addClass('errorcolor');
			}
		}else{
			$(this).addClass('errorcolor');
			$('#amount').val(0);
			$('#discount_per').val(0);
			$('#discount_amt').val(0);
		}
	}else{
		$(this).addClass('errorcolor');
	}
});
$('#rate').on('keyup', function(){
	var val = $(this).val();
	if(val != ''){
		val =parseFloat(val);
		val = val.toFixed(2);
		if(val>0){
			var rt = $('#qty').val();
			if(rt!=''){
				if(rt>0){
					rt = parseFloat(rt);
					rt = rt.toFixed(2);
					var amt = val * rt;
					amt = parseFloat(amt);
					amt = amt.toFixed(2);
					$('#amount').val(amt);
					var dis_per = $('#discount_per').val();
					if(dis_per != '' && dis_per > 0){
						var dis = amt * dis_per/100;
						dis = parseFloat(dis);
						if(dis < amt){
							var total = amt - dis;
							total = parseFloat(total);
							total = total.toFixed(2);
							$('#amount').val(total);
							$('#discount_amt').removeClass('errorcolor');
							$('#discount_per').removeClass('errorcolor');
						}else{
							$(this).addClass('errorcolor');
							$('#discount_amt').addClass('errorcolor');
							$('#discount_per').addClass('errorcolor');
						}
						$('#discount_amt').val(dis);
					}
				}else{
					$('#qty').addClass('errorcolor');
				}
			}else{
				$('#qty').addClass('errorcolor');
			}
		}else{
			$(this).addClass('errorcolor');
			$('#amount').val(0);
			$('#discount_per').val(0);
			$('#discount_amt').val(0);
		}
	}else{
		$(this).addClass('errorcolor');
	}
});

$('#editqty').on('keyup', function(){
	var val = $(this).val();
	if(val != ''){
		val =parseFloat(val);
		val = val.toFixed(2);
		if(val>0){
			var rt = $('#editrate').val();
			if(rt!=''){
				if(rt>0){
					rt = parseFloat(rt);
					rt = rt.toFixed(2);
					var amt = val * rt;
					amt = parseFloat(amt);
					amt = amt.toFixed(2);
					$('#editamount').val(amt);
					var dis_per = $('#editdiscount_per').val();
					if(dis_per != '' && dis_per > 0){
						var dis = amt * dis_per/100;
						dis = parseFloat(dis);
						if(dis < amt){
							var total = amt - dis;
							total = parseFloat(total);
							total = total.toFixed(2);
							$('#editamount').val(total);
							$('#editdiscount_amt').removeClass('errorcolor');
							$('#editdiscount_per').removeClass('errorcolor');
						}else{
							$(this).addClass('errorcolor');
							$('#editdiscount_amt').addClass('errorcolor');
							$('#editdiscount_per').addClass('errorcolor');
						}
						$('#editdiscount_amt').val(dis);
					} 
				}else{
					$('#editrate').addClass('errorcolor');
				}
			}else{
				$('#editrate').addClass('errorcolor');
			}
		}else{
			$(this).addClass('errorcolor');
			$('#editamount').val(0);
			$('#editdiscount_per').val(0);
			$('#editdiscount_amt').val(0);
		}
	}else{
		$(this).addClass('errorcolor');
	}
});
$('#editrate').on('keyup', function(){
	var val = $(this).val();
	if(val != ''){
		val =parseFloat(val);
		val = val.toFixed(2);
		if(val>0){
			var rt = $('#editqty').val();
			if(rt!=''){
				if(rt>0){
					rt = parseFloat(rt);
					rt = rt.toFixed(2);
					var amt = val * rt;
					amt = parseFloat(amt);
					amt = amt.toFixed(2);
					$('#editamount').val(amt);
					var dis_per = $('#editdiscount_per').val();
					if(dis_per != '' && dis_per > 0){
						var dis = amt * dis_per/100;
						dis = parseFloat(dis);
						if(dis < amt){
							var total = amt - dis;
							total = parseFloat(total);
							total = total.toFixed(2);
							$('#editamount').val(total);
							$('#editdiscount_amt').removeClass('errorcolor');
							$('#editdiscount_per').removeClass('errorcolor');
						}else{
							$(this).addClass('errorcolor');
							$('#editdiscount_amt').addClass('errorcolor');
							$('#editdiscount_per').addClass('errorcolor');
						}
						$('#editdiscount_amt').val(dis);
					}
				}else{
					$('#editqty').addClass('errorcolor');
				}
			}else{
				$('#editqty').addClass('errorcolor');
			}
		}else{
			$(this).addClass('errorcolor');
			$('#editamount').val(0);
			$('#editdiscount_per').val(0);
			$('#editdiscount_amt').val(0);
		}
	}else{
		$(this).addClass('errorcolor');
	}
});

$('#additembtn').on('click',function(){
	diserror = 0;
	var error = 0;
	$('#item').focus();
	var item = $('#item option:selected').val();
	var itemname = $('#itemname').val();
	var uom = $('#uom').val();
	var qty = $('#qty').val();
	var rate = $('#rate').val();
	var amt = $('#amount').val();
	var alias = $('#itemalias').val();
	var dis_per = $('#discount_per').val();
	var dis_amt = $('#discount_amt').val();
	if(dis_per == ''){
		dis_per = 0;
	}
	if(dis_amt == ''){
		dis_amt = 0;
	}
	if(rate==''){
		$('#rate').addClass('errorcolor');
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
		amount.push(amt);
		$(".hidden_inputs").append('<input type="hidden" name="itemadd" id="itemad'+add+'" value="'+add+'">');
		$(".hidden_inputs").append('<input type="hidden" name="inameid'+add+'" id="inameid'+add+'" value="'+item+'">');
		$(".hidden_inputs").append('<input type="hidden" name="iname'+add+'" id="iname'+add+'" value="'+itemname+'">');
		$(".hidden_inputs").append('<input type="hidden" name="iuom'+add+'" id="iuom'+add+'" value="'+uom+'">');
		$(".hidden_inputs").append('<input type="hidden" name="iqty'+add+'" id="iqty'+add+'" value="'+qty+'">');
		$(".hidden_inputs").append('<input type="hidden" name="irate'+add+'" id="irate'+add+'" value="'+rate+'">');
		$(".hidden_inputs").append('<input type="hidden" name="iamt'+add+'" id="iamt'+add+'" value="'+amt+'">');
		$(".hidden_inputs").append('<input type="hidden" name="ialias'+add+'" id="ialias'+add+'" value="'+alias+'">');
		$(".hidden_inputs").append('<input type="hidden" name="idisper'+add+'" id="idisper'+add+'" value="'+dis_per+'">');
		$(".hidden_inputs").append('<input type="hidden" name="idisamt'+add+'" id="idisamt'+add+'" value="'+dis_amt+'">');
		$('.tfoot2').hide();
		$("#ItemTable tbody").append('<tr id="itemrow'+add+'"><td><button type="button" class="edititem" id="eitem'+add+'" data="'+add+'"><i class="far fa-edit"></i></button><button type="button" class="delitem" id="ditem'+add+'" data="'+add+'"><i class="far fa-trash-alt"></i></button></td><td>'+itemname+'('+alias+')</td><td>'+uom+'</td><td>'+qty+'</td><td>'+rate+'</td><td>'+dis_amt+' ('+dis_per+'%)</td><td class="ltd">'+amt+'</td></tr>');
		$('.tfoot').show();

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

		$('#item').val('');
		$('#itemname').val('');
		$('#uom').val('');
		$('#itemalias').val('');
		$('#qty').val('');
		$('#rate').val('');
		$('#amount').val('');
		$('#discount_per').val(0);
		$('#discount_amt').val(0);
	}
});

$('#additemeditbtn').click(function(){
	diserror = 0;
	var error = 0;
	$('#edititem').focus();
	var item = $('#edititem option:selected').val();
	var itemname = $('#edititemname').val();
	var uom = $('#edituom').val();
	var qty = $('#editqty').val();
	var rate = $('#editrate').val();
	var amt = $('#editamount').val();
	var did = $('#dfaultid').val();
	var alias = $('#edititemalias').val();
	var dis_per = $('#editdiscount_per').val();
	var dis_amt = $('#editdiscount_amt').val();
	if(dis_per == ''){
		dis_per = 0;
	}
	if(dis_amt == ''){
		dis_amt = 0;
	}
	if(rate==''){
		error = 1;
		$('#editrate').addClass('errorcolor');
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
	$('#inameid'+did).val(item);
	$('#iname'+did).val(itemname);
	$('#iuom'+did).val(uom);
	$('#iqty'+did).val(qty);
	$('#irate'+did).val(remark);
	$('#iamt'+did).val(remark);
	$('#ialias'+did).val(alias);
	$('#idisper'+did).val(dis_per);
	$('#idisamt'+did).val(dis_amt);
	$('#edititemname').val('');
	$('#edititem').val('');
	$('#editqty').val('');
	$('#edituom').val('');
	$('#editrate').val('');
	$('#editamount').val('');
	$('#edititemalias').val('');
	$('#editdiscount_per').val(0);
	$('#editdiscount_amt').val(0);
	$('#itemrow'+did).remove();
	$("#ItemTable tbody").append('<tr id="itemrow'+did+'"><td><button type="button" class="edititem" id="eitem'+did+'" data="'+did+'"><i class="far fa-edit"></i></button><button type="button" class="delitem" id="ditem'+did+'" data="'+did+'"><i class="far fa-trash-alt"></i></button></td><td>'+itemname+'('+alias+')</td><td>'+uom+'</td><td>'+qty+'</td><td>'+rate+'</td><td>'+dis_amt+' ('+dis_per+'%)</td><td>'+amt+'</td></tr>');

	amount = [];
	$.each(itemadd , function(index, val) { 
	  var arrayatm = $('#iamt'+val).val();
	  amount.push(arrayatm);
	});

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

	$('#edit_popup1').css({"transform": "scale(.1)", "-webkit-transform": "scale(.1)", "-moz-transform": "scale(.1)"});
	$('.edit_popupbanner1').fadeOut();

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

$('#discount_per').on('keyup', function(){
	$(this).removeClass('errorcolor');
	$('#discount_amt').removeClass('errorcolor');
	var val = $(this).val();
	var	dis = 0;
	var qty = $('#qty').val();
	var rate = $('#rate').val();
	if(qty > 0 && rate > 0){
		qty = parseFloat(qty);
		rate = parseFloat(rate);
		var total = qty * rate;
		total = parseFloat(total);
		if(val != '' && val > 0){
			dis = total * val/100;
			dis = parseFloat(dis);
			if(dis < total){
				total = total - dis;
				total = total.toFixed(2);
				$('#amount').val(total);
			}else{
				$(this).addClass('errorcolor');
				$('#discount_per').addClass('errorcolor');
			}
		}else{
			qty = parseFloat(qty);
			rate = parseFloat(rate);
			var total = qty * rate;
			total = parseFloat(total);
			total = total.toFixed(2);
			$('#amount').val(total);
		}
	}
	dis = dis.toFixed(2);
	$('#discount_amt').val(dis);

});

$('#discount_amt').on('keyup', function(){
	$(this).removeClass('errorcolor');
	$('#discount_per').removeClass('errorcolor');
	var val = $(this).val();
	var	dis = 0;
	var qty = $('#qty').val();
	var rate = $('#rate').val();
	if(qty > 0 && rate > 0){
		qty = parseFloat(qty);
		rate = parseFloat(rate);
		var total = qty * rate;
		total = parseFloat(total);
		if(val != '' && val > 0){
			dis = val * 100/total;
			dis = parseFloat(dis);
			if(val < total){
				total = total - val;
				total = total.toFixed(2);
				$('#amount').val(total);
			}else{
				$(this).addClass('errorcolor');
				$('#discount_amt').addClass('errorcolor');
			}
		}else{
			qty = parseFloat(qty);
			rate = parseFloat(rate);
			var total = qty * rate;
			total = parseFloat(total);
			total = total.toFixed(2);
			$('#amount').val(total);
		}

	}
	dis = dis.toFixed(2);
	$('#discount_per').val(dis);

});

$('#editdiscount_per').on('keyup', function(){
	$(this).removeClass('errorcolor');
	$('#editdiscount_amt').removeClass('errorcolor');
	var val = $(this).val();
	var	dis = 0;
	var qty = $('#editqty').val();
	var rate = $('#editrate').val();
	if(qty > 0 && rate > 0){
		qty = parseFloat(qty);
		rate = parseFloat(rate);
		var total = qty * rate;
		total = parseFloat(total);
		if(val != '' && val > 0){
			dis = total * val/100;
			dis = parseFloat(dis);
			if(dis < total){
				total = total - dis;
				total = total.toFixed(2);
				$('#editamount').val(total);
			}else{
				$(this).addClass('errorcolor');
				$('#editdiscount_per').addClass('errorcolor');
			}
		}else{
			qty = parseFloat(qty);
			rate = parseFloat(rate);
			var total = qty * rate;
			total = parseFloat(total);
			total = total.toFixed(2);
			$('#editamount').val(total);
		}
	}
	dis = dis.toFixed(2);
	$('#editdiscount_amt').val(dis);

});

$('#editdiscount_amt').on('keyup', function(){
	$(this).removeClass('errorcolor');
	$('#editdiscount_per').removeClass('errorcolor');
	var val = $(this).val();
	var	dis = 0;
	var qty = $('#editqty').val();
	var rate = $('#editrate').val();
	if(qty > 0 && rate > 0){
		qty = parseFloat(qty);
		rate = parseFloat(rate);
		var total = qty * rate;
		total = parseFloat(total);
		if(val != '' && val > 0){
			dis = val * 100/total;
			dis = parseFloat(dis);
			if(val < total){
				total = total - val;
				total = total.toFixed(2);
				$('#editamount').val(total);
			}else{
				$(this).addClass('errorcolor');
				$('#editdiscount_amt').addClass('errorcolor');
			}
		}else{
			qty = parseFloat(qty);
			rate = parseFloat(rate);
			var total = qty * rate;
			total = parseFloat(total);
			total = total.toFixed(2);
			$('#editamount').val(total);
		}

	}
	dis = dis.toFixed(2);
	$('#editdiscount_per').val(dis);

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

$(document).on('click', '.edititem', function(){
	var idstr = $(this).attr("data");
	var val = $('#porder').val();
	if(val!=''){
		val = val.toUpperCase();
		if($('#po'+val).length>0){
			$('.edit_popupbanner1').fadeIn();
			$('#edit_popup1').css({"transform": "scale(1)", "-webkit-transform": "scale(1)", "-moz-transform": "scale(1)"});	$('#itemname').focus();
			$('#edititem').focus();
			$('.epitm'+val).each(function(){
				var itm_id = $(this).val();
				var itm = $(this).attr("data");
				if($("#edititem option[value='"+itm_id+"']").length===0){
					$('#edititem').append($('<option>', {
					    value: itm_id,
					    text: itm
					}));
				}
				
			});
			var itemid = $('#inameid'+idstr).val();
			var name = $('#iname'+idstr).val();
			var uom = $('#iuom'+idstr).val();
			var qty = $('#iqty'+idstr).val();
			var rate = $('#irate'+idstr).val();
			var amt = $('#iamt'+idstr).val();
			var alias = $('#ialias'+idstr).val();
			var disper = $('#idisper'+idstr).val();
			var disamt = $('#idisamt'+idstr).val();
			$('#edititem').val(itemid);
			$('#edititemname').val(name);
			$('#edituom').val(uom);
			$('#editqty').val(qty);
			$('#editrate').val(rate);
			$('#editamount').val(amt);
			$('#edititemalias').val(alias);
			$('#editdiscount_per').val(disper);
			$('#editdiscount_amt').val(disamt);
			$('#dfaultid').val(idstr);
		}else{
			$('#porder').addClass('errorcolor');
		}
	}else{
		$('#porder').addClass('errorcolor');
	}
	
});

$(document).on('click', '.delitem', function(){
	var idstr = $(this).attr("data");
	$('#itemad'+idstr).remove();
	$('#iname'+idstr).remove();
	$('#inameid'+idstr).remove();
	$('#iqty'+idstr).remove();
	$('#iuom'+idstr).remove();
	$('#irate'+idstr).remove();
	$('#iamt'+idstr).remove();
	$('#ialias'+idstr).remove();
	$('#idisper'+idstr).remove();
	$('#idisamt'+idstr).remove();
	itemadd = $.grep(itemadd, function(value) {
		return value != idstr;
	});
	$('#itemrow'+idstr).remove();
	if (itemadd.length === 0) {
		$('#subtotal').val(0);
		$('#discount1').val(0);
		$('#discount2').val(0);
		$('#vat').val(0);
		$('#total').val(0);
		$('.tfoot').hide();
		$('.tfoot2').show();
	    
	}else{
		amount = [];
		$.each(itemadd , function(index, val) { 
		  var arrayatm = $('#iamt'+val).val();
		  amount.push(arrayatm);
		});

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
	}
	
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
	var location = $('input[name=location]').val();
	var invoice_type = $('#invoice_type option:selected').val();
	var supplier = $('#supplier option:selected').val();
	var discount = $('input[name=discount2]').val();
	var amount = $('input[name=total]').val();
	var pod = $('#porder').val();
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
		error = 1;
		$('#invoice').addClass('errorcolor');
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
	if(pod==''){
		error = 1;
		$('#porder').addClass('errorcolor');
	}
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
	if($('#crejob').prop("checked") == false){
		if($('#cajob').prop("checked") == false){
			error = 1;
			$('#tranblock').addClass('errorcolor');
		}
	}else{
		var day = $('#day').val();
		if(day==''){
			error=1;
			$('#day').addClass('errorcolor');
		}
	}
	if(porder==1){
		error = 1;
		$('#porder').addClass('errorcolor');
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
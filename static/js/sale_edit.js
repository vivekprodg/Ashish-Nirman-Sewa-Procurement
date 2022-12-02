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
var dinvtype = $('#dinvtype').val();
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


$('#item').on('change', function(){
	$('#rate').removeClass('errorcolor');
	var idstr = $('#item option:selected').val();
	var name = $('#ini'+idstr).val();
	var uom = $('#ini'+idstr).attr("data");
	var rate = $('#ini'+idstr).attr("name");
	$('#itemname').val(name);
	$('#uom').val(uom);
	$('#rate').val(rate);
	var qty = $('#qty').val();
	if(qty != '' && qty > 0){
		qty = parseFloat(qty);
		var rate = $('#rate').val();
		rate = parseFloat(rate);
		var amt = qty * rate;
		amt = parseFloat(amt);
		amt = amt.toFixed(2);
		$('#amount').val(amt);
	}
});
$('#edititem').on('change', function(){
	$('#editrate').removeClass('errorcolor');
	var idstr = $('#edititem option:selected').val();
	var name = $('#eini'+idstr).val();
	var uom = $('#eini'+idstr).attr("data");
	var rate = $('#eini'+idstr).attr("name");
	$('#edititemname').val(name);
	$('#edituom').val(uom);
	$('#editrate').val(rate);
	var qty = $('#editqty').val();
	if(qty != '' && qty > 0){
		qty = parseFloat(qty);
		var rate = $('#editrate').val();
		rate = parseFloat(rate);
		var amt = qty * rate;
		amt = parseFloat(amt);
		amt = amt.toFixed(2);
		$('#editamount').val(amt);
	}
});

$('#qty').on('keyup', function(){
	$(this).removeClass('errorcolor');
	var qty = $(this).val();
	if(qty != '' && qty > 0){
		qty = parseFloat(qty);
		var rate = $('#rate').val();
		if(rate != '' && rate > 0){
			rate = parseFloat(rate);
			var amt = qty * rate;
			amt =parseFloat(amt);
			amt = amt.toFixed(2);
			$('#amount').val(amt);
		}else{
			$('#rate').addClass('errorcolor');
		}
	}else{
		$('#qty').addClass('errorcolor');
	}
});
$('#editqty').on('keyup', function(){
	$(this).removeClass('errorcolor');
	var qty = $(this).val();
	if(qty != '' && qty > 0){
		qty = parseFloat(qty);
		var rate = $('#editrate').val();
		if(rate != '' && rate > 0){
			rate = parseFloat(rate);
			var amt = qty * rate;
			amt =parseFloat(amt);
			amt = amt.toFixed(2);
			$('#editamount').val(amt);
		}else{
			$('#editrate').addClass('errorcolor');
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
		$('.tfoot2').hide();
		$("#ItemTable tbody").append('<tr id="itemrow'+add+'"><td><button type="button" class="edititem" id="eitem'+add+'" data="'+add+'"><i class="far fa-edit"></i></button><button type="button" class="delitem" id="ditem'+add+'" data="'+add+'"><i class="far fa-trash-alt"></i></button></td><td>'+itemname+'</td><td>'+uom+'</td><td>'+qty+'</td><td>'+rate+'</td><td class="ltd">'+amt+'</td></tr>');
		$('.tfoot').show();

		var sumamount = 0;
		sumamount = parseFloat(sumamount);
		$.each(amount,function(){sumamount+=parseFloat(this) || 0;});
		var sumamoun = sumamount.toFixed(2);
		$('#subtotal').val(sumamoun);

		var disp = $('#discount1').val();
		if(disp!='' && disp > 0){
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
		}else{
			diserror = 1;
			$('#discount2').addClass('errorcolor');
			$('#discount1').addClass('errorcolor');
		}

		$('#item').val('');
		$('#itemname').val('');
		$('#uom').val('');
		$('#qty').val('');
		$('#rate').val('');
		$('#amount').val('');
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
	$('#irate'+did).val(rate);
	$('#iamt'+did).val(amt);
	$('#edititemname').val('');
	$('#edititem').val('');
	$('#editqty').val('');
	$('#edituom').val('');
	$('#editrate').val('');
	$('#editamount').val('');
	$('#itemrow'+did).remove();
	$("#ItemTable tbody").append('<tr id="itemrow'+did+'"><td><button type="button" class="edititem" id="eitem'+did+'" data="'+did+'"><i class="far fa-edit"></i></button><button type="button" class="delitem" id="ditem'+did+'" data="'+did+'"><i class="far fa-trash-alt"></i></button></td><td>'+itemname+'</td><td>'+uom+'</td><td>'+qty+'</td><td>'+rate+'</td><td>'+amt+'</td></tr>');

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
	if(disp!='' && disp > 0){
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
	}else{
		diserror = 1;
		$('#discount2').addClass('errorcolor');
		$('#discount1').addClass('errorcolor');
	}

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

$('#invoice_type').on('change', function(){
	diserror = 0;
	var intype = $('#invoice_type option:selected').val();
	var dis = $('#discount2').val();
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
	$('.edit_popupbanner1').fadeIn();
	$('#edit_popup1').css({"transform": "scale(1)", "-webkit-transform": "scale(1)", "-moz-transform": "scale(1)"});	$('#itemname').focus();
	$('#edititem').focus();
	var itemid = $('#inameid'+idstr).val();
	var name = $('#iname'+idstr).val();
	var uom = $('#iuom'+idstr).val();
	var qty = $('#iqty'+idstr).val();
	var rate = $('#irate'+idstr).val();
	var amt = $('#iamt'+idstr).val();
	$('#edititem').val(itemid);
	$('#edititemname').val(name);
	$('#edituom').val(uom);
	$('#editqty').val(qty);
	$('#editrate').val(rate);
	$('#editamount').val(amt);
	$('#dfaultid').val(idstr);
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
		if(disp!='' && disp > 0){
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
		}else{
			diserror = 1;
			$('#discount2').addClass('errorcolor');
			$('#discount1').addClass('errorcolor');
		}
	}
	
});

$('#SalesForm').on('submit', function(){
	var error = 0;
	$('#spinner1').show();
	var date = $('input[name=date]').val();
	var saleid = $('input[name=saleid]').val();
	var issue_locate = $('input[name=issue_locate]').val();
	var buyer = $('input[name=buyer]').val();
	var invoice_type = $('#invoice_type option:selected').val();
	var discount = $('input[name=discount2]').val();
	var amount = $('input[name=total]').val();
	if(date==''){
		error = 1;
		$('#date').addClass('errorcolor');
	}
	if(saleid==''){
		error = 1;
		$('#saleid').addClass('errorcolor');
	}
	if(issue_locate==''){
		error = 1;
		$('#issue_locate').addClass('errorcolor');
	}
	if(buyer==''){
		error = 1;
		$('#buyer').addClass('errorcolor');
	}
	if(invoice_type==''){
		error = 1;
		$('#invoice_type').addClass('errorcolor');
	}
	if(amount=='' || amount < 0 || amount == 0){
		error = 1;
	}
	if(diserror==1){
		error = 1;
		$('#discount1').addClass('errorcolor');
		$('#discount2').addClass('errorcolor');
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
		document.SalesForm.submit();
	}else{
		$('#spinner1').hide();
	}
	event.preventDefault();
});
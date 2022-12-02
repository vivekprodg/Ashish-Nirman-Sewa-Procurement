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

function url(vehi_num){
  var mat_url = vehi_num.toLowerCase();
  var result = mat_url.replace(/[^a-z0-9\s]/gi, '').replace(/[_\s]/g, '');
  return result;
}

var itemadd = [];
var amount = [];
var peiamount = [];
var totaldper = [];
var totaldamt = [];
var totalvat = [];
var ponum = [];
var add = 0;
var itemer = 0;
var itemeredit = 0;
var diserror = 0;
var pbill = 0;
var porder = 0;
var rec = 0;
var gitemadd = [];
var gadd = 0;
var grec = 0;

//default values=================================

function subproblemval(val){
  var mat_url = val.toLowerCase();
  var result = mat_url.replace(/[^a-z0-9\s]/gi, '').replace(/[_\s]/g, '');
  $('.psubcat').hide();
  if($('#pdisplay'+result).length>0){
  	$('#pdisplay'+result).show();
  }
}

function subproblemassign(val,sub){
  var mat_url = val.toLowerCase();
  var result = mat_url.replace(/[^a-z0-9\s]/gi, '').replace(/[_\s]/g, '');
  $('#subproblem'+result).val(sub);
  $('#subprobval').val(sub);
}

var jnum = $('#jnum').val();
var vtype = $('#dvtype').val();
var vtypeid = $('#dvtypeid').val();
var dnumtype = $('#dnumtype').val();
var vnum = $('#vnum').val();
var dnum = $('#dnum').val();
var kilnum = $('#kilnum').val();
var probnum = $('#probnum').val();
var pcnum = $('#pcnum').val();
var descnum = $('#descnum').val();
var djorder = $('#djorder').val();
var dgjorder = $('#dgjorder').val();

if(djorder=='yes'){
	$('#yesjob').prop("checked", true);
	$('#jorder').val('yes');
	$('#jobnumber').show();
	$('#njobcheck').hide();

	ponum.push(jnum);
	jnumu = jnum.toUpperCase();
	jnuml = jnum.toLowerCase();
	if($('#pvnselban'+jnumu).length>0){
		$('#pvnselban'+jnumu).show();
	}
	if($('#pvnselban'+jnuml).length>0){
		$('#pvnselban'+jnuml).show();
	}
}
if(djorder=='no'){
	$('#nojob').prop("checked", true);
	$('#jorder').val('no');
	$('#jobnumber').hide();
}
if(dgjorder=='yes'){
	$('#gyesjob').prop("checked", true);
	$('#gjorder').val('yes');
	$('#gjdis').show();
	$('#gnjobcheck').hide();
}
if(dgjorder=='no'){
	$('#gnojob').prop("checked", true);
	$('#gjorder').val('no');
	$('#gjdis').val();
}
if(djorder == 'no' && dgjorder == 'yes'){
	$('#vehicle_type').prop("disabled", false);
	$('#chasis_check').prop("disabled", false);
	$('#engine_check').prop("disabled", false);
}
$('.tfoot').show();
$('.tfoot2').hide();
$('#vehicle_type').val(vtypeid);
if(probnum!='' && probnum!='none'){
	$('#problem').val(probnum);
	subproblemval(probnum);
	if(pcnum!='none'){
		subproblemassign(probnum,pcnum);
	}
}
$('.vehidet').show();
if(dnumtype=='chasis'){
	var vehi_num = url(vnum);
	$('#vehitypechasisid'+vtypeid).show();
	$('#vehi_chasis'+vtypeid).val(vnum);
	$('#chasis_check').prop("checked", true);
	var vh = $('#vhc'+vehi_num).attr("name");
	var vhc = $('#vhc'+vehi_num).val();
	var vhe = $('#vhc'+vehi_num).attr("data");
	$('#vehidetnum').text(vh);
	$('#vehidetchasis').text(vhc);
	$('#vehidetengine').text(vhe);
	if(djorder == 'no' && dgjorder == 'yes'){
		$('#vehi_chasis'+vtypeid).prop("disabled", false);
	}
}
if(dnumtype=='engine'){
	var vehi_num = url(vnum);
	$('#vehitypeengineid'+vtypeid).show();
	$('#vehi_engine'+vtypeid).val(vnum);
	$('#engine_check').prop("checked", true);
	var vh = $('#vhe'+vehi_num).attr("data");
	var vhc = $('#vhe'+vehi_num).attr("name");
	var vhe = $('#vhe'+vehi_num).val();
	$('#vehidetnum').text(vh);
	$('#vehidetchasis').text(vhc);
	$('#vehidetengine').text(vhe);
	if(djorder == 'no' && dgjorder == 'yes'){
		$('#vehi_engine'+vtypeid).prop("disabled", false);
	}
}
if(dnumtype=='vehicle'){
	var vehi_num = url(vnum);
	$('#vehitypenumid'+vtypeid).show();
	$('#vehi_number'+vtypeid).val(vnum);
	$('#chasis_check').prop("checked", false);
	$('#engine_check').prop("checked", false);
	var vh = $('#vh'+vehi_num).val();
	var vhc = $('#vh'+vehi_num).attr("name");
	var vhe = $('#vh'+vehi_num).attr("data");
	$('#vehidetnum').text(vh);
	$('#vehidetchasis').text(vhc);
	$('#vehidetengine').text(vhe);
	if(djorder == 'no' && dgjorder == 'yes'){
		$('#vehi_number'+vtypeid).prop("disabled", false);
	}
}

$('.bill_count').each(function(){
	var cha = $(this).val();
	add = add+1;
	itemadd.push(add);
});
$('.irecon').each(function(){
	var cha = $(this).val();
	rec = rec+1;
});
$('.bill_amount').each(function(){
	var cha = $(this).val();
	amount.push(cha);
});
$('.pvnamt').each(function(){
	var cha = $(this).val();
	peiamount.push(cha);
});

if($('.pvntab').length>0){
	$('.pvnshowtable').show();
	$('.pvndet').hide();
	$('.pvntab').each(function(){
		var cha = $(this).val();
		cha = cha.toUpperCase();
		$('#pvndet'+cha).show();
	});
}

$('.gbill_count').each(function(){
	var cha = $(this).val();
	gadd = gadd+1;
	gitemadd.push(gadd);
});
$('.girecon').each(function(){
	var cha = $(this).val();
	grec = grec+1;
});

//============================================

$('#yjobcheck').click(function(){
	$('#yesjob').prop('checked', true);
	$('#nojob').prop('checked', false);
	$('#jorder').val('yes');
	$('#jobnumber').show();
	$('#jobnumber').val('');
	vehi_con();
});

$('#njobcheck').click(function(){
	$('#yesjob').prop('checked', false);
	$('#nojob').prop('checked', true);
	$('#jorder').val('no');
	$('#jobnumber').val('');
	$('#jobnumber').hide();
	$('.pvnselban').hide();
	vehi_con();
	if($('#gyesjob').prop("checked") == true){
		$('#vehicle_type').prop("disabled", false);
		$('#chasis_check').prop("disabled", false);
		$('#engine_check').prop("disabled", false);
	}
});

$('#gyjobcheck').click(function(){
	$('#gyesjob').prop('checked', true);
	$('#gnojob').prop('checked', false);
	$('#gjorder').val('yes');
	$('#gjdis').show();
	$('#gjobnumber').val('');
	if($('#nojob').prop("checked") == true){
		$('#vehicle_type').prop("disabled", false);
		$('#chasis_check').prop("disabled", false);
		$('#engine_check').prop("disabled", false);
	}
});

$('#gnjobcheck').click(function(){
	$('#gyesjob').prop('checked', false);
	$('#gnojob').prop('checked', true);
	$('#gjorder').val('no');
	$('#gjobnumber').val('');
	$('#gjdis').hide();
	vehi_con();
});

function vehi_con(){
	$('#vehidetnum').text('');
	$('#vehidetchasis').text('');
	$('#vehidetengine').text('');
	$('.vehidet').hide();
	$('#vehicle_type').val('');
	$('.vchoice').val('');
	$('#chasis_check').prop("checked", false);
	$('#engine_check').prop("checked", false);
	$('#vehicle_type').prop("disabled", true);
	$('#chasis_check').prop("disabled", true);
	$('#engine_check').prop("disabled", true);
	$('.vchoice').prop("disabled", true);
	$('#vehicle_confirm').val('');
	$('#num_type').val('');
}

$('#vehicle_type').on('change', function(){
	var idstr = $('#vehicle_type option:selected').val();
	var val = $('#vtypename'+idstr).val();
	$('.vehicles').hide();
	if($('#chasis_check').prop("checked") == true){
		$('#vehitypechasisid'+idstr).show();
		$('#vehi_engine'+idstr).prop("disabled", false);
	}else if($('#engine_check').prop("checked") == true){
		$('#vehitypeengineid'+idstr).show();
		$('#vehi_chasis'+idstr).prop("disabled", false);
	}else{
		$('#vehitypenumid'+idstr).show();
		$('#vehi_number'+idstr).prop("disabled", false);
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
			$('#vehi_chasis'+idstr).prop("disabled", false);
		}
	}else{
		if(idstr!=''){
			var val = $('#vtypename'+idstr).val();
			$('#vehitypenumid'+idstr).show();
			$('#vehi_number'+idstr).prop("disabled", false);
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
			$('#vehi_engine'+idstr).prop("disabled", false);
		}
	}else{
		if(idstr!=''){
			var val = $('#vtypename'+idstr).val();
			$('#vehitypenumid'+idstr).show();
			$('#vehi_number'+idstr).prop("disabled", false);
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
$('#jobnumber').on('keyup', function(){
	var val = $(this).val();
	val = val.toUpperCase();
	porder = 0;
	$('.suptabs').hide();
	$('.pvnselban').hide();
	$(this).removeClass('errorcolor');
	$('.porder_e').hide();
	$('.vehicles').hide();
	$('.vehidet').hide();
	$('.goods').removeClass('errorcolor');
	if($('#yesjob').prop("checked")==true){
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
					var po_vehi = $('#po'+val).attr("data");
					if(po_vehi=='yes'){
						var vehit_id = $('#povehi'+val).attr("data-ab");
						var vehi_type = $('#povehi'+val).attr("data");
						var num_type = $('#povehi'+val).attr("name");
						var vehi_num = $('#povehi'+val).val();
						$('#vehicle_type').val(vehit_id);
						$('#vtypeidd').val(vehit_id);
						$('#vtype').val(vehi_type);
						$('#num_type').val(num_type);
						$('#vehicle_confirm').val(vehi_num);
						$('.vehidet').show();
						if(num_type=='chasis'){
							var vnum = url(vehi_num);
							$('#vehitypechasisid'+vehit_id).show();
							$('#vehi_chasis'+vehit_id).val(vehi_num);
							$('#chasis_check').prop("checked", true);
							$('#engine_check').prop("checked", false);
							var vh = $('#vhc'+vnum).attr("name");
							var vhc = $('#vhc'+vnum).val();
							var vhe = $('#vhc'+vnum).attr("data");
							$('#vehidetnum').text(vh);
							$('#vehidetchasis').text(vhc);
							$('#vehidetengine').text(vhe);
						}
						if(num_type=='engine'){
							var vnum = url(vehi_num);
							$('#vehitypeengineid'+vehit_id).show();
							$('#vehi_engine'+vehit_id).val(vehi_num);
							$('#engine_check').prop("checked", true);
							$('#chasis_check').prop("checked", false);
							var vh = $('#vhe'+vnum).attr("data");
							var vhc = $('#vhe'+vnum).attr("name");
							var vhe = $('#vhe'+vnum).val();
							$('#vehidetnum').text(vh);
							$('#vehidetchasis').text(vhc);
							$('#vehidetengine').text(vhe);
						}
						if(num_type=='vehicle'){
							var vnum = url(vehi_num);
							$('#vehitypenumid'+vehit_id).show();
							$('#vehi_number'+vehit_id).val(vehi_num);
							$('#chasis_check').prop("checked", false);
							$('#engine_check').prop("checked", false);
							var vh = $('#vh'+vnum).val();
							var vhc = $('#vh'+vnum).attr("name");
							var vhe = $('#vh'+vnum).attr("data");
							$('#vehidetnum').text(vh);
							$('#vehidetchasis').text(vhc);
							$('#vehidetengine').text(vhe);
						}
					}
				}
			}else{
				$('#pvnselban'+val).show();
				var po_vehi = $('#po'+val).attr("data");
				if(po_vehi=='yes'){
					var vehit_id = $('#povehi'+val).attr("data-ab");
					var vehi_type = $('#povehi'+val).attr("data");
					var num_type = $('#povehi'+val).attr("name");
					var vehi_num = $('#povehi'+val).val();
					$('#vehicle_type').val(vehit_id);
					$('#vtypeidd').val(vehit_id);
					$('#vtype').val(vehi_type);
					$('#num_type').val(num_type);
					$('#vehicle_confirm').val(vehi_num);
					$('.vehidet').show();
					if(num_type=='chasis'){
						var vnum = url(vehi_num);
						$('#vehitypechasisid'+vehit_id).show();
						$('#vehi_chasis'+vehit_id).val(vehi_num);
						$('#chasis_check').prop("checked", true);
						$('#engine_check').prop("checked", false);
						var vh = $('#vhc'+vnum).attr("name");
						var vhc = $('#vhc'+vnum).val();
						var vhe = $('#vhc'+vnum).attr("data");
						$('#vehidetnum').text(vh);
						$('#vehidetchasis').text(vhc);
						$('#vehidetengine').text(vhe);
					}
					if(num_type=='engine'){
						var vnum = url(vehi_num);
						$('#vehitypeengineid'+vehit_id).show();
						$('#vehi_engine'+vehit_id).val(vehi_num);
						$('#engine_check').prop("checked", true);
						$('#chasis_check').prop("checked", false);
						var vh = $('#vhe'+vnum).attr("data");
						var vhc = $('#vhe'+vnum).attr("name");
						var vhe = $('#vhe'+vnum).val();
						$('#vehidetnum').text(vh);
						$('#vehidetchasis').text(vhc);
						$('#vehidetengine').text(vhe);
					}
					if(num_type=='vehicle'){
						var vnum = url(vehi_num);
						$('#vehitypenumid'+vehit_id).show();
						$('#vehi_number'+vehit_id).val(vehi_num);
						$('#chasis_check').prop("checked", false);
						$('#engine_check').prop("checked", false);
						var vh = $('#vh'+vnum).val();
						var vhc = $('#vh'+vnum).attr("name");
						var vhe = $('#vh'+vnum).attr("data");
						$('#vehidetnum').text(vh);
						$('#vehidetchasis').text(vhc);
						$('#vehidetengine').text(vhe);
					}
				}
			}
		}
	}
});


$('#jobnumber').click(function(){
	$('.porder_e').hide();
});

$('#problem').on('change', function(){
	var val = $('#problem option:selected').val();
	subproblem(val);
});

function subproblem(val){
  var mat_url = val.toLowerCase();
  var result = mat_url.replace(/[^a-z0-9\s]/gi, '').replace(/[_\s]/g, '');
  $('.psubcat').hide();
  if($('#pdisplay'+result).length > 0){
  	$('#pdisplay'+result).show();
  	$('#subprobval').val('');
  }else{
  	$('#subprobval').val('none');
  }
}

$('.problemsel').on('change', function(){
	var idstr = $(this).attr("id");
	if($('#'+idstr).length > 0){
		var val = $('#'+idstr).val();
		$('#subprobval').val(val);
	}else{
		$('#subprobval').val('none');
	}
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

$('#itemqty').on('keyup', function(){
	var val = $(this).val();
	itemer = 0;
	if(val != ''){
		val =parseFloat(val);
		val = val.toFixed(2);
		if(val>0){
			var rt = $('#itemrate').val();
			if(rt!=''){
				if(rt>0){
					rt = parseFloat(rt);
					rt = rt.toFixed(2);
					var amt = val * rt;
					amt = parseFloat(amt);
					amt = amt.toFixed(2);
					$('#itemamount').val(amt);
					var dis_per = $('#discount_per').val();
					if(dis_per != '' && dis_per > 0){
						var dis = amt * dis_per/100;
						dis = parseFloat(dis);
						if(dis < amt){
							var total = amt - dis;
							total = parseFloat(total);
							total = total.toFixed(2);
							$('#itemamount').val(total);
							$('#discount_amt').removeClass('errorcolor');
							$('#discount_per').removeClass('errorcolor');
						}else{
							itemer = 1;
							$(this).addClass('errorcolor');
							$('#discount_amt').addClass('errorcolor');
							$('#discount_per').addClass('errorcolor');
						}
						$('#discount_amt').val(dis);
					} 
				}else{
					itemer = 1;
				}
			}else{
				itemer = 1;
			}
		}else{
			itemer = 1;
			$('#itemamount').val(0);
			$('#discount_per').val(0);
			$('#discount_amt').val(0);
		}
	}else{
		itemer = 1;
	}
});
$('#itemrate').on('keyup', function(){
	var val = $(this).val();
	itemer = 0;
	if(val != ''){
		val =parseFloat(val);
		val = val.toFixed(2);
		if(val>0){
			var rt = $('#itemqty').val();
			if(rt!=''){
				if(rt>0){
					rt = parseFloat(rt);
					rt = rt.toFixed(2);
					var amt = val * rt;
					amt = parseFloat(amt);
					amt = amt.toFixed(2);
					$('#itemamount').val(amt);
					var dis_per = $('#discount_per').val();
					if(dis_per != '' && dis_per > 0){
						var dis = amt * dis_per/100;
						dis = parseFloat(dis);
						if(dis < amt){
							var total = amt - dis;
							total = parseFloat(total);
							total = total.toFixed(2);
							$('#itemamount').val(total);
							$('#discount_amt').removeClass('errorcolor');
							$('#discount_per').removeClass('errorcolor');
						}else{
							itemer = 1;
							$(this).addClass('errorcolor');
							$('#discount_amt').addClass('errorcolor');
							$('#discount_per').addClass('errorcolor');
						}
						$('#discount_amt').val(dis);
					}
				}else{
					itemer = 1;
				}
			}else{
				itemer = 1;
			}
		}else{
			itemer = 1;
			$('#itemamount').val(0);
			$('#discount_per').val(0);
			$('#discount_amt').val(0);
		}
	}else{
		itemer = 1;
	}
});

$('#itemqtyedit').on('keyup', function(){
	var val = $(this).val();
	itemeredit = 0;
	if(val != ''){
		val =parseFloat(val);
		val = val.toFixed(2);
		if(val>0){
			var rt = $('#itemrateedit').val();
			if(rt!=''){
				if(rt>0){
					rt = parseFloat(rt);
					rt = rt.toFixed(2);
					var amt = val * rt;
					amt = parseFloat(amt);
					amt = amt.toFixed(2);
					$('#itemamountedit').val(amt);
					var dis_per = $('#editdiscount_per').val();
					if(dis_per != '' && dis_per > 0){
						var dis = amt * dis_per/100;
						dis = parseFloat(dis);
						if(dis < amt){
							var total = amt - dis;
							total = parseFloat(total);
							total = total.toFixed(2);
							$('#itemamountedit').val(total);
							$('#editdiscount_amt').removeClass('errorcolor');
							$('#editdiscount_per').removeClass('errorcolor');
						}else{
							itemer = 1;
							$(this).addClass('errorcolor');
							$('#editdiscount_amt').addClass('errorcolor');
							$('#editdiscount_per').addClass('errorcolor');
						}
						$('#editdiscount_amt').val(dis);
					}
				}else{
					itemeredit = 1;
				}
			}else{
				itemeredit = 1;
			}
		}else{
			itemeredit = 1;
		}
	}else{
		itemeredit = 1;
	}
});
$('#itemrateedit').on('keyup', function(){
	var val = $(this).val();
	itemeredit = 0;
	if(val != ''){
		val =parseFloat(val);
		val = val.toFixed(2);
		if(val>0){
			var rt = $('#itemqtyedit').val();
			if(rt!=''){
				if(rt>0){
					rt = parseFloat(rt);
					rt = rt.toFixed(2);
					var amt = val * rt;
					amt = parseFloat(amt);
					amt = amt.toFixed(2);
					$('#itemamountedit').val(amt);
					var dis_per = $('#editdiscount_per').val();
					if(dis_per != '' && dis_per > 0){
						var dis = amt * dis_per/100;
						dis = parseFloat(dis);
						if(dis < amt){
							var total = amt - dis;
							total = parseFloat(total);
							total = total.toFixed(2);
							$('#itemamountedit').val(total);
							$('#editdiscount_amt').removeClass('errorcolor');
							$('#editdiscount_per').removeClass('errorcolor');
						}else{
							itemer = 1;
							$(this).addClass('errorcolor');
							$('#editdiscount_amt').addClass('errorcolor');
							$('#editdiscount_per').addClass('errorcolor');
						}
						$('#editdiscount_amt').val(dis);
					}
				}else{
					itemeredit = 1;
				}
			}else{
				itemeredit = 1;
			}
		}else{
			itemeredit = 1;
		}
	}else{
		itemeredit = 1;
	}
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

$('.item').on('change', function(){
	var vdstr = $(this).attr("id");
	var idstr = $('#'+vdstr+' option:selected').val();
	var name = $('#ini'+idstr).val();
	var uom = $('#ini'+idstr).attr("data");
	var alias = $('#ini'+idstr).attr("name");
	$('#itemm').val(idstr);
	$('#itemname').val(name);
	$('#itemuom').val(uom);
	$('#itemalias').val(alias);
});
$('.edititemm').on('change', function(){
	var vdstr = $(this).attr("id");
	var idstr = $('#'+vdstr+' option:selected').val();
	var name = $('#eini'+idstr).val();
	var uom = $('#eini'+idstr).attr("data");
	var alias = $('#eini'+idstr).attr("name");
	$('#edititem').val(idstr);
	$('#itemnameedit').val(name);
	$('#itemuomedit').val(uom);
	$('#edititemalias').val(alias);
});

$(document).on('click', '.edititem', function(){
	var idstr = $(this).attr("data");
	$('.edit_popupbanner1').fadeIn();
	$('#edit_popup1').css({"transform": "scale(1)", "-webkit-transform": "scale(1)", "-moz-transform": "scale(1)"});	$('#itemname').focus();
	$('#edititem').focus();
	// if($('#yesjob').prop("checked")==true){
	// 	$('.epitm'+val).each(function(){
	// 		var itm_id = $(this).val();
	// 		var itm = $(this).attr("data");
	// 		if($("#edititem option[value='"+itm_id+"']").length===0){
	// 			$('#edititem').append($('<option>', {
	// 			    value: itm_id,
	// 			    text: itm
	// 			}));
	// 		}
			
	// 	});
	// }else if($('#nojob').prop("checked")==true){
	// 	$('.edit_popupbanner').fadeIn();
	// 	$('#edit_popup').css({"transform": "scale(1)", "-webkit-transform": "scale(1)", "-moz-transform": "scale(1)"});	$('#itemname').focus();
	// 	$('#item').focus();
	// 	$('.eitemclass').each(function(){
	// 		var itm_id = $(this).val();
	// 		var itm = $(this).attr("data");
	// 		if($("#edititem option[value='"+itm_id+"']").length===0){
	// 			$('#edititem').append($('<option>', {
	// 			    value: itm_id,
	// 			    text: itm
	// 			}));
	// 		}
			
	// 	});
	// }else{
	// 	$('#checkblock').addClass('errorcolor');
	// }
	var itemid = $('#iid'+idstr).val();
	var name = $('#iname'+idstr).val();
	var uom = $('#iuom'+idstr).val();
	var qty = $('#iqty'+idstr).val();
	var rate = $('#irate'+idstr).val();
	var amt = $('#iamt'+idstr).val();
	var disper = $('#idisper'+idstr).val();
	var disamt = $('#idisamt'+idstr).val();
	var alias = $('#ialias'+idstr).val();
	$('#itemnameedit').val(name);
	$('#edititem').val(itemid);
	$('#itemuomedit').val(uom);
	$('#itemqtyedit').val(qty);
	$('#itemrateedit').val(rate);
	$('#itemamountedit').val(amt);
	$('#editdiscount_per').val(disper);
	$('#editdiscount_amt').val(disamt);
	$('#edititemalias').val(alias);
	$('#dfaultamount').val(amt);
	$('#dfaultid').val(idstr);
});

$('.pvnsel').on('change', function(){
	var idstr = $(this).attr("id");
	var val = $('#'+idstr+' option:selected').val();
	$('.loading').slideDown();
	$('.goods').removeClass('errorcolor');
	val = val.toUpperCase();
	var po = $('#jobnumber').val();
	if($('.grd'+val).length == 0){
		if($('.gooid'+val).length > 0){
			if(ponum.length===0){
				ponum.push(po);
			}
			if($.inArray(po, ponum)!=-1){
				rec = rec + 1;
				var rus = val + rec;

				var tamt = $('#puriamt'+val).val();
				$(".hidden_inputs").append('<input type="hidden" name="pvnval" class="pvnval" id="pval'+val+'" value="'+val+'">');
				$(".hidden_inputs").append('<input type="hidden" class="tamt" id="tamt'+val+'" value="'+tamt+'">');

				$('.pvnshowtable').show();
				$('.pvndet').hide();
				if($('.pvnval').length>0){
					$('.pvnval').each(function(){
						var cha = $(this).val();
						$('#pvndet'+cha).show();
					});
				}else{
					$('#pvndet'+val).show();
				}
				// var tdisper = $('#puridper'+val).val();
				// var tdisamt = $('#puridamt'+val).val();
				// var tvat = $('#purivat'+val).val();
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
					var rate = $('#rate'+cha).val();
					var disamt = $('#disamt'+cha).val();
					var disper = $('#disper'+cha).val();
					var amt = $('#amt'+cha).val();

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
					$(".hidden_inputs").append('<input type="hidden" name="irate'+add+'" id="irate'+us+'" value="'+rate+'">');
					$(".hidden_inputs").append('<input type="hidden" name="iamt'+add+'" id="iamt'+us+'" value="'+amt+'">');
					$(".hidden_inputs").append('<input type="hidden" name="idisper'+add+'" id="idisper'+us+'" value="'+disper+'">');
					$(".hidden_inputs").append('<input type="hidden" name="idisamt'+add+'" id="idisamt'+us+'" value="'+disamt+'">');
					$('.tfoot2').hide();
					$("#MaintainanceTable tbody").append('<tr id="itemrow'+us+'"><td></td><td>'+item+'('+alias+')</td><td>'+uom+'</td><td>'+qty+'</td><td>'+rate+'</td><td>'+disamt+' ('+disper+'%)</td><td class="ltd">'+amt+'</td></tr>');
					$('.tfoot').show();
				});
				$(".grncol").append('<div class="coldiv grd'+val+'" id="colrec'+rus+'"><span class="coldes">'+val+'</span><button type="button" class="colbtn" name="'+val+'" data="'+rus+'"><i class="fa fa-times"></i></button></div>');
				$('#njobcheck').hide();
				// amount.push(tamt);
				peiamount.push(tamt);
				// totaldper.push(tdisper);
				// totaldamt.push(tdisamt);
				// totalvat.push(tvat);

				var sumpeiamount = 0;
				sumpeiamount = parseFloat(sumpeiamount);
				$.each(peiamount,function(){sumpeiamount+=parseFloat(this) || 0;});
				var sumpeiamoun = sumpeiamount.toFixed(2);

				if(amount.length>0){
					var sumamount = 0;
					sumamount = parseFloat(sumamount);
					$.each(amount,function(){sumamount+=parseFloat(this) || 0;});
					sumpeiamoun = sumpeiamount + sumamount;
					sumpeiamoun = parseFloat(sumpeiamoun);
					sumpeiamoun = sumpeiamoun.toFixed(2);
				}

				// var sumdper = 0;
				// sumdper = parseFloat(sumdper);
				// $.each(totaldper,function(){sumdper+=parseFloat(this) || 0;});
				// var sumdpe = sumdper.toFixed(2);

				// var sumdamt = 0;
				// sumdamt = parseFloat(sumdamt);
				// $.each(totaldamt,function(){sumdamt+=parseFloat(this) || 0;});
				// var sumdam = sumdamt.toFixed(2);

				// var sumvat = 0;
				// sumvat = parseFloat(sumvat);
				// $.each(totalvat,function(){sumvat+=parseFloat(this) || 0;});
				// var sumva = sumvat.toFixed(2);

				$('#subtotal').val(sumpeiamoun);
				// $('#discount2').val(sumdam);
				// $('#discount1').val(sumdpe);
				// $('#vat').val(sumva);
				var labour = $('#labour').val();
				if(labour != ''){
					if(labour>0 || labour==0){
						labour = parseFloat(labour);
						var grand = labour + parseFloat(sumpeiamoun);
						grand = parseFloat(grand);
						grand= grand.toFixed(2);
						$('#total').val(grand);
						$('#labour').removeClass('errorcolor');
					}else{
						$('#labour').addClass('errorcolor');
					}
				}else{
					$('#labour').addClass('errorcolor');
				}
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
		$('#irate'+cha).remove();
		$('#iamt'+cha).remove();
		$('#idisamt'+cha).remove();
		$('#idisper'+cha).remove();

		itemadd = $.grep(itemadd, function(value) {
			return value != hac;
		});
		$('#itemrow'+cha).remove();
		$('#colrec'+idstr).remove();
	});
	$('#pvndet'+pval).hide();
	$('.pvnval').each(function(){
		var val = $(this).val();
		if(val==pval){
			$('#tamt'+val).remove();
			// $('#tdisper'+val).remove();
			// $('#tdisamt'+val).remove();
			// $('#tvat'+val).remove();
			$('#pval'+val).remove();
		}
	});
	if($('.pvnval').length==0){
		$('.pvndet').hide();
		$('.pvnshowtable').hide();
		$('#njobcheck').show();
	}
	if(itemadd.length === 0){
		$('#subtotal').val(0);
		$('#labour').val(0);
	    $('#total').val(0);
		ponum = [];
		peiamount = [];
		$('.pvndet').hide();
		$('.pvnshowtable').hide();
		if(gitemadd.length === 0){
			// totaldper = [];
			// totaldamt = [];
			// totalvat = [];
			$('.tfoot').hide();
			$('.tfoot2').show();
		}
	}else{
		peiamount = [];
		// totaldper = [];
		// totaldamt = [];
		// totalvat = [];
		$('.pvnval').each(function(){
			var val = $(this).val();
			var tamt = $('#tamt'+val).val();
			// var tdisper =  $('#tdisper'+val).val();
			// var tdisamt = $('#tdisamt'+val).val();
			// var tvat = $('#tvat'+val).val();
			peiamount.push(tamt);
			// totaldper.push(tdisper);
			// totaldamt.push(tdisamt);
			// totalvat.push(tvat);
		});
		var sumpeiamoun = 0;
		var sumpeiamount = 0;
		var sumamount = 0;
		if(peiamount.length>0){
			sumpeiamount = 0;
			sumpeiamount = parseFloat(sumpeiamount);
			$.each(peiamount,function(){sumpeiamount+=parseFloat(this) || 0;});
			sumpeiamoun = sumpeiamount.toFixed(2);
		}

		if(amount.length>0){
			sumamount = 0;
			sumamount = parseFloat(sumamount);
			$.each(amount,function(){sumamount+=parseFloat(this) || 0;});
			sumpeiamoun = sumamount.toFixed(2);
		}
		if(amount.length>0 && peiamount.length>0){
			sumpeiamoun = sumpeiamount + sumamount;
			sumpeiamoun = parseFloat(sumpeiamoun);
			sumpeiamoun = sumpeiamoun.toFixed(2);
		}

		// var sumdper = 0;
		// sumdper = parseFloat(sumdper);
		// $.each(totaldper,function(){sumdper+=parseFloat(this) || 0;});
		// var sumdpe = sumdper.toFixed(2);

		// var sumdamt = 0;
		// sumdamt = parseFloat(sumdamt);
		// $.each(totaldamt,function(){sumdamt+=parseFloat(this) || 0;});
		// var sumdam = sumdamt.toFixed(2);

		// var sumvat = 0;
		// sumvat = parseFloat(sumvat);
		// $.each(totalvat,function(){sumvat+=parseFloat(this) || 0;});
		// var sumva = sumvat.toFixed(2);

		$('#subtotal').val(sumpeiamoun);
		// $('#discount2').val(sumdam);
		// $('#discount1').val(sumdpe);
		// $('#vat').val(sumva);

		var labour = $('#labour').val();
		if(labour != ''){
			if(labour>0 || labour==0){
				labour = parseFloat(labour);
				var grand = labour + parseFloat(sumpeiamoun);
				grand = parseFloat(grand);
				grand= grand.toFixed(2);
				$('#total').val(grand);
				$('#labour').removeClass('errorcolor');
			}else{
				$('#labour').addClass('errorcolor');
			}
		}else{
			$('#labour').addClass('errorcolor');
		}
	}
	$('.loading').slideUp();

});

//internal transfer number entry=====================================

$('#gjobnumber').on('keypress',function(e){
	if(e.which===13){
		var idstr = $(this).val();
		$('.loading').slideDown();
		$('.goods').removeClass('errorcolor');
		$(this).removeClass('errorcolor');
		val = idstr.toUpperCase();
		if($('.grd'+val).length == 0){
			if($('.ggooid'+val).length > 0){
				grec = grec + 100;
				var rus = val + grec;
				$(".hidden_inputs").append('<input type="hidden" name="gpvnval" class="gpvnval" id="gpval'+val+'" value="'+val+'">');

				$('.ggooid'+val).each(function(){
					var cha = $(this).val();
					var item = $('#gitem'+cha).val();
					var itemid = $('#gitemid'+cha).val();
					var uom = $('#guom'+cha).val();
					var qty = $('#gqty'+cha).val();
					var alias = $('#galias'+cha).val();

					gadd = gadd + 100;
					gitemadd.push(gadd);
					var us = val+gadd;
					$(".hidden_inputs").append('<input type="hidden" class="girec'+rus+'" value="'+us+'" data="'+gadd+'">');
					$(".hidden_inputs").append('<input type="hidden" name="gitemadd" id="gitemad'+us+'" value="'+gadd+'">');
					$(".hidden_inputs").append('<input type="hidden" name="gipvn'+gadd+'" id="gipvn'+us+'" value="'+val+'">');
					$(".hidden_inputs").append('<input type="hidden" name="ginameid'+gadd+'" id="ginameid'+us+'" value="'+itemid+'">');
					$(".hidden_inputs").append('<input type="hidden" name="giname'+gadd+'" id="giname'+us+'" value="'+item+'">');
					$(".hidden_inputs").append('<input type="hidden" name="giuom'+gadd+'" id="giuom'+us+'" value="'+uom+'">');
					$(".hidden_inputs").append('<input type="hidden" name="giqty'+gadd+'" id="giqty'+us+'" value="'+qty+'">');
					$(".hidden_inputs").append('<input type="hidden" name="gialias'+gadd+'" id="gialias'+us+'" value="'+alias+'">');
					$('.tfoot2').hide();
					$("#MaintainanceTable tbody").append('<tr id="gitemrow'+us+'"><td>'+val+'</td><td>'+item+'('+alias+')</td><td>'+uom+'</td><td>'+qty+'</td><td>0</td><td>0</td><td class="ltd">0</td></tr>');
					$('.tfoot').show();
				});
				$(".grncol").append('<div class="coldiv grd'+val+'" id="colrec'+rus+'"><span class="coldes">'+val+'</span><button type="button" class="gcolbtn" name="'+val+'" data="'+rus+'"><i class="fa fa-times"></i></button></div>');
				$('#gnjobcheck').hide();
				
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

$(document).on('click', '.gcolbtn', function(e){
	var idstr = $(this).attr("data");
	var pval = $(this).attr("name");
	$('.loading').slideDown();
	$('.girec'+idstr).each(function(){
		var cha = $(this).val();
		var hac = $(this).attr("data");
		$('#gitemad'+cha).remove();
		$('#gipvn'+cha).remove();
		$('#ginameid'+cha).remove();
		$('#giname'+cha).remove();
		$('#giuom'+cha).remove();
		$('#giqty'+cha).remove();
		$('#gialias'+cha).remove();

		gitemadd = $.grep(gitemadd, function(value) {
			return value != hac;
		});
		$('#gitemrow'+cha).remove();
		$('#colrec'+idstr).remove();
	});
	$('.gpvnval').each(function(){
		var val = $(this).val();
		if(val==pval){
			$('#gpval'+val).remove();
		}
	});
	if($('.gpvnval').length==0){
		$('#gnjobcheck').show();
	}
	if(gitemadd.length === 0){
		if(itemadd.length === 0){
			$('#subtotal').val(0);
		    $('#labour').val(0);
		    $('#total').val(0);
			ponum = [];
			peiamount = [];
			$('.pvndet').hide();
			$('.pvnshowtable').hide();
			// totaldper = [];
			// totaldamt = [];
			// totalvat = [];
			$('.tfoot').hide();
			$('.tfoot2').show();
		}
	}
	$('.loading').slideUp();

});

//======================================================================

$('#additembtn').click(function(){
	diserror = 0;
	var error = 0;
	$('#item').focus();
	$('#itemerr').empty();
	var itemid = $('#itemm').val();
	var itemname = $('#itemname').val();
	var alias = $('#itemalias').val();
	var uom = $('#itemuom').val();
	var itemqty = $('#itemqty').val();
	var itemrate = $('#itemrate').val();
	var itemamount = $('#itemamount').val();
	var dis_per = $('#discount_per').val();
	var dis_amt = $('#discount_amt').val();
	var billty = $('#bill_type option:selected').val();
	var cval = $('#category option:selected').val();
	var curl = search_url(cval);
	var sval = $('#subcategory'+curl+' option:selected').val();
	var surl = search_url(sval);
	var mainu = caturl+''+surl;
	if($('#itemshow'+mainu).length>0){
		var ival = $('#item'+mainu+' option:selected').val();
		if(ival==''){
			error = 1;
			$('#item'+mainu).addClass('errorcolor');
		}else{
			if(itemid!=ival){
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
	if(dis_per == ''){
		dis_per = 0;
	}
	if(dis_amt == ''){
		dis_amt = 0;
	}
	if(itemid == ''){
		error = 1;
		$('#itemm').addClass('errorcolor');
	}
	if(itemname == ''){
		error = 1;
		$('#itemname').addClass('errorcolor');
	}
	if(uom == ''){
		error = 1;
		$('#itemuom').addClass('errorcolor');
	}
	if(itemqty == ''){
		error = 1;
		$('#itemqty').addClass('errorcolor');
	}
	if(itemrate == ''){
		error = 1;
		$('#itemrate').addClass('errorcolor');
	}
	if(itemamount == ''){
		error = 1;
		$('#itemamount').addClass('errorcolor');
	}
	if(itemer == 0 && error==0){
		add = add + 1;
		itemadd.push(add);
		amount.push(itemamount);
		// console.log(amount);
		// console.log(itemadd);
		$(".hidden_inputs").append('<input type="hidden" name="exitemadd" id="exitemad'+add+'" value="'+add+'">');
		$(".hidden_inputs").append('<input type="hidden" name="itemadd" id="itemad'+add+'" value="'+add+'">');
		$(".hidden_inputs").append('<input type="hidden" name="iid'+add+'" id="iid'+add+'" value="'+itemid+'">');
		$(".hidden_inputs").append('<input type="hidden" name="iname'+add+'" id="iname'+add+'" value="'+itemname+'">');
		$(".hidden_inputs").append('<input type="hidden" name="iuom'+add+'" id="iuom'+add+'" value="'+uom+'">');
		$(".hidden_inputs").append('<input type="hidden" name="iqty'+add+'" id="iqty'+add+'" value="'+itemqty+'">');
		$(".hidden_inputs").append('<input type="hidden" name="irate'+add+'" id="irate'+add+'" value="'+itemrate+'">');
		$(".hidden_inputs").append('<input type="hidden" name="iamt'+add+'" id="iamt'+add+'" value="'+itemamount+'">');
		$(".hidden_inputs").append('<input type="hidden" name="idisper'+add+'" id="idisper'+add+'" value="'+dis_per+'">');
		$(".hidden_inputs").append('<input type="hidden" name="idisamt'+add+'" id="idisamt'+add+'" value="'+dis_amt+'">');
		$(".hidden_inputs").append('<input type="hidden" name="ialias'+add+'" id="ialias'+add+'" value="'+alias+'">');
		$('#itemname').val('');
		$('#itemm').val('');
		$('#uom').val('');
		$('#itemqty').val('');
		$('#itemalias').val('');
		$('#itemrate').val(0);
		$('#itemamount').val(0);
		$('#discount_per').val(0);
		$('#discount_amt').val(0);
		$('.item').val('');
		$('#category').val('');
		$('.subcatshow').hide();
		$('.itemshow').hide();
		$("#MaintainanceTable tbody").append('<tr id="itemrow'+add+'"><td><button type="button" class="edititem" id="eitem'+add+'" data="'+add+'"><i class="far fa-edit"></i></button><button type="button" class="delitem" id="ditem'+add+'" data="'+add+'"><i class="far fa-trash-alt"></i></button></td><td>'+itemname+'('+alias+')</td><td>'+uom+'</td><td>'+itemqty+'</td><td>'+itemrate+'</td><td>'+dis_amt+' ('+dis_per+'%)</td><td class="ltd">'+itemamount+'</td></tr>');
		// $("#MaintainanceTable tbody").append('<tr id="itemrow'+add+'"><td><button type="button" class="edititem" id="eitem'+add+'" data="'+add+'"><i class="far fa-edit"></i></button><button type="button" class="delitem" id="ditem'+add+'" data="'+add+'"><i class="far fa-trash-alt"></i></button></td><td>'+itemname+'('+alias+')</td><td>'+uom+'</td><td>'+itemqty+'</td><td>'+itemrate+'</td><td class="ltd">'+itemamount+'</td></tr>');
		$('.tfoot2').hide();
		$('.tfoot').show();
		var sumamount = 0;
		sumamount = parseFloat(sumamount);
		$.each(amount,function(){sumamount+=parseFloat(this) || 0;});
		var sumamoun = sumamount.toFixed(2);
		if(peiamount.length>0){
			var sumpeiamount = 0;
			sumpeiamount = parseFloat(sumpeiamount);
			$.each(peiamount,function(){sumpeiamount+=parseFloat(this) || 0;});
			sumamoun = sumamount + sumpeiamount;
			sumamoun = parseFloat(sumamoun);
			sumamoun = sumamoun.toFixed(2);
		}
		$('#subtotal').val(sumamoun);
		var labour = $('#labour').val();
		if(labour != ''){
			if(labour>0 || labour==0){
				labour = parseFloat(labour);
				var grand = labour + parseFloat(sumamoun);
				grand = parseFloat(grand);
				grand = grand.toFixed(2);
				$('#total').val(grand);
				$('#labour').removeClass('errorcolor');
			}else{
				$('#labour').addClass('errorcolor');
			}
		}else{
			$('#labour').addClass('errorcolor');
		}
		$('#itemm').val('');
		$('#itemname').val('');
		$('#itemuom').val('');
		$('#itemqty').val('');
		$('#itemrate').val('');
		$('#discount_per').val(0);
		$('#discount_amt').val(0);
		$('#itemamount').val('');
	}
});

$('#additemeditbtn').click(function(){
	diserror = 0;
	var error = 0;
	$('#edititem').focus();
	$('#itemerredit').empty();
	var itemid = $('#edititem').val();
	var itemname = $('#itemnameedit').val();
	var alias = $('#edititemalias').val();
	var itemqty = $('#itemqtyedit').val();
	var uom = $('#itemuomedit').val();
	var itemrate = $('#itemrateedit').val();
	var itemamount = $('#itemamountedit').val();
	var damount = $('#dfaultamount').val();
	var dis_per = $('#editdiscount_per').val();
	var dis_amt = $('#editdiscount_amt').val();
	var did = $('#dfaultid').val();
	var billty = $('#bill_type option:selected').val();
	var cval = $('#editcategory option:selected').val();
	if(cval!=''){
		var curl = search_url(cval);
		var sval = $('#editsubcategory'+curl+' option:selected').val();
		var surl = search_url(sval);
		var mainu = caturl+''+surl;
		if($('#edititemshow'+mainu).length>0){
			var ival = $('#edititem'+mainu+' option:selected').val();
			if(ival==''){
				error = 1;
				$('#edititem'+mainu).addClass('errorcolor');
			}else{
				if(itemid!=ival){
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
	if(dis_per == ''){
		dis_per = 0;
	}
	if(dis_amt == ''){
		dis_amt = 0;
	}
	if(itemid == ''){
		error = 1;
		$('#edititem').addClass('errorcolor');
	}
	if(itemname == ''){
		error = 1;
		$('#itemnameedit').addClass('errorcolor');
	}
	if(uom == ''){
		error = 1;
		$('#itemuomedit').addClass('errorcolor');
	}
	if(itemqty == ''){
		error = 1;
		$('#itemqtyedit').addClass('errorcolor');
	}
	if(itemrate == ''){
		error = 1;
		$('#itemrateedit').addClass('errorcolor');
	}
	if(itemamount == ''){
		error = 1;
		$('#itemamountedit').addClass('errorcolor');
	}
	if(itemeredit == 0 && error==0){
		// amount = $.grep(amount, function(value) {
		//   return value != damount;
		// });
		amount = [];
		// console.log(amount);
		// console.log(itemadd);
		$('#iid'+did).val(itemid);
		$('#iname'+did).val(itemname);
		$('#ialias'+did).val(alias);
		$('#iqty'+did).val(itemqty);
		$('#iuom'+did).val(uom);
		$('#irate'+did).val(itemrate);
		$('#iamt'+did).val(itemamount);
		$('#idisper'+did).val(dis_per);
		$('#idisamt'+did).val(dis_amt);
		$('#edititem').val('');
		$('#itemnameedit').val('');
		$('#itemuomedit').val('');
		$('#itemqtyedit').val('');
		$('#edititemalias').val('');
		$('#itemrateedit').val(0);
		$('#itemamountedit').val(0);
		$('#editdiscount_per').val(0);
		$('#editdiscount_amt').val(0);
		$('.edititem').val('');
		$('#editcategory').val('');
		$('.editsubcatshow').hide();
		$('.edititemshow').hide();
		$('#itemrow'+did).remove();
		$("#MaintainanceTable tbody").append('<tr id="itemrow'+did+'"><td><button type="button" class="edititem" id="eitem'+did+'" data="'+did+'"><i class="far fa-edit"></i></button><button type="button" class="delitem" id="ditem'+did+'" data="'+did+'"><i class="far fa-trash-alt"></i></button></td><td>'+itemname+'('+alias+')</td><td>'+uom+'</td><td>'+itemqty+'</td><td>'+itemrate+'</td><td>'+dis_amt+' ('+dis_per+'%)</td><td class="ltd">'+itemamount+'</td></tr>');
		// $("#MaintainanceTable tbody").append('<tr id="itemrow'+did+'"><td><button type="button" class="edititem" id="eitem'+did+'" data="'+did+'"><i class="far fa-edit"></i></button><button type="button" class="delitem" id="ditem'+did+'" data="'+did+'"><i class="far fa-trash-alt"></i></button></td><td>'+itemname+'('+alias+')</td><td>'+uom+'</td><td>'+itemqty+'</td><td>'+itemrate+'</td><td class="ltd">'+itemamount+'</td></tr>');
		$.each(itemadd , function(index, val) { 
		  var arrayatm = $('#iamt'+val).val();
		  amount.push(arrayatm);
		});
		var sumamount = 0;
		sumamount = parseFloat(sumamount);
		$.each(amount,function(){sumamount+=parseFloat(this) || 0;});
		var sumamoun = sumamount.toFixed(2);
		if(peiamount.length>0){
			var sumpeiamount = 0;
			sumpeiamount = parseFloat(sumpeiamount);
			$.each(peiamount,function(){sumpeiamount+=parseFloat(this) || 0;});
			sumamoun = sumamount + sumpeiamount;
			sumamoun = parseFloat(sumamoun);
			sumamoun = sumamoun.toFixed(2);
		}
		$('#subtotal').val(sumamoun);
		var labour = $('#labour').val();
		if(labour != ''){
			if(labour>0 || labour==0){
				labour = parseFloat(labour);
				var grand = labour + parseFloat(sumamoun);
				grand = parseFloat(grand);
				grand = grand.toFixed(2);
				$('#total').val(grand);
				$('#labour').removeClass('errorcolor');
			}else{
				$('#labour').addClass('errorcolor');
			}
		}else{
			$('#labour').addClass('errorcolor');
		}
		$('#edititem').val('');
		$('#itemnameedit').val('');
		$('#itemuomedit').val('');
		$('#edititemalias').val('');
		$('#itemqtyedit').val('');
		$('#itemrateedit').val('');
		$('#editdiscount_per').val(0);
		$('#editdiscount_amt').val(0);
		$('#itemamountedit').val('');
		$('#edit_popup1').css({"transform": "scale(.1)", "-webkit-transform": "scale(.1)", "-moz-transform": "scale(.1)"});
		$('.edit_popupbanner1').fadeOut();
	}
});

$(document).on('click', '.delitem', function(){
	diserror = 0;
	var idstr = $(this).attr("data");
	$('#itemad'+idstr).remove();
	$('#exitemad'+idstr).remove();
	$('#iid'+idstr).remove();
	$('#iname'+idstr).remove();
	$('#iuom'+idstr).remove();
	$('#iqty'+idstr).remove();
	$('#irate'+idstr).remove();
	$('#iamt'+idstr).remove();
	$('#idisper'+idstr).remove();
	$('#idisamt'+idstr).remove();
	$('#ialias'+idstr).remove();
	amount = [];
	itemadd = $.grep(itemadd, function(value) {
		return value != idstr;
	});
	$('#itemrow'+idstr).remove();
	if (itemadd.length === 0) {
		$('#subtotal').val(0);
	    $('#labour').val(0);
	    // $('#vat').val(0);
	    $('#total').val(0);
		if (gitemadd.length === 0) {
		    // $('#discount1').val(0);
		    // $('#discount2').val(0);
		    $('.tfoot').hide();
		    $('.tfoot2').show();
	    }
	    
	}else{
		$.each(itemadd , function(index, val) {
			if($('#iamt'+val).length>0){
				var arrayatm = $('#iamt'+val).val();
		  		amount.push(arrayatm);
			} 
		});
		var sumpeiamoun = 0;
		var sumpeiamount = 0;
		var sumamount = 0;
		if(peiamount.length>0){
			var sumpeiamount = 0;
			sumpeiamount = parseFloat(sumpeiamount);
			$.each(peiamount,function(){sumpeiamount+=parseFloat(this) || 0;});
			sumpeiamoun = sumpeiamount.toFixed(2);
		}

		if(amount.length>0){
			var sumamount = 0;
			sumamount = parseFloat(sumamount);
			$.each(amount,function(){sumamount+=parseFloat(this) || 0;});
			sumpeiamoun = sumamount.toFixed(2);
		}
		if(amount.length>0 && peiamount.length>0){
			sumpeiamoun = sumpeiamount + sumamount;
			sumpeiamoun = parseFloat(sumpeiamoun);
			sumpeiamoun = sumpeiamoun.toFixed(2);
		}
		$('#subtotal').val(sumpeiamoun);
		var labour = $('#labour').val();
		if(labour != ''){
			if(labour>0 || labour==0){
				labour = parseFloat(labour);
				var grand = labour + parseFloat(sumpeiamoun);
				grand = parseFloat(grand);
				grand= grand.toFixed(2);
				$('#total').val(grand);
				$('#labour').removeClass('errorcolor');
			}else{
				$('#labour').addClass('errorcolor');
			}
		}else{
			$('#labour').addClass('errorcolor');
		}
	}
	
});

$('#labour').click(function(){
	$(this).removeClass('errorcolor');
});

$('#labour').on('keyup', function(){
	diserror = 0;
	var val = $(this).val();
	var suma = $('#subtotal').val();
	if(val!=''){
		if(val>0 || val==0){
			suma = parseFloat(suma);
			val = parseFloat(val);
			var total = val + suma;
			total = parseFloat(total);
			total= total.toFixed(2);
			$('#total').val(total);
			$(this).removeClass('errorcolor');
		}else{
			$(this).addClass('errorcolor');
		}
	}else{
		$(this).addClass('errorcolor');
	}
});

$('#bill_type').on('change', function(){
	diserror = 0;
	var val = $('#bill_type option:selected').val();
	var subtotal = $('#subtotal').val();
	var labour = $('#labour').val();
	var disp = $('#discount1').val();
	if(disp != '' && disp > 0){
		var dis = parseFloat(subtotal) * disp/100;
		var disv = dis.toFixed(2);
		$('#discount2').val(disv);
	}else{
		var dis = $('#discount2').val();
	}
	if(subtotal != '' && subtotal > 0){
		subtotal = parseFloat(subtotal);
		if(dis != '' && dis > 0){
			dis = parseFloat(dis);
			if(dis < subtotal){
				var total = subtotal - dis;
				total = parseFloat(total);
				if(labour != '' && (labour > 0 || labour==0)){
					labour = parseFloat(labour);
					total = labour + total;
					total = parseFloat(total);
					if(val == 'VAT Bill'){
						var vat = total * 13/100;
						vat = parseFloat(vat);
						var grand = total + vat;
						grand = parseFloat(grand);
						grand = grand.toFixed(2);
						vat = vat.toFixed(2);
					}else{
						var vat = 0;
						var grand = total.toFixed(2);
					}
					$('#vat').val(vat);
					$('#total').val(grand);
					$('#labour').removeClass('errorcolor');
				}else{
					$('#labour').addClass('errorcolor');
				}
			}else{
				diserror = 1;
				$('#discount2').addClass('errorcolor');
				$('#discount1').addClass('errorcolor');
			}
		}else{
			if(labour != '' && (labour > 0 || labour==0)){
				labour = parseFloat(labour);
				total = labour + total;
				total = parseFloat(total);
				if(val == 'VAT Bill'){
					var vat = total * 13/100;
					vat = parseFloat(vat);
					var grand = total + vat;
					grand = parseFloat(grand);
					grand = grand.toFixed(2);
					vat = vat.toFixed(2);
				}else{
					var vat = 0;
					var grand = total.toFixed(2);
				}
				$('#vat').val(vat);
				$('#total').val(grand);
				$('#labour').removeClass('errorcolor');
			}else{
				$('#labour').addClass('errorcolor');
			}
		}
	}
});

$('#discount1').on('keyup', function(){
	diserror = 0;
	$(this).removeClass('errorcolor');
	$('#discount2').removeClass('errorcolor');
	var val = $(this).val();
	var intype = $('#bill_type option:selected').val();
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
				$('#bill_type').addClass('errorcolor');
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
			$('#bill_type').addClass('errorcolor');
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
	var intype = $('#bill_type option:selected').val();
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
				$('#bill_type').addClass('errorcolor');
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
			$('#bill_type').addClass('errorcolor');
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
	var qty = $('#itemqty').val();
	var rate = $('#itemrate').val();
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
				$('#itemamount').val(total);
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
			$('#itemamount').val(total);
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
	var qty = $('#itemqty').val();
	var rate = $('#itemrate').val();
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
				$('#itemamount').val(total);
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
			$('#itemamount').val(total);
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
	var qty = $('#itemqtyedit').val();
	var rate = $('#itemrateedit').val();
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
				$('#itemamountedit').val(total);
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
			$('#itemamountedit').val(total);
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
	var qty = $('#itemqtyedit').val();
	var rate = $('#itemrateedit').val();
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
				$('#itemamountedit').val(total);
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
			$('#itemamountedit').val(total);
		}

	}
	dis = dis.toFixed(2);
	$('#editdiscount_per').val(dis);

});

$('#checkblock').click(function(){
	$(this).removeClass('errorcolor');
	$('#gcheckblock').removeClass('errorcolor');
});
$('#gcheckblock').click(function(){
	$(this).removeClass('errorcolor');
	$('#checkblock').removeClass('errorcolor');
});
$('#tranblock').click(function(){
	$(this).removeClass('errorcolor');
});
$('.maintainitems').click(function(){
	$(this).css({"border": "none"});
});
$('.goods').click(function(){
	$(this).removeClass('errorcolor');
});
// $('.jobmodule').click(function(){
// 	$(this).css({"border": "none"});
// });

$('#MaintainanceForm').on('submit', function(){
	var error = 0;
	$('#spinner1').show();
	var vehicle;
	var vehicle_type;
	var driver;
	var driver_id;
	var kilometer;
	var vendor;
	var part;
	var est_cost;
	var description;
	var jedate;
	var japprove;
	var jobnumber;
	var gjobnumber;
	var date = $('input[name=date]').val();
	if(date==''){
		error=1;
		$('#date').addClass('errorcolor');
	}
	// var discount1 = $('#discount1').val();
	// var discount2 = $('#discount2').val();
	// if(discount1=='' || discount2=='' || discount1<0 || discount2<0){
	// 	$('#discount1').val(0);
	// 	$('#discount2').val(0);
	// }
	var billdate = $('input[name=invoice_date]').val();
	if(billdate==''){
		error=1;
		$('#invoice_date').addClass('errorcolor');
	}
	var billnum = $('input[name=invoice]').val();
	if(billnum==''){
		error=1;
		$('#invoice').addClass('errorcolor');
	}
	
	// var problem = $('#problem option:selected').val();
	// if(problem==''){
	// 	error=1;
	// 	$('#problem').addClass('errorcolor');
	// }
	// var billtype = $('#bill_type option:selected').val();
	// if(billtype==''){
	// 	error=1;
	// 	$('#billtype').addClass('errorcolor');
	// }
	// var supplier = $('#supplier option:selected').val();
	// if(supplier==''){
	// 	error=1;
	// 	$('#supplier').addClass('errorcolor');
	// }

	var lbour = $('#labour').val();
	if(lbour=='' || lbour < 0){
		error=1;
		$('#labour').addClass('errorcolor');
	}

	if($('#yesjob').prop("checked") == true){
		jobnumber = $('#jobnumber').val();
		if(jobnumber==''){
			error = 1;
			$('#jobnumber').addClass('errorcolor');
		}else{
			if($('.pvnval').length<0){
				error = 1;
				var val = jobnumber.toUpperCase();
				$('#pvnselban'+val).addClass('errorcolor');
			}
		}
	}else if($('#nojob').prop("checked") == true){
		jobnumber = '';
	}else{
		error = 1;
		$('#checkblock').addClass('errorcolor');
	}

	if($('#gyesjob').prop("checked") == true){
		if($('.gpvnval').length<0){
			error = 1;
			var val = gjobnumber.toUpperCase();
			$('#gjobnumber').addClass('errorcolor');
		}
	}else if($('#gnojob').prop("checked") == true){
		gjobnumber = '';
	}else{
		error = 1;
		$('#gcheckblock').addClass('errorcolor');
	}

	var hour = $('#hour').val();
	if(hour==''){
		error=1;
		$('#hour').addClass('errorcolor');
	}
	var kilometer = $('#kilometer').val();
	if(kilometer==''){
		error=1;
		$('#kilometer').addClass('errorcolor');
	}

	if($('#nojob').prop("checked") == true){
		if($('#gyesjob').prop("checked") == true){
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
	}

	if($('#nojob').prop("checked") == true && $('#gnojob').prop("checked") == true){
		error = 1;
		$('#checkblock').addClass('errorcolor');
		$('#gcheckblock').addClass('errorcolor');
	}

	if(porder==1){
		error = 1;
		$('#jobnumber').addClass('errorcolor');
	}

	if(itemadd.length===0 && gitemadd.length===0){
		error = 1;
		$('.goods').addClass('errorcolor');
	}

	if(error==0){
		document.MaintainanceForm.submit();
	}else{
		$('#spinner1').hide();
	}
	event.preventDefault();
});
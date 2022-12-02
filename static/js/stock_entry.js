$('#StockEditForm input').on('keypress', function(e) {
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

// search edit=============================
if($('#scat').length>0){
	var scat = $('#scat').val();
	var sscat = $('#sscat').val();
	var ssite = $('#ssite').val();
	if(scat!='' && scat!='None'){
		var scaturl = search_url(scat);
		$('#searchcategory').val(scat);
		if(sscat!='' && sscat!='None'){
			$('.subcatsearch').hide();
			$('#subcatsearch'+scaturl).show();
			$('#subcatsearch'+scaturl).val(sscat);
		}
	}
	if(ssite!='' && ssite!='None'){
		$('#searchsite').val(ssite);
	}
}

//======================================
function search_url(val){
  var url = val.toLowerCase();
  var result = url.replace(/[^a-z0-9\s]/gi, '').replace(/[_\s]/g, '');
  return result;
}
$('#searchcategory').on('change', function(){
	var val = $('#searchcategory option:selected').val();
	var url = search_url(val);
	$('.subcatsearch').hide();
	if($('#subcatsearch'+url).length>0){
		$('#subcatsearch'+url).show();
		var sval = $('#subcatsearch'+url+' option:selected').val();
		$('#subcsearch').val(sval);
	}else{
		$('#subcsearch').val('');
	}
});
$('.subcatsearch').on('change', function(){
	var idstr = $(this).attr("id");
	var val = $('#'+idstr+' option:selected').val();
	$('#subcsearch').val(val);
});

$('#stock_category').on('change', function(){
	var val = $('#stock_category option:selected').val();
	var url = search_url(val);
	$('#categoryurl').val(url);
	$('.subcategory').val('');
	$('.subcatshow').hide();
	if($('#subcatshow'+url).length>0){
		$('#subcatshow'+url).show();
		var sval = $('#subcategory'+url+' option:selected').val();
		if(sval!=''){
			$('#subcatval').val(sval);
			var surl = search_url(sval);
			$('#subcatvalurl').val(surl);
		}else{
			$('#subcatval').val('');
			$('#subcatvalurl').val('');
		}
	}else{
		$('#subcatval').val('');
		$('#subcatvalurl').val('');
	}
});
$('.subcategory').on('change', function(){
	var idstr = $(this).attr("id");
	var val = $('#'+idstr+' option:selected').val();
	$('#subcatval').val(val);
	var surl = search_url(val);
	$('#subcatvalurl').val(surl);
	var mcat = $('#categoryurl').val();
	var murl = mcat+''+surl;
	$('#mainurl').val(murl);
});

var sitec = 0;
$('#site').on('change', function(){
	var val = $('#site option:selected').val();
	var url = val.toLowerCase();
  	url = url.replace(/[^a-z0-9\s]/gi, '').replace(/[_\s]/g, '');
  	if($('#sites'+url).length == 0){
  		sitec = sitec + 1;
		siteid = 'siteid'+sitec;
		$('.sitecol').append('<div id="'+url+'"></div>');
		var $div = $('#siteb').clone().attr('id', null);
		$('#'+url).html($div);
		$("#"+url+" .siteblock").show();
		$("#"+url+" .siteblock .sblock_head span").text(val);
		$("#"+url+" .siteblock .closeblock").attr('data', ''+url);
	  	$("#"+url+" .siteblock .sblock_body .quantity").attr('name', 'qty'+url);
	  	$("#"+url+" .siteblock .sblock_body .quantity").attr('data', ''+url);
	  	$("#"+url+" .siteblock .sblock_body .quantity").attr('id', 'qty'+url);
	  	$("#"+url+" .siteblock .sblock_body .rate").attr('name', 'rate'+url);
	  	$("#"+url+" .siteblock .sblock_body .rate").attr('data', ''+url);
	  	$("#"+url+" .siteblock .sblock_body .rate").attr('id', 'rate'+url);
	  	$("#"+url+" .siteblock .sblock_body .amount").attr('name', 'amt'+url);
	  	$("#"+url+" .siteblock .sblock_body .amount").attr('data', ''+url);
	  	$("#"+url+" .siteblock .sblock_body .amount").attr('id', 'amt'+url);
	  	$(".hidden_inputs").append('<input type="hidden" name="sites" id="sites'+url+'" value="'+url+'">');
	  	$(".hidden_inputs").append('<input type="hidden" name="site_name'+url+'" id="site_name'+url+'" value="'+val+'">');
  	}
  	$(this).val('');
});
$(document).on('click', '.closeblock', function(){
	var idstr = $(this).attr("data");
	$('#'+idstr).remove();
	$('#sites'+idstr).remove();
	$('#site_name'+idstr).remove();
	sitec = sitec - 1;
});
$(document).on('keyup', '.quantity', function(){
	var val = $(this).val();
	var idstr = $(this).attr("data");
	$(this).removeClass('errorcolor');
	if(val != ''){
		val =parseFloat(val);
		if(val>0 || val == 0){
			var rt = $('#rate'+idstr).val();
			if(rt!=''){
				if(rt>0 || rt == 0){
					rt = parseFloat(rt);
					var amt = val * rt;
					amt = parseFloat(amt);
					amt = amt.toFixed(2);
					$('#amt'+idstr).val(amt);
				}else{
					$('#rate'+idstr).addClass('errorcolor');
				}
			}else{
				$('#rate'+idstr).addClass('errorcolor');
			}
		}else{
			$(this).addClass('errorcolor');
		}
	}else{
		$(this).addClass('errorcolor');
	}
});
$(document).on('keyup', '.rate', function(){
	var val = $(this).val();
	var idstr = $(this).attr("data");
	$(this).removeClass('errorcolor');
	if(val != ''){
		val =parseFloat(val);
		if(val>0 || val == 0){
			var rt = $('#qty'+idstr).val();
			if(rt!=''){
				if(rt>0 || rt == 0){
					rt = parseFloat(rt);
					var amt = val * rt;
					amt = parseFloat(amt);
					amt = amt.toFixed(2);
					$('#amt'+idstr).val(amt);
				}else{
					$('#qty'+idstr).addClass('errorcolor');
				}
			}else{
				$('#qty'+idstr).addClass('errorcolor');
			}
		}else{
			$(this).addClass('errorcolor');
		}
	}else{
		$(this).addClass('errorcolor');
	}
});

$('#name').on('keyup', function(){
	name_url();
});
$('#StockForm').on('submit', function(){
	$('#spinner1').show();
	var error = 0;
	var name = $('input[name=name]').val();
	var url = $('input[name=url]').val();
	var alias = $('input[name=alias]').val();
	var stock_cat = $('#stock_category option:selected').val();
	var surl = $('#categoryurl').val();
	var mainurl = $('#mainurl').val();
	var uom = $('#uom option:selected').val();
	var stock_type = $('#stock_type option:selected').val();
	if(stock_cat==''){
		error = 1;
		$('#stock_category').addClass('errorcolor');
	}
	if(surl==''){
		error = 1;
		$('#stock_category').addClass('errorcolor');
	}
	if($('#subcatshow'+surl).length>0){
		var sval = $('#subcategory'+surl).val();
		if(sval==''){
			error = 1;
			$('#subcategory'+surl).addClass('errorcolor');
		}else{
			var ssval = $('#subcatval').val();
			var ssurl = search_url(sval);
			var sssurl = $('#subcatvalurl').val();
			if(ssval!=sval){
				error = 1;
				$('#subcategory'+surl).addClass('errorcolor');
			}
			if(ssurl!=sssurl){
				error = 1;
				$('#subcategory'+surl).addClass('errorcolor');
			}
		}
	}else{
		error= 1;
		$('#stock_category').addClass('errorcolor');
	}
	if(name==''){
		error = 1;
		$('#name').addClass('errorcolor');
	}
	if(mainurl==''){
		error = 1;
		$('#stock_category').addClass('errorcolor');
	}
	if(uom==''){
		error = 1;
		$('#uom').addClass('errorcolor');
	}
	if(stock_type==''){
		error = 1;
		$('#stock_type').addClass('errorcolor');
	}
	if(sitec!=0){
		$('.sites').each(function(){
			var val = $(this).val();
			var qty = $('#qty'+val).val();
			var rate = $('#rate'+val).val();
			if(qty == '' || qty < 0){
				$('#qty'+val).val(0);
				$('#amt'+val).val(0);
			}
			if(rate == '' || rate < 0){
				$('#rate'+val).val(0);
				$('#amt'+val).val(0);
			}
		});
	}
	if(error==0){
		document.StockForm.submit();
	}else{
		$('#spinner1').hide();
	}
	event.preventDefault();
});

function name_url(){
  var name = $('#name').val();
  $('#url').val(name);
  var url = $('#url').val().toLowerCase();
  var result = url.replace(/[^a-z0-9\s]/gi, '').replace(/[_\s]/g, '');
  $('#url').val(result);
}

$('.sup_edit').click(function(){
	var idstr = $(this).attr("data");
	var name = $('#name'+idstr).val();
	var alias = $('#ali'+idstr).val();
	var url = $('#url'+idstr).val();
	var cat = $('#cat'+idstr).val();
	var scat = $('#subcat'+idstr).val();
	var uom = $('#uom'+idstr).val();
	var opening = $('#opening'+idstr).val();
	var qty = $('#qty'+idstr).val();
	var rate = $('#rate'+idstr).val();
	var amt = $('#amt'+idstr).val();
	var type = $('#type'+idstr).val();
	var s_site = $('#s_site'+idstr).val();
	$('#suid').val(idstr);
	$('#dname').val(name);
	$('#name').val(name);
	$('#url').val(url);
	$('#alias').val(alias);
	$('#category').val(cat);
	$('#subcategory').val(scat);
	$('#catinp').val(cat);
	$('#uom').val(uom);
	$('#uominp').val(uom);
	$('#type').val(type);
	$('#typeinp').val(type);
	$('#opening').val(opening);
	$('#dopen').val(opening);
	$('#quantity').val(qty);
	$('#rate').val(rate);
	$('#amount').val(amt);
	$('#editsite').val(s_site);
	$('#siteinp').val(s_site);
	$('.edit_popupbanner').fadeIn();
	$('#edit_popup').css({"transform": "scale(1)", "-webkit-transform": "scale(1)", "-moz-transform": "scale(1)"});
});
$('#close_edit').click(function(){
	$('#name').val('');
	$('#url').val('');
	$('#alias').val('');
	$('#category').val('');
	$('#subcategory').val('');
	$('#uom').val('');
	$('#type').val('');
	$('#opening').val('');
	$('#quantity').val('');
	$('#rate').val('');
	$('#amount').val('');
	$('#editsite').val('');
	$('#edit_popup').css({"transform": "scale(.1)", "-webkit-transform": "scale(.1)", "-moz-transform": "scale(.1)"});
	$('.edit_popupbanner').fadeOut();
});
$('.sup_delete').click(function(){
	$('.del_popupbanner').fadeIn();
	var idstr = $(this).attr("data");
	$('#sid').val(idstr);
	$('#del_popup').css({"transform": "scale(1)", "-webkit-transform": "scale(1)", "-moz-transform": "scale(1)"});
});
$('#cancel_btn').on('click', function(){
	$('#sid').val('');
	$('#del_popup').css({"transform": "scale(.1)", "-webkit-transform": "scale(.1)", "-moz-transform": "scale(.1)"});
	$('.del_popupbanner').fadeOut();
});


$('#quantity').on('keyup', function(){
	var val = $(this).val();
	$(this).removeClass('errorcolor');
	$('#quantity').removeClass('errorcolor');
	$('#amount').removeClass('errorcolor');
	if(val != ''){
		val =parseFloat(val);
		if(val>0 || val == 0){
			var rt = $('#rate').val();
			if(rt!=''){
				if(rt>0 || rt == 0){
					rt = parseFloat(rt);
					var amt = val * rt;
					amt = parseFloat(amt);
					amt = amt.toFixed(2);
					$('#amount').val(amt);
				}else{
					$('#rate').addClass('errorcolor');
				}
			}else{
				$('#rate').addClass('errorcolor');
			}
		}else{
			$(this).addClass('errorcolor');
		}
	}else{
		$(this).addClass('errorcolor');
	}
});
$('#rate').on('keyup', function(){
	var val = $(this).val();
	$(this).removeClass('errorcolor');
	$('#quantity').removeClass('errorcolor');
	$('#amount').removeClass('errorcolor');
	if(val != ''){
		val =parseFloat(val);
		if(val>0 || val == 0){
			var rt = $('#quantity').val();
			if(rt!=''){
				if(rt>0 || rt == 0){
					rt = parseFloat(rt);
					var amt = val * rt;
					amt = parseFloat(amt);
					amt = amt.toFixed(2);
					$('#amount').val(amt);
				}else{
					$('#quantity').addClass('errorcolor');
				}
			}else{
				$('#quantity').addClass('errorcolor');
			}
		}else{
			$(this).addClass('errorcolor');
		}
	}else{
		$(this).addClass('errorcolor');
	}
});

$('#opening').on('keyup', function(){
	var val = $(this).val();
	$(this).removeClass('errorcolor');
	$('#quantity').removeClass('errorcolor');
	$('#amount').removeClass('errorcolor');
	if(val!=''){
		val =parseFloat(val);
		if(val>0 || val == 0){
			var dopen = $('#dopen').val();
			var idstr = $('#suid').val();
			var qty = $('#qty'+idstr).val();
			dopen = parseFloat(dopen);
			if(qty>0){
				if(val<dopen){
					qty = parseFloat(qty);
					qty = qty - dopen;
					qty = qty + val;
					var rate = $('#rate').val();
					var amt = 0;
					if(rate!=''){
						rate = parseFloat(rate);
						if(rate>0){
							amt = rate * qty;
						}
					}else{
						$('#rate').addClass('errorcolor');
					}
					amt = parseFloat(amt);
					amt = amt.toFixed(2);
					qty = qty.toFixed(2);
					$('#quantity').val(qty);
					$('#amount').val(amt);
				}
				if(val>dopen){
					qty = parseFloat(qty);
					var nqty = val - dopen;
					nqty = parseFloat(nqty);
					qty = qty + nqty;
					var rate = $('#rate').val();
					var amt = 0;
					if(rate!=''){
						rate = parseFloat(rate);
						if(rate>0){
							amt = rate * qty;
						}
					}else{
						$('#rate').addClass('errorcolor');
					}
					amt = parseFloat(amt);
					amt = amt.toFixed(2);
					qty = qty.toFixed(2);
					$('#quantity').val(qty);
					$('#amount').val(amt);
				}
				if(val==dopen){
					qty = parseFloat(qty);
					var rate = $('#rate').val();
					var amt = 0;
					if(rate!=''){
						rate = parseFloat(rate);
						if(rate>0){
							amt = rate * qty;
						}
					}else{
						$('#rate').addClass('errorcolor');
					}
					amt = parseFloat(amt);
					amt = amt.toFixed(2);
					qty = qty.toFixed(2);
					$('#quantity').val(qty);
					$('#amount').val(amt);
				}
			}
			if(qty==0){
				qty = val;
				qty = parseFloat(qty);
				var rate = $('#rate').val();
				var amt = 0;
				if(rate!=''){
					rate = parseFloat(rate);
					if(rate>0){
						amt = rate * qty;
					}
				}else{
					$('#rate').addClass('errorcolor');
				}
				amt = parseFloat(amt);
				amt = amt.toFixed(2);
				qty = qty.toFixed(2);
				$('#quantity').val(qty);
				$('#amount').val(amt);
			}
		}else{
			$(this).addClass('errorcolor');
		}
	}else{
		$(this).addClass('errorcolor');
	}
});

$('#StockEditForm').on('submit', function(){
	var error = 0;
	$('#spinner1').show();
	var name = $('input[name=name]').val();
	var url = $('input[name=url]').val();
	var alias = $('input[name=alias]').val();
	var stock_cat = $('#category option:selected').val();
	var uom = $('#uom option:selected').val();
	var stock_type = $('#type option:selected').val();
	var opening = $('#opening').val();
	var quantity = $('#quantity').val();
	var rate = $('#rate').val();
	var amount = $('#amount').val();
	var site = $('#editsite').val();
	if(name==''){
		error = 1;
		$('#name').addClass('errorcolor');
	}
	// if(alias==''){
	// 	error = 1;
	// 	$('#alias').addClass('errorcolor');
	// }
	if(stock_cat==''){
		error = 1;
		$('#category').addClass('errorcolor');
	}
	if(uom==''){
		error = 1;
		$('#uom').addClass('errorcolor');
	}
	if(stock_type==''){
		error = 1;
		$('#type').addClass('errorcolor');
	}
	if(site==''){
		error = 1;
		$('#editsite').addClass('errorcolor');
	}
	if(opening=='' || opening<0){
		error = 1;
		$('#opening').addClass('errorcolor');
	}
	if(rate=='' || rate<0){
		$('#rate').val(0);
		$('#amount').val(0);
	}
	if(quantity<0 || amount<0){
		error = 1;
		$('#quantity').addClass('errorcolor');
		$('#amount').addClass('errorcolor');
	}
	if(error==0){
		document.StockEditForm.submit();
	}else{
		$('#spinner1').hide();
	}
	event.preventDefault();
});

$('#StockSearch').on('submit', function(){
	var error = 0;
	var scat = $('#searchcategory option:selected').val();
	var ssite = $('#searchsite option:selected').val();
	var search = $('#ssearch').val();
	if(scat=='' && ssite=='' && search==''){
		error = 1;
	}
	if(error==0){
		document.StockSearch.submit();
	}
	event.preventDefault();
});
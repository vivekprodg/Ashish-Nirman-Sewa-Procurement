
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
	if(scat!='' && scat!='None'){
		var scaturl = search_url(scat);
		$('#searchcategory').val(scat);
		if(sscat!='' && sscat!='None'){
			$('.subcatsearch').hide();
			$('#subcatsearch'+scaturl).show();
			$('#subcatsearch'+scaturl).val(sscat);
		}
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

$('#name').on('keyup', function(){
	name_url();
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
	var caturl = search_url(cat);
	var scat = $('#subcat'+idstr).val();
	var uom = $('#uom'+idstr).val();
	var type = $('#type'+idstr).val();
	$('#suid').val(idstr);
	$('#dname').val(name);
	$('#dalias').val(alias);
	$('#duom').val(uom);
	$('#name').val(name);
	$('#url').val(url);
	$('#alias').val(alias);
	$('#category').val(cat);
	$('#uom').val(uom);
	$('#type').val(type);
	$('.subcatshow').hide();
	if($('#subcatshow'+caturl).length>0){
		$('#subcatshow'+caturl).show();
		$('#subcategory'+caturl).val(scat);
		$('#subcatval').val(scat);
	}
	$('.edit_popupbanner').fadeIn();
	$('#edit_popup').css({"transform": "scale(1)", "-webkit-transform": "scale(1)", "-moz-transform": "scale(1)"});
});
$('#close_edit').click(function(){
	$('#name').val('');
	$('#url').val('');
	$('#alias').val('');
	$('#category').val('');
	$('#uom').val('');
	$('#type').val('');
	$('#subcatval').val('');
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

$('#category').on('change', function(){
	var val = $('#category option:selected').val();
	var url = search_url(val);
	$('.subcatshow').hide();
	if($('#subcatshow'+url).length>0){
		$('#subcatshow'+url).show();
		var sval = $('#subcategory'+url+' option:selected').val();
		$('#subcatval').val(sval);
	}else{
		$('#subcatval').val('');
	}
});
$('.subcategory').on('change', function(){
	var idstr = $(this).attr("id");
	console.log(idstr);
	var val = $('#'+idstr+' option:selected').val();
	$('#subcatval').val(val);
});


$('#StockEditForm').on('submit', function(){
	var error = 0;
	$('#spinner1').show();
	var name = $('input[name=name]').val();
	var url = $('input[name=url]').val();
	var alias = $('input[name=alias]').val();
	var stock_cat = $('#category option:selected').val();
	var scurl = search_url(stok_cat);
	var uom = $('#uom option:selected').val();
	var stock_type = $('#type option:selected').val();
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
	if($('#subcategory'+scurl).length>0){
		var subcat = $('#subcategory'+scurl+' option:selected').val();
		if(subcat==''){
			error = 1;
			$('#subcategory'+scurl).addClass('errorcolor');
		}
	}
	if(uom==''){
		error = 1;
		$('#uom').addClass('errorcolor');
	}
	if(stock_type==''){
		error = 1;
		$('#type').addClass('errorcolor');
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
	var search = $('#ssearch').val();
	if(scat=='' && search==''){
		error = 1;
	}
	if(error==0){
		document.StockSearch.submit();
	}
	event.preventDefault();
});
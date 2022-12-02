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
function url(){
  var name = $('#name').val();
  $('#url').val(name);
  var mat_url = $('#url').val().toLowerCase();
  var result = mat_url.replace(/[^a-z0-9\s]/gi, '').replace(/[_\s]/g, '');
  $('#url').val(result);
}
function suburl(val){
  var mat_url = val.toLowerCase();
  var result = mat_url.replace(/[^a-z0-9\s]/gi, '').replace(/[_\s]/g, '');
  return result;
}
$('#name').on('keyup', function(){
	url();
});
$('#StockCategoryForm').on('submit', function(){
	var error = 0;
	$('#spinner1').show();
	var name = $('#name').val();
	var url = $('#url').val();
	if(name==''){
		error = 1;
		$('#name').addClass('errorcolor');
	}
	if(url==''){
		error = 1;
		$('#name').addClass('errorcolor');
	}
	if(error==0){
		document.StockCategoryForm.submit();
	}else{
		$('#spinner1').hide();
	}
	event.preventDefault();
});
$('#StockSubCategoryForm').on('submit', function(){
	var error = 0;
	$('#spinner2').show();
	var cat = $('#stock_category option:selected').val();
	var caturl = suburl(cat);
	$('#caturl').val(caturl);
	var name = $('#subname').val();
	var url = suburl(name);
	$('#suburl').val(url);
	if(cat==''){
		error = 1;
		$('#stock_category').addClass('errorcolor');
	}
	if(name==''){
		error = 1;
		$('#subname').addClass('errorcolor');
	}
	if(url==''){
		error = 1;
		$('#subname').addClass('errorcolor');
	}
	if(error==0){
		document.StockSubCategoryForm.submit();
	}else{
		$('#spinner2').hide();
	}
	event.preventDefault();
});

$('.sup_edit').click(function(){
	var idstr = $(this).attr("data");
	var name = $('#name'+idstr).val();
	var url = $('#url'+idstr).val();
	$('#luid').val(idstr);
	$('#editname').val(name);
	$('#default').val(name);
	$('#editurl').val(url);
	$('.edit_popupbanner').fadeIn();
	$('#edit_popup').css({"transform": "scale(1)", "-webkit-transform": "scale(1)", "-moz-transform": "scale(1)"});
});
$('#close_edit').click(function(){
	$('#editname').val('');
	$('#editurl').val('');
	$('#default').val('');
	$('#edit_popup').css({"transform": "scale(.1)", "-webkit-transform": "scale(.1)", "-moz-transform": "scale(.1)"});
	$('.edit_popupbanner').fadeOut();
});

$('.sub_edit').click(function(){
	var idstr = $(this).attr("data");
	var name = $('#sname'+idstr).val();
	var url = $('#surl'+idstr).val();
	var scname = $('#scname'+idstr).val();
	var scurl = $('#scurl'+idstr).val();
	$('#sluid').val(idstr);
	$('#editstock_category').val(scname);
	$('#editsubname').val(name);
	$('#defaultsub').val(name);
	$('#editcaturl').val(scurl);
	$('#editsuburl').val(url);
	$('.subedit_popupbanner').fadeIn();
	$('#subedit_popup').css({"transform": "scale(1)", "-webkit-transform": "scale(1)", "-moz-transform": "scale(1)"});
});
$('#subclose_edit').click(function(){
	$('#editstock_category').val('');
	$('#editcaturl').val('');
	$('#editsubname').val('');
	$('#defaultsub').val('');
	$('#editsuburl').val('');
	$('#subedit_popup').css({"transform": "scale(.1)", "-webkit-transform": "scale(.1)", "-moz-transform": "scale(.1)"});
	$('.subedit_popupbanner').fadeOut();
});

$('.sup_delete').click(function(){
	$('.del_popupbanner').fadeIn();
	var idstr = $(this).attr("data");
	$('#lid').val(idstr);
	$('#del_popup').css({"transform": "scale(1)", "-webkit-transform": "scale(1)", "-moz-transform": "scale(1)"});
});
$('#cancel_btn').on('click', function(){
	$('#lid').val('');
	$('#del_popup').css({"transform": "scale(.1)", "-webkit-transform": "scale(.1)", "-moz-transform": "scale(.1)"});
	$('.del_popupbanner').fadeOut();
});

$('.sub_delete').click(function(){
	$('.subdel_popupbanner').fadeIn();
	var idstr = $(this).attr("data");
	$('#slid').val(idstr);
	$('#subdel_popup').css({"transform": "scale(1)", "-webkit-transform": "scale(1)", "-moz-transform": "scale(1)"});
});
$('#subcancel_btn').on('click', function(){
	$('#slid').val('');
	$('#subdel_popup').css({"transform": "scale(.1)", "-webkit-transform": "scale(.1)", "-moz-transform": "scale(.1)"});
	$('.subdel_popupbanner').fadeOut();
});

function editurl(){
  var name = $('#editname').val();
  $('#editurl').val(name);
  var mat_url = $('#editurl').val().toLowerCase();
  var result = mat_url.replace(/[^a-z0-9\s]/gi, '').replace(/[_\s]/g, '');
  $('#editurl').val(result);
}
$('#editname').on('keyup', function(){
	editurl();
});

$('#StockCategoryEditForm').on('submit', function(){
	var error = 0;
	$('#spinner2').show();
	var name = $('#editname').val();
	var url = $('#editurl').val();
	if(name==''){
		error = 1;
		$('#editname').addClass('errorcolor');
	}
	if(url==''){
		error = 1;
		$('#editname').addClass('errorcolor');
	}
	if(error==0){
		document.StockCategoryEditForm.submit();
	}else{
		$('#spinner2').hide();
	}
	event.preventDefault();
});

$('#StockSubCategoryEditForm').on('submit', function(){
	var error = 0;
	$('#spinner2').show();
	var cname = $('#editstock_category option:selected').val();
	var caturl = suburl(cname);
	$('#editcaturl').val(caturl);
	var name = $('#editsubname').val();
	var url = suburl(name);
	$('#editsuburl').val(url);
	if(cname==''){
		error = 1;
		$('#editstock_category').addClass('errorcolor');
	}
	if(name==''){
		error = 1;
		$('#editsubname').addClass('errorcolor');
	}
	if(url==''){
		error = 1;
		$('#editsuburl').addClass('errorcolor');
	}
	if(error==0){
		document.StockSubCategoryEditForm.submit();
	}else{
		$('#spinner2').hide();
	}
	event.preventDefault();
});
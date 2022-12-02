
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
	var uom = $('#uom'+idstr).val();
	var type = $('#type'+idstr).val();
	$('#suid').val(idstr);
	$('#dname').val(name);
	$('#name').val(name);
	$('#url').val(url);
	$('#alias').val(alias);
	$('#category').val(cat);
	$('#uom').val(uom);
	$('#type').val(type);
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


$('#StockEditForm').on('submit', function(){
	var error = 0;
	$('#spinner1').show();
	var name = $('input[name=name]').val();
	var url = $('input[name=url]').val();
	var alias = $('input[name=alias]').val();
	var stock_cat = $('#category option:selected').val();
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
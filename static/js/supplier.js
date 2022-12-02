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
$('#SupplierForm').on('submit', function(){
	var error = 0;
	$('#spinner1').show();
	var name = $('#name').val();
	var address = $('#address').val();
	var pan = $('#pan').val();
	var landline = $('#landline').val();
	var category = $('#category option:selected').val();
	var nperson1 = $('#person1').val();
	var eperson1 = $('#person1email').val();
	var cperson1 = $('#person1contact').val();
	var nperson2 = $('#person2').val();
	var eperson2 = $('#person2email').val();
	var cperson2 = $('#person2contact').val();
	var opening = $('#opening').val();
	if(name==''){
		error = 1;
		$('#name').addClass('errorcolor');
	}
	if(address==''){
		error = 1;
		$('#address').addClass('errorcolor');
	}
	if(pan==''){
		error = 1;
		$('#pan').addClass('errorcolor');
	}
	if(landline==''){
		error = 1;
		$('#landline').addClass('errorcolor');
	}
	if(category==''){
		error = 1;
		$('#category').addClass('errorcolor');
	}
	if(opening==''||opening<0){
		error = 1;
		$('#opening').addClass('errorcolor');
	}
	if(error==0){
		document.SupplierForm.submit();
	}else{
		$('#spinner1').hide();
	}
	event.preventDefault();
});

$('.sup_edit').click(function(){
	var idstr = $(this).attr("data");
	var name = $('#name'+idstr).val();
	var address = $('#add'+idstr).val();
	var pan = $('#pan'+idstr).val();
	var land = $('#land'+idstr).val();
	var cat = $('#cat'+idstr).val();
	var p1 = $('#p1'+idstr).val();
	var p1email = $('#p1email'+idstr).val();
	var p1mob = $('#p1mob'+idstr).val();
	var p2 = $('#p2'+idstr).val();
	var p2email = $('#p2email'+idstr).val();
	var p2mob = $('#p2mob'+idstr).val();
	var opening = $('#open'+idstr).val();
	$('#suid').val(idstr);
	$('#name').val(name);
	$('#address').val(address);
	$('#pan').val(pan);
	$('#landline').val(land);
	$('#category').val(cat);
	$('#person1').val(p1);
	$('#person1email').val(p1email);
	$('#person1contact').val(p1mob);
	$('#person2').val(p2);
	$('#person2email').val(p2email);
	$('#person2contact').val(p2mob);
	$('#opening').val(opening);
	$('.edit_popupbanner').fadeIn();
	$('#edit_popup').css({"transform": "scale(1)", "-webkit-transform": "scale(1)", "-moz-transform": "scale(1)"});
});
$('#close_edit').click(function(){
	$('#name').val('');
	$('#address').val('');
	$('#pan').val('');
	$('#landline').val('');
	$('#category').val('');
	$('#person1').val('');
	$('#person1email').val('');
	$('#person1contact').val('');
	$('#person2').val('');
	$('#person2email').val('');
	$('#person2contact').val('');
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
$('#paysup').click(function(){
	$('.cre_popupbanner').fadeIn();
	$('#cre_popup').css({"transform": "scale(1)", "-webkit-transform": "scale(1)", "-moz-transform": "scale(1)"});
});
$('#close_cre').click(function(){
	$('#cre_popup').css({"transform": "scale(.2)", "-webkit-transform": "scale(.2)", "-moz-transform": "scale(.2)"});
	$('.cre_popupbanner').fadeOut();
});
$('#selsup').on('change', function(){
	$('#spinner_cre').show();
});

$('#SupplierEditForm').on('submit', function(){
	var error = 0;
	$('#spinner1').show();
	var name = $('#name').val();
	var address = $('#address').val();
	var pan = $('#pan').val();
	var landline = $('#landline').val();
	var category = $('#category option:selected').val();
	var nperson1 = $('#person1').val();
	var eperson1 = $('#person1email').val();
	var cperson1 = $('#person1contact').val();
	var nperson2 = $('#person2').val();
	var eperson2 = $('#person2email').val();
	var cperson2 = $('#person2contact').val();
	var opening = $('#opening').val();
	if(name==''){
		error = 1;
		$('#name').addClass('errorcolor');
	}
	if(address==''){
		error = 1;
		$('#address').addClass('errorcolor');
	}
	if(pan==''){
		error = 1;
		$('#pan').addClass('errorcolor');
	}
	if(landline==''){
		error = 1;
		$('#landline').addClass('errorcolor');
	}
	if(category==''){
		error = 1;
		$('#category').addClass('errorcolor');
	}
	if(opening==''||opening<0){
		error = 1;
		$('#opening').addClass('errorcolor');
	}
	if(error==0){
		document.SupplierEditForm.submit();
	}else{
		$('#spinner1').hide();
	}
	event.preventDefault();
});
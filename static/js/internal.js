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
	$('#uom').val(uom);
	$('#itemalias').val(alias);
});
$('.edititemm').on('change', function(){
	var vdstr = $(this).attr("id");
	var idstr = $('#'+vdstr+' option:selected').val();
	var name = $('#eini'+idstr).val();
	var uom = $('#eini'+idstr).attr("data");
	var alias = $('#eini'+idstr).attr("name");
	$('#edititem').val(idstr);
	$('#edititemname').val(name);
	$('#edituom').val(uom);
	$('#edititemalias').val(alias);
});

var add = 0;
var itemadd = [];
$('#additembtn').click(function(){
	var error = 0;
	$('#item').focus();
	var item = $('#itemm').val();
	var itemname = $('#itemname').val();
	var alias = $('#itemalias').val();
	var uom = $('#uom').val();
	var qty = $('#qty').val();
	var cval = $('#category option:selected').val();
	var curl = search_url(cval);
	var sval = $('#subcategory'+curl+' option:selected').val();
	var surl = search_url(sval);
	var mainu = curl+''+surl;
	if($('#itemshow'+mainu).length>0){
		var ival = $('#item'+mainu+' option:selected').val();
		if(ival==''){
			error = 1;
			$('#item'+mainu).addClass('errorcolor');
		}else{
			if(item!=ival){
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
	if(itemname == '' || item == '' ){
		error = 1;
		$('#itemm').addClass('errorcolor');
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
		$(".hidden_inputs").append('<input type="hidden" name="itemadd" id="itemad'+add+'" value="'+add+'">');
		$(".hidden_inputs").append('<input type="hidden" name="inameid'+add+'" id="inameid'+add+'" value="'+item+'">');
		$(".hidden_inputs").append('<input type="hidden" name="iname'+add+'" id="iname'+add+'" value="'+itemname+'">');
		$(".hidden_inputs").append('<input type="hidden" name="iuom'+add+'" id="iuom'+add+'" value="'+uom+'">');
		$(".hidden_inputs").append('<input type="hidden" name="iqty'+add+'" id="iqty'+add+'" value="'+qty+'">');
		$(".hidden_inputs").append('<input type="hidden" name="ialias'+add+'" id="ialias'+add+'" value="'+alias+'">');
		$('#itemm').val('');
		$('#itemname').val('');
		$('#uom').val('');
		$('#qty').val('');
		$('.item').val('');
		$('#category').val('');
		$('.subcatshow').hide();
		$('.itemshow').hide();
		$("#ItemTable tbody").append('<tr id="itemrow'+add+'"><td><button type="button" class="edititem" id="eitem'+add+'" data="'+add+'"><i class="far fa-edit"></i></button><button type="button" class="delitem" id="ditem'+add+'" data="'+add+'"><i class="far fa-trash-alt"></i></button></td><td>'+itemname+'('+alias+')</td><td>'+uom+'</td><td>'+qty+'</td></tr>');
		$('.tfoot2').hide();
	}
});

$('#additemeditbtn').click(function(){
	$('#item').focus();
	var itemname = $('#edititemname').val();
	var item = $('#edititem').val();
	var qty = $('#editqty').val();
	var uom = $('#edituom').val();
	var did = $('#dfaultid').val();
	var alias = $('#edititemalias').val();
	var cval = $('#editcategory option:selected').val();
	if(cval!=''){
		var curl = search_url(cval);
		var sval = $('#editsubcategory'+curl+' option:selected').val();
		var surl = search_url(sval);
		var mainu = curl+''+surl;
		if($('#edititemshow'+mainu).length>0){
			var ival = $('#edititem'+mainu+' option:selected').val();
			if(ival==''){
				error = 1;
				$('#edititem'+mainu).addClass('errorcolor');
			}else{
				if(item!=ival){
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
	$('#inameid'+did).val(item);
	$('#iname'+did).val(itemname);
	$('#iuom'+did).val(uom);
	$('#iqty'+did).val(qty);
	$('#ialias'+did).val(alias);
	$('#edititemname').val('');
	$('#edititem').val('');
	$('#editqty').val('');
	$('#edituom').val('');
	$('#edititemalias').val('');
	$('.edititem').val('');
	$('#editcategory').val('');
	$('.editsubcatshow').hide();
	$('.edititemshow').hide();
	$('#itemrow'+did).remove();
	$("#ItemTable tbody").append('<tr id="itemrow'+did+'"><td><button type="button" class="edititem" id="eitem'+did+'" data="'+did+'"><i class="far fa-edit"></i></button><button type="button" class="delitem" id="ditem'+did+'" data="'+did+'"><i class="far fa-trash-alt"></i></button></td><td>'+itemname+'('+alias+')</td><td>'+uom+'</td><td>'+qty+'</td></tr>');
	$('#edit_popup1').css({"transform": "scale(.1)", "-webkit-transform": "scale(.1)", "-moz-transform": "scale(.1)"});
	$('.edit_popupbanner1').fadeOut();

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
	var alias = $('#ialias'+idstr).val();
	$('#edititem').val(itemid);
	$('#edititemname').val(name);
	$('#edituom').val(uom);
	$('#editqty').val(qty);
	$('#edititemalias').val(alias);
	$('#dfaultid').val(idstr);
});

$(document).on('click', '.delitem', function(){
	var idstr = $(this).attr("data");
	$('#itemad'+idstr).remove();
	$('#iname'+idstr).remove();
	$('#inameid'+idstr).remove();
	$('#iqty'+idstr).remove();
	$('#iuom'+idstr).remove();
	$('#ialias'+idstr).remove();
	itemadd = $.grep(itemadd, function(value) {
		return value != idstr;
	});
	$('#itemrow'+idstr).remove();
	if (itemadd.length === 0) {
		$('.tfoot2').show();
	    
	}
	
});

$('#MaterialIssueForm').on('submit', function(){
	var error = 0;
	$('#spinner1').show();
	var date = $('input[name=date]').val();
	var issue_locate = $('input[name=issue_locate]').val();
	var receive_locate = $('input[name=receive_locate]').val();
	if(date==''){
		error = 1;
		$('#date').addClass('errorcolor');
	}
	if(issue_locate==''){
		error = 1;
		$('#issue_locate').addClass('errorcolor');
	}
	if(receive_locate==''){
		error = 1;
		$('#receive_locate').addClass('errorcolor');
	}
	if(itemadd.length === 0) {
		error = 1;
	    $('.goods').addClass('errorcolor');
	}
	if(error==0){
		document.MaterialIssueForm.submit();
	}else{
		$('#spinner1').hide();
	}
	event.preventDefault();
});
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
	$('.already_error').hide();
});
$('.goods').click(function(){
	$(this).removeClass('errorcolor');
});

var add = 0;
var rec = 0;
var itemadd = [];
var diserror = 0;
$('#pvn').on('keypress',function(e){
	if(e.which===13){
		diserror = 0;
		$('.goods').removeClass('errorcolor');
		$('.loading').slideDown();
		$('#pvn').removeClass('errorcolor');
		var val = $('#pvn').val();
		val = val.toUpperCase();
		if($('.grd'+val).length == 0){
			if($('.gooid'+val).length > 0){
				rec = rec + 1;
				var rus = val+rec;
				$('.gooid'+val).each(function(){
					var cha = $(this).val();
					var item = $('#item'+cha).val();
					var itemid = $('#itemid'+cha). val();
					var uom = $('#uom'+cha). val();
					var qty = $('#qty'+cha). val();
					var alias = $('#alias'+cha). val();

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
					$('.tfoot2').hide();
					$("#ItemTable tbody").append('<tr id="itemrow'+us+'"><td>'+item+'('+alias+')</td><td>'+uom+'</td><td>'+qty+'</td></tr>');
					$('.tfoot').show();
					$('#pvn').val('');
					$('#pvn').focus();
				});
				$(".grncol").append('<div class="coldiv grd'+val+'" id="colrec'+rus+'"><span class="coldes">'+val+'</span><button type="button" class="colbtn" data="'+rus+'"><i class="fa fa-times"></i></button></div>');

			}else{
				$('#pvn').addClass('errorcolor');
			}
		}else{
			$('#pvn').addClass('errorcolor');
		}
		$('.loading').slideUp();
	}
});

$(document).on('click', '.colbtn', function(e){
	var idstr = $(this).attr("data");
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

		itemadd = $.grep(itemadd, function(value) {
			return value != hac;
		});
		$('#itemrow'+cha).remove();
	});
	if(itemadd.length === 0){
		$('#colrec'+idstr).remove();
		$('tfoot').hide();
		$('.tfoot2').show();
	}
	$('.loading').slideUp();

});

$('#GoodsForm').on('submit', function(){
	var error = 0;
	$('#spinner1').show();
	var date = $('input[name=date]').val();
	var grn = $('input[name=grn]').val();
	var vehicle = $('#vehicle').val();
	if(date==''){
		error = 1;
		$('#date').addClass('errorcolor');
	}
	if(grn==''){
		error = 1;
		$('#grn').addClass('errorcolor');
	}
	if(itemadd.length === 0) {
		error = 1;
	    $('.goods').addClass('errorcolor');
	}
	if(error==0){
		document.GoodsForm.submit();
	}else{
		$('#spinner1').hide();
	}
	event.preventDefault();
});
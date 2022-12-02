$('#perop').addClass('btnclass');

$('#mainad').addClass('btnclass');
$('#mainadop').show();

$('#notimainad').addClass('btnclass');
$('#mainadnoti').show();

$('#perop').click(function(){
	$(this).addClass('btnclass');
	$('#pernoti').removeClass('btnclass');
	$('#notify_permit').hide();
	$('#operation_permit').show();
});
$('#pernoti').click(function(){
	$(this).addClass('btnclass');
	$('#perop').removeClass('btnclass');
	$('#operation_permit').hide();
	$('#notify_permit').show();
});

$('#mainad').click(function(){
	$('.uoperbtn').removeClass('btnclass');
	$(this).addClass('btnclass');
	$('#mainstop').hide();
	$('#siteadop').hide();
	$('#sitestop').hide();
	$('#mainadop').show();
});
$('#mainst').click(function(){
	$('.uoperbtn').removeClass('btnclass');
	$(this).addClass('btnclass');
	$('#mainstop').show();
	$('#siteadop').hide();
	$('#sitestop').hide();
	$('#mainadop').hide();
});
$('#sitead').click(function(){
	$('.uoperbtn').removeClass('btnclass');
	$(this).addClass('btnclass');
	$('#mainstop').hide();
	$('#siteadop').show();
	$('#sitestop').hide();
	$('#mainadop').hide();
});
$('#sitest').click(function(){
	$('.uoperbtn').removeClass('btnclass');
	$(this).addClass('btnclass');
	$('#mainstop').hide();
	$('#siteadop').hide();
	$('#sitestop').show();
	$('#mainadop').hide();
});

$('#notimainad').click(function(){
	$('.unperbtn').removeClass('btnclass');
	$(this).addClass('btnclass');
	$('#mainstnoti').hide();
	$('#siteadnoti').hide();
	$('#sitestnoti').hide();
	$('#mainadnoti').show();
});
$('#notimainst').click(function(){
	$('.unperbtn').removeClass('btnclass');
	$(this).addClass('btnclass');
	$('#mainstnoti').show();
	$('#siteadnoti').hide();
	$('#sitestnoti').hide();
	$('#mainadnoti').hide();
});
$('#notisitead').click(function(){
	$('.unperbtn').removeClass('btnclass');
	$(this).addClass('btnclass');
	$('#mainstnoti').hide();
	$('#siteadnoti').show();
	$('#sitestnoti').hide();
	$('#mainadnoti').hide();
});
$('#notisitest').click(function(){
	$('.unperbtn').removeClass('btnclass');
	$(this).addClass('btnclass');
	$('#mainstnoti').hide();
	$('#siteadnoti').hide();
	$('#sitestnoti').show();
	$('#mainadnoti').hide();
});

$('.cngpermission').on('change', function(){
	var idstr = $(this).attr("data");
	var user = $(this).attr("name");
	// $('.pro_ban').show('slide', {direction: 'right'}, 200);
	if($(this).prop("checked") == true){
		status = 'yes';
	}else{
		status = 'no';
	}
	var formData = {
		'pid': idstr,
		'status': status,
		'user': user,
		'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
	}
	$.ajax({
		type: 'POST',
		url: '/account/update-operation-permission/',
		data: formData,
		encode: true
	})
	.done(function(data) {
		// $('.pro_ban').hide();
		// setTimeout(function(){
		// 	$('.success_ban').show('slide', {direction: 'right'}, 200);
		// },1000);
		// setTimeout(function(){
		// 	$('.success_ban').hide('slide', {direction: 'right'}, 200);
		// }, 3000);

	});
});

$('.cngnotify').on('change', function(){
	var idstr = $(this).attr("data");
	var user = $(this).attr("name");
	// $('.pro_ban').show('slide', {direction: 'right'}, 200);
	if($(this).prop("checked") == true){
		status = 'yes';
	}else{
		status = 'no';
	}
	var formData = {
		'pid': idstr,
		'status': status,
		'user': user,
		'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
	}
	$.ajax({
		type: 'POST',
		url: '/account/update-notify-permission/',
		data: formData,
		encode: true
	})
	.done(function(data) {
		// $('.pro_ban').hide();
		// setTimeout(function(){
		// 	$('.success_ban').show('slide', {direction: 'right'}, 200);
		// },1000);
		// setTimeout(function(){
		// 	$('.success_ban').hide('slide', {direction: 'right'}, 200);
		// }, 3000);

	});
});
window.addEventListener( "pageshow", function ( event ) {
  var historyTraversal = event.persisted ||
                         ( typeof window.performance != "undefined" &&
                              window.performance.navigation.type === 2 );
  if ( historyTraversal ) {
    // Handle page restore.
    window.location.reload();
  }
});
$(document).on("wheel", "input[type=number]", function (e) {
    $(this).blur();
});

$('.dropdown-menu').on('click', function (e) {
   e.stopPropagation();
 });

$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})

setInterval(
function(){
  $('#badge2').load('/noti-count/');
}, 1000);

$('#notify-dropdown').on('click', function(){
  $('#notification_dropdown').load("/noti/");
});

var nav = $('nav').height();
$('.content').css({"margin-top": nav+"px"});

let sidebar = document.querySelector(".sidebar");
let closeBtn = document.querySelector("#btn");
let collapse = document.querySelector("#collapse");
let searchBtn = document.querySelector("#search");

closeBtn.addEventListener("click", ()=>{
  sidebar.classList.toggle("open");
  menuBtnChange();//calling the function(optional)
});
collapse.addEventListener("click", ()=>{
  sidebar.classList.toggle("open");
  menuBtnChange();//calling the function(optional)
});

searchBtn.addEventListener("click", ()=>{ // Sidebar open when you click on the search iocn
  sidebar.classList.toggle("open");
  menuBtnChange(); //calling the function(optional)
});

// following are the code to change sidebar button(optional)
function menuBtnChange() {
 if(sidebar.classList.contains("open")){
   closeBtn.classList.replace("bx-menu", "bx-menu-alt-right");//replacing the iocns class
 }else {
   closeBtn.classList.replace("bx-menu-alt-right","bx-menu");//replacing the iocns class
 }
}
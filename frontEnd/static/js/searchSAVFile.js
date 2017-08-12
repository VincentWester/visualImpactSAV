var show_per_page = 10;
var current_page = 0;

function set_display(first, last) {
  $('#results').children().css('display', 'none');
  $('#page_navigation').css('display', 'inline');
  $('#results').children().slice(first, last).css('display', 'block');
}

function previous(){
    if($('.active').prev('.page_link').length) go_to_page(current_page - 1);
}

function next(){
    if($('.active').next('.page_link').length) go_to_page(current_page + 1);
}

function go_to_page(page_num){
  current_page = page_num;
  start_from = current_page * show_per_page;
  end_on = start_from + show_per_page;
  set_display(start_from, end_on);
  $('#page_navigation .active').removeClass('active');
  $('#id' + page_num).addClass('active');
} 

$(document).ready(function() {

  var number_of_pages = Math.ceil($('.reference-file').size() / show_per_page);
   
  var nav = ''
  if (number_of_pages > 1) {
    nav = '<ul class="pagination" style="margin-left : 325px;"><li><a href="javascript:previous();"> << </a></li>';
    var i = -1;
    while(number_of_pages > ++i){
      nav += '<li class="page_link'
      if(!i) nav += ' active';
      nav += '" id="id' + i +'">';
      nav += '<a href="javascript:go_to_page(' + i +')">'+ (i + 1) +'</a></li>';
    }
    nav += '<li><a href="javascript:next();"> >> </a></li></ul>';
  } 

  $('#page_navigation').html(nav);
  set_display(0, show_per_page);
   
});
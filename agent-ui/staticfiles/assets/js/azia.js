$(function(){
  'use strict'

  // This template is mobile first so active menu in navbar
  // has submenu displayed by default but not in desktop
  // so the code below will hide the active menu if it's in desktop
  if(window.matchMedia('(min-width: 992px)').matches) {
    $('.kt-navbar .active').removeClass('show');
    $('.kt-header-menu .active').removeClass('show');
  }

  // Shows header dropdown while hiding others
  $('.kt-header .dropdown > a').on('click', function(e) {
    e.preventDefault();
    $(this).parent().toggleClass('show');
    $(this).parent().siblings().removeClass('show');
  });

  // Showing submenu in navbar while hiding previous open submenu
  $('.kt-navbar .with-sub').on('click', function(e) {
    e.preventDefault();
    $(this).parent().toggleClass('show');
    $(this).parent().siblings().removeClass('show');
  });

  // this will hide dropdown menu from open in mobile
  $('.dropdown-menu .kt-header-arrow').on('click', function(e){
    e.preventDefault();
    $(this).closest('.dropdown').removeClass('show');
  });

  // this will show navbar in left for mobile only
  $('#azNavShow, #azNavbarShow').on('click', function(e){
    e.preventDefault();
    $('body').addClass('kt-navbar-show');
  });

  // this will hide currently open content of page
  // only works for mobile
  $('#azContentLeftShow').on('click touch', function(e){
    e.preventDefault();
    $('body').addClass('kt-content-left-show');
  });

  // This will hide left content from showing up in mobile only
  $('#azContentLeftHide').on('click touch', function(e){
    e.preventDefault();
    $('body').removeClass('kt-content-left-show');
  });

  // this will hide content body from showing up in mobile only
  $('#azContentBodyHide').on('click touch', function(e){
    e.preventDefault();
    $('body').removeClass('kt-content-body-show');
  })

  // navbar backdrop for mobile only
  $('body').append('<div class="kt-navbar-backdrop"></div>');
  $('.kt-navbar-backdrop').on('click touchstart', function(){
    $('body').removeClass('kt-navbar-show');
  });

  // Close dropdown menu of header menu
  $(document).on('click touchstart', function(e){
    e.stopPropagation();

    // closing of dropdown menu in header when clicking outside of it
    var dropTarg = $(e.target).closest('.kt-header .dropdown').length;
    if(!dropTarg) {
      $('.kt-header .dropdown').removeClass('show');
    }

    // closing nav sub menu of header when clicking outside of it
    if(window.matchMedia('(min-width: 992px)').matches) {

      // Navbar
      var navTarg = $(e.target).closest('.kt-navbar .nav-item').length;
      if(!navTarg) {
        $('.kt-navbar .show').removeClass('show');
      }

      // Header Menu
      var menuTarg = $(e.target).closest('.kt-header-menu .nav-item').length;
      if(!menuTarg) {
        $('.kt-header-menu .show').removeClass('show');
      }

      if($(e.target).hasClass('kt-menu-sub-mega')) {
        $('.kt-header-menu .show').removeClass('show');
      }

    } else {

      //
      if(!$(e.target).closest('#azMenuShow').length) {
        var hm = $(e.target).closest('.kt-header-menu').length;
        if(!hm) {
          $('body').removeClass('kt-header-menu-show');
        }
      }
    }

  });

  $('#azMenuShow').on('click', function(e){
    e.preventDefault();
    $('body').toggleClass('kt-header-menu-show');
  })

  $('.kt-header-menu .with-sub').on('click', function(e){
    e.preventDefault();
    $(this).parent().toggleClass('show');
    $(this).parent().siblings().removeClass('show');
  })

  $('.kt-header-menu-header .close').on('click', function(e){
    e.preventDefault();
    $('body').removeClass('kt-header-menu-show');
  })

});

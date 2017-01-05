'use strict';

/* global Prism:true */

(function () {
  Prism.plugins.NormalizeWhitespace.setDefaults({
    'remove-trailing': true,
    'remove-indent': true,
    'left-trim': true,
    'right-trim': true,
    'indent': 0,
    'remove-initial-line-feed': false,
    'tabs-to-spaces': 1
  });

  var $nav = void 0,
      $header = void 0;
  var scrollHandler = function scrollHandler() {
    if (window.scrollY > $header[0].scrollHeight) {
      $nav.addClass('is-fixed');
    } else {
      $nav.removeClass('is-fixed');
    }
  };

  $(window).on('scroll', function (e) {
    window.requestAnimationFrame(scrollHandler);
  });

  $(function () {
    $nav = $('#ptn-nav');
    $header = $('#ptn-header');
  });
})();
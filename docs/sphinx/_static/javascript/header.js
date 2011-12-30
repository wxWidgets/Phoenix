/*
 * header.js
 * ~~~~~~~~~
 *
 * This script fixes a problem with internal links caused by a fixed header.
 *
 * Contributed for the TurboGears docs theme by Christoph Zwerschke.
 *
 * :copyright: Copyright 2010 by by Christoph Zwerschke.
 * :license: BSD, see LICENSE for details.
 *
 */

$(function() {
  if ($('div.related').css('position') != 'fixed')
    return;
  var header_height = $('div.related').height();
  if (!header_height)
    return;
  var current_hash = null;

  function on_hash_change() {
    if (current_hash.length < 2 || current_hash.substr(0, 1) != '#')
      return;
    hash_element = $(document.getElementById && 0 ?
      document.getElementById(current_hash.substr(1)) :
      current_hash.replace(/[;&,.+*~':"!\^$\[\]()=>|\/@\\]/g,'\\$&'));
    if (!hash_element.length)
      return;
    if (hash_element.offset().top - $(window).scrollTop() < header_height)
      window.scrollBy(0, -header_height);
   }

  function check_hash_change() {
    if (document.location.hash != current_hash) {
      current_hash = document.location.hash;
      if (current_hash)
          window.setTimeout(on_hash_change, 100);
    }
  }

  check_hash_change();
  if ('onhashchange' in window)
    $(window).bind('hashchange', check_hash_change);
  else
    $(window).scroll(check_hash_change);

  /* remove CSS trick for fixing the header problem */
  $('div.headerfix').removeClass('headerfix');
});

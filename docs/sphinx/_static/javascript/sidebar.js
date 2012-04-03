/*
 * sidebar.js
 * ~~~~~~~~~~
 *
 * This script makes the Sphinx sidebar collapsible and moveable.
 *
 * .sphinxsidebar contains .sphinxsidebarwrapper.  The script adds
 * in .sphixsidebar, after .sphinxsidebarwrapper, the #sidebarbutton
 * used to collapse, expand and move the sidebar.
 *
 * The script saves per-browser/per-session cookies used to remember
 * the collapsed state and position of the sidebar among the pages.
 * Once the browser is closed the cookies are deleted and the position
 * reset to the default set in the style sheed.
 *
 * Modifications and improvements made 2010 by Christoph Zwerschke.
 *
 * :copyright: Copyright 2007-2010 by the Sphinx team, see AUTHORS.
 * :license: BSD, see LICENSE for details.
 *
 */

$(function() {
  var body = $('div.document');
  var body_width = body.width();
  var footer = $('div.footer');
  var sidebar = $('div.sphinxsidebar');
  var sidebarwrapper = $('div.sphinxsidebarwrapper');
  var sidebarbutton = $('<div id="sidebarbutton"><div></div></div>');
  var sbw_width = sidebar.width();
  var sbb_width = 9;
  var dark_color = 'darkgrey';
  var light_color = sidebarwrapper.css('color');
  var opacity_factor = $.browser.msie ? 1 : 0.75;
  var collapsed = sidebarwrapper.is(':not(:visible)');
  var rightside = sidebar.css('right') == '0px';
  var dragging = null;

  function set_sidebar() {
    var width = collapsed ? 0 : sbw_width;
    if (rightside) {
      sidebar.css({
        'width': width,
        'left': 'auto',
        'right': 0
      });
      sidebarbutton.css({
        'right': collapsed ? 0 : width,
        'left': 'auto'
      });
      body.add(footer).css({
        'margin-right': width + sbb_width,
        'margin-left': 0
      });
    } else {
      sidebar.css({
        'width': width,
        'right': 'auto',
        'left': '0'
      });
      sidebarbutton.css({
        'left': collapsed ? 0 : width,
        'right': 'auto'
      });
      body.add(footer).css({
        'margin-left': width + sbb_width,
        'margin-right': 0
      });
    }
    sidebarbutton.find('div').text(rightside == collapsed ? '«' : '»');
  }

  function toggle_sidebar() {
    collapsed ? expand_sidebar() : collapse_sidebar();
  }

  function collapse_sidebar() {
    collapsed = true;
    sidebarwrapper.hide();
    set_sidebar();
    sidebarbutton.attr('title', _('Expand sidebar'));
    document.cookie = 'sidebar_collapsed=1';
  }

  function expand_sidebar() {
    collapsed = false;
    sidebarwrapper.show();
    set_sidebar();
    sidebarbutton.attr('title', _('Collapse sidebar'));
    document.cookie = 'sidebar_collapsed=0';
  }

  function add_sidebar_button() {
    sidebar.css('width', (collapsed ? 0 : sbw_width) + sbb_width);
    sidebarbutton.attr('title', _('Collapse sidebar'));
    sidebarbutton.css({
        'color': light_color,
        'font-size': 14,
        'text-align': 'center',
        'border-left': '1px solid ' + 'white',
        'border-right': '1px solid ' + 'white',
        'padding': '1px 0',
        'margin': '0',
        'width': sbb_width - 2,
        'cursor': 'pointer',
        'position': 'fixed',
        'left': collapsed ? 0 : sbw_width,
        'top': sidebar.css('top'),
        'bottom': 0
    });
    sidebarbutton.find('div').css({
       'position': 'relative',
       'top': '50%',
       'margin-top': -8
    });
    set_sidebar();
    sidebarbutton.hover(
      function() {
          sidebarbutton.css('background-color', dark_color);
      },
      function() {
          sidebarbutton.css('background-color', light_color);
      }
    );
    sidebarbutton.mousedown(
      function(e) {
          if (dragging != null || e.which != 1) return;
          dragging = {
            'dragged': false,
            'pageX': e.pageX
          };
          sidebarbutton.css('cursor', 'move');
      }
    );
    sidebar.add(body).mouseup(
      function(e) {
        if (dragging == null)
          return;
        e.preventDefault();
        if (dragging.dragged) {
          var left = sidebar.offset().left;
          if (rightside)
            left = body_width - left;
          if (left < 0 && !collapsed)
            collapse_sidebar();
          else if (left < body_width / 2 &&
              left < sbw_width + 2 * sbw_width && collapsed)
            expand_sidebar();
          else {
            if (left > body_width / 2)
              rightside = !rightside;
            set_sidebar();
          }
          if (opacity_factor != 1)
            sidebar.css('opacity', dragging.opacity);
          document.cookie = 'sidebar_rightside=' + (rightside ? '1' : '0');
        } else
          toggle_sidebar();
        sidebarbutton.css('cursor', 'pointer');
        dragging = null;
        e.stopPropagation();
      }
    );
    sidebar.add(body).mousemove(
      function(e) {
        if (dragging == null)
          return;
        e.preventDefault();
        var pageX = e.pageX;
        side = 'left';
        sidebarbutton.css('left', pageX);
        if (rightside)
          pageX += sbb_width;
        else
          pageX -= sbw_width;
        sidebar.css('left', pageX);
        if (!dragging.dragged) {
          dragging.dragged = true;
          if (collapsed) {
            sidebar.css('width', sbw_width);
            sidebarwrapper.show();
          }
          if (opacity_factor != 1) {
            dragging.opacity = sidebar.css('opacity');
            sidebar.css('opacity', opacity_factor * dragging.opacity);
          }
        }
        e.stopPropagation();
      }
    );
    sidebar.append(sidebarbutton);
    light_color = sidebarbutton.css('background-color');
  }

  function set_position_from_cookie() {
    if (!document.cookie)
      return;
    var items = document.cookie.split(';');
    for (var k = 0; k < items.length; k++) {
      var key_val = items[k].split('=');
      var key = $.trim(key_val[0]);
      var val = $.trim(key_val[1]);
      if (key == 'sidebar_collapsed')
        collapsed = val == '1';
      else if (key == 'sidebar_rightside')
        rightside = val == '1';
    }
  }

  set_position_from_cookie();
  if (sidebar.length)
    add_sidebar_button();
});

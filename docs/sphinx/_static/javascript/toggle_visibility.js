/*
 * toggle_visibility.js
 * --------------------
 *
 * These functions enable the user to toggle the visibility of a block of
 * the document, which is delimited by a <div> tag with an expected id
 * attribute.  The magic happens via using the id of the object passed to
 * toggle visibility to make the id's used to find the other elements that
 * will be operated upon.
 */

function hasClass(ele,cls) {
    return ele.className.match(new RegExp('(\\s|^)'+cls+'(\\s|$)'));
}

function addClass(ele,cls) {
    if (!this.hasClass(ele,cls)) ele.className += " "+cls;
}

function removeClass(ele,cls) {
    if (hasClass(ele,cls)) {
        var reg = new RegExp('(\\s|^)'+cls+'(\\s|$)');
        ele.className=ele.className.replace(reg,' ');
    }
}

function toggleVisibility(linkObj) {
    var base = linkObj.getAttribute('id');
    var summary = document.getElementById(base + '-summary');
    var content = document.getElementById(base + '-content');
    var trigger = document.getElementById(base + '-trigger');
    var cookieName = base + '-savedState'
    if ( hasClass(linkObj,'closed') ) {
        summary.style.display = 'none';
        content.style.display = 'block';
        trigger.src = '_static/images/open.png';
        removeClass(linkObj,'closed');
        addClass(linkObj,'opened');
        $.cookie(cookieName, 'opened');
    } else if ( hasClass(linkObj,'opened') ) {
        summary.style.display = 'block';
        content.style.display = 'none';
        trigger.src = '_static/images/closed.png';
        removeClass(linkObj,'opened');
        addClass(linkObj,'closed');
        $.cookie(cookieName, 'closed');
    }
    return false;
}


function toggleVisibilityOnLoad(linkObj) {
    var base = linkObj.getAttribute('id');
    var cookieName = base + '-savedState'
    var state = $.cookie(cookieName);
    if ( state == 'opened' ) {
        toggleVisibility(linkObj);
    }
}


/*
 * inheritancetoggle.js
 * --------------------
 *
 * These functions enable the user to toggle the visibility of a block of
 * the document, which is delimited by a <div> tag with an expected id
 * attribute.
 */

const initialiseCollapsible = () => {
  // global elements used by the functions.
  const coll_checkbox = document.getElementById("collapsible-inheritance")
  const coll_label = document.getElementsByClassName("collapsible-label")[0]
  
  // exit early if the document has no collapsible for some reason
  if (typeof coll_checkbox === "undefined") {
    return
  }

  const hide_collapsible = () => {
    coll_checkbox.checked = false
    coll_label.title = _("Show inheritance diagram")
    window.localStorage.setItem("inheritance", "hidden")
  }

  const show_collapsible = () => {
    coll_checkbox.checked = true
    coll_label.title = _("Hide inheritance diagram")
    window.localStorage.setItem("inheritance", "visible")
  }

  coll_checkbox.addEventListener("change", () => {
    (coll_checkbox.checked === true) ? show_collapsible() : hide_collapsible()
  })

  const coll_state = window.localStorage.getItem("inheritance")
  if (coll_state === "hidden") {
    hide_collapsible()
  }
  else if (coll_state === "visible") {
    show_collapsible()
  }
}

if (document.readyState !== "loading") {
  initialiseCollapsible()
}
else {
  document.addEventListener("DOMContentLoaded", initialiseCollapsible)
}

let inheritanceLabels = document.querySelectorAll('.collapsible-label');

Array.from(inheritanceLabels).forEach(label => {
  label.addEventListener('keydown', e => {
    // 32 === spacebar
    // 13 === enter
    if (e.which === 32 || e.which === 13) {
      e.preventDefault();
      label.click();
    };
  });
});


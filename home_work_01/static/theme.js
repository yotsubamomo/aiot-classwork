/* Light / dark theme switch (WI-UI-THEME-1).
 *
 * Loaded synchronously in <head>, before the stylesheet is applied, so a saved
 * choice is set on <html data-theme="…"> before the first paint (no flash of the
 * other theme). Without a saved choice the page follows the system setting
 * (styles.css `prefers-color-scheme`), exactly as before. The "Dark mode" button
 * (#theme-toggle, aria-pressed) switches between the two and keeps the choice in
 * this browser only (localStorage; nothing is sent anywhere). Storage can be
 * unavailable (private mode, blocked site data) — then the switch still works for
 * the current page and nothing is remembered.
 *
 * The Taiwan Map card is dark in both themes (P-1); only the page tokens change.
 */
(function () {
  "use strict";

  var KEY = "hw01-theme";
  var root = document.documentElement;
  var media = window.matchMedia ? window.matchMedia("(prefers-color-scheme: dark)") : null;

  function stored() {
    try {
      var value = window.localStorage.getItem(KEY);
      return value === "dark" || value === "light" ? value : null;
    } catch (e) {
      return null;
    }
  }

  function effective() {
    return root.getAttribute("data-theme") || (media && media.matches ? "dark" : "light");
  }

  var saved = stored();
  if (saved) root.setAttribute("data-theme", saved);

  function sync(button) {
    button.setAttribute("aria-pressed", effective() === "dark" ? "true" : "false");
  }

  document.addEventListener("DOMContentLoaded", function () {
    var button = document.getElementById("theme-toggle");
    if (!button) return;
    sync(button);
    button.addEventListener("click", function () {
      var next = effective() === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      try {
        window.localStorage.setItem(KEY, next);
      } catch (e) {
        /* not remembered; the page still switches */
      }
      sync(button);
    });
    // Following the system (no saved choice): keep the pressed state in step
    // when the system setting changes while the page is open.
    if (media) {
      var onChange = function () { sync(button); };
      if (media.addEventListener) media.addEventListener("change", onChange);
      else if (media.addListener) media.addListener(onChange);
    }
  });
})();

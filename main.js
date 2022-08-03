/*!
 * jQuery JavaScript Library v1.5.2
 * http://jquery.com/
 *
 * Copyright 2011, John Resig
 * Dual licensed under the MIT or GPL Version 2 licenses.
 * http://jquery.org/license
 *
 * Includes Sizzle.js
 * http://sizzlejs.com/
 * Copyright 2011, The Dojo Foundation
 * Released under the MIT, BSD, and GPL Licenses.
 *
 * Date: Thu Mar 31 15:28:23 2011 -0400
 */


function copy(id) {
  var copyText = document.getElementById(id);

  /* Copy the text inside the text field */
  navigator.clipboard.writeText(copyText.innerText);

  var tip = document.getElementById(id+'tip');
  tip.style.transition = "all 0.5"
  tip.style.backgroundColor = 'rgb(23, 255, 100)';
  tip.innerHTML = 'Text copied successfully';
  setTimeout(function() {
  tip.style.backgroundColor = '#555';
  tip.innerHTML = 'Click to copy';
}, 1500);
}


console.log("Good")










/*
mail: gigachads_@outlook.com
pw: Srgwmgcf5
*/
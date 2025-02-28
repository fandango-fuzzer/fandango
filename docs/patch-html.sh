#!/bin/sh
# Patch generated HTML output

patch -c -N _build/html/_static/copybutton.js <<EOF
*** _build/html/_static/copybutton-orig.js	Fri Feb 28 22:16:14 2025
--- _build/html/_static/copybutton.js	Fri Feb 28 22:16:56 2025
***************
*** 216,221 ****
--- 216,227 ----
      if (textContent.endsWith("\n")) {
          textContent = textContent.slice(0, -1)
      }
+
+     // EXTRA: Get rid of '$ ' prompt
+     if (textContent.startsWith("$ ")) {
+         textContent = textContent.slice(2)
+     }
+
      return textContent
  }

EOF

rm -f _build/html/_static/copybutton.js.*

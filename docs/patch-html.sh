#!/bin/sh
# Patch generated HTML output

# Do not copy the prompt when copying code blocks
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

for file in _build/html/[A-Z]*.html; do
# Some sh variants also match lowercase files, so we filter them out
echo $file | grep '/[A-Z]*.html' >/dev/null || continue
# Patch the file to change the PDF download button
patch -c -N $file <<EOF
***************
*** 340,348 ****
        
        
        <li>
! <button onclick="window.print()"
    class="btn btn-sm btn-download-pdf-button dropdown-item"
!   title="Print to PDF"
    data-bs-placement="left" data-bs-toggle="tooltip"
  >
    
--- 340,348 ----
        
        
        <li>
! <a href="_static/fandango.pdf" target="_blank"
    class="btn btn-sm btn-download-pdf-button dropdown-item"
!   title="Download PDF"
    data-bs-placement="left" data-bs-toggle="tooltip"
  >
    
***************
*** 351,357 ****
    <i class="fas fa-file-pdf"></i>
    </span>
  <span class="btn__text-container">.pdf</span>
! </button>
  </li>
        
    </ul>
--- 351,357 ----
    <i class="fas fa-file-pdf"></i>
    </span>
  <span class="btn__text-container">.pdf</span>
! </a>
  </li>
        
    </ul>

EOF
done
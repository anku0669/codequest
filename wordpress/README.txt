⚡ Ironyx Code — WordPress upload package
=========================================

WHAT'S HERE
  ironyx-code/        ← the whole static app (upload THIS folder to your site)
  embed-example.html  ← open in a browser to preview the iframe embed

QUICK STEPS
  1. Upload the "ironyx-code" folder to your WordPress site, e.g.:
        wp-content/uploads/ironyx-code/
     (use cPanel File Manager or FTP)

  2. Add a "Custom HTML" block to any page and paste:

        <iframe
          src="/wp-content/uploads/ironyx-code/index.html"
          title="Ironyx Code"
          style="width:100%;height:90vh;border:0;border-radius:12px;"
          loading="lazy"
          allow="clipboard-write"></iframe>

  3. Publish. Done!

NOTES
  • No Node server, database, or API key needed.
  • Python / JavaScript / TypeScript run in the visitor's browser.
  • Other languages run via the free public Wandbox engine (needs internet).
  • Serve your site over HTTPS to avoid mixed-content blocks.
  • Don't rename the css/, js/, or data/ folders.

Full guide: see WORDPRESS.md in the main package.

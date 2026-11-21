# jitlegal.github.io

Public pages for JIT Legal, served at https://jitlegal.github.io. Product code lives in private
repositories; only small public pages (home, product pages, privacy policies) live here.

| Path | Page |
| --- | --- |
| `/` | JIT Legal home |
| `/leadfeed/` | Lead Feed product page |
| `/leadfeed/privacy.html` | Lead Feed privacy policy (linked from the Google OAuth consent screen) |

Add a product by creating `site/<product>/` with its own `index.html` and `privacy.html`, and list
it on the home page. Everything under `site/` is published by `.github/workflows/pages.yml` after
a secret scan and a broken-link check; pull requests run the checks without publishing.

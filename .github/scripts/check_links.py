"""Fail if any internal link or #fragment in site/ points nowhere (stdlib only, offline)."""
import pathlib
import sys
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "site").resolve()


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.ids = [], set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if tag == "a" and a.get("name"):
            self.ids.add(a["name"])
        for key in ("href", "src"):
            if a.get(key):
                self.links.append(a[key])


def parse(path):
    p = Page()
    p.feed(path.read_text(encoding="utf-8"))
    return p


def target(page, url):
    parts = urlsplit(url)
    if parts.scheme or parts.netloc:  # external: not checked offline
        return None, None
    path = unquote(parts.path)
    if not path:
        dest = page
    elif path.startswith("/"):
        dest = ROOT / path.lstrip("/")
    else:
        dest = page.parent / path
    if dest.is_dir() or path.endswith("/"):
        dest = dest / "index.html"
    return dest.resolve(), parts.fragment


pages = sorted(ROOT.rglob("*.html"))
cache, errors = {}, []
for page in pages:
    for url in parse(page).links:
        dest, frag = target(page, url)
        if dest is None:
            continue
        rel = page.relative_to(ROOT)
        if ROOT not in dest.parents or not dest.is_file():
            errors.append(f"{rel}: {url} -> missing")
        elif frag and dest.suffix == ".html":
            ids = cache.setdefault(dest, parse(dest).ids)
            if frag not in ids:
                errors.append(f"{rel}: {url} -> no #{frag}")

print(f"{len(pages)} pages checked")
for e in errors:
    print("BROKEN", e)
sys.exit(1 if errors else 0)

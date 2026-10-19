from html.parser import HTMLParser
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
HTML_FILE = ROOT / "site" / "index.html"
assert HTML_FILE.is_file(), "site/index.html is missing"
html = HTML_FILE.read_text(encoding="utf-8")

class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.scripts = []
        self.in_script = False
        self.script_parts = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "script" and not attrs.get("src"):
            self.in_script = True
            self.script_parts = []

    def handle_data(self, data):
        if self.in_script:
            self.script_parts.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self.in_script:
            self.scripts.append("".join(self.script_parts))
            self.in_script = False

parser = SiteParser()
parser.feed(html)
parser.close()

assert "SolarDraft" in html, "SolarDraft branding is missing"
for element_id in ("generate", "drawing", "download", "validation", "system", "strings", "modules"):
    assert f'id="{element_id}"' in html, f"Required element #{element_id} is missing"
assert len(parser.ids) == len(set(parser.ids)), "Duplicate HTML id attributes found"
assert parser.scripts, "No inline JavaScript found"

for i, script in enumerate(parser.scripts):
    with tempfile.NamedTemporaryFile("w", suffix=".js", encoding="utf-8", delete=False) as f:
        f.write(script)
        js_path = Path(f.name)
    try:
        result = subprocess.run(["node", "--check", str(js_path)], text=True, capture_output=True)
        if result.returncode:
            raise AssertionError(f"JavaScript syntax check failed for inline script {i + 1}:\n{result.stderr}")
    finally:
        js_path.unlink(missing_ok=True)

print("PASS: SolarDraft HTML structure and required controls")
print(f"PASS: {len(parser.ids)} unique element IDs")
print(f"PASS: {len(parser.scripts)} inline JavaScript block(s) passed node --check")

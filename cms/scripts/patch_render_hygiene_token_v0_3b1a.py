from pathlib import Path
import re

path = Path("scripts/validation/validate_readme_render_hygiene_v0_2b2.py")
text = path.read_text(encoding="utf-8", errors="replace")
text = text.replace("CMS--SA-v0.3b11", "CMS--SA-v0.3b1a")
text = text.replace("v0.3b11", "v0.3b1a")
text = re.sub(r"CMS--SA-v0\.3b1(?!a)\b", "CMS--SA-v0.3b1a", text)
text = re.sub(r"v0\.3b1(?!a)\b", "v0.3b1a", text)
text = re.sub(r"CMS--SA-v0\.3b(?!1a|1)\b", "CMS--SA-v0.3b1a", text)
text = re.sub(r"v0\.3b(?!1a|1)\b", "v0.3b1a", text)
path.write_text(text, encoding="utf-8")
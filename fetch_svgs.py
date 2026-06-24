import urllib.request
import json
import xml.etree.ElementTree as ET

slugs = [
    "python", "react", "fastapi", "postgresql", "sqlite", 
    "bootstrap", "stripe", "html5", "css3", "javascript", 
    "pandas", "googlegemini", "openai", "pytorch", 
    "nodedotjs", "flask", "django", "numpy", "scikitlearn",
    "redis", "mongodb"
]

results = {}

for slug in slugs:
    url = f"https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/{slug}.svg"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            svg_content = response.read().decode('utf-8')
            
            # Parse XML
            root = ET.fromstring(svg_content)
            # Find the path d attribute
            path_d = ""
            # Simple Icons SVGs have the path directly as child of svg
            namespaces = {'svg': 'http://www.w3.org/2000/svg'}
            # Try to get path
            path_elem = root.find('.//{http://www.w3.org/2000/svg}path')
            if path_elem is None:
                path_elem = root.find('.//path')
            if path_elem is not None:
                path_d = path_elem.get('d')
            
            # Also get viewBox
            viewbox = root.get('viewBox', '0 0 24 24')
            
            results[slug] = {
                "d": path_d,
                "viewBox": viewbox
            }
            print(f"Successfully fetched {slug}")
    except Exception as e:
        print(f"Error fetching {slug}: {e}")

# Save results
with open("fetched_svgs.json", "w") as f:
    json.dump(results, f, indent=2)

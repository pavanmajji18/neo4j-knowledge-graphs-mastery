import os
import subprocess
import sys

def generate_visual():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(base_dir, "assets", "card_template.html")
    output_png = os.path.join(base_dir, "assets", "linkedin_visual_06_graph_traversal.png")

    file_url = f"file:///{os.path.abspath(html_path).replace(os.sep, '/')}"

    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    ]

    browser_bin = None
    for p in chrome_paths:
        if os.path.exists(p):
            browser_bin = p
            break

    if not browser_bin:
        raise RuntimeError("Neither Chrome nor Edge was found on this system.")

    args = [
        browser_bin,
        "--headless",
        "--no-sandbox",
        "--disable-gpu",
        "--hide-scrollbars",
        "--force-device-scale-factor=1",
        "--window-size=1600,1000",
        f"--screenshot={output_png}",
        file_url
    ]

    print(f"Rendering {file_url} -> {output_png} using {os.path.basename(browser_bin)}...")
    res = subprocess.run(args, capture_output=True, text=True, timeout=30)
    if os.path.exists(output_png):
        print(f"Success! Generated {output_png} ({os.path.getsize(output_png)} bytes)")
    else:
        print(f"Failed. stdout: {res.stdout}, stderr: {res.stderr}")
        sys.exit(1)

if __name__ == "__main__":
    generate_visual()


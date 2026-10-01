import os
from playwright.sync_api import sync_playwright
V='file://'+os.path.abspath('scratchpad/journey/coltest.html')
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':760},device_scale_factor=2)
    pg.goto(V); pg.wait_for_timeout(400); pg.screenshot(path='scratchpad/journey/coltest.png'); b.close()
print('ok')

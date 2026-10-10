from playwright.sync_api import sync_playwright
import re,io
src=io.open('redteam_air.py',encoding='utf-8').read()
print(src[src.index("def ouvre"):src.index("def ouvre")+900] if "def ouvre" in src else src[7000:8200])

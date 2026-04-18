from browser import document, window
from browser.local_storage import storage
import json

header_links = document.select_one(".header-links")
header_logged_in_links = document.select_one(".header-logged-in-links")

log_out_button = document.select_one(".log-out-button")

def log_out(event):
    storage.clear()
    window.location.reload()

def try_log_in():
    api_key = storage.get("api_key")

    if not api_key:
        return
    header_links.style.display = "none"
    header_logged_in_links.style.display = "flex"
    
log_out_button.bind("click", log_out)

try_log_in()

window.try_log_in = try_log_in
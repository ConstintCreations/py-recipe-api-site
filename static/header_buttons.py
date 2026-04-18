from browser import document, window
from browser.local_storage import storage

header_links = document.select_one(".header-links")
header_logged_in_links = document.select_one(".header-logged-in-links")

username_link = document.select_one(".my-recipes-link")
log_out_button = document.select_one(".log-out-button")

def log_out(event):
    storage.clear()
    window.location.reload()

def try_log_in():
    api_key = storage.get("api_key")
    username = storage.get("username")

    if not username:
        username = "User"

    if not api_key:
        return
    
    username_link.text = username
    header_links.style.display = "none"
    header_logged_in_links.style.display = "flex"
    
log_out_button.bind("click", log_out)

try_log_in()

window.try_log_in = try_log_in
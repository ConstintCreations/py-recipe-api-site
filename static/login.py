from browser import document, aio
from browser.timer import set_timeout, clear_timeout
from browser.local_storage import storage
import json

login_input = document.select_one(".login-key")
login_button = document.select_one(".login-key-button")
login_info = document.select_one(".login-info")

hide_info_timer = None

def hide_login_info():
    login_info.style.display = "none"
    login_info.text = ""

def show_login_info(text:str = "Oops, it looks like I haven't implemented this yet! :c", hide_timer:bool = True):
    global hide_info_timer
    login_info.text = text
    login_info.style.display = "block"

    if hide_info_timer:
        clear_timeout(hide_info_timer)
    if hide_timer:
        hide_info_timer = set_timeout(hide_login_info, 5000)


async def login_button_click(event):

    api_key = login_input.value.strip()

    if not(api_key):
        show_login_info("Please enter your API Key.")
        return

    await login_user(api_key)

async def login_user(api_key:str):
    request = await aio.get(
        "/recipes/me",
        headers={"x-api-key": api_key}
    )

    if request.status == 200:
        storage["api_key"] = api_key
        show_login_info(text = "Success! You are now logged in.")
    else:
        if request.status == 401:
            show_login_info(text = "Oops! It looks like this API Key is invalid.")
        else:
            show_login_info(text = f"Oh No! An unknown error occured. ({request.status})")


def login_button_click_handler(event):
    aio.run(login_button_click(event)) 

login_button.bind("click", login_button_click_handler)
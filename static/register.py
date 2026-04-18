from browser import document, aio, window
from browser.timer import set_timeout, clear_timeout
from browser.local_storage import storage
import json

register_button = document.select_one(".register-name-button")
register_name = document.select_one(".register-name")
register_info = document.select_one(".register-info")

hide_info_timer = None
username = ""

def hide_register_info():
    register_info.style.display = "none"
    register_info.text = ""

def show_register_info(text:str = "Oops, it looks like I haven't implemented this yet! :c", hide_timer:bool = True):
    global hide_info_timer
    register_info.text = text
    register_info.style.display = "block"

    if hide_info_timer:
        clear_timeout(hide_info_timer)
    if hide_timer:
        hide_info_timer = set_timeout(hide_register_info, 5000)


async def register_button_click(event):
    global username

    username = register_name.value.strip()

    if not(username):
        show_register_info("Please enter a username.")
        return

    await register_user()

async def register_user():
    global username
    request = await aio.post(
        "/register",
        headers={
            "Content-Type": "application/json"
        },
        data=json.dumps({"name": username})
    )

    data = json.loads(request.data)

    if request.status == 200:
        storage["api_key"] = data['api_key']
        storage["username"] = username
        window.try_log_in()
        show_register_info(text = f"Success! You are now logged in with your new API Key: {data['api_key']}", hide_timer = False)
    else:
        if request.status == 400:
            show_register_info(text = "Oops! There is alread a user with the same username. Try again with a different name.")
        else:
            show_register_info(text = f"Oh No! An unknown error occured. ({request.status})")


def register_button_click_handler(event):
    aio.run(register_button_click(event)) 

register_button.bind("click", register_button_click_handler)
from browser import document, aio, window, html
from browser.local_storage import storage
import json

params = window.URLSearchParams.new(window.location.search)
page_user_id_raw = params.get("id")

recipes = document.select_one(".user-recipes")

user_title = document.select_one(".user-title")

async def get_user_username(page_user_id:int):
    request = await aio.get(f"/user/{page_user_id}")

    if request.status == 200:
        data = json.loads(request.data)
        user_title.text = f"{data['username']}'s Public Recipes:"
        user_title.style.textAlign = "left"
        
    elif request.status == 404:
        user_title.text = "User Not Found"

async def get_user_data(page_user_id:int):

    await get_user_username(page_user_id)

    request = await aio.get(f"/recipes/user/{page_user_id}")

    if request.status == 200:
        data = json.loads(request.data)
        for recipe in data["recipes"]:
            recipe_element = window.create_recipe_element(recipe, False)
            recipes <= recipe_element
        
    elif request.status == 404:
        user_title.text = "User Not Found"
    else:
        user_title.text = f"Unknown Error ({request.status})"
        
    
def compare_user_ids():
    global page_user_id_raw
    if not(page_user_id_raw):
        user_title.text = "No ID Specified"
        return
    
    try:
        page_user_id = int(page_user_id_raw)
    except(Exception):
        user_title.text = "Invalid ID"
        return
    
    try: 
        if not storage['user_id']:
            aio.run(get_user_data(page_user_id))
            return
        
        user_id = int(storage['user_id'])

        if user_id == page_user_id:
            window.location.href = "/static/me.html"
        else:
            aio.run(get_user_data(page_user_id))
    except(Exception):
        aio.run(get_user_data(page_user_id))

compare_user_ids()
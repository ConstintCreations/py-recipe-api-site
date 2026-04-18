from browser import document, aio, window, html
from browser.local_storage import storage
import json

params = window.URLSearchParams.new(window.location.search)
recipe_id_raw = params.get("id")

error_text = document.select_one(".recipe-full-error")
recipe_container = document.select_one(".recipe-full")

image = document.select_one(".recipe-image-full")
title = document.select_one(".recipe-title-full")
username = document.select_one(".recipe-username-full")
is_public = document.select_one(".recipe-is-public-full")
description = document.select_one(".recipe-description-full")
ingredients_list = document.select_one(".recipe-ingredients-list")
instructions = document.select_one(".recipe-instructions-full")

buttons_container = document.select_one(".recipe-full-buttons")
edit_button = document.select_one(".recipe-full-edit")
delete_button = document.select_one(".recipe-full-delete")

async def load_recipe():
    global recipe_id_raw
    if not(recipe_id_raw):
        error_text.text = "No ID Specified"
        return
    
    try:
        recipe_id = int(recipe_id_raw)
    except(Exception):
        error_text.text = "Invalid ID"
        return
    
    api_key = storage["api_key"]
    user_id = storage["user_id"]

    if not api_key or not user_id:
        error_text.text = "Invalid ID"
        return

    request = await aio.get(f"/recipes/{recipe_id}", headers = {"x-api-key": api_key})

    if request.status == 200:
        data = json.loads(request.data)
        error_text.style.display = "none"

        if int(user_id) == int(data['user']['user_id']):
            buttons_container.style.display = "flex"

        if "image_url" in data:
            image.style.backgroundImage = f"url({data['image_url']})"
            image.style.display = "block"

        title.text = data['title']

        if data['description']:
            description.text = data['description']
        else:
            description.text = "No Description"

        username.href = f"/static/user.html?id={data['user']['user_id']}"
        username.text = data['user']['username']

        is_public.text = "(Public)" if data['public'] else "(Private)"

        instructions.text = data['instructions']

        for item in data['ingredients'].split(","):
            li = html.LI(item.strip(), Class="recipe-ingredients-list-item")
            ingredients_list <= li

        recipe_container.style.display = "flex"

    else:
        if request.status == 401:
            error_text.text = "Invalid API Key"
        elif request.status == 404:
            error_text.text = "Recipe Not Found"
        elif request.status == 403:
            error_text.text = "This Recipe is Private"
        else:
            error_text.text = f"Unknown Error ({request.status})"

def load_recipe_handler():
    aio.run(load_recipe())

load_recipe_handler()

async def try_delete_recipe():
    global recipe_id_raw
    if not(recipe_id_raw):
        error_text.text = "No ID Specified"
        return
    
    try:
        recipe_id = int(recipe_id_raw)
    except(Exception):
        error_text.text = "Invalid ID"
        return
    
    api_key = storage["api_key"]
    if not api_key:
        return
    
    request = await aio.ajax("DELETE", f"/recipes/{recipe_id}", headers = {"x-api-key": api_key})

    if request.status == 200:
        window.location.href = "/static/me.html"

def delete_recipe_handler(event):
    aio.run(try_delete_recipe())

delete_button.bind("click", delete_recipe_handler)
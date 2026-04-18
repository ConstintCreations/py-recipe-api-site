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

edit_form_background = document.select_one(".recipe-editor-form-background")

edit_form = document.select_one(".recipe-editor")
exit_form_button = document.select_one(".recipe-editor-exit-button")
cancel_form_button = document.select_one(".form-recipe-cancel")

can_edit = False

async def load_recipe():
    global can_edit
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
            can_edit = True

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

async def try_edit_recipe():
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

    

    form_title = document.select_one(".form-recipe-title").value
    form_description = document.select_one(".form-recipe-description").value
    form_ingredients = document.select_one(".form-recipe-ingredients").value
    form_instructions = document.select_one(".form-recipe-instructions").value

    body = {}

    if form_title.strip():
        body["title"] = form_title.strip()
    if form_description.strip():
        body["description"] = form_description.strip()
    if form_ingredients.strip():
        body["ingredients"] = form_ingredients.strip()
    if form_instructions.strip():
        body["instructions"] = form_instructions.strip()

    if not body:
        return

    request = await aio.ajax("PATCH", f"/recipes/{recipe_id}", headers = {"x-api-key": api_key, "Content-Type": "application/json"}, data = json.dumps(body))

    if request.status == 200:
        window.location.reload()

def edit_recipe_handler(event):
    event.preventDefault()
    aio.run(try_edit_recipe())

edit_form.bind("submit", edit_recipe_handler)

def show_edit_recipe(event):
    if not can_edit:
        return
    
    edit_form_background.style.display = "grid"

def hide_edit_recipe(event):
    edit_form_background.style.display = "none"

edit_button.bind("click", show_edit_recipe)

exit_form_button.bind("click", hide_edit_recipe)
cancel_form_button.bind("click", hide_edit_recipe)
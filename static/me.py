from browser import document, aio, window
from browser.local_storage import storage
import json

user_title = document.select_one(".me-user-title")
user_recipes = document.select_one(".me-user-recipes")

user_info = document.select_one(".me-user-info")
api_key_text = document.select_one(".me-api-key-text")
recipe_count_text = document.select_one(".me-recipe-count-text")


create_recipe_form_background = document.select_one(".recipe-creator-form-background")

show_create_recipe_form = document.select_one(".show-create-recipe")
exit_create_recipe_form = document.select_one(".recipe-creator-exit-button")
cancel_create_recipe_form = document.select_one(".form-recipe-cancel")

create_recipe_form = document.select_one(".recipe-creator")

async def try_get_data():
    api_key = storage.get("api_key")
    username = storage.get("username")

    if not username:
        username = "User"

    if not api_key:
        return
    
    user_title.style.textAlign = "left"
    user_title.text = f"{username}'s Recipes:"

    api_key_text.text = api_key
    user_info.style.display = "flex"
    
    user_recipes.style.display = "flex"

    await load_my_recipes()

async def load_my_recipes():
    api_key = storage.get("api_key")
    if not api_key:
        return

    request = await aio.get(
        "/recipes/me",
        headers={"x-api-key": api_key}
    )

    if request.status == 200:
        data = json.loads(request.data)
        recipe_count_text.text = data["total"]
        for recipe in data["recipes"]:
            recipe_element = window.create_recipe_element(recipe)
            user_recipes <= recipe_element

async def recipe_submit(event):
    title = document.select_one(".form-recipe-title").value
    image_url = document.select_one(".form-recipe-img-url").value
    is_private = document.select_one(".form-recipe-is-private").checked
    description = document.select_one(".form-recipe-description").value
    ingredients = document.select_one(".form-recipe-ingredients").value
    instructions = document.select_one(".form-recipe-instructions").value

    api_key = storage.get("api_key")
    if not api_key:
        return
    
    body = {
        "title": title,
        "description": description or None,
        "ingredients": ingredients,
        "instructions": instructions,
        "is_public": not is_private,
        "image_url": image_url or None
    }
    
    request = await aio.post(
        "/recipes",
        headers={
            "x-api-key": api_key,
            "Content-Type": "application/json"
        },
        data = json.dumps(body)
    )

    if request.status == 200:
        window.location.reload()


def try_get_data_handler():
    aio.run(try_get_data())

try_get_data_handler()

def copy_api_key(event):
    window.navigator.clipboard.writeText(api_key_text.text)

api_key_text.bind("click", copy_api_key)

def show_recipe_creation(event):
    create_recipe_form_background.style.display = "grid"

def hide_recipe_creation(event):
    create_recipe_form_background.style.display = "none"

def handle_recipe_submit(event):
    event.preventDefault()
    aio.run(recipe_submit(event))

show_create_recipe_form.bind("click", show_recipe_creation)

exit_create_recipe_form.bind("click", hide_recipe_creation)
cancel_create_recipe_form.bind("click", hide_recipe_creation)

create_recipe_form.bind("submit", handle_recipe_submit)
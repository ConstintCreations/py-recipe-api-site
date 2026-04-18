from browser import document, aio, html, window
from browser.local_storage import storage
import json

user_title = document.select_one(".me-user-title")
user_recipes = document.select_one(".me-user-recipes")

user_info = document.select_one(".me-user-info")
api_key_text = document.select_one(".me-api-key-text")
recipe_count_text = document.select_one(".me-recipe-count-text")

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
            recipe_element = create_recipe_element(recipe)
            user_recipes <= recipe_element

def try_get_data_handler():
    aio.run(try_get_data())

try_get_data_handler()

def create_recipe_element(recipe):
    recipe_div = html.DIV(Class="recipe")
    image_div = html.DIV(Class="recipe-image")
    info_div = html.DIV(Class="recipe-info")

    title_link = html.A(f"[{'Public' if recipe['public'] else 'Private'}] {recipe['title']}", href=f"/static/recipe.html", Class="recipe-title")
    ingredients_text = html.H3(f"Ingredients: {recipe['ingredients']}", Class="recipe-ingredients")
    description_text = html.P(recipe['description'], Class="recipe-description")

    username_link = html.A(recipe['user']['username'], href="/static/user.html", Class="recipe-username")

    info_div <= title_link
    info_div <= ingredients_text
    info_div <= description_text

    recipe_div <= image_div
    recipe_div <= info_div
    recipe_div <= username_link

    return recipe_div    

def copy_api_key(event):
    window.navigator.clipboard.writeText(api_key_text.text)

api_key_text.bind("click", copy_api_key)
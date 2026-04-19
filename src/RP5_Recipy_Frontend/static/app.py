from browser import document, aio, window
import json

recipes = document.select_one(".recipes")

async def load_public_recipes():

    request = await aio.get(
        "/recipes/public",
    )

    if request.status == 200:
        data = json.loads(request.data)
        
        for recipe in data["recipes"]:
            recipe_element = window.create_recipe_element(recipe, False)
            recipes <= recipe_element

def load_public_recipes_handler():
    aio.run(load_public_recipes())

load_public_recipes_handler()  
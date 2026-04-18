from browser import html, window

def create_recipe_element(recipe, show_public_private:bool = True):
    recipe_div = html.DIV(Class="recipe")
    image_div = html.DIV(Class="recipe-image")
    info_div = html.DIV(Class="recipe-info")

    if "image_url" in recipe:
        image_div.style.backgroundImage = f"url({recipe['image_url']})"

    if show_public_private:
        title_link = html.A(f"[{'Public' if recipe['public'] else 'Private'}] {recipe['title']}", href=f"/static/recipe.html", Class="recipe-title")
    else:
        title_link = html.A({recipe['title']}, href=f"/static/recipe.html", Class="recipe-title")
    ingredients_text = html.H3(f"Ingredients: {recipe['ingredients']}", Class="recipe-ingredients")

    if recipe["description"]:
        description_text = html.P(recipe['description'], Class="recipe-description")
    else:
        description_text = html.P("", Class="recipe-description")

    username_link = html.A(recipe['user']['username'], href="/static/user.html", Class="recipe-username")

    info_div <= title_link
    info_div <= ingredients_text
    info_div <= description_text

    recipe_div <= image_div
    recipe_div <= info_div
    recipe_div <= username_link

    return recipe_div    

window.create_recipe_element = create_recipe_element
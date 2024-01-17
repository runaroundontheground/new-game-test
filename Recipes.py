from GlobalVariables import recipes



# make recipes here


def addRecipe(recipeType, recipeName, requiredItems, recipeShape = None):
    """
    recipeType:
        can be "exact", "nearExact", or "shapeless"

    recipeName:
        name of the recipe as a str

    requiredItems:
        list containing dicts that contain a count for each item as well as the item name \n
        shovel as an example
            [{"name": "stick", "count": 2},
            {"name": "cobblestone", "count": 1}]

    recipeShape:
        only required for exact and nearExact recipes, 
    """
    

    recipe = {"recipeType": recipeType,
              "requiredItems": requiredItems,
              }
    


    recipes[recipeName] = recipe











addRecipe("nearExact", "stick", [{"name": "planks", "count": 2}])
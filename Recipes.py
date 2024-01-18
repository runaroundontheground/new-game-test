from GlobalVariables import recipes, items



# make recipes here


def addRecipe(recipeType, recipeName, requiredItems, output, outputCount = 1, recipeShape = None):
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
    
    output and outputCount:
        what item should be gived from crafting this (items["itemname"])
        how many of this items should be given from crafting it?

    recipeShape:
        only required for exact and nearExact recipes, 
    """
    

    recipe = {
              "requiredItems": requiredItems,
              "itemOutput": output,
              "itemOutputCount": outputCount
              }
    
    if recipeType == "exact":
        recipe["recipeShape"] = recipeShape
    


    recipes[recipeType][recipeName] = recipe




def makeRecipesExist():


    addRecipe("shapeless", "logToPlanks", [{"name": "log", "count": 1}], items["planks"], 4)

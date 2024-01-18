from GlobalVariables import recipes, items



# make recipes here


def addRecipe(
        recipeType, recipeName, requiredItems, output, outputCount = 1, recipeShape = None,
        requiredGridSize = 2, recipeInstructions = None
              ):
    """
    recipeType:
        can be "exact", "nearExact", or "shapeless"

    recipeName:
        name of the recipe as a str

    requiredItems:
        dict with an item name key and a required count of said item
            {"log": 2}
    
    output and outputCount:
        what item should be gived from crafting this (items["itemname"])
        how many of this items should be given from crafting it?

    recipeShape:
        only required for exact recipes, just a list with however many dicts it takes
        to list off the slot id and item name for that slot

    requiredGridSize:
        default 2, what size of grid is needed to craft this
        only planned working values are 2 and 3, 
        if the size is > 2 then recipes for grid size 3 will also have those recipes

    recipeInstructions:
        special list of stuff, allows for using operators and comparing slot contents
        see recipe stuff in player to figure it out, not gonna write it here
    """
    

    recipe = {
              "requiredItems": requiredItems,
              "output": output,
              "outputCount": outputCount
              }
    
    if recipeType == "exact":
        recipe["recipeShape"] = recipeShape
    
    if recipeType == "nearExact":
        recipe["recipeInstructions"] = recipeInstructions
    


    recipes[requiredGridSize][recipeType][recipeName] = recipe

    if requiredGridSize != 3:
        recipes[3][recipeType][recipeName] = recipe





def makeRecipesExist():


    addRecipe("shapeless", "logToPlanks", {"log": 1}, items["planks"], 4)
    
    addRecipe("nearExact", "planksToSticks", {"planks": 2}, items["stick"], 4,
              requiredGridSize = 2,
              recipeInstructions = {
                  "startingItem": "planks",
                  "directions": ["up", "down"],
                  "operators": "xor",
                  "items": ["planks", "planks"]
                                    }
              )

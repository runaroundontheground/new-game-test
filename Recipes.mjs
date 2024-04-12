import { showLoadingProgress, recipes, items } from "./GlobalVariables.mjs"

showLoadingProgress("loading Recipes.mjs");


function addRecipe(
    recipeType, recipeName, requiredItems, output, outputCount = 1, recipeShape,
    requiredGridSize = 2, instructions
) {
    /*
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

    instructions:
        special list of stuff, allows for using operators and comparing slot contents
        see recipe stuff in player to figure it out, not gonna write it here
    */


    let recipe = {
        "requiredItems": requiredItems,
        "output": output,
        "outputCount": outputCount
    }

    if (recipeType == "exact") {
        recipe.recipeShape = recipeShape;
    };

    if (recipeType == "nearExact") {
        recipe.instructions = instructions;
    };



    recipes[requiredGridSize][recipeType][recipeName] = recipe;

    if (requiredGridSize != 3) {
        recipes[3][recipeType][recipeName] = recipe;
    };

};





export function makeRecipesExist() {
    /*
        how recipes should be formatted
        list, contains multiple instructions
        instructions = [
            { if it needs an operator, it'll use this
                "up": "planks",
                "operator": "xor",
                "down": "planks"
            },
            {
                "up": "planks"
            }
        ]
     instructions = {
           "up": "planks",
           "operator": "xor",
           "down": "planks"
    }  }
    }
     if at any point there needs to be multiple directions to find something (it's not just adjacent)
     then this can be used: "up,up,right": "planks"
    
    */

    addRecipe("shapeless", "craftingTable", { "planks": 4 }, items["crafting table"], 1);

    addRecipe("shapeless", "logToPlanks", { "log": 1 }, items["planks"], 4);

    addRecipe("nearExact", "planksToSticks", { "planks": 2 }, items["stick"], 4, undefined,
        2,
        {
            "startingItemName": "planks",
            "directions": ["up", "down"],
            "operators": ["xor"],
            "items": ["planks", "planks"]
        }
    )

    addRecipe("exact", "stone pickaxe", { "stick": 2, "cobblestone": 3 }, items["stone pickaxe"], 1,
        {
            0: "cobblestone",
            1: "cobblestone",
            2: "cobblestone",
            4: "stick",
            7: "stick"
        }, 3
    )

};

showLoadingProgress("Recipes.mjs loaded");
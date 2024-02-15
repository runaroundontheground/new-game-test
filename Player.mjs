import {
    consoleLog, camera, blockSize, gravity, chunkSize, maxStackSize, entities, recipes, items,
    canvasWidth, canvasHeight, chunks, fps, itemEntitySize, keys, keysPressed, mouse, random, showLoadingProgress
} from "./GlobalVariables.mjs";
showLoadingProgress("loading Player.mjs");

import {
    getChunkCoord, getBlockCoord, findBlock,
    generateChunkTerrain, smallScaleBlockUpdates
} from "./Worldgen.mjs";

import { ItemEntity } from "./Entities.mjs";
import { PlaceableItem } from "./Items.mjs";



 
class Player {
    constructor() {
        // player's actual coordinate is
        // top left and above corner
        this.x = 0;
        this.y = 0;
        this.z = 0;
        // velocity
        this.xv = 0;
        this.yv = 0;
        this.zv = 0;
 
        this.acceleration = 0.6;
        this.maxHorizontalSpeed = 5;
        this.slipperyness = 5;
        this.normalJumpForce = 10;
 
        this.booleans = {
            "blockStepUsed": false
        };
 
 
        this.width = blockSize - 5;
        this.height = blockSize - 5;
        this.image = {
            "rectData": Rect(0, 0, this.width, this.height),
            "color": "red"
        };

        // this is to make rendering work currently and should be removed later!

        
 
        this.position = [this.x, this.y, this.z];
        this.chunkCoord = [0, 0]
        this.blockCoord = [0, 0, 0]
 
        this.rect = Rect(0, 0, this.width, this.width);
 
        // how i'm organizing the collision
        // default is the same height as player
        //above + down, or right, etc is one block higher
        // below + a side is one block below player
        // it's true if there is a block, otherwise it's false
        // this doesn't include blocks that have no collision, like water as well
 
        this.collision = {
            "below": false,
            "above": false,
 
            "right": false,
            "left": false,
            "up": false,
            "down": false,
 
            "aboveRight": false,
            "aboveLeft": false,
            "aboveUp": false,
            "aboveDown": false,
            
            "insideOfBlock": "air"
        };
 
        // hooray, inventory time!
        let widthOfInventoryInSlots = 9;
        let heightOfInventoryInSlots = 3;
 
 
        function createALotOfInventoryThings() {
    
            let inventoryWidthInPixels = canvasWidth / 3;
            let slotSizeInPixels = Math.round(inventoryWidthInPixels / widthOfInventoryInSlots);
 
            let gapBetweenSlots = Math.round(slotSizeInPixels / 5);
 
 
            let backgroundColor = [150, 150, 150]
            let slotColor = [125, 125, 125]
            let selectedSlotColor = [175, 175, 175, 0]
            let alphaForUI = 255;
 
            let emptySpaceBetweenItemAndSlotBorder = gapBetweenSlots / 2
 
            let itemIconShift = emptySpaceBetweenItemAndSlotBorder
 
            inventoryWidthInPixels += gapBetweenSlots * (widthOfInventoryInSlots + 1)
 
            let inventoryHeightInPixels = (slotSizeInPixels * heightOfInventoryInSlots)
            inventoryHeightInPixels += gapBetweenSlots * (heightOfInventoryInSlots + 1)
 
            // add some more height to the inventory for crafting grid and armor? if added
            let craftingAndArmorHeightInSlots = 4.25
            
            let craftingAndArmorWidthInPixels = inventoryWidthInPixels
            let craftingAndArmorHeightInPixels = (slotSizeInPixels * craftingAndArmorHeightInSlots)
            craftingAndArmorHeightInPixels += (gapBetweenSlots * craftingAndArmorHeightInSlots + 1)
 
            let craftingTableSizeInPixels = (round(craftingAndArmorWidthInPixels), round(craftingAndArmorHeightInPixels))
 
 
            let craftingAndArmorSizeInPixels = (round(craftingAndArmorWidthInPixels), round(craftingAndArmorHeightInPixels))
            
            let craftingAndArmorBackground = pygame.surface.Surface(craftingAndArmorSizeInPixels)
            craftingAndArmorBackground.fill(backgroundColor)
 
            let craftingTableBackground = pygame.Surface(craftingTableSizeInPixels)
            craftingTableBackground.fill(backgroundColor)
 
            let inventorySizeInPixels = (round(inventoryWidthInPixels), round(inventoryHeightInPixels))
 
            let inventoryBackground = pygame.surface.Surface(inventorySizeInPixels)
            inventoryBackground.fill(backgroundColor)
            
            let slotSurface = pygame.surface.Surface((slotSizeInPixels, slotSizeInPixels))
            slotSurface.fill(slotColor)
 
            let size = (slotSizeInPixels + gapBetweenSlots * 2, slotSizeInPixels + gapBetweenSlots * 2)
            let selectedSlotSurface = pygame.surface.Surface(size)
            selectedSlotSurface.fill((selectedSlotColor))
 
            // the thing here needs to be replaced with ctx.strokeRect or something
            let fillRect = Rect(gapBetweenSlots, gapBetweenSlots, slotSizeInPixels, slotSizeInPixels);
            selectedSlotSurface.fill((255, 255, 255), fillRect)
            selectedSlotSurface.set_colorkey((255, 255, 255))
 
            let hotbarSizeInPixels = (round(inventorySizeInPixels[0]), round(slotSizeInPixels + (gapBetweenSlots * 2)))
            let hotbarSurface = pygame.surface.Surface(hotbarSizeInPixels)
            hotbarSurface.fill(backgroundColor)
 
            if (alphaForUI < 255) {
                hotbarSurface.set_alpha(alphaForUI)
                inventoryBackground.set_alpha(alphaForUI)
                craftingAndArmorBackground.set_alpha(alphaForUI)
                slotSurface.set_alpha(alphaForUI)
            };
 
            let craftingAndArmorXForBlit = (canvasWidth - (craftingAndArmorWidthInPixels)) / 2 
            let craftingAndArmorYForBlit = (canvasHeight - (craftingAndArmorHeightInPixels + inventoryHeightInPixels))# - (slotSizeInPixels * craftingAndArmorHeightInSlots)
            craftingAndArmorYForBlit /= 2
 
            let craftingTableXForBlit = craftingAndArmorXForBlit
            let craftingTableYForBlit = craftingAndArmorYForBlit - slotSizeInPixels * 0
 
            let fontShift = font.size("1")
 
            this.craftingResultSlot = {
                "contents": "empty",
                "count": 0,
                2: {
                    "renderPosition": (0, 0),
                    "selectedSlotRenderPosition": (0, 0),
                    "itemCountRenderPosition": (0, 0),
                    "rect": Rect(0, 0, 0, 0), // used for mouse collision
                },
                3: {
                    "renderPosition": (0, 0),
                    "selectedSlotRenderPosition": (0, 0),
                    "itemCountRenderPosition": (0, 0),
                    "rect": Rect(0, 0, 0, 0), // used for mouse collision
                }
            }
 
            craftingSlot = {
                "contents": "empty",
                "count": 0,
                2: {
                    "renderPosition": (0, 0),
                    "selectedSlotRenderPosition": (0, 0),
                    "itemCountRenderPosition": (0, 0),
                    "rect": pygame.Rect(0, 0, 0, 0), # used for mouse collision
                },
                3: {
                    "renderPosition": (0, 0),
                    "selectedSlotRenderPosition": (0, 0),
                    "itemCountRenderPosition": (0, 0),
                    "rect": pygame.Rect(0, 0, 0, 0), # used for mouse collision
                },
                "slotId": 0
            }
 
            armorSlot = {
                "contents": "empty",
                "renderPosition": (0, 0),
                "selectedSlotRenderPosition": (0, 0),
                "rect": pygame.Rect(0, 0, 0, 0),
                "slotId": 0
            }
 
            this.isCrafting = false
 
            this.crafting = {
                2: {
                "slots": {
                    0: craftingSlot, 1: craftingSlot,
                    2: craftingSlot, 3: craftingSlot,
                    "resultSlot": 0,
                }},
                3: {
                    "slots": {
                    0: craftingSlot, 1: craftingSlot,
                    2: craftingSlot, 3: craftingSlot,
                    4: craftingSlot, 5: craftingSlot,
                    6: craftingSlot, 7: craftingSlot,
                    8: craftingSlot, "resultSlot": 0
                }},
                "gridSize": 2
 
                             }
            this.totalCraftingContents = {}
            this.armor = {
                "head": armorSlot,
                "chest": armorSlot,
                "legs": armorSlot,
                "feet": armorSlot
            }
 
            # actually add content spots to the armor/crafting
            
 
            resultSlot = craftingSlot.copy()
 
            # create output slot for player's crafting 2x2 grid
            slotX = ((widthOfInventoryInSlots) * slotSizeInPixels)
            slotY = (slotSizeInPixels * 1.5)
 
            renderX = slotX + craftingAndArmorXForBlit + itemIconShift
            renderY = slotY + craftingAndArmorYForBlit + itemIconShift
 
            rectX = renderX - itemIconShift
            rectY = renderY - itemIconShift
 
            
            
            craftingAndArmorBackground.blit(slotSurface, (slotX, slotY))
 
            resultSlot["renderPosition"] = (renderX, renderY)
            resultSlot["rect"] = pygame.Rect(rectX, rectY, slotSizeInPixels, slotSizeInPixels)
            resultSlot["selectedSlotRenderPosition"] = (rectX - gapBetweenSlots, rectY - gapBetweenSlots)
            resultSlot["itemCountRenderPosition"] = (rectX + slotSizeInPixels - fontShift[0] - 1, rectY + slotSizeInPixels - fontShift[1] - 1)
            resultSlot["slotId"] = "resultSlot"
 
            this.crafting[2]["slots"]["resultSlot"] = resultSlot.copy()
 
 
 
 
 
 
            # create output slot for the 3x3 grid
            slotX = ((widthOfInventoryInSlots - 2) * slotSizeInPixels) + slotSizeInPixels * 1.7
            slotY = (slotSizeInPixels * 2.1)
 
            renderX = slotX + craftingTableXForBlit + itemIconShift
            renderY = slotY + craftingTableYForBlit + itemIconShift
 
            rectX = renderX - itemIconShift
            rectY = renderY - itemIconShift
 
            
            
            craftingTableBackground.blit(slotSurface, (slotX, slotY))
 
            resultSlot["renderPosition"] = (renderX, renderY)
            resultSlot["rect"] = pygame.Rect(rectX, rectY, slotSizeInPixels, slotSizeInPixels)
            resultSlot["selectedSlotRenderPosition"] = (rectX - gapBetweenSlots, rectY - gapBetweenSlots)
            resultSlot["itemCountRenderPosition"] = (rectX + slotSizeInPixels - fontShift[0] - 1, rectY + slotSizeInPixels - fontShift[1] - 1)
            resultSlot["slotId"] = "resultSlot"
 
            this.crafting[3]["slots"]["resultSlot"] = resultSlot.copy()
 
 
            craftingTableBackground.blit(slotSurface, (slotX, slotY))
           
 
 
            slotId = 0
 
            # create and blit the crafting slots for the player's crafting grid
            for y in range(2):
                for x in range(2):
                    
                    
 
                    
                    slotX = ((widthOfInventoryInSlots - 4) * slotSizeInPixels) + (x * slotSizeInPixels) + ((x + 1) * gapBetweenSlots)
                    slotY = (slotSizeInPixels * 0.75) + (y * slotSizeInPixels + ((y + 1) * gapBetweenSlots))
 
                    renderX = slotX + craftingAndArmorXForBlit + itemIconShift
                    renderY = slotY + craftingAndArmorYForBlit + itemIconShift
 
                    rectX = renderX - itemIconShift
                    rectY = renderY - itemIconShift
 
                    newCraftingSlot = craftingSlot.copy()
                    
                    
                    craftingAndArmorBackground.blit(slotSurface, (slotX, slotY))
                    newCraftingSlot["renderPosition"] = (renderX, renderY)
                    newCraftingSlot["rect"] = pygame.Rect(rectX, rectY, slotSizeInPixels, slotSizeInPixels)
                    newCraftingSlot["selectedSlotRenderPosition"] = (rectX - gapBetweenSlots, rectY - gapBetweenSlots)
                    newCraftingSlot["itemCountRenderPosition"] = (rectX + slotSizeInPixels - fontShift[0] - 1, rectY + slotSizeInPixels - fontShift[1] - 1)
                    newCraftingSlot["slotId"] = slotId
 
                    this.crafting[2]["slots"][slotId] = newCraftingSlot
 
                    slotId += 1
 
 
            slotId = 0
            # create and blit slots for the crafting table grid
            for y in range(3):
                for x in range(3):
                    slotX = ((widthOfInventoryInSlots - 6) * slotSizeInPixels) + (x * slotSizeInPixels) + ((x + 1) * gapBetweenSlots)
                    slotY = (slotSizeInPixels * 0.75) + (y * slotSizeInPixels + ((y + 1) * gapBetweenSlots))
 
                    renderX = slotX + craftingTableXForBlit + itemIconShift
                    renderY = slotY + craftingTableYForBlit + itemIconShift
 
                    rectX = renderX - itemIconShift
                    rectY = renderY - itemIconShift
 
                    
                    
                    newCraftingSlot = craftingSlot
                    
                    
                    craftingTableBackground.blit(slotSurface, (slotX, slotY))
                    newCraftingSlot["renderPosition"] = (renderX, renderY)
                    newCraftingSlot["rect"] = pygame.Rect(rectX, rectY, slotSizeInPixels, slotSizeInPixels)
                    newCraftingSlot["selectedSlotRenderPosition"] = (rectX - gapBetweenSlots, rectY - gapBetweenSlots)
                    newCraftingSlot["itemCountRenderPosition"] = (rectX + slotSizeInPixels - fontShift[0] - 1, rectY + slotSizeInPixels - fontShift[1] - 1)
                    newCraftingSlot["slotId"] = slotId
 
                    this.crafting[3]["slots"][slotId] = newCraftingSlot.copy()
 
                    slotId += 1
 
 
            # put an arrow that goes towards the result slot for crafting in the 2x2 grid
            a = (widthOfInventoryInSlots - 0.60) * slotSizeInPixels
            b = (slotSizeInPixels*0.75) + slotSizeInPixels * 1.1
 
            c = (a, b)
            d = (a + (slotSizeInPixels/3), b + (slotSizeInPixels/3)/2)
            e = (a, b + slotSizeInPixels/3)
 
            f = (c, d, e)
 
            pygame.draw.polygon(craftingAndArmorBackground, selectedSlotColor, f)
 
            rect = pygame.Rect(a - slotSizeInPixels/1.4, b + slotSizeInPixels/8.5,
                               slotSizeInPixels/1.3, slotSizeInPixels/9)
            pygame.draw.rect(craftingAndArmorBackground, selectedSlotColor, rect)
 
            craftingAndArmorSurface = craftingAndArmorBackground
 
 
            # put an arrow that goes towards the result slot for crafting in the 3x3 grid
            a = (widthOfInventoryInSlots - 0.60) * slotSizeInPixels - slotSizeInPixels * 0.8
            b = (slotSizeInPixels*0.75) + slotSizeInPixels * 1.1 + slotSizeInPixels / 1.8
 
            c = (a, b)
            d = (a + (slotSizeInPixels/3), b + (slotSizeInPixels/3)/2)
            e = (a, b + slotSizeInPixels/3)
 
            f = (c, d, e)
 
            pygame.draw.polygon(craftingTableBackground, selectedSlotColor, f)
 
            rect = pygame.Rect(a - slotSizeInPixels/1.4, b + slotSizeInPixels/8.5,
                               slotSizeInPixels/1.3, slotSizeInPixels/9)
            pygame.draw.rect(craftingTableBackground, selectedSlotColor, rect)
 
            craftingTableSurface = craftingTableBackground
 
 
 
 
            inventoryXForBlit = (canvasWidth - inventoryWidthInPixels) / 2 
            inventoryYForBlit = craftingAndArmorYForBlit + craftingAndArmorHeightInPixels
 
            hotbarXForBlit = inventoryXForBlit
            hotbarYForBlit = (canvasHeight - hotbarSizeInPixels[1]) - (hotbarSizeInPixels[1] / 2)
 
            inventorySlot = {
                "contents": "empty", # this is where itemData goes
                "count": 0, # how many of x item is in this slot
                "renderPosition": (0, 0),
                "selectedSlotRenderPosition": (0, 0),
                "itemCountRenderPosition": (0, 0),
                "rect": pygame.Rect(0, 0, 0, 0), # used for mouse collision
                "slotId": 0
            }
 
            this.inventory = []
            this.hotbar = []
 
            slotId = 0
 
            for y in range(heightOfInventoryInSlots):
                for x in range(widthOfInventoryInSlots):
 
                    slotX = (x * slotSizeInPixels) + ((x + 1) * gapBetweenSlots)
                    slotY = (y * slotSizeInPixels + ((y + 1) * gapBetweenSlots))
 
                    inventoryBackground.blit(slotSurface, (slotX, slotY))
 
                    renderX = inventoryXForBlit + slotX + itemIconShift
                    renderY = inventoryYForBlit + slotY + itemIconShift
 
                    rectX = renderX - itemIconShift
                    rectY = renderY - itemIconShift
 
                    updatedInventorySlot = inventorySlot.copy()
                    
   
                    
 
                    updatedInventorySlot["renderPosition"] = (renderX, renderY)
                    updatedInventorySlot["itemCountRenderPosition"] = (rectX + slotSizeInPixels - fontShift[0] - 1, rectY + slotSizeInPixels - fontShift[1] - 1)
                    updatedInventorySlot["selectedSlotRenderPosition"] = (rectX - gapBetweenSlots,
                                                                        rectY - gapBetweenSlots)
                    updatedInventorySlot["rect"] = pygame.Rect(rectX, rectY,
                                                            slotSizeInPixels, slotSizeInPixels)
                    updatedInventorySlot["slotId"] = slotId
                    slotId += 1
                    
 
                    this.inventory.append(updatedInventorySlot)
 
 
            
 
 
 
            inventorySurface = inventoryBackground        
        
            # create hotbar data
            slotId = 0
            for x in range(widthOfInventoryInSlots):
 
                slotX = (x * slotSizeInPixels) + ((x + 1) * gapBetweenSlots)
                slotY = gapBetweenSlots
 
                renderX = hotbarXForBlit + slotX + itemIconShift
                renderY = hotbarYForBlit + slotY + itemIconShift
 
                rectX = renderX - itemIconShift
                rectY = renderY - itemIconShift
 
                fontShift = font.size("1")
 
                updatedInventorySlot = inventorySlot.copy()
 
                updatedInventorySlot["renderPosition"] = (renderX, renderY)
                updatedInventorySlot["itemCountRenderPosition"] = (rectX + slotSizeInPixels - fontShift[0] - 1, rectY + slotSizeInPixels - fontShift[1] - 1)
                updatedInventorySlot["selectedSlotRenderPosition"] = (rectX - gapBetweenSlots,
                                                                    rectY - gapBetweenSlots)
                updatedInventorySlot["rect"] = pygame.Rect(rectX, rectY,
                                                        slotSizeInPixels, slotSizeInPixels)
                updatedInventorySlot["slotId"] = slotId
                slotId += 1
 
                hotbarSurface.blit(slotSurface, (slotX, slotY))
 
                this.hotbar.append(updatedInventorySlot)
            
            inventoryRect = pygame.Rect(inventoryXForBlit, inventoryYForBlit,
                                        inventoryWidthInPixels, inventoryHeightInPixels)
            
            hotbarRect = pygame.Rect(hotbarXForBlit, hotbarYForBlit,
                                    inventoryWidthInPixels, hotbarSizeInPixels[1])
        
            craftingAndArmorRect = pygame.Rect(craftingAndArmorXForBlit, craftingAndArmorYForBlit,
                                               craftingAndArmorWidthInPixels, craftingAndArmorHeightInPixels)
            
            craftingTableRect = pygame.Rect(
                craftingTableXForBlit, craftingTableYForBlit,
                craftingTableSizeInPixels[0], craftingTableSizeInPixels[1]
            )
            
 
            this.inventoryRenderingData = {
                "inventoryRenderPosition": (inventoryXForBlit, inventoryYForBlit),
                "craftingAndArmorRenderPosition": (craftingAndArmorXForBlit, craftingAndArmorYForBlit),
                "hotbarRenderPosition": (hotbarXForBlit, hotbarYForBlit),
                "inventorySurface": inventorySurface,
                "craftingAndArmorSurface": craftingAndArmorSurface,
                "craftingTableSurface": craftingTableSurface,
                "craftingTableRenderPosition": (craftingTableXForBlit, craftingTableYForBlit),
                "hotbarSurface": hotbarSurface,
                "itemIconShift": itemIconShift,
                "slotSize": slotSizeInPixels,
                "selectedSlotSurface": selectedSlotSurface
            }
 
            this.otherInventoryData = {
            # rects are here
            "inventoryRect": inventoryRect,
            "hotbarRect": hotbarRect,
            "craftingAndArmorRect": craftingAndArmorRect,
            "craftingTableRect": craftingTableRect,
            # thigns that aren't rects are here
            "currentHotbarSlot": 0, # id/index of the slot in the hotbar
            "open": false,
            "slotId": 0,
            "showCraftingAndArmor": true,
            "showCraftingTable": false
            }
            
        };
 
        createALotOfInventoryThings()
 
 
        this.timers = {
 
        }
 
        # blocks up AND down of reach
        this.verticalBlockReach = 3
        this.horizontalBlockReach = 3
        this.canReachSelectedBlock = false
 
        this.blockBreakProgress = 0
        this.currentBreakingBlock = None
    
 
 
    def generalMovement(this, deltaTime):
 
        left = keys[0][pygame.K_a]
        right = keys[0][pygame.K_d]
        up = keys[0][pygame.K_w]
        down = keys[0][pygame.K_s]
        space = keys[0][pygame.K_SPACE]
        
        this.chunkCoord = getChunkCoord(this.x, this.z)
        this.blockCoord = getBlockCoord(this.x, this.y, this.z)
 
        this.rect.x = this.x
        this.rect.y = this.z
 
    
        
        for dictKey in this.collision.keys():
            this.collision[dictKey] = false
 
        # faster? access to variables that need to be used a lot in collision
        rightSide = this.x + this.width
        bottomSide = this.z + this.width
        underSide = this.y - this.height
        
        def doCollisionBelow():
            topLeft = findBlock(this.x, underSide - 3, this.z, ignoreWater = true)
            topRight = findBlock(rightSide, underSide - 3, this.z, ignoreWater = true)
            bottomLeft = findBlock(this.x, underSide - 3, bottomSide, ignoreWater = true)
            bottomRight = findBlock(rightSide, underSide - 3, bottomSide, ignoreWater = true)
            if topLeft or topRight or bottomLeft or bottomRight:
                this.collision["below"] = true
        doCollisionBelow()
 
        def doCollisionAbove():
            topLeft = findBlock(this.x, this.y, this.z, ignoreWater = true)
            topRight = findBlock(rightSide, this.y, this.z, ignoreWater = true)
            bottomLeft = findBlock(this.x, this.y, bottomSide, ignoreWater = true)
            bottomRight = findBlock(rightSide, this.y, bottomSide, ignoreWater = true)
            if topLeft or topRight or bottomLeft or bottomRight:
                this.collision["above"] = true
        
        doCollisionAbove()
 
        def doCollisionToRight():
            temporaryNumber = rightSide + 1
            aboveTopRight = findBlock(temporaryNumber, this.y, this.z, ignoreWater = true)
            aboveBottomRight = findBlock(temporaryNumber, this.y, bottomSide, ignoreWater = true)
            belowBottomRight = findBlock(temporaryNumber, underSide, bottomSide, ignoreWater = true)
            belowTopRight = findBlock(temporaryNumber, underSide, this.z, ignoreWater = true)
            if aboveTopRight or aboveBottomRight or belowBottomRight or belowTopRight:
                this.collision["right"] = true
 
        doCollisionToRight()
        
        def doCollisionToLeft():
            temporaryNumber = this.x - 1
            aboveTopLeft = findBlock(temporaryNumber, this.y, this.z, ignoreWater = true)
            aboveBottomLeft = findBlock(temporaryNumber, this.y, bottomSide, ignoreWater = true)
            belowBottomLeft = findBlock(temporaryNumber, underSide, bottomSide, ignoreWater = true)
            belowTopLeft = findBlock(temporaryNumber, underSide, this.z, ignoreWater = true)
            if aboveBottomLeft or aboveTopLeft or belowBottomLeft or belowTopLeft:
                this.collision["left"] = true
 
        doCollisionToLeft()
 
        def doCollisionToUp():
            aboveTopLeft = findBlock(this.x, this.y, this.z - 1, ignoreWater = true)
            aboveTopRight = findBlock(rightSide, this.y, this.z - 1, ignoreWater = true)
            belowTopRight = findBlock(rightSide, underSide, this.z - 1, ignoreWater = true)
            belowTopLeft = findBlock(this.x, underSide, this.z - 1, ignoreWater = true)
            if aboveTopLeft or aboveTopRight or belowTopLeft or belowTopRight:
                this.collision["up"] = true
 
        doCollisionToUp()
 
        def doCollisionToDown():
            aboveBottomLeft = findBlock(this.x, this.y, bottomSide + 1, ignoreWater = true)
            aboveBottomRight = findBlock(rightSide, this.y, bottomSide + 1, ignoreWater = true)
            belowBottomRight = findBlock(rightSide, underSide, bottomSide + 1, ignoreWater = true)
            belowBottomLeft = findBlock(this.x, underSide, bottomSide + 1, ignoreWater = true)
            if aboveBottomLeft or aboveBottomRight or belowBottomRight or belowBottomLeft:
                this.collision["down"] = true
 
        doCollisionToDown()
 
        def checkForBeingInsideOfABlock():
            center = findBlock(this.x + this.width/2, this.y - this.height/2, this.z + this.width/2, extraInfo = true)
            this.collision["insideOfBlock"] = center["type"]
 
        checkForBeingInsideOfABlock()
 
        temporaryNumber = (this.y - this.height) + blockSize + 3
        # SEPARATE THESE LATER INTO FUNCTIONS
        aboveToTopRight = findBlock(rightSide + this.xv + 3, temporaryNumber, this.z, ignoreWater = true)
        aboveToBottomRight = findBlock(rightSide + this.xv + 3, temporaryNumber, bottomSide, ignoreWater = true)
        if aboveToTopRight or aboveToBottomRight:
            this.collision["aboveRight"] = true
 
        aboveToTopLeft = findBlock(this.x + this.xv - 3, temporaryNumber, this.z, ignoreWater = true)
        aboveToBottomLeft = findBlock(this.x + this.xv - 3, temporaryNumber, bottomSide, ignoreWater = true)
        if aboveToTopLeft or aboveToBottomLeft:
            this.collision["aboveLeft"] = true
 
        aboveToLeftUp = findBlock(this.x, temporaryNumber, this.z + this.zv - 3, ignoreWater = true)
        aboveToRightUp = findBlock(rightSide, temporaryNumber, this.z + this.zv - 3, ignoreWater = true)
        if aboveToLeftUp or aboveToRightUp:
            this.collision["aboveUp"] = true
        
        aboveToRightDown = findBlock(rightSide, temporaryNumber, bottomSide + this.zv + 3, ignoreWater = true)
        aboveToLeftDown = findBlock(this.x, temporaryNumber, bottomSide + this.zv + 3, ignoreWater = true)
        if aboveToLeftDown or aboveToRightDown:
            this.collision["aboveDown"] = true
 
 
 
 
 
        currentMaxHorizontalSpeed = this.maxHorizontalSpeed
        if this.collision["insideOfBlock"] == "water":
            currentMaxHorizontalSpeed = this.maxHorizontalSpeed / 2
 
         # x and z axis movement
        if right and not this.collision["right"]:
            if this.xv < currentMaxHorizontalSpeed:
                this.xv += this.acceleration
 
        if left and not this.collision["left"]:
            if this.xv > -currentMaxHorizontalSpeed:
                this.xv -= this.acceleration
 
        if up and not this.collision["up"]:
            if this.zv > -currentMaxHorizontalSpeed:
                this.zv -= this.acceleration
 
        if down and not this.collision["down"]:
            if this.zv < currentMaxHorizontalSpeed:
                this.zv += this.acceleration
 
         # y axis movement
        if space:
            if this.collision["insideOfBlock"] == "water":
                # do water stuff
                jumpForce = this.normalJumpForce / 3
 
                this.yv = jumpForce
            else:
                if this.collision["below"]:
                    # do jump stuff
                    jumpForce = this.normalJumpForce
 
                    this.yv = jumpForce
            
 
 
         # do gravity
        if not this.collision["below"]:
            yvChange = gravity
            if this.collision["insideOfBlock"] == "water":
                yvChange /= 5
            this.yv -= yvChange
        elif this.yv < 0:
            this.yv = 0
            this.y = this.blockCoord[1] * blockSize + this.height
            # re-do collisions, hopefully fixes colliding with walls while hitting
            # the ground hard, looks like it didn't fix it?
            #doCollisionToDown()
            #doCollisionToLeft()
            #doCollisionToUp()
            #doCollisionToRight()
         # don't let player fall out of the world
        if this.y < -300:
            this.y = chunkSize[1] * blockSize
            this.yv = 0
 
         # don't let player go through ceilings
        if this.collision["above"]:
            if this.yv > 0:
                this.y -= this.yv
                this.yv = 0
 
         # wall collision
         # and block step up (go up blocks without jumping
 
 
        this.booleans["blockStepUsed"] = false
 
        if this.collision["up"]:
            a = this.collision["below"]
            b = not this.collision["aboveUp"]
            c = not this.booleans["blockStepUsed"]
            d = up
            if a and b and c and d:
                this.y += blockSize
                # update collision, since player's been moved a lot
                doCollisionToDown()
                doCollisionToLeft()
                doCollisionToRight()
                this.booleans["blockStepUsed"] = true
            else:
                this.z += abs(this.zv)
                this.zv = 0
                this.z += 1
        if this.collision["right"]:
            a = this.collision["below"]
            b = not this.collision["aboveRight"]
            c = not this.booleans["blockStepUsed"]
            d = right
            if a and b and c and d:
                this.y += blockSize
                # update collision, since player's been moved a lot
                doCollisionToDown()
                doCollisionToLeft()
                doCollisionToUp()
                this.booleans["blockStepUsed"] = true
            else: 
                this.x -= abs(this.xv)
                this.xv = 0
                this.x -= 1
 
        if this.collision["left"]:
            a = this.collision["below"]
            b = not this.collision["aboveLeft"]
            c = not this.booleans["blockStepUsed"]
            d = left
            if a and b and c and d:
                this.y += blockSize
                # update collision, since player's been moved a lot
                doCollisionToDown()
                doCollisionToRight()
                doCollisionToUp()
                this.booleans["blockStepUsed"] = true
            else:
                this.x += abs(this.xv)
                this.xv = 0
                this.x += 1
            
        if this.collision["down"]:
            a = this.collision["below"]
            b = not this.collision["aboveDown"]
            c = not this.booleans["blockStepUsed"]
            d = down
            if a and b and c and d:
                this.y += blockSize
                # update collision, since player's been moved a lot
                doCollisionToLeft()
                doCollisionToRight()
                doCollisionToUp()
                this.booleans["blockStepUsed"] = true
            else:
                this.x -= abs(this.zv)
                this.zv = 0
                this.z -= 1
       
 
 
         
        # force player speed cap
        if this.xv > currentMaxHorizontalSpeed:
            this.xv = currentMaxHorizontalSpeed
        if this.xv < -currentMaxHorizontalSpeed:
            this.xv = -currentMaxHorizontalSpeed
 
        if this.zv > currentMaxHorizontalSpeed:
            this.zv = currentMaxHorizontalSpeed
        if this.zv < -currentMaxHorizontalSpeed:
            this.zv = -currentMaxHorizontalSpeed
        
         # friction is handled below
        if (not left and not right) or (left and right):
            this.xv -= this.xv / this.slipperyness
            if this.xv > -0.1 and this.xv < 0.1:
                this.xv = 0
        if (not up and not down) or (up and down):
            this.zv -= this.zv / this.slipperyness
            if this.zv > -0.1 and this.zv < 0.1:
                this.zv = 0
        
 
 
         # don't let player get stuck inside of blocks
        if this.collision["insideOfBlock"] != "air":
            if this.collision["insideOfBlock"] != "water":
                this.y += 5
        
 
         # do all the position updates that other things use
        this.xv = round(this.xv * 100) / 100
        this.yv = round(this.yv * 100) / 100
        this.zv = round(this.zv * 100) / 100
 
        this.x += (this.xv * deltaTime)
        this.y += (this.yv * deltaTime)
        this.z += (this.zv * deltaTime)
 
        
        
 
        this.position = (this.x, this.y, this.z)
 
 
 
    def giveItem(this, item, count = 1):
        
        def checkForStackables(container, done, count, item):
            if not done and item.stackable:
                for slot in container:
                    if slot["contents"] != "empty":
                        if slot["contents"].name == item.name:
                            if slot["count"] != maxStackSize:
                                
 
                                addedCount = count + slot["count"]
                                if addedCount <= maxStackSize:
 
                                    slot["count"] = addedCount
                                    return true
                                elif addedCount > maxStackSize:
                                    slot["count"] = maxStackSize
                                    count = addedCount - maxStackSize
                                    break
            return done
            
        def checkForEmptySlots(container, done, count, item):
            if not done:
                for slot in container:
                    if slot["contents"] == "empty":
                        slot["contents"] = item
                        slot["count"] = count
                        
                        
                        return true
            return done
 
            
 
        done = false
 
        done = checkForStackables(this.hotbar, done, count, item)
        done = checkForStackables(this.inventory, done, count, item)
 
        done = checkForEmptySlots(this.hotbar, done, count, item)
        done = checkForEmptySlots(this.inventory, done, count, item)
 
        if not done:
            print("giving the item failed")
 
        return done
 
 
 
    def doInventoryThings(this):
 
        
        def toggleInventoryVisibility():
            if keysPressed[pygame.K_e]:
                if this.otherInventoryData["open"]:
                    this.otherInventoryData["open"] = false
                else:
                    this.otherInventoryData["open"] = true
 
            for slot in this.inventory:
                if slot["contents"] != "empty":
                    slot["contents"].slotId = slot["slotId"]
            for slot in this.hotbar:
                if slot["contents"] != "empty":
                    slot["contents"].slotId = slot["slotId"]
        toggleInventoryVisibility()
 
 
        def adjustMouseSelectedBlockHeight():
            # change the selected height of the mouse
            mouse.selectedY = this.y
 
            if keysPressed[pygame.K_PERIOD]:
                if mouse.selectedYChange < this.verticalBlockReach:
                    mouse.selectedYChange += 1
                
            if keysPressed[pygame.K_COMMA]:
                if mouse.selectedYChange > -this.verticalBlockReach:
                    mouse.selectedYChange -= 1
 
            mouse.selectedY += mouse.selectedYChange * blockSize
            
 
            if mouse.selectedY <= 0:
                mouse.selectedY = blockSize
            if mouse.selectedY >= chunkSize[1] * blockSize:
                mouse.selectedY = chunkSize[1] * (blockSize - 1)
        adjustMouseSelectedBlockHeight()
 
 
        def changeSelectedHotbarSlot():
            if not this.otherInventoryData["open"]:
                for i in range(1, 10):
                    keyboardInput = getattr(pygame, "K_" + str(i))
                    if keysPressed[keyboardInput]:
                        this.otherInventoryData["currentHotbarSlot"] = i - 1
        changeSelectedHotbarSlot()
 
 
        def dropItems():
            # drop items from the hotbar
            if keysPressed[pygame.K_q]:
                if not this.otherInventoryData["open"]:
                    currentHotbarSlot = this.otherInventoryData["currentHotbarSlot"]
                    item = this.hotbar[currentHotbarSlot]["contents"]
 
                    if item != "empty":
 
                        x = this.x + this.width/2 - itemEntitySize/2
                        y = this.y - this.height/2
                        z = this.z + this.width/2 - itemEntitySize/2
 
                        # figure out velocity for angle of player to mouse
 
                        xDiff = mouse.cameraRelativeX - x
                        yDiff = mouse.cameraRelativeZ - z
 
                        angle = math.atan2(yDiff, xDiff)                        
 
                        xv = math.cos(angle) * 3
                        yv = 2
                        zv = math.sin(angle) * 3
 
                        count = 1
 
                        item.drop(x, y, z, xv, yv, zv, this, count)
        dropItems()
 
 
        def hotbarHeldItemStuff():
            if not this.otherInventoryData["open"]:
                index = this.otherInventoryData["currentHotbarSlot"]
                slotData = this.hotbar[index]
                item = slotData["contents"]
 
                if mouse.buttons["pressed"]["left"] or mouse.buttons["left"]:
                    this.doStuffOnLeftClick(item)
 
                if item != "empty":
 
                    if mouse.buttons["pressed"]["right"]:
                        item.RMBPressedAction(this)
                    elif mouse.buttons["right"]:
                        item.RMBAction(this)
                else:
                    this.doStuffOnRightClick
        hotbarHeldItemStuff()
 
 
        def mouseInteractionWithInventory():
            mouse.inPlayerInventory = false
            mouse.inPlayerHotbar = false
            mouse.inPlayerCraftingAndArmor = false
            mouse.inPlayerCraftingTable = false
            mouse.inASlot = false
 
            def inventoryContentInteraction(container):
                if container == "hotbar":
                    invSection = this.hotbar
                    otherInvSection = this.inventory
                elif container == "inventory":
                    invSection = this.inventory
                    otherInvSection = this.hotbar
                elif container == "crafting":
                    invSection = this.crafting[this.crafting["gridSize"]]["slots"]
                    otherInvSection = this.inventory
                elif container == "armor":
                    invSection = this.armor
                    otherInvSection = this.inventory
                def checkStackablesInOtherInvSection(amountToMove, item, done):
                            """
                            amountToMove: either "max" or an int less than 64 \n
                            done: used to see if the interaction is done
                            """
 
                            if item != "empty" and not done:
                                if item.stackable:
                                    for otherSlot in otherInvSection:
                                        otherItem = otherSlot["contents"]
 
                                        if otherItem != "empty" and otherSlot["count"] < maxStackSize:
                                            if otherItem.stackable and item.name == otherItem.name:
                                                if otherSlot["count"] == maxStackSize:
                                                    break
                                                if amountToMove == "max":
                                                    movingCount = slot["count"] + otherSlot["count"]
                                                        # combine the count
                                                    if movingCount <= maxStackSize:
                                                        
 
                                                        if slot == this.crafting[this.crafting["gridSize"]]["slots"]["resultSlot"]:
                                                            movingCount = slot["count"]
                                                            movingCount *= this.crafting["possibleCrafts"]
 
                                                            if movingCount + otherSlot["count"] <= maxStackSize:
 
                                                                for key, craftingSlot in this.crafting[this.crafting["gridSize"]]["slots"].items():
                                                                    if key != "resultSlot":
                                                                        # subtract the amount of items crafted
                                                                        craftingSlot["count"] -= this.crafting["possibleCrafts"]
                                                                        
 
                                                                        if craftingSlot["count"] <= 0:
 
                                                                            craftingSlot["count"] = 0
                                                                            craftingSlot["contents"] = "empty"
                                                            
                                                                otherSlot["count"] += movingCount
 
                                                        else:
                                                            otherSlot["count"] = movingCount
                                                                        
                                                            slot["count"] = 0
                                                            slot["contents"] = "empty"
 
                                                        
                                                        
                                                        done = true
                                                        return true
 
                                                    # make the other stack full, reduce item count
                                                    # in first slot so the later update catches it
                                                    elif movingCount > maxStackSize:
                                                        if slot != this.crafting[this.crafting["gridSize"]]["slots"]["resultSlot"]:
                                                            slot["count"] = movingCount - maxStackSize
                                                            otherSlot["count"] = maxStackSize
 
 
                                                else: # not moving max amount
                                                    if slot != this.crafting[this.crafting["gridSize"]]["slots"]["resultSlot"]:
                                                        otherSlotNewCount = otherSlot["count"] + amountToMove
                                                        slotNewCount = slot["count"] - amountToMove
 
                                                        # subtract from first slot, add to the second if possible
                                                        if otherSlotNewCount <= maxStackSize and slotNewCount >= 0:
                                                            slot["count"] = slotNewCount
                                                            otherSlot["count"] = otherSlotNewCount
 
                                                            if slotNewCount == 0:
                                                                slot["contents"] = "empty"
 
                                                            return true
                            return done
 
                def checkEmptySlotsInOtherInvSection(amountToMove, item, done):
                    """
                    amountToMove: either "max" or an int less than 64 \n
                    done: used to see if the interaction is done
                    """
                    if item != "empty" and not done:
                        for otherSlot in otherInvSection:
                            otherItem = otherSlot["contents"]
 
                            if otherItem == "empty":
                                if amountToMove == "max":
                                    otherSlot["contents"] = slot["contents"]
                                    
 
                                    if slot == this.crafting[this.crafting["gridSize"]]["slots"]["resultSlot"]:
 
                                        craftedCount = slot["count"] * this.crafting["possibleCrafts"]
                                        if craftedCount <= maxStackSize:
 
                                            otherSlot["count"] = craftedCount
 
                                            for key, craftingSlot in this.crafting[this.crafting["gridSize"]]["slots"].items():
                                                if key != "resultSlot":
                                                    # subtract one item from the slot, since it's consumed
                                                    craftingSlot["count"] -= this.crafting["possibleCrafts"]
 
                                                    if craftingSlot["count"] <= 0:
 
                                                        craftingSlot["count"] = 0
                                                        craftingSlot["contents"] = "empty"
                                    else:
                                        otherSlot["count"] = slot["count"]
 
                                    slot["contents"] = "empty"
                                    slot["count"] = 0
                                        
                                    
                                    return true
 
                                else: # not moving max amount
                                    if slot != this.crafting[this.crafting["gridSize"]]["slots"]["resultSlot"]:
 
                                        slotNewCount = slot["count"] - amountToMove
 
                                        # subtract from first slot, add to the second if possible
                                        if slotNewCount >= 0:
                                            slot["count"] = slotNewCount
                                            otherSlot["count"] = amountToMove
                                            otherSlot["contents"] = slot["contents"]
 
                                            if slotNewCount == 0:
                                                slot["contents"] = "empty"
                                        
                                            
                                            return true
                    return done
 
 
 
                def interactionForThisSlot(slot):
                        
                        item = slot["contents"]
                        
                        if slot["rect"].collidepoint(mouse.x, mouse.y):
                            # communicate rendering information via the mouse
                            
                            mouse.hoveredSlotId = slot["slotId"]
                            mouse.inASlot = true
 
 
                            def slotInteractionWithMouseItem(clickType):
                                        ctrlPressed = keys[0][pygame.K_LCTRL]
                                        if not keys[0][pygame.K_LSHIFT]:
                                            # try to pick up or swap the item in slot and mouse.heldItem
                                            mouseItem = mouse.heldItem["contents"]
                                            if mouseItem != "empty" and not ctrlPressed:
                                                if slot["slotId"] != "resultSlot":
                                                    if item != "empty":
                                                        if mouseItem.stackable and item.stackable and mouseItem.name == item.name:
                                                        
                                                            if clickType == "left click":
                                                                addedCount = mouse.heldItem["count"] + slot["count"]
                                                            elif clickType == "right click":
                                                                addedCount = slot["count"] + 1
                                                            
                                                            if addedCount <= maxStackSize:
                                                                if clickType == "left click":
 
                                                                    mouse.heldItem["contents"] = "empty"
                                                                    mouse.heldItem["count"] = 0
                                                                    
                                                                elif clickType == "right click":
                                                                    mouse.heldItem["count"] -= 1
                                                                    if mouse.heldItem["count"] <= 0:
                                                                        mouse.heldItem["contents"] = "empty"
 
 
                                                                slot["count"] = addedCount
 
 
                                                            elif addedCount > maxStackSize and clickType == "left click":
                                                                newMouseSlotCount = addedCount - maxStackSize
 
                                                                slot["count"] = maxStackSize
                                                                mouse.heldItem["count"] = newMouseSlotCount
                                                        elif clickType == "left click": # not stacking the item, swap it with mouse's item
 
                                                            newSlotCount = mouse.heldItem["count"]
                                                            newSlotItem = mouse.heldItem["contents"]
 
                                                            mouse.heldItem["count"] = slot["count"]
                                                            mouse.heldItem["contents"] = slot["contents"]
 
                                                            slot["count"] = newSlotCount
                                                            slot["contents"] = newSlotItem
 
 
                                                    else: # clicked item has nothing there, put mouse contents there
                                                        if clickType == "left click":
 
                                                            slot["contents"] = mouse.heldItem["contents"]
                                                            slot["count"] = mouse.heldItem["count"]
 
                                                            mouse.heldItem["count"] = 0
                                                            mouse.heldItem["contents"] = "empty"
                                                        elif clickType == "right click":
 
                                                            slot["contents"] = mouse.heldItem["contents"]
                                                            slot["count"] = 1
                                                            mouse.heldItem["count"] -= 1
                                                            if mouse.heldItem["count"] <= 0:
                                                                mouse.heldItem["contents"] = "empty"
 
 
                                            else: # mouse has no item in it, see if the item can be picked up
                                                if item != "empty":
 
                                                    if clickType == "left click":
 
                                                        mouse.heldItem["count"] = slot["count"]
                                                        mouse.heldItem["contents"] = slot["contents"]
 
                                                        slot["count"] = 0
                                                        slot["contents"] = "empty"
 
                                                        # do special things if its the crafting result
                                                        if slot == this.crafting[this.crafting["gridSize"]]["slots"]["resultSlot"]:
                                                            #this.crafting["possibleCrafts"] -= 1
                                                            for key, craftingSlot in this.crafting[this.crafting["gridSize"]]["slots"].items():
                                                                if key != "resultSlot":
                                                                    # subtract one item from the slot, since it's consumed
                                                                    if craftingSlot["count"] > 1:
 
                                                                        craftingSlot["count"] -= 1
                                                                    else: # just remove the item entirely
 
                                                                        craftingSlot["count"] = 0
                                                                        craftingSlot["contents"] = "empty"
 
                                                    elif clickType == "right click":
                                                        # just disable right clicking on a result slot
                                                        if slot != this.crafting[this.crafting["gridSize"]]["slots"]["resultSlot"]:
                                                            # you can't do this with unstackable items
                                                            if slot["contents"].stackable:
                                                                if slot["count"] > 1:
                                                                    if not ctrlPressed:
                                                                    
 
                                                                        newMouseCount = math.ceil(slot["count"]/2)
                                                                        newSlotCount = slot["count"] - newMouseCount
 
                                                                        mouse.heldItem["contents"] = slot["contents"]
                                                                        mouse.heldItem["count"] = newMouseCount
 
                                                                        slot["count"] = newSlotCount
                                                                    else: # put one item into mouse
                                                                        mouse.heldItem["count"] = 1
                                                                        mouse.heldItem["contents"] = slot["contents"]
 
                                                                        slot["count"] -= 1
 
 
                            
                            done = false
                            # fast transfer options
                            if mouse.buttons["pressed"]["left"]:
                                
                                if keys[0][pygame.K_LSHIFT]:
                                    # move all items from this slot (if possible)
                                    done = checkStackablesInOtherInvSection("max", item, done)
                                    done = checkEmptySlotsInOtherInvSection("max", item, done)
                                    
                                    
                            
                                if keys[0][pygame.K_LCTRL]:
                                    # move a single item from this slot (if possible)
                                    done = checkStackablesInOtherInvSection(1, item, done)
                                    done = checkEmptySlotsInOtherInvSection(1, item, done)
                                       
 
                            if not done:
                                if mouse.buttons["pressed"]["left"]:
                                    slotInteractionWithMouseItem("left click")
                                elif mouse.buttons["pressed"]["right"]:
                                    slotInteractionWithMouseItem("right click")
                                    
 
 
 
 
                if container != "crafting" and container != "armor":
                    for slot in invSection:
                        interactionForThisSlot(slot)
                else:
                    for key, slot in invSection.items():
                        interactionForThisSlot(slot)
 
 
 
 
            if this.otherInventoryData["open"]:
                mouse.inPlayerCraftingAndArmor = this.otherInventoryData["craftingAndArmorRect"].collidepoint(mouse.x, mouse.y)
                mouse.inPlayerInventory = this.otherInventoryData["inventoryRect"].collidepoint(mouse.x, mouse.y)
                mouse.inPlayerHotbar = this.otherInventoryData["hotbarRect"].collidepoint(mouse.x, mouse.y)
                mouse.inPlayerCraftingTable = this.otherInventoryData["craftingTableRect"].collidepoint(mouse.x, mouse.y)
 
                if mouse.inPlayerInventory:
                    inventoryContentInteraction("inventory")
                if mouse.inPlayerHotbar:
                    inventoryContentInteraction("hotbar")
                if mouse.inPlayerCraftingAndArmor:
                    inventoryContentInteraction("crafting")
                    inventoryContentInteraction("armor")
        
 
            # attempt to place mouse's item back in the player's inventory
            if not this.otherInventoryData["open"]:
 
                if mouse.heldItem["contents"] != "empty":
                    item = mouse.heldItem["contents"]
                    
 
                    def checkForStackables(container, done):
                        if not done:
                            
                            for slot in container:
                                if slot["contents"] != "empty" and mouse.heldItem["contents"] != "empty":
                                    if slot["contents"].stackable and mouse.heldItem["contents"].stackable:
                                        if slot["contents"].name == mouse.heldItem["contents"].name:
                                            if slot["count"] == maxStackSize:
                                                break
                                            mouseItem = mouse.heldItem["contents"]
                                            mouseCount = mouse.heldItem["count"]
 
                                            item = slot["contents"]
                                            count = slot["count"]
 
                                            addedCount = count + mouseCount
 
                                            if addedCount <= maxStackSize:
                                                slot["count"] = addedCount
                                                mouse.heldItem["count"] = 0
                                                mouse.heldItem["contents"] = "empty"
 
                                                return true
                                            
                                            if addedCount > maxStackSize:
                                                newMouseCount = addedCount - maxStackSize
 
                                                slot["count"] = maxStackSize
                                                mouse.heldItem["count"] = newMouseCount
 
                                                return true
                        return done
 
                    def checkForEmptySlots(container, done):
                        if not done:
 
                            for slot in container:
                                if slot["contents"] == "empty":
                                    item = mouse.heldItem["contents"]
                                    count = mouse.heldItem["count"]
 
                                    slot["contents"] = item
                                    slot["count"] = count
 
                                    mouse.heldItem["contents"] = "empty"
                                    mouse.heldItem["count"] = 0
                                    
                                    return true
                        return done
                        
                                    
                                    
 
 
                    done = false
 
                    done = checkForStackables(this.hotbar, done)
                    done = checkForStackables(this.inventory, done)
 
                    done = checkForEmptySlots(this.hotbar, done)
                    done = checkForEmptySlots(this.inventory, done)
 
                    
 
                    
 
                    if not done:
 
                        # center of player
                        x = this.x + this.width/2
                        y = this.y - this.height/2
                        z = this.z + this.width/2
 
                        # figure out velocity for angle of player to mouse
 
                        xDiff = mouse.cameraRelativeX - x
                        yDiff = mouse.cameraRelativeZ - z
 
                        angle = math.atan2(yDiff, xDiff)                        
 
                        xv = math.cos(angle) * 3
                        yv = 2
                        zv = math.sin(angle) * 3
 
                        item.drop(x, y, z, xv, yv, zv)
        mouseInteractionWithInventory()   
 
        def recipeChecksAndStuff():
            # dict with total amount of each item in crafting slots
            this.totalCraftingContents = {}
            this.isCrafting = false
            this.crafting["possibleCrafts"] = 0
 
 
            
            for key, slot in this.crafting[this.crafting["gridSize"]]["slots"].items():
                if key != "resultSlot":
                    if slot["contents"] != "empty":
                        if not this.totalCraftingContents.get(slot["contents"].name, false):
                            
                            this.totalCraftingContents[slot["contents"].name] = 0
                        
                        this.totalCraftingContents[slot["contents"].name] += 1
            
            lowestItemCount = maxStackSize
            
 
            for key, slot in this.crafting[this.crafting["gridSize"]]["slots"].items():
                if key != "resultSlot":
                    if slot["contents"] != "empty":
                        if slot["count"] < lowestItemCount:
                            lowestItemCount = slot["count"]
 
            
            
            
            this.crafting["possibleCrafts"] = lowestItemCount
 
 
 
            if this.crafting["possibleCrafts"] > 0:
                this.isCrafting = true
 
            foundARecipe = false
            recipeThatWasFound = None
 
            def exactRecipeDetection(recipe):
                
                
                if this.totalCraftingContents == recipe["requiredItems"]:
                    pass
 
            
 
                return false, None
            
            def nearExactRecipeLogic(recipe):
                
                def checkForSpecificItemInSlot(instructions):
                    """
                    startingItemName, directions, operators, and items are contained in instructions
 
                    example:
                    direction = ["left", "right"], operator = ["xor"], items = ["planks", "planks"]
                    
                    
                    checks for "planks" in the slot to the left and the slot to the right
                    
                    compares the values of does this slot have this specific item
                    """
 
                    def checkADirection(direction, startingSlotId):
                        gridSize = this.crafting["gridSize"]
 
                        if direction == "up":
 
                            testSlotId = startingSlotId - gridSize
                            if testSlotId >= 0 and testSlotId < (gridSize**2):
 
                                item = this.crafting[gridSize]["slots"][testSlotId]["contents"]
                                
                                if item != "empty":
                                    return item.name
                                return "empty"
                            else:
                                
                                return "no item"
                            
                        elif direction == "down":
                            testSlotId = startingSlotId + gridSize
                            
                            if testSlotId >= 0 and testSlotId < (gridSize**2):
                                
                                item = this.crafting[gridSize]["slots"][testSlotId]["contents"]
                                
                                if item != "empty":
                                    return item.name
                                return "empty"
                                
                            else:
                                return "no item"
                                
                        elif direction == "right":
                            testSlotId = startingSlotId + 1
                            temporaryGridSize = gridSize - 1
 
                            if testSlotId >= 0 and testSlotId < (gridSize**2):
 
                                if testSlotId == gridSize:
                                    return "no item"
 
                                
                                while testSlotId > temporaryGridSize:
 
                            
                                    temporaryGridSize += gridSize
 
                                    if temporaryGridSize >= gridSize:
                                        return "no item"
                                    if testSlotId == temporaryGridSize - 1:
                                        return "no item"
 
                                item = this.crafting[gridSize]["slots"][testSlotId]["contents"]
                                if item != "empty":
                                    return item.name
                                return "empty"
                            
                        elif direction == "left":
                            print("no code written for left yet lol")
                                
                        
 
                        return "no item"
 
 
                            
 
                
                    for slotId, slot in this.crafting[this.crafting["gridSize"]]["slots"].items():
                        if slotId != "resultSlot":
                            item = slot["contents"]
                            if item != "empty":
                                if item.name == instructions["startingItemName"]:
                                    
                                    usesOperators = len(instructions["operators"]) > 0
 
                                    directions = instructions["directions"]
                                    operators = instructions["operators"]
                                    items = instructions["items"]
 
                                    if not usesOperators:
                                        # only checks one direction (not gonna be common)
                                        slotFound = checkADirection(directions[0], slotId)
                                        if slotFound == items[0]:
                                            return true
 
                                    else: # this recipe uses operators, will be more complicated
                                        lenOfDirections = len(directions)
                                        lenOfItems = len(items)
                                        lenOfOperators = len(operators)
 
                                        slotsChecked = []
 
                                        
 
                                        for i in range(lenOfDirections):
                                            currentDirection = directions[i]
                                            currentItem = items[i]
                                            
                                            slotDictThing = {
                                                "direction": currentDirection,
                                                "containsCorrectItem": false
                                            }
 
                                            itemName = checkADirection(currentDirection, slotId)
 
                                            if itemName == items[i]:
                                                
                                                slotDictThing["containsCorrectItem"] = true
 
 
                                            slotsChecked.append(slotDictThing)
 
                                        conditions = []
 
                                        for i in slotsChecked:
                                            conditions.append(i["containsCorrectItem"])                                        
 
                                        hasAnEvenNumberOfConditions = len(conditions)%2 == 0
                                        
 
                                        length = len(conditions)
                                        if not hasAnEvenNumberOfConditions:
                                            length -= 1
                                        i = 1
 
                                        betterConditionsList = []
 
                                        while i < length:
 
                                            conditionA = conditions[i - 1]
                                            conditionB = conditions[i]
 
                                            conditionList = [conditionA, conditionB]
                                            
                                            betterConditionsList.append(conditionList)
 
                                            i += 2 # increment by two, grouping together conditions
 
 
 
                                        for i in range(lenOfOperators):
                                            # i should probably modify how i am doing operators to specify which
                                            # directions should use what operators (example: right "and" left)
                                            # another example: up "neither" down
                                            # and also should probably add in the ability to specify multiple
                                            # directions for something, ex top right is up and right
                                            # or i could just have "top right" be a valid direction
                                            # yeah ima just do that
                                            # or i could have the directions be like {up: 2}, {right: 1},
                                            # that would be up 2 slots, right 1 slot
                                            # operators still need to be grouped with directions at some point though
 
                                            operator = operators[i]
                                            conditionA, conditionB = betterConditionsList[i]
                                            
 
                                            if operator == "xor":
                                                if (conditionA or conditionB) and (conditionA != conditionB):
                                                    return true
 
                                            if operator == "and":
                                                if conditionA and conditionB:
                                                    return true
 
                                            if operator == "neither":
                                                if not conditionA and not conditionB:
                                                    return true
 
                                            if operator == "or":
                                                if conditionA or conditionB:
                                                    return true
                                                
                                            #print("didn't fulfill any checks")
 
 
 
 
                    return false
 
                                    
 
 
 
                    
                if this.totalCraftingContents == recipe["requiredItems"]:
            
                    instructions = recipe["recipeInstructions"]
 
                    foundARecipe = checkForSpecificItemInSlot(instructions)
 
                    if foundARecipe:
                        return true, recipe
 
 
                return false, None
 
            def shapelessRecipeLogic(recipe):
               
                if this.totalCraftingContents == recipe["requiredItems"]:
                    return true, recipe
                
 
 
 
                return false, None
 
            
            
            
            if this.isCrafting:
 
                for recipe in recipes[this.crafting["gridSize"]]["exact"].values():
                    foundARecipe, recipeThatWasFound = exactRecipeDetection(recipe)
                    if foundARecipe:
                        break
 
                if not foundARecipe:
                    for recipe in recipes[this.crafting["gridSize"]]["nearExact"].values():
                        foundARecipe, recipeThatWasFound = nearExactRecipeLogic(recipe)
                        if foundARecipe:
                            break
                
                if not foundARecipe:
                    for recipe in recipes[this.crafting["gridSize"]]["shapeless"].values():
                        foundARecipe, recipeThatWasFound = shapelessRecipeLogic(recipe)
                        if foundARecipe:
                            break
 
                    
            if foundARecipe:
                this.crafting[this.crafting["gridSize"]]["slots"]["resultSlot"]["contents"] = recipeThatWasFound["output"]
                this.crafting[this.crafting["gridSize"]]["slots"]["resultSlot"]["count"] = recipeThatWasFound["outputCount"]
            else:
                this.crafting[this.crafting["gridSize"]]["slots"]["resultSlot"]["contents"] = "empty"
                this.crafting[this.crafting["gridSize"]]["slots"]["resultSlot"]["count"] = 0
 
 
 
            
                        
 
        recipeChecksAndStuff()
 
 
        
    def handleTimers(this):
        for key, timerValue in this.timers.items():
            if timerValue > 0:
                timerValue -= 1
            if timerValue < 0:
                timerValue += 1
            if timerValue != 0:
                print(str(key) + " " + str(timerValue))
            this.timers[key] = timerValue
 
 
 
    def updateCamera(this):
        camera.x -= round((camera.x - this.x + camera.centerTheCamera[0]) / camera.smoothness)
        camera.y = this.y
        camera.z -= round((camera.z - this.z + camera.centerTheCamera[1]) / camera.smoothness)
        
        camera.currentChunk = getChunkCoord(camera.x, camera.z)
 
 
 
    def updateImageThings(this):
        imageX = this.x - camera.x
        imageY = this.z - camera.z
        
        coordinate = (imageX, imageY)
        this.imageData = (this.image, coordinate)
 
 
 
    def doStuff(this, deltaTime):
        # need to update mouse's camera relative things here, don't want circular imports
        mouse.cameraRelativeX = round((this.x + mouse.x) - canvasWidth/2)
        mouse.cameraRelativeZ = round((this.z + mouse.y) - canvasHeight/2)
        mouse.cameraRelativePos = (mouse.cameraRelativeX, mouse.cameraRelativeZ)
        
        this.generalMovement(deltaTime)
        this.doInventoryThings()
        
        this.handleTimers()
        
        this.updateCamera()
        this.updateImageThings()
 
 
 
    def positionInSpawnArea(this):
        for y in range(chunkSize[1] - 1):
            if findBlock(0, y * blockSize, 0):
                if not findBlock(0, (y + 1) * blockSize, 0):
                    this.y = (y * blockSize) + this.height
                    break
            else:
                this.y = chunkSize[1] * blockSize
 
 
 
    def doStuffOnRightClick(this, heldItem = "empty"):
        hoveredBlockType = mouse.hoveredBlock["block"]["type"]
        
        if hoveredBlockType == "crafting table":
            this.otherInventoryData["showCraftingAndArmor"] = false
            this.otherInventoryData["showCraftingTable"] = true
            this.crafting["gridSize"] = 3
 
 
    def doStuffOnLeftClick(this, currentlyHeldItem = "empty"):
        item = currentlyHeldItem
 
        breakingPower = 1
        breakingSpeed = 1
        breakingType = "none"
        attack = 1
        knockback = 1
        slowestBreakSpeed = 20/fps
 
        if item != "empty":
            if item.itemType == "ToolItem":
                breakingPower = item.breakingPower
                breakingSpeed = item.breakingSpeed
                breakingType = item.breakingType
                attack = item.attack
                knockback = item.knockback
            
        
        # run a test for interaction with entitys, hitting them, etc
        # if colliderect(mouse.x, mouse.y) with an entity's hitbox or something
 
        # else:
        # break blocks
        if this.currentBreakingBlock != mouse.hoveredBlock["block"]:
            this.blockBreakProgress = 0
 
        if this.canReachSelectedBlock:
 
            this.currentBreakingBlock = mouse.hoveredBlock["block"]
            block = this.currentBreakingBlock
            
            if block["hardness"] != "infinity":
                correctTool = false
                powerfulEnoughTool = false
 
                if breakingPower >= block["hardness"]:
                    powerfulEnoughTool = true
                if breakingType == block["effectiveTool"]:
                    correctTool = true
                
                
                if powerfulEnoughTool and correctTool:
                    this.blockBreakProgress += breakingSpeed / fps
                else:
 
                    this.blockBreakProgress += slowestBreakSpeed / fps
 
 
                
 
 
 
                # breaking stuff is based on seconds of time,
                # in tools, the breaking speed is a percentage of a second per frame
 
                if this.blockBreakProgress >= fps:
                    this.blockBreakProgress = 0
 
                    if correctTool or block["dropsWithNoTool"]:
                    
                        itemData = PlaceableItem(block["type"])
 
                        chunkCoord = mouse.hoveredBlock["chunkCoord"]
                        blockCoord = mouse.hoveredBlock["blockCoord"]
                        x = (chunkCoord[0] * chunkSize[0]) * blockSize
                        y = blockCoord[1] * blockSize
                        z = (chunkCoord[1] * chunkSize[0]) * blockSize
 
                        x += blockCoord[0] * blockSize
                        z += blockCoord[2] * blockSize
 
                    
                    
                        count = 1
                        xv = random.randint(-3, 3)
                        zv = random.randint(-3, 3)
                        if true: # replace later with silk touch or something
                            if block["type"] == ("grass" or "snowy grass"):
                                itemData.name = "dirt"
                            if block["type"] == ("stone" or "snowy stone"):
                                itemData.name = "cobblestone"
                            
                            
                        entity = ItemEntity(itemData, count, x, y, z, xv, 5, zv)
                        entities.append(entity)
 
                    air = {
                        "type": "air",
                        "render": false,
                        "alphaValue": 255,
                        "hardness": "infinity",
                        "effectiveTool": "none"
                    }
 
                    chunks[chunkCoord]["data"][blockCoord] = air.copy()
 
                    smallScaleBlockUpdates(chunkCoord, blockCoord)
 
                
                
 
    def changeCraftingGrid(this, gridSize):
        
 
        # attempt to place items back into inventory
        
        done = false
 
        def checkStackables(slot, done):
            if slot["contents"] != "empty":
                if slot["contents"].stackable:
                    for otherSlot in this.inventory.values():
                        if otherSlot["contents"] != "empty":
                            if otherSlot["contents"].stackable:
                                newOtherSlotCount = slot["count"] + otherSlot["count"]
                                if newOtherSlotCount <= maxStackSize:
                                    otherSlot["count"] = newOtherSlotCount
                                    slot["count"] = 0
                                    slot["contents"] = 0
                                    return true
                                
                                else:
                                    slot["count"] -= newOtherSlotCount - maxStackSize
                                    otherSlot["count"] = maxStackSize
            return done
        
        def checkEmptySlots(slot, done):
            if slot["contents"] != "empty":
                for otherSlot in this.inventory.values():
                    if otherSlot["contents"] == "empty":
                        otherSlot["contents"] = slot["contents"]
                        otherSlot["count"] = slot["count"]
                        slot["contents"] = "empty"
                        slot["count"] = 0
                        return true
 
 
 
 
            return done
 
 
 
        for slotId, slot in this.crafting[this.crafting["gridSize"]]["slots"].items():
            if slotId != "resultSlot":
                done = checkStackables(slot, done)
                done = checkEmptySlots(slot, done)
 
            else:
                # figure out dropping these into inventory or ground
                slot["contents"] = "empty"
                slot["count"] = 0
 
 
                    
 
        if not done:
 
            # center of player
            x = this.x + this.width/2
            y = this.y - this.height/2
            z = this.z + this.width/2
 
            # figure out velocity for angle of player to mouse
 
            xDiff = mouse.cameraRelativeX - x
            yDiff = mouse.cameraRelativeZ - z
 
            angle = math.atan2(yDiff, xDiff)                        
 
            xv = math.cos(angle) * 3
            yv = 2
            zv = math.sin(angle) * 3
 
            for slotId, slot in this.crafting[this.crafting["gridSize"]]["slots"].items():
 
                item.drop(x, y, z, xv, yv, zv)
 
 
        if gridSize == 2:
            this.otherInventoryData["showCraftingAndArmor"] = true
            this.otherInventoryData["showCraftingTable"] = false
            this.crafting["gridSize"] = gridSize
        elif gridSize == 3:
            this.otherInventoryData["showCraftingAndArmor"] = false
            this.otherInventoryData["showCraftingTable"] = true
            this.crafting["gridSize"] = gridSize
                };
};
            
 
export let player = new Player();
 
 
  


showLoadingProgress("Player.mjs initialized")
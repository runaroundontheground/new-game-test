import {
    consoleLog, camera, blockSize, gravity, chunkSize, maxStackSize, entities, recipes, items,
    canvasWidth, canvasHeight, chunks, fps, itemEntitySize, keys, keysPressed, mouse, random, showLoadingProgress, Rect
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
            let slotSizeInPixels = Math.Math.round(inventoryWidthInPixels / widthOfInventoryInSlots);
 
            let gapBetweenSlots = Math.Math.round(slotSizeInPixels / 5);
 
 
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
 
            let craftingTableSizeInPixels = (Math.round(craftingAndArmorWidthInPixels), Math.round(craftingAndArmorHeightInPixels))
 
 
            let craftingAndArmorSizeInPixels = (Math.round(craftingAndArmorWidthInPixels), Math.round(craftingAndArmorHeightInPixels))
            
            let craftingAndArmorBackground = pygame.surface.Surface(craftingAndArmorSizeInPixels)
            craftingAndArmorBackground.fill(backgroundColor)
 
            let craftingTableBackground = pygame.Surface(craftingTableSizeInPixels)
            craftingTableBackground.fill(backgroundColor)
 
            let inventorySizeInPixels = (Math.round(inventoryWidthInPixels), Math.round(inventoryHeightInPixels))
 
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
 
            let hotbarSizeInPixels = (Math.round(inventorySizeInPixels[0]), Math.round(slotSizeInPixels + (gapBetweenSlots * 2)))
            let hotbarSurface = pygame.surface.Surface(hotbarSizeInPixels)
            hotbarSurface.fill(backgroundColor)
 
            if (alphaForUI < 255) {
                hotbarSurface.set_alpha(alphaForUI)
                inventoryBackground.set_alpha(alphaForUI)
                craftingAndArmorBackground.set_alpha(alphaForUI)
                slotSurface.set_alpha(alphaForUI)
            };
 
            let craftingAndArmorXForBlit = (canvasWidth - (craftingAndArmorWidthInPixels)) / 2 
            let craftingAndArmorYForBlit = (canvasHeight - (craftingAndArmorHeightInPixels + inventoryHeightInPixels))// - (slotSizeInPixels * craftingAndArmorHeightInSlots)
            craftingAndArmorYForBlit /= 2
 
            let craftingTableXForBlit = craftingAndArmorXForBlit
            let craftingTableYForBlit = craftingAndArmorYForBlit - slotSizeInPixels * 0
 
            let fontShift = font.size("1")
 
            this.craftingResultSlot = {
                "contents": "empty",
                "count": 0,
                2: {
                    "renderPosition": [0, 0],
                    "selectedSlotRenderPosition": [0, 0],
                    "itemCountRenderPosition": [0, 0],
                    "rect": Rect(0, 0, 0, 0), // used for mouse collision
                },
                3: {
                    "renderPosition": [0, 0],
                    "selectedSlotRenderPosition": [0, 0],
                    "itemCountRenderPosition": [0, 0],
                    "rect": Rect(0, 0, 0, 0), // used for mouse collision
                }
            }
 
            let craftingSlot = {
                "contents": "empty",
                "count": 0,
                2: {
                    "renderPosition": [0, 0],
                    "selectedSlotRenderPosition": [0, 0],
                    "itemCountRenderPosition": [0, 0],
                    "rect": Rect(0, 0, 0, 0), // used for mouse collision
                },
                3: {
                    "renderPosition": [0, 0],
                    "selectedSlotRenderPosition": [0, 0],
                    "itemCountRenderPosition": [0, 0],
                    "rect": Rect(0, 0, 0, 0), // used for mouse collision
                },
                "slotId": 0
            }
 
            let armorSlot = {
                "contents": "empty",
                "renderPosition": [0, 0],
                "selectedSlotRenderPosition": [0, 0],
                "rect": Rect(0, 0, 0, 0),
                "slotId": 0
            }
 
            this.isCrafting = false
 
            this.crafting = {
                2: {
                "slots": [
                    craftingSlot, craftingSlot,
                    craftingSlot, craftingSlot
                ],
                "resultSlot": 0
                },
                3: {
                    "slots": [
                    craftingSlot, craftingSlot,
                    craftingSlot, craftingSlot,
                    craftingSlot, craftingSlot,
                    craftingSlot, craftingSlot,
                    craftingSlot
                    ],
                    "resultSlot": 0
                },
                "gridSize": 2
            }
            this.totalCraftingContents = {}
            this.armor = [ // head, chest, legs, feet
                armorSlot,
                armorSlot,
                armorSlot,
                armorSlot
            ]
            
 
            // actually add content spots to the armor/crafting
            
 
            let resultSlot = craftingSlot
 
            // create output slot for player's crafting 2x2 grid
            let slotX = ((widthOfInventoryInSlots) * slotSizeInPixels)
            let slotY = (slotSizeInPixels * 1.5)
 
            let renderX = slotX + craftingAndArmorXForBlit + itemIconShift
            let renderY = slotY + craftingAndArmorYForBlit + itemIconShift
 
            let rectX = renderX - itemIconShift
            let rectY = renderY - itemIconShift
 
            
            
            craftingAndArmorBackground.blit(slotSurface, (slotX, slotY))
 
            resultSlot["renderPosition"] = [renderX, renderY]
            resultSlot["rect"] = Rect(rectX, rectY, slotSizeInPixels, slotSizeInPixels)
            resultSlot["selectedSlotRenderPosition"] = [rectX - gapBetweenSlots, rectY - gapBetweenSlots]
            resultSlot["itemCountRenderPosition"] = [rectX + slotSizeInPixels - fontShift[0] - 1, rectY + slotSizeInPixels - fontShift[1] - 1]
            resultSlot["slotId"] = "resultSlot"
 
            this.crafting[2].resultSlot = resultSlot;
 
 
 
 
 
 
            // create output slot for the 3x3 grid
            slotX = ((widthOfInventoryInSlots - 2) * slotSizeInPixels) + slotSizeInPixels * 1.7
            slotY = (slotSizeInPixels * 2.1)
 
            renderX = slotX + craftingTableXForBlit + itemIconShift
            renderY = slotY + craftingTableYForBlit + itemIconShift
 
            rectX = renderX - itemIconShift
            rectY = renderY - itemIconShift
 
            
            
            craftingTableBackground.blit(slotSurface, (slotX, slotY))
 
            resultSlot["renderPosition"] = [renderX, renderY]
            resultSlot["rect"] = Rect(rectX, rectY, slotSizeInPixels, slotSizeInPixels)
            resultSlot["selectedSlotRenderPosition"] = [rectX - gapBetweenSlots, rectY - gapBetweenSlots]
            resultSlot["itemCountRenderPosition"] = [rectX + slotSizeInPixels - fontShift[0] - 1, rectY + slotSizeInPixels - fontShift[1] - 1]
            resultSlot["slotId"] = "resultSlot"
 
            this.crafting[3]["slots"]["resultSlot"] = resultSlot
 
 
            craftingTableBackground.blit(slotSurface, (slotX, slotY))
           
 
 
            let slotId = 0
 
            // create and blit the crafting slots for the player's crafting grid
            for (let y = 0; y < 2; y++) {
                for (let x = 0; x < 2; x++) {
                    
                    
 
                    
                    slotX = ((widthOfInventoryInSlots - 4) * slotSizeInPixels) + (x * slotSizeInPixels) + ((x + 1) * gapBetweenSlots)
                    slotY = (slotSizeInPixels * 0.75) + (y * slotSizeInPixels + ((y + 1) * gapBetweenSlots))
 
                    renderX = slotX + craftingAndArmorXForBlit + itemIconShift
                    renderY = slotY + craftingAndArmorYForBlit + itemIconShift
 
                    rectX = renderX - itemIconShift
                    rectY = renderY - itemIconShift
 
                    let newCraftingSlot = craftingSlot
                    
                    
                    craftingAndArmorBackground.blit(slotSurface, (slotX, slotY))
                    newCraftingSlot["renderPosition"] = [renderX, renderY]
                    newCraftingSlot["rect"] = Rect(rectX, rectY, slotSizeInPixels, slotSizeInPixels)
                    newCraftingSlot["selectedSlotRenderPosition"] = [rectX - gapBetweenSlots, rectY - gapBetweenSlots]
                    newCraftingSlot["itemCountRenderPosition"] = [rectX + slotSizeInPixels - fontShift[0] - 1, rectY + slotSizeInPixels - fontShift[1] - 1]
                    newCraftingSlot["slotId"] = slotId
 
                    this.crafting[2]["slots"][slotId] = newCraftingSlot
 
                    slotId += 1
            };
        };
 
 
            slotId = 0
            // create and blit slots for the crafting table grid
            for (let y = 0; y < 3; y++) {
                for (let x = 0; x < 3; x++) {
                    slotX = ((widthOfInventoryInSlots - 6) * slotSizeInPixels) + (x * slotSizeInPixels) + ((x + 1) * gapBetweenSlots)
                    slotY = (slotSizeInPixels * 0.75) + (y * slotSizeInPixels + ((y + 1) * gapBetweenSlots))
 
                    renderX = slotX + craftingTableXForBlit + itemIconShift
                    renderY = slotY + craftingTableYForBlit + itemIconShift
 
                    rectX = renderX - itemIconShift
                    rectY = renderY - itemIconShift
 
                    
                    
                    let newCraftingSlot = craftingSlot
                    
                    
                    craftingTableBackground.blit(slotSurface, (slotX, slotY))
                    newCraftingSlot["renderPosition"] = [renderX, renderY]
                    newCraftingSlot["rect"] = Rect(rectX, rectY, slotSizeInPixels, slotSizeInPixels)
                    newCraftingSlot["selectedSlotRenderPosition"] = [rectX - gapBetweenSlots, rectY - gapBetweenSlots]
                    newCraftingSlot["itemCountRenderPosition"] = [rectX + slotSizeInPixels - fontShift[0] - 1, rectY + slotSizeInPixels - fontShift[1] - 1]
                    newCraftingSlot["slotId"] = slotId
 
                    this.crafting[3]["slots"][slotId] = newCraftingSlot
 
                    slotId += 1
            };
        };
 
 
            // put an arrow that goes towards the result slot for crafting in the 2x2 grid
            let a = (widthOfInventoryInSlots - 0.60) * slotSizeInPixels
            let b = (slotSizeInPixels*0.75) + slotSizeInPixels * 1.1
 
            let c = (a, b)
            let d = (a + (slotSizeInPixels/3), b + (slotSizeInPixels/3)/2)
            let e = (a, b + slotSizeInPixels/3)
 
            let f = (c, d, e)
 
            pygame.draw.polygon(craftingAndArmorBackground, selectedSlotColor, f)
 
            let rect = Rect(a - slotSizeInPixels/1.4, b + slotSizeInPixels/8.5,
                               slotSizeInPixels/1.3, slotSizeInPixels/9)
            pygame.draw.rect(craftingAndArmorBackground, selectedSlotColor, rect)
 
            let craftingAndArmorSurface = craftingAndArmorBackground
 
 
            // put an arrow that goes towards the result slot for crafting in the 3x3 grid
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
 
            let craftingTableSurface = craftingTableBackground
 
 
 
 
            let inventoryXForBlit = (canvasWidth - inventoryWidthInPixels) / 2 
            let inventoryYForBlit = craftingAndArmorYForBlit + craftingAndArmorHeightInPixels
 
            let hotbarXForBlit = inventoryXForBlit
            let hotbarYForBlit = (canvasHeight - hotbarSizeInPixels[1]) - (hotbarSizeInPixels[1] / 2)
 
            let inventorySlot = {
                "contents": "empty", // this is where itemData goes
                "count": 0, // how many of x item is in this slot
                "renderPosition": (0, 0),
                "selectedSlotRenderPosition": (0, 0),
                "itemCountRenderPosition": (0, 0),
                "rect": Rect(0, 0, 0, 0), // used for mouse collision
                "slotId": 0
            }
 
            this.inventory = []
            this.hotbar = []
 
            slotId = 0
 
            for (let y = 0; y < heightOfInventoryInSlots; y++) {
                for (let x = 0; x < widthOfInventoryInSlots; x++) {
 
                    slotX = (x * slotSizeInPixels) + ((x + 1) * gapBetweenSlots)
                    slotY = (y * slotSizeInPixels + ((y + 1) * gapBetweenSlots))
 
                    inventoryBackground.blit(slotSurface, (slotX, slotY))
 
                    renderX = inventoryXForBlit + slotX + itemIconShift
                    renderY = inventoryYForBlit + slotY + itemIconShift
 
                    rectX = renderX - itemIconShift
                    rectY = renderY - itemIconShift
 
                    updatedInventorySlot = inventorySlot
                    
   
                    
 
                    updatedInventorySlot["renderPosition"] = [renderX, renderY]
                    updatedInventorySlot["itemCountRenderPosition"] = [rectX + slotSizeInPixels - fontShift[0] - 1, rectY + slotSizeInPixels - fontShift[1] - 1]
                    updatedInventorySlot["selectedSlotRenderPosition"] = [rectX - gapBetweenSlots,
                                                                        rectY - gapBetweenSlots]
                    updatedInventorySlot["rect"] = Rect(rectX, rectY,
                                                            slotSizeInPixels, slotSizeInPixels)
                    updatedInventorySlot["slotId"] = slotId
                    slotId += 1
                    
 
                    this.inventory.push(updatedInventorySlot)
            };
        };
 
 
            
 
 
 
            let inventorySurface = inventoryBackground        
        
            // create hotbar data
            slotId = 0
            for (let x = 0; x < widthOfInventoryInSlots; x++) {
 
                slotX = (x * slotSizeInPixels) + ((x + 1) * gapBetweenSlots)
                slotY = gapBetweenSlots
 
                renderX = hotbarXForBlit + slotX + itemIconShift
                renderY = hotbarYForBlit + slotY + itemIconShift
 
                rectX = renderX - itemIconShift
                rectY = renderY - itemIconShift
 
                fontShift = font.size("1")
 
                updatedInventorySlot = inventorySlot
 
                updatedInventorySlot["renderPosition"] = (renderX, renderY)
                updatedInventorySlot["itemCountRenderPosition"] = (rectX + slotSizeInPixels - fontShift[0] - 1, rectY + slotSizeInPixels - fontShift[1] - 1)
                updatedInventorySlot["selectedSlotRenderPosition"] = (rectX - gapBetweenSlots,
                                                                    rectY - gapBetweenSlots)
                updatedInventorySlot["rect"] = pygame.Rect(rectX, rectY,
                                                        slotSizeInPixels, slotSizeInPixels)
                updatedInventorySlot["slotId"] = slotId
                slotId += 1
 
                hotbarSurface.blit(slotSurface, (slotX, slotY))
 
                this.hotbar.push(updatedInventorySlot)
            };
            
            let inventoryRect = Rect(inventoryXForBlit, inventoryYForBlit,
                                        inventoryWidthInPixels, inventoryHeightInPixels)
            
            let hotbarRect = Rect(hotbarXForBlit, hotbarYForBlit,
                                    inventoryWidthInPixels, hotbarSizeInPixels[1])
                
            let craftingAndArmorRect = Rect(craftingAndArmorXForBlit, craftingAndArmorYForBlit,
                                               craftingAndArmorWidthInPixels, craftingAndArmorHeightInPixels)
            
            let craftingTableRect = Rect(
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
            // rects are here
            "inventoryRect": inventoryRect,
            "hotbarRect": hotbarRect,
            "craftingAndArmorRect": craftingAndArmorRect,
            "craftingTableRect": craftingTableRect,
            // thigns that aren't rects are here
            "currentHotbarSlot": 0, // id/index of the slot in the hotbar
            "open": false,
            "slotId": 0,
            "showCraftingAndArmor": true,
            "showCraftingTable": false
            }
            
        };
 
        createALotOfInventoryThings()
 
 
        this.timers = {
 
        }
 
        // blocks up AND down of reach
        this.verticalBlockReach = 3
        this.horizontalBlockReach = 3
        this.canReachSelectedBlock = false
 
        this.blockBreakProgress = 0
        this.currentBreakingBlock = None
    
 
 
    this.generalMovement = function (deltaTime) {
        
        this.chunkCoord = getChunkCoord(this.x, this.z)
        this.blockCoord = getBlockCoord(this.x, this.y, this.z)
 
        this.rect.x = this.x;
        this.rect.y = this.z;
 
    
        Object.keys(this.collision).forEach( function (key) {
            this.collision[key] = false;
        })
 
        // faster? access to variables that need to be used a lot in collision
        let rightSide = this.x + this.width;
        let bottomSide = this.z + this.width;
        let underSide = this.y - this.height;
        
        function doCollisionBelow() {
            let topLeft = findBlock(this.x, underSide - 3, this.z, ignoreWater = true)
            let topRight = findBlock(rightSide, underSide - 3, this.z, ignoreWater = true)
            let bottomLeft = findBlock(this.x, underSide - 3, bottomSide, ignoreWater = true)
            let bottomRight = findBlock(rightSide, underSide - 3, bottomSide, ignoreWater = true)
            if (topLeft || topRight || bottomLeft || bottomRight) {
                this.collision["below"] = true;
            };
        };
        doCollisionBelow()
 
        function doCollisionAbove() {
            let topLeft = findBlock(this.x, this.y, this.z, ignoreWater = true)
            let topRight = findBlock(rightSide, this.y, this.z, ignoreWater = true)
            let bottomLeft = findBlock(this.x, this.y, bottomSide, ignoreWater = true)
            let bottomRight = findBlock(rightSide, this.y, bottomSide, ignoreWater = true)
            if (topLeft || topRight || bottomLeft || bottomRight) {
                this.collision["above"] = true
            };
        };
        doCollisionAbove()
 
        function doCollisionToRight() {
            let temporaryNumber = rightSide + 1
            let aboveTopRight = findBlock(temporaryNumber, this.y, this.z, ignoreWater = true)
            let aboveBottomRight = findBlock(temporaryNumber, this.y, bottomSide, ignoreWater = true)
            let belowBottomRight = findBlock(temporaryNumber, underSide, bottomSide, ignoreWater = true)
            let belowTopRight = findBlock(temporaryNumber, underSide, this.z, ignoreWater = true)
            if (aboveTopRight || aboveBottomRight || belowBottomRight || belowTopRight) {
                this.collision["right"] = true;
            };
        };
 
        doCollisionToRight()
        
        function doCollisionToLeft() {
            let temporaryNumber = this.x - 1
            let aboveTopLeft = findBlock(temporaryNumber, this.y, this.z, ignoreWater = true)
            let aboveBottomLeft = findBlock(temporaryNumber, this.y, bottomSide, ignoreWater = true)
            let belowBottomLeft = findBlock(temporaryNumber, underSide, bottomSide, ignoreWater = true)
            let belowTopLeft = findBlock(temporaryNumber, underSide, this.z, ignoreWater = true)
            if (aboveBottomLeft || aboveTopLeft || belowBottomLeft || belowTopLeft) {
                this.collision["left"] = true
            };
        };
        doCollisionToLeft()
 
        function doCollisionToUp() {
            let aboveTopLeft = findBlock(this.x, this.y, this.z - 1, ignoreWater = true)
            let aboveTopRight = findBlock(rightSide, this.y, this.z - 1, ignoreWater = true)
            let belowTopRight = findBlock(rightSide, underSide, this.z - 1, ignoreWater = true)
            let belowTopLeft = findBlock(this.x, underSide, this.z - 1, ignoreWater = true)
            if (aboveTopLeft || aboveTopRight || belowTopLeft || belowTopRight) {
                this.collision["up"] = true
            };
        };
 
        doCollisionToUp()
 
        function doCollisionToDown() {
            let aboveBottomLeft = findBlock(this.x, this.y, bottomSide + 1, ignoreWater = true)
            let aboveBottomRight = findBlock(rightSide, this.y, bottomSide + 1, ignoreWater = true)
            let belowBottomRight = findBlock(rightSide, underSide, bottomSide + 1, ignoreWater = true)
            let belowBottomLeft = findBlock(this.x, underSide, bottomSide + 1, ignoreWater = true)
            if (aboveBottomLeft || aboveBottomRight || belowBottomRight || belowBottomLeft) {
                this.collision["down"] = true
            };
        };
 
        doCollisionToDown()
 
        function checkForBeingInsideOfABlock() {
            let center = findBlock(this.x + this.width/2, this.y - this.height/2, this.z + this.width/2, extraInfo = true)
            this.collision["insideOfBlock"] = center["type"]
        };
        checkForBeingInsideOfABlock()
 
        let temporaryNumber = (this.y - this.height) + blockSize + 3
        // SEPARATE THESE LATER INTO FUNCTIONS
        let aboveToTopRight = findBlock(rightSide + this.xv + 3, temporaryNumber, this.z, ignoreWater = true)
        let aboveToBottomRight = findBlock(rightSide + this.xv + 3, temporaryNumber, bottomSide, ignoreWater = true)
        if (aboveToTopRight || aboveToBottomRight) {
            this.collision["aboveRight"] = true
        };
 
        let aboveToTopLeft = findBlock(this.x + this.xv - 3, temporaryNumber, this.z, ignoreWater = true)
        let aboveToBottomLeft = findBlock(this.x + this.xv - 3, temporaryNumber, bottomSide, ignoreWater = true)
        if (aboveToTopLeft || aboveToBottomLeft) {
            this.collision["aboveLeft"] = true
        }
 
        let aboveToLeftUp = findBlock(this.x, temporaryNumber, this.z + this.zv - 3, ignoreWater = true)
        let aboveToRightUp = findBlock(rightSide, temporaryNumber, this.z + this.zv - 3, ignoreWater = true)
        if (aboveToLeftUp || aboveToRightUp) {
            this.collision["aboveUp"] = true
        };
        
        let aboveToRightDown = findBlock(rightSide, temporaryNumber, bottomSide + this.zv + 3, ignoreWater = true)
        let aboveToLeftDown = findBlock(this.x, temporaryNumber, bottomSide + this.zv + 3, ignoreWater = true)
        if (aboveToLeftDown || aboveToRightDown) {
            this.collision["aboveDown"] = true
        };
 
 
 
 
 
        let currentMaxHorizontalSpeed = this.maxHorizontalSpeed;
        if (this.collision["insideOfBlock"] == "water") {
            currentMaxHorizontalSpeed = this.maxHorizontalSpeed / 2
        };

         // x and z axis movement
        if (keys.d && !this.collision["right"]) {
            if (this.xv < currentMaxHorizontalSpeed) {
                this.xv += this.acceleration
            };
        };
        
 
        if (keys.a && !this.collision["left"]) {
            if (this.xv > -currentMaxHorizontalSpeed) {
                this.xv -= this.acceleration
            };
        };
 
        if (keys.w && !this.collision["up"]) {

            if (this.zv > -currentMaxHorizontalSpeed) {
                this.zv -= this.acceleration
            };
        };
 
        if (keys.s && !this.collision["down"]) {
            if (this.zv < currentMaxHorizontalSpeed) {
                this.zv += this.acceleration
            };
        };
 
        // y axis movement
        if (keys[" "]) {
            if (this.collision["insideOfBlock"] == "water") {
                // do water stuff
                let jumpForce = this.normalJumpForce / 3
 
                this.yv = jumpForce
            } else {
                if (this.collision["below"]) {
                    // do jump stuff
                    let jumpForce = this.normalJumpForce
 
                    this.yv = jumpForce
                };
            };
        };
            
 
 
         // do gravity
        if (!this.collision["below"]) {
            let yvChange = gravity
            if (this.collision["insideOfBlock"] == "water") {
                yvChange /= 5
            };
            this.yv -= yvChange
        } else { if (this.yv < 0) {
            this.yv = 0
            this.y = this.blockCoord[1] * blockSize + this.height
            // re-do collisions, hopefully fixes colliding with walls while hitting
            // the ground hard, looks like it didn't fix it?
            //doCollisionToDown()
            //doCollisionToLeft()
            //doCollisionToUp()
            //doCollisionToRight()
        };
         // don't let player fall out of the world
        if (this.y < -300) {
            this.y = chunkSize[1] * blockSize
            this.yv = 0
        };
 
        // don't let player go through ceilings
        if (this.collision["above"]) {
            if (this.yv > 0) {
                this.y -= this.yv
                this.yv = 0
            };
        };
 
        // wall collision
        // and block step up (go up blocks without jumping
 
 
        this.booleans["blockStepUsed"] = false
 
        if (this.collision["up"]) {
            let a = this.collision["below"]
            let b = !this.collision["aboveUp"]
            let c = !this.booleans["blockStepUsed"]
            let d = keys.w
            if (a && b && c && d) {
                this.y += blockSize
                // update collision, since player's been moved a lot
                doCollisionToDown()
                doCollisionToLeft()
                doCollisionToRight()
                this.booleans["blockStepUsed"] = true
            } else {
                this.z += abs(this.zv)
                this.zv = 0
                this.z += 1
            };
        };

        if (this.collision["right"]) {
            let a = this.collision["below"]
            let b = !this.collision["aboveRight"]
            let c = !this.booleans["blockStepUsed"]
            let d = keys.d
            if (a && b && c && d) {
                this.y += blockSize
                // update collision, since player's been moved a lot
                doCollisionToDown()
                doCollisionToLeft()
                doCollisionToUp()
                this.booleans["blockStepUsed"] = true
            } else {
                this.x -= abs(this.xv)
                this.xv = 0
                this.x -= 1
            };
        };
 
        if (this.collision["left"]) {
            let a = this.collision["below"]
            let b = !this.collision["aboveLeft"]
            let c = !this.booleans["blockStepUsed"]
            let d = keys.a
            if (a && b && c && d) {
                this.y += blockSize
                // update collision, since player's been moved a lot
                doCollisionToDown()
                doCollisionToRight()
                doCollisionToUp()
                this.booleans["blockStepUsed"] = true
            } else {
                this.x += abs(this.xv)
                this.xv = 0
                this.x += 1
            };
        };
            
        if (this.collision["down"]) {
            let a = this.collision["below"]
            let b = !this.collision["aboveDown"]
            let c = !this.booleans["blockStepUsed"]
            let d = keys.s
            if (a && b && c && d) {
                this.y += blockSize
                // update collision, since player's been moved a lot
                doCollisionToLeft()
                doCollisionToRight()
                doCollisionToUp()
                this.booleans["blockStepUsed"] = true
            } else {
                this.x -= abs(this.zv)
                this.zv = 0
                this.z -= 1
            };
        };
       
 
 
         
        // force player speed cap
        if (this.xv > currentMaxHorizontalSpeed) {this.xv = currentMaxHorizontalSpeed;};
        if (this.xv < -currentMaxHorizontalSpeed) {this.xv = -currentMaxHorizontalSpeed;};
 
        if (this.zv > currentMaxHorizontalSpeed) {this.zv = currentMaxHorizontalSpeed;};
        if (this.zv < -currentMaxHorizontalSpeed) {this.zv = -currentMaxHorizontalSpeed;};
        
        // friction
        if ((!keys.a && !keys.d) || (keys.a && keys.d)) {
            this.xv -= this.xv / this.slipperyness;
            if (Math.abs(this.xv) < 0.1) {this.xv = 0;};
        };
        if ((!keys.w && !keys.s) || (keys.w && keys.s)) {
            this.zv -= this.zv / this.slipperyness
            if (Math.abs(this.zv) < 0.1) {this.zv = 0;};
        };
        
 
 
        // don't let player get stuck inside of blocks
        if (this.collision["insideOfBlock"] != "air" && 
            this.collision["insideOfBlock"] != "water") {this.y += 5;};
        
 
        // do all the position updates that other things use
        this.xv = Math.round(this.xv * 100) / 100;
        this.yv = Math.round(this.yv * 100) / 100;
        this.zv = Math.round(this.zv * 100) / 100;
 
        this.x += (this.xv * deltaTime);
        this.y += (this.yv * deltaTime);
        this.z += (this.zv * deltaTime);
 
        
        
 
        this.position = [this.x, this.y, this.z];
 
         };
 
    this.giveItem = function (item, count = 1) {
        
        function checkForStackables(container, done, count, item) {
            if (!done && item.stackable) {
                for (let i = 0; i < container.length; i++) {

                    let slot = container[i];
                    if (slot.contents == "empty" || slot.contents.name != item.name ||
                        slot.contents.cound == maxStackSize)
                    {
                        return done;
                    }
        

                    let addedCount = count + slot["count"]
                    if (addedCount <= maxStackSize) {

                        slot["count"] = addedCount
                        return true
                    } else {if (addedCount > maxStackSize) {
                        slot["count"] = maxStackSize
                        count = addedCount - maxStackSize
                        break
                    }};
                    container[i] = slot;

                };

            }
            return done
        };
    
        function checkForEmptySlots(container, done, count, item) {
            if (!done) {
                container.forEach( function (slot) {
                    if (slot.contents == "empty") {
                        slot.contents = item;
                        slot.count = count;

                        return true;
                    }
                });
            };
            return done
        };
 
            
 
        done = false
 
        done = checkForStackables(this.hotbar, done, count, item)
        done = checkForStackables(this.inventory, done, count, item)
 
        done = checkForEmptySlots(this.hotbar, done, count, item)
        done = checkForEmptySlots(this.inventory, done, count, item)
 
        if (!done) {consoleLog("failed to give item");};
 
        return done
    };
 



    this.moveItem = function (movingItemSlot, movingItem, amount, receivingContainer) {
        // these parameters will be changed by the function, hopefully it works?
        // this function will return whether the operation was successful or not
        let receivingSlotId = undefined;

        // search for which slot to move stuff to
        for (let i = 0; i < receivingContainer.length; i++) {
            let slot = receivingContainer[i];
            let item = slot.contents;

            if (movingItem.stackable) {
                if (item != "empty" && item.stackable === true && item.name === movingItem.name
                    && slot.count < maxStackSize) {
                    receivingSlotId = i;
                    break;
                }
            } else {
                if (item == "empty") {
                    receivingSlotId = i;
                    break;
                }
            }
        }

        if (receivingSlotId === undefined && movingItem.stackable) {
            for (let i = 0; i < receivingContainer.length; i++) {
                let slot = receivingContainer[i];
                let item = slot.contents;

                if (item === "empty") {
                    receivingSlotId = i;
                    break;
                }
            }
        }

        // make sure moving amount makes sense
        if (amount > movingItemSlot.count) {
            amount = movingItemSlot.count;
        }

    
        if (receivingSlotId !== undefined) {
            // important! make sure the parameter gets updated from receivingSlot
            let receivingSlot = receivingContainer[receivingSlotId];
            let movingCount = receivingSlot.count + amount;

            if (movingCount <= maxStackSize) {
                receivingSlot.count = movingCount;
                receivingSlot.contents = movingItem;

                movingItem = "empty";
                movingItemSlot.count = 0;
            } else {
                let leftOverCount = movingCount - maxStackSize;
                receivingSlot.count = maxStackSize;
                receivingSlot.contents = movingItem; // set the item to the moving one, just in case

                movingItemSlot = leftOverCount;
            }

            receivingContainer[receivingSlotId] = receivingSlot;
            return true;
        }
        return false;
    }
 
    this.doInventoryThings = function () {

        
        if (keysPressed.e) {this.otherInventoryData.open = !this.otherInventoryData.open;};


        this.inventory.forEach( function(slot) {
            if (slot.contents != "empty") {slot.contents.slotId = slot.slotId;};
        })
        this.hotbar.forEach( function(slot) {
            if (slot.contents != "empty") {slot.contents.slotId = slot.slotId;};
        })
 
 
        function adjustMouseSelectedBlockHeight() {
            // change the selected height of the mouse
            mouse.selectedY = this.y
 
            if (keysPressed["."]) {
                if (mouse.selectedYChange < this.verticalBlockReach) {
                    mouse.selectedYChange += 1;};
            };
                
            if (keysPressed[","]) {
                if (mouse.selectedYChange > -this.verticalBlockReach) {
                    mouse.selectedYChange -= 1;
                };
            };
 
            mouse.selectedY += mouse.selectedYChange * blockSize;
            
 
            if (mouse.selectedY <= 0) {mouse.selectedY = blockSize;};
            if (mouse.selectedY >= chunkSize[1] * blockSize) {mouse.selectedY = chunkSize[1] * (blockSize - 1);};
        };
        adjustMouseSelectedBlockHeight()
 
 
        // change hotbar slot based on pressing stuff
        let numberList = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"];
        numberList.forEach( function (number) {
            if (key[number]) {this.otherInventoryData.currentHotbarSlot = Number(number);};
        })
 
 
        function dropItems() {
            // drop items from the hotbar
            if (keysPressed.q) {
                if (!this.otherInventoryData.open) {
                    let currentHotbarSlot = this.otherInventoryData.currentHotbarSlot;
                    let item = this.hotbar[currentHotbarSlot].contents;
 
                    if (item != "empty") {
 
                        let x = this.x + this.width/2 - itemEntitySize/2;
                        let y = this.y - this.height/2;
                        let z = this.z + this.width/2 - itemEntitySize/2;
 
                        // figure out velocity for angle of player to mouse
 
                        let xDiff = mouse.cameraRelativeX - x;
                        let yDiff = mouse.cameraRelativeZ - z;
 
                        let angle = Math.atan2(yDiff, xDiff);

                        let dropVelocity = 3
 
                        let xv = Math.cos(angle) * dropVelocity;
                        let yv = 2;
                        let zv = Math.sin(angle) * dropVelocity;
 
                        let count = 1;
 
                        item.drop(x, y, z, xv, yv, zv, this, count);
                    };
                };
            };
        };
        dropItems();
 
 
        function hotbarHeldItemStuff() {
            if (!this.otherInventoryData.open) {
                let index = this.otherInventoryData.currentHotbarSlot;
                let slotData = this.hotbar[index];
                let item = slotData.contents;
 
                if (mouse.buttons.pressed.left || mouse.buttons["left"]) {
                    this.doStuffOnLeftClick(item)
                };
 
                if (item != "empty") {
 
                    if (mouse.buttons["pressed"]["right"]) {
                        item.RMBPressedAction(this);
                    } else {if (mouse.buttons.right) {item.RMBAction(this); }};
                } else {
                    this.doStuffOnRightClick(item)
                };
            };
        };
        hotbarHeldItemStuff();
 
        function updateMouseInventoryCollision () {
            mouse.inPlayerInventory = false;
            mouse.inPlayerHotbar = false;
            mouse.inPlayerCraftingAndArmor = false;
            mouse.inPlayerCraftingTable = false;
            mouse.inASlot = false;

            mouse.inPlayerCraftingAndArmor = this.otherInventoryData.craftingAndArmorRect.collide.point(mouse.x, mouse.y)
            mouse.inPlayerInventory = this.otherInventoryData.inventoryRect.collide.point(mouse.x, mouse.y)
            mouse.inPlayerHotbar = this.otherInventoryData.hotbarRect.collide.point(mouse.x, mouse.y)
            mouse.inPlayerCraftingTable = this.otherInventoryData.craftingTableRect.collide.point(mouse.x, mouse.y)
        }
        updateMouseInventoryCollision();

        // need to rework crafting to be a list, or it won't work with the moveItem function
        // probably separate the crafting slot from the rest of the other slots, do special logic

        function mouseInteractionWithContainer(container, otherContainer = undefined, isResultSlot = false) {
            for (let i = 0; i < container.length; i++) {
                let slot = container[i];
                if (slot.rect.collide.point(mouse.x, mouse.y)) {
                    mouse.inASlot = true;
                    // only do quick transfer things if the other container is specified
                    if (otherContainer !== undefined) {
                        // do a quick transfer of max items
                        if (keys.shift && !keys.ctrl) {
                            if (!isResultSlot) {
                            this.moveItem(container[i], container[i].contents, 64, otherContainer);
                            break;
                            } else {
                                // figure out what to write in order to crafting maximum number of items
                            }
                        }
                        // move a single item
                        if (keys.ctrl && !keys.shift && !isResultSlot) {
                            this.moveItem(container[i], container[i].contents, 1, otherContainer);
                            break;
                        }
                    };

                    if (!keys.ctrl && !keys.shift) {
                        // do left click interaction
                        if (mouse.buttons.pressed.left && !mouse.buttons.right) {
                            let tempItem = mouse.heldSlot.contents;
                            let tempCount = mouse.heldSlot.count;

                            mouse.heldSlot.contents = container[i].contents;
                            mouse.heldSlot.count = container[i].count;

                            container[i].contents = tempItem;
                            container[i].count = tempCount;

                            break;
                            };
                    
                        // do right click interaction
                        if (mouse.buttons.pressed.right && !mouse.buttons.left) {
                            // grab half of the item count, try not to dupe things
                            if (mouse.heldSlot.contents === "empty") {
                                let newMouseSlotCount = Math.ceil(slot.count/2);
                                let newSlotCount = slot.count - newMouseSlotCount;

                                mouse.heldSlot.count = newMouseSlotCount;
                                mouse.heldSlot.contents = slot.contents;
                                container[i].count = newSlotCount;
                                if (newSlotCount <= 0) {
                                    container[i].contents = "empty";
                                }
                            }
                            // place a single item into that slot, if it's the same
                            if (mouse.heldSlot.contents !== "empty") {
                                if (mouse.heldSlot.contents.name == slot.contents.name &&
                                    slot.contents.stackable && mouse.heldSlot.contents.stackable) {
                                        let newSlotCount = slot.count + 1;
                                        let newMouseSlotCount = mouse.heldSlot.count - 1;

                                        if (newSlotCount <= maxStackSize && newMouseSlotCount >= 0) {
                                            container[i].count = newSlotCount;
                                            mouse.heldSlot.count = newMouseSlotCount;
                                            if (newMouseSlotCount <= 0) {
                                                mouse.heldSlot.contents = 0;
                                        }
                                    }
                                }
                            }
                        };
                    }
            }
        }
    };
      
 
 
 
 
        if (this.otherInventoryData.open) {
            
            if (mouse.inPlayerInventory) {
             // this part with the storage thing has no basis, storage containers don't exist yet
                let otherContainer = undefined;
                if (this.storageUIOpen) {
                    otherContainer = this.currentStorageBlock;
                }
                mouseInteractionWithContainer(this.inventory, otherContainer);
            }
            if (mouse.inPlayerHotbar) {
                let otherContainer = undefined;
                if (this.storageUIOpen) {
                    otherContainer = this.currentStorageBlock;
                }
                mouseInteractionWithContainer(this.hotbar, otherContainer);
            }
            if (mouse.inPlayerCraftingAndArmor) {
                let gridSize = this.crafting.gridSize;
                mouseInteractionWithContainer(this.crafting[gridSize].resultSlot, this.inventory);
                mouseInteractionWithContainer(this.crafting[gridSize].slots, this.inventory);
                mouseInteractionWithContainer(this.armor, this.inventory);
            }
            // checks for this haven't been implemented yet
            if (mouse.inStorageUI) {

            }
        }
        


        // attempt to place mouse's item back in the player's inventory if inventory is closed
        if (!this.otherInventoryData.open) {

            if (mouse.heldSlot.contents !== "empty") {
                
                let itemWasMoved = this.moveItem(mouse.heldSlot, mouse.heldSlot.contents, 64, this.inventory);
                if (!itemWasMoved) {
                    itemWasMoved = this.moveItem(mouse.heldSlot, mouse.heldSlot.contents, 64, this.hotbar);
                }
                

                if (!itemWasMoved) {

                    // center of player
                    let x = this.x + this.width/2
                    let y = this.y - this.height/2
                    let z = this.z + this.width/2

                    // figure out velocity for angle of player to mouse

                    let xDiff = mouse.cameraRelativeX - x
                    let yDiff = mouse.cameraRelativeZ - z

                    let angle = Math.atan2(yDiff, xDiff)                        

                    let xv = Math.cos(angle) * 3
                    let yv = 2
                    let zv = Math.sin(angle) * 3

                    mouse.heldSlot.contents.drop(x, y, z, xv, yv, zv, mouse.heldSlot.count);
                };
            };
        };
    
 
        function recipeChecksAndStuff () {
            // dict with total amount of each item in crafting slots
            this.totalCraftingContents = {};
            this.isCrafting = false;
            this.crafting.possibleCrafts = 0;

            // this for loop doesn't include the result slot
            for (const slot of this.crafting[this.crafting.gridSize].slots) {
                if (slot.contents !== "empty") {
                    if (this.totalCraftingContents[slot.contents].name === undefined) {
                        this.totalCraftingContents[slot.contents.name] = 0;
                    }
                    this.totalCraftingContents[slot["contents"].name] += 1;
                }
            }
                            
                        
            let lowestItemCount = maxStackSize;
            
 
            for (const slot of this.crafting[this.crafting.gridSize].slots) {
                if (slot.contents !== "empty" && slot.count < lowestItemCount) {
                    lowestItemCount = slot.count;
                }
            }
 

            this.crafting["possibleCrafts"] = lowestItemCount;
 
 
 
            if (this.crafting["possibleCrafts"] > 0) {this.isCrafting = true}
 
            let foundARecipe = false
            let recipeThatWasFound = undefined;
 
            function exactRecipeDetection(recipe) {
                // doesn't exist yet
                
                if (this.totalCraftingContents == recipe.requiredItems) {

                }
                    
 
                return false, undefined
            };
            
            function nearExactRecipeLogic(recipe) {
                
                function checkForSpecificItemInSlot(instructions) {
                    /*
                    startingItemName, directions, operators, and items are contained in instructions
 
                    example:
                    direction = ["left", "right"], operator = ["xor"], items = ["planks", "planks"]
                    
                    
                    checks for "planks" in the slot to the left and the slot to the right
                    
                    compares the values of does this slot have this specific item
                    */
 
                    function checkADirection(direction, startingSlotId) {
                        let gridSize = this.crafting["gridSize"]
                        let testSlotId = 0
                        switch (direction) {
                            case "up":
                                testSlotId = startingSlotId - gridSize;
                                if (testSlotId >= 0 && testSlotId < (grideSize**2)) {
                                    let item = this.crafting[gridSize].slots[testSlotId].contents;
                                    if (item != "empty") {return item.name;}
                                }
                                return "no item";
                            
                            case "down":
                                testSlotId = startingSlotId + gridSize;
                                if (testSlotId >= 0 && testSlotId < (gridSize**2)) {
                                    let item = this.crafting[gridSize].slots[testSlotId].contents;
                                    if (item != "empty") {return item.name};
                                }
                                return "no item";
                            
                            case "right":
                                testSlotId = startingSlotId + 1;
                                let temporaryGridSize = gridSize - 1;
                                if (testSlotId >= 0 && testSlotId < (gridSize**2)) {
                                    if (testSlotId == gridSize) {return "no item"};
                                    while (testSlotId > temporaryGridSize) {
                                        temporaryGridSize += gridSize;
                                        if (temporaryGridSize >= gridSize
                                            || testSlotId == temporaryGridSize) {return "no item"};
                                    }
                                    let item = this.crafting[gridSize].slots[testSlotId].contents;
                                    if (item != "empty") {return item.name};
                                    return "empty";
                                }
                        }
                        return "no item"
                    };
 
                    for (let i = 0; i < this.crafting[this.crafting.gridSize].slots; i++) {
                        let slot = this.crafting[this.crafting.gridSize].slots[i];
                        let item = slot.contents;

                        if (item != "empty" && item.name == instructions.startingItemName) {
                            let usesOperators = instructions.operators.length > 0;
                            
                            let directions = instructions.directions;
                            let operators = instructions.operators;
                            let items = instructions.items;

                            if (!usesOperators) {
                                let slotFound = checkADirection(directions[0], i);
                                if (slotFound == items[0]) {return true}
                            } else {
                                let slotsChecked = [];

                                for (let i = 0; i < directions.length; i++) {
                                    let currentDirection = directions[i];
                                    let currentItem = items[i];

                                    let slotDictThing = {
                                        "direction": currentDirection,
                                        "containsCorrectItem": false
                                    }
                                    let itemName = checkADirection(currentDirection, i);

                                    if (itemName == items[i]) {
                                        slotDictThing.containsCorrectItem = true;
                                    }
                                    slotsChecked.push(slotDictThing);
                                }
                                let conditions = [];

                                for (const slot of slotsChecked) {
                                    conditions.push(slot.containsCorrectItem);
                                }
                                let hasAnEvenNumberOfConditions = conditions.length % 2 === 0;
                                let length = conditions.length;
                                if (!hasAnEvenNumberOfConditions) {length -= 1};
                                let betterConditionsList = [];
                                for (let i = 0; i < length; i += 2) {
                                    let conditionA = conditions[i - 1];
                                    let conditionB = conditions[i];

                                    betterConditionsList.push([conditionA, conditionB]);
                                }
                                for (let i = 0; i < operators.length; i++) {
                                     // i should probably modify how i am doing operators to specify which
                                    // directions should use what operators (example: right "and" left)
                                    // another example: up "neither" down
                                    // and also should probably add in the ability to specify multiple
                                    // directions for something, ex top right is up and right
                                    // or i could just have "top right" be a valid direction
                                    // yeah ima just do that
                                    // or i could have the directions be like {up: 2}, {right: 1},
                                    // that would be up 2 slots, right 1 slot
                                    // operators still need to be grouped with directions at some point though
                                    let operator = operators[i];
                                    let conditionA = betterConditionsList[i][0];
                                    let conditionB = betterConditionsList[i][1];
                                    
                                    if (operator == "xor") {
                                        if ((conditionA || conditionB) && (conditionA !== conditionB)) {return true;};
                                    }
                                    if (operator == "and") {
                                        if (conditionA && conditionB) {return true;};
                                    }
                                    if (operator == "neither") {
                                        if (!conditionA && !conditionB) {return true};
                                    }
                                    if (operator == "or") {
                                        if (conditionA || conditionB) {return true;}
                                    }

                                    consoleLog("invalid recipe operator or something like that")
                                }
                            }
                        }
                    }
 
 
 
 
                    return false
                };
 
                                    
 
 
 
                    
                if (this.totalCraftingContents == recipe["requiredItems"]) {
             
                    let foundARecipe = checkForSpecificItemInSlot(recipe.instructions)
 
                    if (foundARecipe) {return [true, recipe]};
                }
                return [false, undefined];
            };
 
            function shapelessRecipeLogic(recipe) {
               
                if (this.totalCraftingContents == recipe.requiredItems) {return [true, recipe];};
                return [false, undefined];
            };
 
            
            
            
            if (this.isCrafting) {
 
                for (const recipe of Object.values(recipes[this.crafting.gridSize].exact)) {
                    let recipeDataStuff = exactRecipeDetection(recipe);
                    foundARecipe = recipeDataStuff[0];
                    recipeThatWasFound = recipeDataStuff[1];
                    if (foundARecipe) {break;};
                };
 
                if (!foundARecipe) {
                    for (const recipe of Object.keys( recipes[this.crafting.gridSize].nearExact )) {
                        let recipeDataStuff = nearExactRecipeLogic(recipe);
                        foundARecipe = recipeDataStuff[0];
                        recipeThatWasFound = recipeDataStuff[1];
                        if (foundARecipe) {break;};
                    }
                };
                
                if (!foundARecipe) {
                    for (const recipe of Object.keys ( recipes[this.crafting.gridSize].shapeless )) {
                        let recipeDataStuff = shapelessRecipeLogic(recipe);
                        foundARecipe = recipeDataStuff[0];
                        recipeThatWasFound = recipeDataStuff[1];
                        if (foundARecipe) {break;};
                    };
                };
            };
 
            let gridSize = this.crafting.gridSize;
            if (foundARecipe) {
                this.crafting[gridSize].resultSlot.contents = recipeThatWasFound.output;
                this.crafting[gridSize].resultSlot.count = recipeThatWasFound.outputCount;
            } else {
                this.crafting[gridSize].resultSlot.contents = "empty";
                this.crafting[gridSize].resultSlot.count = 0;
            };
 
 
 
            
                        
        };
        recipeChecksAndStuff();

 
};
        
    this.handleTimers = function () {
        for (let i = 0; i < Object.keys(this.timers); i++) {
            let timerValue = this.timers[i];
            if (timerValue > 0) {timerValue -= 1;};
            if (timerValue < 0) {timerValue += 1;};
            this.timers[i] = timerValue;
        }
    };
 
 
 
    this.updateCamera = function () {
        camera.x -= Math.round((camera.x - this.x + camera.centerTheCamera[0]) / camera.smoothness)
        camera.y = this.y
        camera.z -= Math.round((camera.z - this.z + camera.centerTheCamera[1]) / camera.smoothness)
        
        camera.currentChunk = getChunkCoord(camera.x, camera.z)
    };
 
 
 
    this.updateImageThings = function () {
        imageX = this.x - camera.x
        imageY = this.z - camera.z
        
        coordinate = [imageX, imageY]
        this.imageData = [this.image, coordinate]
    };
 
 
 
    this.doStuff = function (deltaTime) {
        // need to update mouse's camera relative things here, don't want circular imports
        mouse.cameraRelativeX = Math.round((this.x + mouse.x) - canvasWidth/2)
        mouse.cameraRelativeZ = Math.round((this.z + mouse.y) - canvasHeight/2)
        mouse.cameraRelativePos = (mouse.cameraRelativeX, mouse.cameraRelativeZ)
        
        this.generalMovement(deltaTime)
        this.doInventoryThings()
        
        this.handleTimers()
        
        this.updateCamera()
        this.updateImageThings()
    };
 
 
 
    this.positionInSpawnArea = function () {
        for (let y = 0; y < chunkSize[1] - 1; y++) {
            if (findBlock(0, y * blockSize, 0)) {
                if (!findBlock(0, (y + 1) * blockSize, 0)) {
                    this.y = (y * blockSize) + this.height;
                    break;
                }
            } else {
                this.y = chunkSize[1] * blockSize + this.height;
            }
        }
    };
 
 
 
    this.doStuffOnRightClick = function (heldItem = "empty") {
        let hoveredBlockType = mouse.hoveredBlock.block.type;
        
        if (hoveredBlockType == "crafting table") {
            this.otherInventoryData.showCraftingAndArmor = false;
            this.otherInventoryData.showCraftingTable = true;
            this.crafting.gridSize = 3;
        };
    };
 
 
    this.doStuffOnLeftClick = function (currentlyHeldItem = "empty") {
        let item = currentlyHeldItem;
 
        let breakingPower = 1
        let breakingSpeed = 1
        let breakingType = "none"
        let attack = 1
        let knockback = 1
        let slowestBreakSpeed = 20/fps
 
        if (item != "empty") {
            if (item.itemType == "ToolItem") {
                breakingPower = item.breakingPower;
                breakingSpeed = item.breakingSpeed;
                breakingType = item.breakingType;
                attack = item.attack;
                knockback = item.knockback;
            };
        };
            
        
        // run a test for interaction with entitys, hitting them, etc
        // if colliderect(mouse.x, mouse.y) with an entity's hitbox or something
 
        // else:
        // break blocks
        if (this.currentBreakingBlock != mouse.hoveredBlock.block) {this.blockBreakProgress = 0;};
 
        if (this.canReachSelectedBlock) {
 
            this.currentBreakingBlock = mouse.hoveredBlock.block;
            let block = this.currentBreakingBlock;
            
            if (block["hardness"] != "infinity") {
                let correctTool = false
                let powerfulEnoughTool = false
 
                if (breakingPower >= block.hardness) {powerfulEnoughTool = true;};
                if (breakingType == block.effectiveTool) {correctTool = true;};
                
                
                if (powerfulEnoughTool && correctTool) {
                    this.blockBreakProgress += breakingSpeed / fps;
                } else {this.blockBreakProgress += slowestBreakSpeed / fps;};
 
 
                // breaking stuff is based on seconds of time,
                // in tools, the breaking speed is a percentage of a second per frame
 
                if (this.blockBreakProgress >= fps) {
                    this.blockBreakProgress = 0
 
                    if (correctTool || block.dropsWithNoTool) {
                    
                        let itemData = PlaceableItem(block["type"])
 
                        let chunkCoord = mouse.hoveredBlock.chunkCoord;
                        let blockCoord = mouse.hoveredBlock.blockCoord;
                        let x = (chunkCoord[0] * chunkSize[0]) * blockSize
                        let y = blockCoord[1] * blockSize
                        let z = (chunkCoord[1] * chunkSize[0]) * blockSize
 
                        x += blockCoord[0] * blockSize
                        z += blockCoord[2] * blockSize
 
                    
                    
                        let count = 1
                        let xv = random.randint(-3, 3)
                        let zv = random.randint(-3, 3)
                        if (true) { // replace later with silk touch or something
                            if (block.type == ("grass" || "snowy grass")) {itemData.name = "dirt"};
                            if (block.type == ("stone" || "snowy stone")) {itemData.name = "cobblestone";};
                        };
                            
                        let yv = 5;
                        let entity = ItemEntity(itemData, count, x, y, z, xv, yv, zv);
                        entities.append(entity);
                    };
 
                    let air = {
                        "type": "air",
                        "render": false,
                        "alphaValue": 255,
                        "hardness": "infinity",
                        "effectiveTool": "none"
                    };
 
                    chunks[chunkCoord.toString()].data[blockCoord.toString()] = air.copy()
 
                    smallScaleBlockUpdates(chunkCoord, blockCoord);
                };
            };
        };
    };
 
                
                
 
    this.changeCraftingGrid = function (gridSize) {
        
 
        // attempt to place items back into inventory, otherwise drop them
        
 
        for (let i = 0; i < this.crafting[this.crafting.gridSize].slots; i++) {
            
            if (this.crafting[this.crafting.gridSize].slots[i].contents !== "empty") {
            // try to put into inventory, if that fails, put into hotbar, if that fails, drop it
            let itemMoved = this.moveItem(this.crafting[this.crafting.gridSize].slots[i],
                this.crafting[this.crafting.gridSize].slots[i].contents, maxStackSize, this.inventory);
            
            if (!itemMoved) {
                itemMoved = this.moveItem(this.crafting[this.crafting.gridSize].slots[i],
                                            this.crafting[this.crafting.gridSize].slots[i].contents,
                                            maxStackSize, this.hotbar);
            }


            if (!itemMoved) {
                // center of player
                let x = this.x + this.width/2
                let y = this.y - this.height/2
                let z = this.z + this.width/2
    
                // figure out velocity for angle of player to mouse
    
                let xDiff = mouse.cameraRelativeX - x
                let yDiff = mouse.cameraRelativeZ - z
    
                let angle = Math.atan2(yDiff, xDiff)                        
    
                let xv = Math.cos(angle) * 3
                let yv = 2
                let zv = Math.sin(angle) * 3
    
                this.crafting[this.crafting.gridSize].slots[i].contents.drop(x, y, z, xv, yv, zv)

            };
        }
    };
        for slotId, slot in this.crafting[this.crafting["gridSize"]]["slots"].items():
            if slotId != "resultSlot":
                let itemMoved = false;
                done = checkStackables(slot, done)
                done = checkEmptySlots(slot, done)
 
            else:
                // figure out dropping these into inventory or ground
                slot["contents"] = "empty"
                slot["count"] = 0
 
 
 
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


    };
};
            
 
export let player = new Player();
 
 
  


showLoadingProgress("Player.mjs initialized")
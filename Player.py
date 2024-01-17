from GlobalVariables import camera, blockSize, gravity, chunkSize, maxStackSize, entities
from GlobalVariables import screenWidth, screenHeight, chunks, font, FPS, itemEntitySize
from Worldgen import getChunkCoord, getBlockCoord, findBlock, generateChunkTerrain, smallScaleBlockUpdates
from Controls import keysPressed, keys, mouse
from Entities import ItemEntity
from Items import PlaceableItem
import pygame, math, random



class Player():
    def __init__(self):
        # player's actual coordinate is
        # top left and above corner
        self.x = 0
        self.y = 0
        self.z = 0
         # velocity
        self.xv = 0
        self.yv = 0
        self.zv = 0

        self.acceleration = 0.6
        self.maxHorizontalSpeed = 5
        self.slipperyness = 5
        self.normalJumpForce = 10

        self.booleans = {
            "blockStepUsed": False
        }


        self.width = blockSize - 5
        self.height = blockSize - 5
        self.image = pygame.surface.Surface((self.width, self.width))
        # this is to make rendering work currently and should be removed later!
        self.image.fill((255, 0, 0))
        
        self.imageData = (self.image, (0, 0))

        self.position = (self.x, self.y, self.z)
        self.chunkCoord = (0, 0)
        self.blockCoord = (0, 0, 0)

        self.rect = pygame.rect.Rect(0, 0, self.width, self.width)

        # how i'm organizing the collision
        # default is the same height as player
        # above + down, or right, etc is one block higher
        # below + a side is one block below player
        # it's true if there is a block, otherwise it's false
        # this doesn't include blocks that have no collision, like water as well

        self.collision = {
            "below": False,
            "above": False,

            "right": False,
            "left": False,
            "up": False,
            "down": False,

            "aboveRight": False,
            "aboveLeft": False,
            "aboveUp": False,
            "aboveDown": False,
            
            "insideOfBlock": "air"
        }

        # hooray, inventory time!
        widthOfInventoryInSlots = 9
        heightOfInventoryInSlots = 3


        def createALotOfInventoryThings():
    
            # width and height
            inventoryWidthInPixels = screenWidth / 3
            slotSizeInPixels = round(inventoryWidthInPixels / widthOfInventoryInSlots)

            gapBetweenSlots = round(slotSizeInPixels / 5)


            backgroundColor = (150, 150, 150)
            slotColor = (125, 125, 125)
            selectedSlotColor = (175, 175, 175, 0)
            alphaForUI = 255

            emptySpaceBetweenItemAndSlotBorder = gapBetweenSlots / 2

            itemIconShift = emptySpaceBetweenItemAndSlotBorder

            inventoryWidthInPixels += gapBetweenSlots * (widthOfInventoryInSlots + 1)

            inventoryHeightInPixels = (slotSizeInPixels * heightOfInventoryInSlots)
            inventoryHeightInPixels += gapBetweenSlots * (heightOfInventoryInSlots + 1)

            # add some more height to the inventory for crafting grid and armor? if added
            craftingAndArmorHeightInSlots = 4.25
            
            craftingAndArmorWidthInPixels = inventoryWidthInPixels
            craftingAndArmorHeightInPixels = (slotSizeInPixels * craftingAndArmorHeightInSlots)
            craftingAndArmorHeightInPixels += (gapBetweenSlots * craftingAndArmorHeightInSlots + 1)

            craftingAndArmorSizeInPixels = (round(craftingAndArmorWidthInPixels), round(craftingAndArmorHeightInPixels))
            
            craftingAndArmorBackground = pygame.surface.Surface(craftingAndArmorSizeInPixels)
            craftingAndArmorBackground.fill(backgroundColor)

            inventorySizeInPixels = (round(inventoryWidthInPixels), round(inventoryHeightInPixels))

            inventoryBackground = pygame.surface.Surface(inventorySizeInPixels)
            inventoryBackground.fill(backgroundColor)
            
            slotSurface = pygame.surface.Surface((slotSizeInPixels, slotSizeInPixels))
            slotSurface.fill(slotColor)

            size = (slotSizeInPixels + gapBetweenSlots * 2, slotSizeInPixels + gapBetweenSlots * 2)
            selectedSlotSurface = pygame.surface.Surface(size)
            selectedSlotSurface.fill((selectedSlotColor))

            fillRect = pygame.rect.Rect(gapBetweenSlots, gapBetweenSlots, slotSizeInPixels, slotSizeInPixels)
            selectedSlotSurface.fill((255, 255, 255), fillRect)
            selectedSlotSurface.set_colorkey((255, 255, 255))

            hotbarSizeInPixels = (round(inventorySizeInPixels[0]), round(slotSizeInPixels + (gapBetweenSlots * 2)))
            hotbarSurface = pygame.surface.Surface(hotbarSizeInPixels)
            hotbarSurface.fill(backgroundColor)

            if alphaForUI < 255:
                hotbarSurface.set_alpha(alphaForUI)
                inventoryBackground.set_alpha(alphaForUI)
                craftingAndArmorBackground.set_alpha(alphaForUI)
                slotSurface.set_alpha(alphaForUI)

            craftingAndArmorXForBlit = (screenWidth - (craftingAndArmorWidthInPixels)) / 2 
            craftingAndArmorYForBlit = (screenHeight - (craftingAndArmorHeightInPixels + inventoryHeightInPixels))# - (slotSizeInPixels * craftingAndArmorHeightInSlots)
            craftingAndArmorYForBlit /= 2


            fontShift = font.size("1")

            self.craftingResultSlot = {
                "contents": "empty",
                "count": 0,
                "renderPosition": (0, 0),
                "selectedSlotRenderPosition": (0, 0),
                "itemCountRenderPosition": (0, 0),
                "rect": pygame.Rect(0, 0, 0, 0), # used for mouse collision
            }


            self.crafting = []
            self.armor = []# head, chest, legs, feet

            # actually add content spots to the armor/crafting
            craftingSlot = {
                "contents": "empty",
                "count": 0,
                "renderPosition": (0, 0),
                "selectedSlotRenderPosition": (0, 0),
                "itemCountRenderPosition": (0, 0),
                "rect": pygame.Rect(0, 0, 0, 0), # used for mouse collision
                "slotId": 0
            }



            slotX = ((widthOfInventoryInSlots) * slotSizeInPixels)
            slotY = (slotSizeInPixels * 1.5)

            renderX = slotX + craftingAndArmorXForBlit + itemIconShift
            renderY = slotY + craftingAndArmorYForBlit + itemIconShift

            rectX = renderX - itemIconShift
            rectY = renderY - itemIconShift

            
            
            craftingAndArmorBackground.blit(slotSurface, (slotX, slotY))

            self.craftingResultSlot["renderPosition"] = (renderX, renderY)
            self.craftingResultSlot["rect"] = pygame.Rect(rectX, rectY, slotSizeInPixels, slotSizeInPixels)
            self.craftingResultSlot["selectedSlotRenderPosition"] = (rectX - gapBetweenSlots, rectY - gapBetweenSlots)
            self.craftingResultSlot["itemCountRenderPosition"] = (rectX + slotSizeInPixels - fontShift[0] - 1, rectY + slotSizeInPixels - fontShift[1] - 1)

           


            slotId = 0

            # create and blit the crafting slots
            for x in range(2):
                for y in range(2):
                    
                    

                    slotId += 1
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
                    newCraftingSlot["slotId"] = 0

                    self.crafting.append(newCraftingSlot)


            # put an arrow that goes towards the result slot for crafting
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




            inventoryXForBlit = (screenWidth - inventoryWidthInPixels) / 2 
            inventoryYForBlit = craftingAndArmorYForBlit + craftingAndArmorHeightInPixels

            hotbarXForBlit = inventoryXForBlit
            hotbarYForBlit = (screenHeight - hotbarSizeInPixels[1]) - (hotbarSizeInPixels[1] / 2)

            inventorySlot = {
                "contents": "empty", # this is where itemData goes
                "count": 0, # how many of x item is in this slot
                "renderPosition": (0, 0),
                "selectedSlotRenderPosition": (0, 0),
                "itemCountRenderPosition": (0, 0),
                "rect": pygame.Rect(0, 0, 0, 0), # used for mouse collision
                "slotId": 0
            }

            self.inventory = []
            self.hotbar = []

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
                    

                    self.inventory.append(updatedInventorySlot)


            



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

                self.hotbar.append(updatedInventorySlot)
            
            inventoryRect = pygame.Rect(inventoryXForBlit, inventoryYForBlit,
                                        inventoryWidthInPixels, inventoryHeightInPixels)
            
            hotbarRect = pygame.Rect(hotbarXForBlit, hotbarYForBlit,
                                    inventoryWidthInPixels, hotbarSizeInPixels[1])
        
            craftingAndArmorRect = pygame.Rect(craftingAndArmorXForBlit, craftingAndArmorYForBlit,
                                               craftingAndArmorWidthInPixels, craftingAndArmorHeightInPixels)
            

            self.inventoryRenderingData = {
                "inventoryRenderPosition": (inventoryXForBlit, inventoryYForBlit),
                "craftingAndArmorRenderPosition": (craftingAndArmorXForBlit, craftingAndArmorYForBlit),
                "hotbarRenderPosition": (hotbarXForBlit, hotbarYForBlit),
                "inventorySurface": inventorySurface,
                "craftingAndArmorSurface": craftingAndArmorSurface,
                "hotbarSurface": hotbarSurface,
                "itemIconShift": itemIconShift,
                "slotSize": slotSizeInPixels,
                "selectedSlotSurface": selectedSlotSurface
            }

            self.otherInventoryData = {
            "inventoryRect": inventoryRect,
            "hotbarRect": hotbarRect,
            "craftingAndArmorRect": craftingAndArmorRect,

            "currentHotbarSlot": 0, # id/index of the slot in the hotbar
            "open": False,
            "slotId": 0,
            "showCraftingAndArmor": True # will be set to false if player is looking in a chest or something
            }

        createALotOfInventoryThings()


        self.timers = {

        }

        # blocks up AND down of reach
        self.verticalBlockReach = 3
        self.horizontalBlockReach = 3
        self.canReachSelectedBlock = False

        self.blockBreakProgress = 0
        self.currentBreakingBlock = None




    def generalMovement(self, deltaTime):

        left = keys[0][pygame.K_a]
        right = keys[0][pygame.K_d]
        up = keys[0][pygame.K_w]
        down = keys[0][pygame.K_s]
        space = keys[0][pygame.K_SPACE]
        
        self.chunkCoord = getChunkCoord(self.x, self.z)
        self.blockCoord = getBlockCoord(self.x, self.y, self.z)

        self.rect.x = self.x
        self.rect.y = self.z

    
        
        for dictKey in self.collision.keys():
            self.collision[dictKey] = False

        # faster? access to variables that need to be used a lot in collision
        rightSide = self.x + self.width
        bottomSide = self.z + self.width
        underSide = self.y - self.height
        
        def doCollisionBelow():
            topLeft = findBlock(self.x, underSide - 3, self.z, ignoreWater = True)
            topRight = findBlock(rightSide, underSide - 3, self.z, ignoreWater = True)
            bottomLeft = findBlock(self.x, underSide - 3, bottomSide, ignoreWater = True)
            bottomRight = findBlock(rightSide, underSide - 3, bottomSide, ignoreWater = True)
            if topLeft or topRight or bottomLeft or bottomRight:
                self.collision["below"] = True
        
        doCollisionBelow()

        def doCollisionAbove():
            topLeft = findBlock(self.x, self.y, self.z, ignoreWater = True)
            topRight = findBlock(rightSide, self.y, self.z, ignoreWater = True)
            bottomLeft = findBlock(self.x, self.y, bottomSide, ignoreWater = True)
            bottomRight = findBlock(rightSide, self.y, bottomSide, ignoreWater = True)
            if topLeft or topRight or bottomLeft or bottomRight:
                self.collision["above"] = True
        
        doCollisionAbove()

        def doCollisionToRight():
            temporaryNumber = rightSide + 1
            aboveTopRight = findBlock(temporaryNumber, self.y, self.z, ignoreWater = True)
            aboveBottomRight = findBlock(temporaryNumber, self.y, bottomSide, ignoreWater = True)
            belowBottomRight = findBlock(temporaryNumber, underSide, bottomSide, ignoreWater = True)
            belowTopRight = findBlock(temporaryNumber, underSide, self.z, ignoreWater = True)
            if aboveTopRight or aboveBottomRight or belowBottomRight or belowTopRight:
                self.collision["right"] = True

        doCollisionToRight()
        
        def doCollisionToLeft():
            temporaryNumber = self.x - 1
            aboveTopLeft = findBlock(temporaryNumber, self.y, self.z, ignoreWater = True)
            aboveBottomLeft = findBlock(temporaryNumber, self.y, bottomSide, ignoreWater = True)
            belowBottomLeft = findBlock(temporaryNumber, underSide, bottomSide, ignoreWater = True)
            belowTopLeft = findBlock(temporaryNumber, underSide, self.z, ignoreWater = True)
            if aboveBottomLeft or aboveTopLeft or belowBottomLeft or belowTopLeft:
                self.collision["left"] = True

        doCollisionToLeft()

        def doCollisionToUp():
            aboveTopLeft = findBlock(self.x, self.y, self.z - 1, ignoreWater = True)
            aboveTopRight = findBlock(rightSide, self.y, self.z - 1, ignoreWater = True)
            belowTopRight = findBlock(rightSide, underSide, self.z - 1, ignoreWater = True)
            belowTopLeft = findBlock(self.x, underSide, self.z - 1, ignoreWater = True)
            if aboveTopLeft or aboveTopRight or belowTopLeft or belowTopRight:
                self.collision["up"] = True

        doCollisionToUp()

        def doCollisionToDown():
            aboveBottomLeft = findBlock(self.x, self.y, bottomSide + 1, ignoreWater = True)
            aboveBottomRight = findBlock(rightSide, self.y, bottomSide + 1, ignoreWater = True)
            belowBottomRight = findBlock(rightSide, underSide, bottomSide + 1, ignoreWater = True)
            belowBottomLeft = findBlock(self.x, underSide, bottomSide + 1, ignoreWater = True)
            if aboveBottomLeft or aboveBottomRight or belowBottomRight or belowBottomLeft:
                self.collision["down"] = True

        doCollisionToDown()

        def checkForBeingInsideOfABlock():
            center = findBlock(self.x + self.width/2, self.y - self.height/2, self.z + self.width/2, extraInfo = True)
            self.collision["insideOfBlock"] = center["type"]

        checkForBeingInsideOfABlock()

        temporaryNumber = (self.y - self.height) + blockSize + 3
        # SEPARATE THESE LATER INTO FUNCTIONS
        aboveToTopRight = findBlock(rightSide + self.xv + 3, temporaryNumber, self.z, ignoreWater = True)
        aboveToBottomRight = findBlock(rightSide + self.xv + 3, temporaryNumber, bottomSide, ignoreWater = True)
        if aboveToTopRight or aboveToBottomRight:
            self.collision["aboveRight"] = True

        aboveToTopLeft = findBlock(self.x + self.xv - 3, temporaryNumber, self.z, ignoreWater = True)
        aboveToBottomLeft = findBlock(self.x + self.xv - 3, temporaryNumber, bottomSide, ignoreWater = True)
        if aboveToTopLeft or aboveToBottomLeft:
            self.collision["aboveLeft"] = True

        aboveToLeftUp = findBlock(self.x, temporaryNumber, self.z + self.zv - 3, ignoreWater = True)
        aboveToRightUp = findBlock(rightSide, temporaryNumber, self.z + self.zv - 3, ignoreWater = True)
        if aboveToLeftUp or aboveToRightUp:
            self.collision["aboveUp"] = True
        
        aboveToRightDown = findBlock(rightSide, temporaryNumber, bottomSide + self.zv + 3, ignoreWater = True)
        aboveToLeftDown = findBlock(self.x, temporaryNumber, bottomSide + self.zv + 3, ignoreWater = True)
        if aboveToLeftDown or aboveToRightDown:
            self.collision["aboveDown"] = True





        currentMaxHorizontalSpeed = self.maxHorizontalSpeed
        if self.collision["insideOfBlock"] == "water":
            currentMaxHorizontalSpeed = self.maxHorizontalSpeed / 2

         # x and z axis movement
        if right and not self.collision["right"]:
            if self.xv < currentMaxHorizontalSpeed:
                self.xv += self.acceleration

        if left and not self.collision["left"]:
            if self.xv > -currentMaxHorizontalSpeed:
                self.xv -= self.acceleration

        if up and not self.collision["up"]:
            if self.zv > -currentMaxHorizontalSpeed:
                self.zv -= self.acceleration

        if down and not self.collision["down"]:
            if self.zv < currentMaxHorizontalSpeed:
                self.zv += self.acceleration

         # y axis movement
        if space:
            if self.collision["insideOfBlock"] == "water":
                # do water stuff
                jumpForce = self.normalJumpForce / 3

                self.yv = jumpForce
            else:
                if self.collision["below"]:
                    # do jump stuff
                    jumpForce = self.normalJumpForce

                    self.yv = jumpForce
            


         # do gravity
        if not self.collision["below"]:
            yvChange = gravity
            if self.collision["insideOfBlock"] == "water":
                yvChange /= 5
            self.yv -= yvChange
        elif self.yv < 0:
            self.yv = 0
            self.y = self.blockCoord[1] * blockSize + self.height
            # re-do collisions, hopefully fixes colliding with walls while hitting
            # the ground hard, looks like it didn't fix it?
            #doCollisionToDown()
            #doCollisionToLeft()
            #doCollisionToUp()
            #doCollisionToRight()
         # don't let player fall out of the world
        if self.y < -300:
            self.y = chunkSize[1] * blockSize
            self.yv = 0

         # don't let player go through ceilings
        if self.collision["above"]:
            if self.yv > 0:
                self.y -= self.yv
                self.yv = 0

         # wall collision
         # and block step up (go up blocks without jumping


        self.booleans["blockStepUsed"] = False

        if self.collision["up"]:
            a = self.collision["below"]
            b = not self.collision["aboveUp"]
            c = not self.booleans["blockStepUsed"]
            d = up
            if a and b and c and d:
                self.y += blockSize
                # update collision, since player's been moved a lot
                doCollisionToDown()
                doCollisionToLeft()
                doCollisionToRight()
                self.booleans["blockStepUsed"] = True
            else:
                self.z += abs(self.zv)
                self.zv = 0
                self.z += 1

        if self.collision["right"]:
            a = self.collision["below"]
            b = not self.collision["aboveRight"]
            c = not self.booleans["blockStepUsed"]
            d = right
            if a and b and c and d:
                self.y += blockSize
                # update collision, since player's been moved a lot
                doCollisionToDown()
                doCollisionToLeft()
                doCollisionToUp()
                self.booleans["blockStepUsed"] = True
            else: 
                self.x -= abs(self.xv)
                self.xv = 0
                self.x -= 1

        if self.collision["left"]:
            a = self.collision["below"]
            b = not self.collision["aboveLeft"]
            c = not self.booleans["blockStepUsed"]
            d = left
            if a and b and c and d:
                self.y += blockSize
                # update collision, since player's been moved a lot
                doCollisionToDown()
                doCollisionToRight()
                doCollisionToUp()
                self.booleans["blockStepUsed"] = True
            else:
                self.x += abs(self.xv)
                self.xv = 0
                self.x += 1
            
        if self.collision["down"]:
            a = self.collision["below"]
            b = not self.collision["aboveDown"]
            c = not self.booleans["blockStepUsed"]
            d = down
            if a and b and c and d:
                self.y += blockSize
                # update collision, since player's been moved a lot
                doCollisionToLeft()
                doCollisionToRight()
                doCollisionToUp()
                self.booleans["blockStepUsed"] = True
            else:
                self.x -= abs(self.zv)
                self.zv = 0
                self.z -= 1
       


         
        # force player speed cap
        if self.xv > currentMaxHorizontalSpeed:
            self.xv = currentMaxHorizontalSpeed
        if self.xv < -currentMaxHorizontalSpeed:
            self.xv = -currentMaxHorizontalSpeed

        if self.zv > currentMaxHorizontalSpeed:
            self.zv = currentMaxHorizontalSpeed
        if self.zv < -currentMaxHorizontalSpeed:
            self.zv = -currentMaxHorizontalSpeed
        
         # friction is handled below
        if (not left and not right) or (left and right):
            self.xv -= self.xv / self.slipperyness
            if self.xv > -0.1 and self.xv < 0.1:
                self.xv = 0
        if (not up and not down) or (up and down):
            self.zv -= self.zv / self.slipperyness
            if self.zv > -0.1 and self.zv < 0.1:
                self.zv = 0
        


         # don't let player get stuck inside of blocks
        if self.collision["insideOfBlock"] != "air":
            if self.collision["insideOfBlock"] != "water":
                self.y += 5
        

         # do all the position updates that other things use
        self.xv = round(self.xv * 100) / 100
        self.yv = round(self.yv * 100) / 100
        self.zv = round(self.zv * 100) / 100

        self.x += (self.xv * deltaTime)
        self.y += (self.yv * deltaTime)
        self.z += (self.zv * deltaTime)

        
        

        self.position = (self.x, self.y, self.z)

    def giveItem(self, item, count = 1):
        
        def checkForStackables(container, done, count, item):
            if not done and item.stackable:
                for slot in container:
                    if slot["contents"] != "empty":
                        if slot["contents"].name == item.name:
                            if slot["count"] != maxStackSize:
                                

                                addedCount = count + slot["count"]
                                if addedCount <= maxStackSize:

                                    slot["count"] = addedCount
                                    return True
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
                        
                        
                        return True
            return done

            

        done = False

        done = checkForStackables(self.hotbar, done, count, item)
        done = checkForStackables(self.inventory, done, count, item)

        done = checkForEmptySlots(self.hotbar, done, count, item)
        done = checkForEmptySlots(self.inventory, done, count, item)

        if not done:
            print("giving the item failed")

        return done


    def doInventoryThings(self):

        
        def toggleInventoryVisibility():
            if keysPressed[pygame.K_e]:
                if self.otherInventoryData["open"]:
                    self.otherInventoryData["open"] = False
                else:
                    self.otherInventoryData["open"] = True

            for slot in self.inventory:
                if slot["contents"] != "empty":
                    slot["contents"].slotId = slot["slotId"]
            for slot in self.hotbar:
                if slot["contents"] != "empty":
                    slot["contents"].slotId = slot["slotId"]
        toggleInventoryVisibility()


        def adjustMouseSelectedBlockHeight():
            # change the selected height of the mouse
            mouse.selectedY = self.y

            if keysPressed[pygame.K_PERIOD]:
                if mouse.selectedYChange < self.verticalBlockReach:
                    mouse.selectedYChange += 1
                
            if keysPressed[pygame.K_COMMA]:
                if mouse.selectedYChange > -self.verticalBlockReach:
                    mouse.selectedYChange -= 1

            mouse.selectedY += mouse.selectedYChange * blockSize
            

            if mouse.selectedY <= 0:
                mouse.selectedY = blockSize
            if mouse.selectedY >= chunkSize[1] * blockSize:
                mouse.selectedY = chunkSize[1] * (blockSize - 1)
        adjustMouseSelectedBlockHeight()

        def changeSelectedHotbarSlot(numberPress):
            if not self.otherInventoryData["open"]:
                keyboardInput = getattr(pygame, "K_" + str(numberPress))
                if keysPressed[keyboardInput]:
                    self.otherInventoryData["currentHotbarSlot"] = numberPress - 1
        
        for i in range(1, 10):
            changeSelectedHotbarSlot(i)

        def dropItems():
            # drop items from the hotbar
            if keysPressed[pygame.K_q]:
                if not self.otherInventoryData["open"]:
                    currentHotbarSlot = self.otherInventoryData["currentHotbarSlot"]
                    item = self.hotbar[currentHotbarSlot]["contents"]

                    if item != "empty":

                        x = self.x + self.width/2 - itemEntitySize/2
                        y = self.y - self.height/2
                        z = self.z + self.width/2 - itemEntitySize/2

                        # figure out velocity for angle of player to mouse

                        xDiff = mouse.cameraRelativeX - x
                        yDiff = mouse.cameraRelativeZ - z

                        angle = math.atan2(yDiff, xDiff)                        

                        xv = math.cos(angle) * 3
                        yv = 2
                        zv = math.sin(angle) * 3

                        count = 1

                        item.drop(x, y, z, xv, yv, zv, self, count)
        dropItems()


        

        def hotbarHeldItemStuff():
            if not self.otherInventoryData["open"]:
                index = self.otherInventoryData["currentHotbarSlot"]
                slotData = self.hotbar[index]
                item = slotData["contents"]

                if mouse.buttons["pressed"]["left"] or mouse.buttons["left"]:
                    self.doStuffOnLeftClick(item)

                if item != "empty":

                    if mouse.buttons["pressed"]["right"]:
                        item.RMBPressedAction(self)
                    elif mouse.buttons["right"]:
                        item.RMBAction(self)

        hotbarHeldItemStuff()

        def mouseInteractionWithInventory():
            mouse.inPlayerInventory = False
            mouse.inPlayerHotbar = False
            mouse.inASlot = False

            def inventoryContentInteraction(container):
                if container == "hotbar":
                    invSection = self.hotbar
                    otherInvSection = self.inventory
                elif container == "inventory":
                    invSection = self.inventory
                    otherInvSection = self.hotbar
                elif container == "craftingAndArmor":
                    invSection = self.craftingAndArmor
                    otherInvSection = self.inventory

                for slot in invSection:
                    item = slot["contents"]

                    if slot["rect"].collidepoint(mouse.x, mouse.y):
                        # communicate rendering information via the mouse
                        mouse.hoveredSlotId = slot["slotId"]
                        mouse.inASlot = True
                        # NEED TO DO:
                        # add logic for crafting slots and also the result slot

                        def checkStackablesInOtherInvSection(amountToMove, done):
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
                                                        otherSlot["count"] = movingCount
                                                        slot["count"] = 0
                                                        slot["contents"] = "empty"
                                                        
                                                        done = True
                                                        return True

                                                    # make the other stack full, reduce item count
                                                    # in first slot so the later update catches it
                                                    elif movingCount > maxStackSize:
                                                        slot["count"] = movingCount - maxStackSize
                                                        otherSlot["count"] = maxStackSize

                                                else: # not moving max amount
                                                    otherSlotNewCount = otherSlot["count"] + amountToMove
                                                    slotNewCount = slot["count"] - amountToMove

                                                    # subtract from first slot, add to the second if possible
                                                    if otherSlotNewCount <= maxStackSize and slotNewCount >= 0:
                                                        slot["count"] = slotNewCount
                                                        otherSlot["count"] = otherSlotNewCount

                                                        if slotNewCount == 0:
                                                            slot["contents"] = "empty"

                                                        return True
                            return done

                        def checkEmptySlotsInOtherInvSection(amountToMove, done):
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
                                            otherSlot["count"] = slot["count"]

                                            slot["contents"] = "empty"
                                            slot["count"] = 0
                                                
                                            
                                            return True

                                        else: # not moving max amount
                                            slotNewCount = slot["count"] - amountToMove

                                            # subtract from first slot, add to the second if possible
                                            if slotNewCount >= 0:
                                                slot["count"] = slotNewCount
                                                otherSlot["count"] = amountToMove
                                                otherSlot["contents"] = slot["contents"]

                                                if slotNewCount == 0:
                                                    slot["contents"] = "empty"
                                            
                                                
                                                return True
                            return done

                        # fast transfer options
                        if mouse.buttons["pressed"]["left"]:
                            done = False
                            
                            if keys[0][pygame.K_LSHIFT]:
                                # move all items from this slot (if possible)
                                done = checkStackablesInOtherInvSection("max", done)
                                done = checkEmptySlotsInOtherInvSection("max", done)
                                
                                
                        
                            if keys[0][pygame.K_LCTRL]:
                                # move a single item from this slot (if possible)
                                done = checkStackablesInOtherInvSection(1, done)
                                done = checkEmptySlotsInOtherInvSection(1, done)
                                    

                            if not done:
                                if not keys[0][pygame.K_LSHIFT] and not keys[0][pygame.K_LCTRL]:
                                    # try to pick up or swap the item in slot and mouse helditem
                                    mouseItem = mouse.heldItem["contents"]
                                    if mouseItem != "empty":
                                        if item != "empty":
                                            if mouseItem.stackable and item.stackable and mouseItem.name == item.name:
                                            
                                                addedCount = mouse.heldItem["count"] + slot["count"]
                                                
                                                if addedCount <= maxStackSize:
                                                    mouse.heldItem["contents"] = "empty"
                                                    mouse.heldItem["count"] = 0

                                                    slot["count"] = addedCount


                                                elif addedCount > maxStackSize:
                                                    newMouseSlotCount = addedCount - maxStackSize

                                                    slot["count"] = maxStackSize
                                                    mouse.heldItem["count"] = newMouseSlotCount
                                            else: # not stacking the item, swap it with mouse's item
                                                newSlotCount = mouse.heldItem["count"]
                                                newSlotItem = mouse.heldItem["contents"]

                                                mouse.heldItem["count"] = slot["count"]
                                                mouse.heldItem["contents"] = slot["contents"]

                                                slot["count"] = newSlotCount
                                                slot["contents"] = newSlotItem


                                        else: # clicked item has nothing there, put mouse contents there
                                            slot["contents"] = mouse.heldItem["contents"]
                                            slot["count"] = mouse.heldItem["count"]

                                            mouse.heldItem["count"] = 0
                                            mouse.heldItem["contents"] = "empty"


                                    else: # mouse has no item in it
                                        if item != "empty":
                                            mouse.heldItem["count"] = slot["count"]
                                            mouse.heldItem["contents"] = slot["contents"]

                                            slot["count"] = 0
                                            slot["contents"] = "empty"



            if self.otherInventoryData["open"]:
                mouse.inPlayerCraftingAndArmor = self.otherInventoryData["craftingAndArmorRect"].collidepoint(mouse.x, mouse.y)
                mouse.inPlayerInventory = self.otherInventoryData["inventoryRect"].collidepoint(mouse.x, mouse.y)
                mouse.inPlayerHotbar = self.otherInventoryData["hotbarRect"].collidepoint(mouse.x, mouse.y)

                if mouse.inPlayerInventory:
                    inventoryContentInteraction("inventory")
                if mouse.inPlayerHotbar:
                    inventoryContentInteraction("hotbar")
                if mouse.inPlayerCraftingAndArmor:
                    inventoryContentInteraction("craftingAndArmor")
        

            # attempt to place mouse's item back in the player's inventory
            if not self.otherInventoryData["open"]:

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

                                                return True
                                            
                                            if addedCount > maxStackSize:
                                                newMouseCount = addedCount - maxStackSize

                                                slot["count"] = maxStackSize
                                                mouse.heldItem["count"] = newMouseCount

                                                return True
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
                                    
                                    return True
                        return done
                        
                                    
                                    


                    done = False

                    done = checkForStackables(self.hotbar, done)
                    done = checkForStackables(self.inventory, done)

                    done = checkForEmptySlots(self.hotbar, done)
                    done = checkForEmptySlots(self.inventory, done)

                    

                    

                    if not done:

                        # center of player
                        x = self.x + self.width/2
                        y = self.y - self.height/2
                        z = self.z + self.width/2

                        # figure out velocity for angle of player to mouse

                        xDiff = mouse.cameraRelativeX - x
                        yDiff = mouse.cameraRelativeZ - z

                        angle = math.atan2(yDiff, xDiff)                        

                        xv = math.cos(angle) * 3
                        yv = 2
                        zv = math.sin(angle) * 3

                        item.drop(x, y, z, xv, yv, zv)

        mouseInteractionWithInventory()   

        
    def handleTimers(self):
        for key, timerValue in self.timers.items():
            if timerValue > 0:
                timerValue -= 1
            if timerValue < 0:
                timerValue += 1
            if timerValue != 0:
                print(str(key) + " " + str(timerValue))
            self.timers[key] = timerValue

    def updateCamera(self):
        camera.x -= round((camera.x - self.x + camera.centerTheCamera[0]) / camera.smoothness)
        camera.y = self.y
        camera.z -= round((camera.z - self.z + camera.centerTheCamera[1]) / camera.smoothness)
        
        camera.currentChunk = getChunkCoord(camera.x, camera.z)

    def updateImageThings(self):
        imageX = self.x - camera.x
        imageY = self.z - camera.z
        
        coordinate = (imageX, imageY)
        self.imageData = (self.image, coordinate)

    def doStuff(self, deltaTime):
        # need to update mouse's camera relative things here, don't want circular imports
        mouse.cameraRelativeX = round((self.x + mouse.x) - screenWidth/2)
        mouse.cameraRelativeZ = round((self.z + mouse.y) - screenHeight/2)
        mouse.cameraRelativePos = (mouse.cameraRelativeX, mouse.cameraRelativeZ)
        
        self.generalMovement(deltaTime)
        self.doInventoryThings()
        
        self.handleTimers()
        
        self.updateCamera()
        self.updateImageThings()

    def positionInSpawnArea(self):
        for y in range(chunkSize[1] - 1):
            if findBlock(0, y * blockSize, 0):
                if not findBlock(0, (y + 1) * blockSize, 0):
                    self.y = (y * blockSize) + self.height
                    break
            else:
                self.y = chunkSize[1] * blockSize

    def doStuffOnLeftClick(self, currentlyHeldItem = "empty"):
        item = currentlyHeldItem

        breakingPower = 1
        breakingSpeed = 1
        breakingType = "none"
        attack = 1
        knockback = 1
        slowestBreakSpeed = 1

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
        if self.currentBreakingBlock != mouse.hoveredBlock["block"]:
            self.blockBreakProgress = 0

        if self.canReachSelectedBlock:

            self.currentBreakingBlock = mouse.hoveredBlock["block"]
            block = self.currentBreakingBlock
            
            if block["hardness"] != "infinity":
                correctTool = False
                powerfulEnoughTool = False

                if breakingPower >= block["hardness"]:
                    powerfulEnoughTool = True
                if breakingType == block["effectiveTool"]:
                    correctTool = True
                
                
                if powerfulEnoughTool and correctTool:
                    self.blockBreakProgress += breakingSpeed / FPS
                else:
                    self.blockBreakProgress += slowestBreakSpeed / FPS


                





                if self.blockBreakProgress >= block["hardness"]:
                    self.blockBreakProgress = 0

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
                        if True: # replace later with silk touch or something
                            if block["type"] == ("grass" or "snowy grass"):
                                itemData.name = "dirt"
                            if block["type"] == ("stone" or "snowy stone"):
                                itemData.name = "cobblestone"
                            
                            
                        entity = ItemEntity(itemData, count, x, y, z, xv, 5, zv)
                        entities.append(entity)

                    air = {
                        "type": "air",
                        "render": False,
                        "alphaValue": 0,
                        "hardness": "infinity",
                        "effectiveTool": "none"
                    }

                    chunks[chunkCoord]["data"][blockCoord] = air

                    smallScaleBlockUpdates(chunkCoord, blockCoord)

                
                

            


            

player = Player()






print("player initialized")
from widelyUsedVariables import camera, blockSize, gravity, chunkSize, maxStackSize
from widelyUsedVariables import screenWidth, screenHeight, chunks, font
from worldgen import getChunkCoord, getBlockCoord, findBlock, generateChunkTerrain
from controls import keysPressed, keys, mouse
import pygame, math



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

        # how i'm organizing the collision
        # default is the same height as player
        # above + down, or right, etc is one block higher
        # below + a side is one block below player
        # it's true if there is a block, otherwise it's false

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
    
        # width and height
        inventoryWidthInPixels = screenWidth / 3
        slotSizeInPixels = round(inventoryWidthInPixels / widthOfInventoryInSlots)

        gapBetweenSlots = round(slotSizeInPixels / 5)


        backgroundColor = (150, 150, 150)
        slotColor = (125, 125, 125)
        selectedSlotColor = (175, 175, 175, 0)
        alphaForUI = 0

        emptySpaceBetweenItemAndSlotBorder = gapBetweenSlots / 2

        itemIconShift = emptySpaceBetweenItemAndSlotBorder

        inventoryWidthInPixels += gapBetweenSlots * (widthOfInventoryInSlots + 1)

        inventoryHeightInPixels = (slotSizeInPixels * heightOfInventoryInSlots)
        inventoryHeightInPixels += gapBetweenSlots * (heightOfInventoryInSlots + 1)

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

        if alphaForUI != 0:
            hotbarSurface.set_alpha(alphaForUI)
            inventoryBackground.set_alpha(alphaForUI)
            slotSurface.set_alpha(alphaForUI)

        inventoryXForBlit = (screenWidth - inventoryWidthInPixels) / 2
        inventoryYForBlit = (screenHeight - inventoryHeightInPixels) / 2

        hotbarXForBlit = inventoryXForBlit
        hotbarYForBlit = (screenHeight - hotbarSizeInPixels[1]) - (hotbarSizeInPixels[1] / 2)

        inventorySlot = {
            "contents": "empty", # this is where itemData goes
            "count": 0, # how many of x item is in this slot
            "renderPosition": (0, 0),
            "selectedSlotRenderPosition": (0, 0),
            "itemCountRenderPosition": (0, 0),
            "rect": pygame.Rect(0, 0, 0, 0) # used for mouse collision
        }
        
        self.inventory = []
        self.hotbar = []

        for y in range(heightOfInventoryInSlots):
            for x in range(widthOfInventoryInSlots):
                slotX = (x * slotSizeInPixels) + ((x + 1) * gapBetweenSlots)
                slotY = (y * slotSizeInPixels) + ((y + 1) * gapBetweenSlots)

                inventoryBackground.blit(slotSurface, (slotX, slotY))

                renderX = inventoryXForBlit + slotX + itemIconShift
                renderY = inventoryYForBlit + slotY + itemIconShift

                rectX = renderX - itemIconShift
                rectY = renderY - itemIconShift

                updatedInventorySlot = inventorySlot.copy()
                
                fontShift = font.size("1")

                updatedInventorySlot["renderPosition"] = (renderX, renderY)
                updatedInventorySlot["itemCountRenderPosition"] = (rectX + slotSizeInPixels - fontShift[0] - 1, rectY + slotSizeInPixels - fontShift[1] - 1)
                updatedInventorySlot["selectedSlotRenderPosition"] = (rectX - gapBetweenSlots,
                                                                      rectY - gapBetweenSlots)
                updatedInventorySlot["rect"] = pygame.Rect(rectX, rectY,
                                                           slotSizeInPixels, slotSizeInPixels)

                self.inventory.append(updatedInventorySlot)

        inventorySurface = inventoryBackground        
    
        # create hotbar data
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

            hotbarSurface.blit(slotSurface, (slotX, slotY))

            self.hotbar.append(updatedInventorySlot)
        
        inventoryRect = pygame.Rect(inventoryXForBlit, inventoryYForBlit,
                                    inventoryWidthInPixels, inventoryHeightInPixels)
        
        hotbarRect = pygame.Rect(hotbarXForBlit, hotbarYForBlit,
                                 inventoryWidthInPixels, hotbarSizeInPixels[1])

        self.inventoryRenderingData = {
            "inventoryRenderPosition": (inventoryXForBlit, inventoryYForBlit),
            "hotbarRenderPosition": (hotbarXForBlit, hotbarYForBlit),
            "inventorySurface": inventorySurface,
            "hotbarSurface": hotbarSurface,
            "itemIconShift": itemIconShift,
            "slotSize": slotSizeInPixels,
            "selectedSlotSurface": selectedSlotSurface
        }

        self.otherInventoryData = {
            "inventoryRect": inventoryRect,
            "hotbarRect": hotbarRect,
            "currentHotbarSlotSelected": 0, # id/index of the slot in the hotbar
            "open": False
        }

        self.timers = {
            # timer for how long to wait when holding RMB when placing blocks
            "blockPlacement": 0
        }
        # x blocks up AND down of reach
        self.verticalBlockReach = 3
        self.horizontalBlockReach = 3




    def generalMovement(self, deltaTime):

        left = keys[0][pygame.K_a]
        right = keys[0][pygame.K_d]
        up = keys[0][pygame.K_w]
        down = keys[0][pygame.K_s]
        space = keys[0][pygame.K_SPACE]
        
        self.chunkCoord = getChunkCoord(self.x, self.z)
        self.blockCoord = getBlockCoord(self.x, self.y, self.z)

        def doPlayerCollision():
            
            for dictKey in self.collision.keys():
                self.collision[dictKey] = False

            # faster? access to variables that need to be used a lot in collision
            rightSide = self.x + self.width
            bottomSide = self.z + self.width
            underSide = self.y - self.height

            topLeft = findBlock(self.x, underSide - 3, self.z, ignoreWater = True)
            topRight = findBlock(rightSide, underSide - 3, self.z, ignoreWater = True)
            bottomLeft = findBlock(self.x, underSide - 3, bottomSide, ignoreWater = True)
            bottomRight = findBlock(rightSide, underSide - 3, bottomSide, ignoreWater = True)
            if topLeft or topRight or bottomLeft or bottomRight:
                self.collision["below"] = True
            
            topLeft = findBlock(self.x, self.y, self.z, ignoreWater = True)
            topRight = findBlock(rightSide, self.y, self.z, ignoreWater = True)
            bottomLeft = findBlock(self.x, self.y, bottomSide, ignoreWater = True)
            bottomRight = findBlock(rightSide, self.y, bottomSide, ignoreWater = True)
            if topLeft or topRight or bottomLeft or bottomRight:
                self.collision["above"] = True
            

            temporaryNumber = rightSide + 1
            aboveTopRight = findBlock(temporaryNumber, self.y, self.z, ignoreWater = True)
            aboveBottomRight = findBlock(temporaryNumber, self.y, bottomSide, ignoreWater = True)
            belowBottomRight = findBlock(temporaryNumber, underSide + 2, bottomSide, ignoreWater = True)
            belowTopRight = findBlock(temporaryNumber, underSide + 2, self.z, ignoreWater = True)
            if aboveTopRight or aboveBottomRight or belowBottomRight or aboveBottomRight:
                self.collision["right"] = True
                    
            
            temporaryNumber = self.x - 1
            aboveTopLeft = findBlock(temporaryNumber, self.y, self.z, ignoreWater = True)
            aboveBottomLeft = findBlock(temporaryNumber, self.y, bottomSide, ignoreWater = True)
            belowBottomLeft = findBlock(temporaryNumber, underSide, bottomSide, ignoreWater = True)
            belowTopLeft = findBlock(temporaryNumber, underSide, self.z, ignoreWater = True)
            if aboveBottomLeft or aboveTopLeft or belowBottomLeft or belowTopLeft:
                self.collision["left"] = True

            aboveTopLeft = findBlock(self.x, self.y, self.z - 1, ignoreWater = True)
            aboveTopRight = findBlock(rightSide, self.y, self.z - 1, ignoreWater = True)
            belowTopRight = findBlock(rightSide, underSide, self.z - 1, ignoreWater = True)
            belowTopLeft = findBlock(self.x, underSide, self.z - 1, ignoreWater = True)
            if aboveTopLeft or aboveTopRight or belowTopLeft or belowTopRight:
                self.collision["up"] = True

            aboveBottomLeft = findBlock(self.x, self.y, bottomSide + 1, ignoreWater = True)
            aboveBottomRight = findBlock(rightSide, self.y, bottomSide + 1, ignoreWater = True)
            belowBottomRight = findBlock(rightSide, underSide, bottomSide + 1, ignoreWater = True)
            belowBottomLeft = findBlock(self.x, underSide, bottomSide + 1, ignoreWater = True)
            if aboveBottomLeft or aboveBottomRight or belowBottomRight or belowBottomLeft:
                self.collision["down"] = True

            center = findBlock(self.x + self.width/2, self.y - self.height/2, self.z + self.width/2, extraInfo = True)
            self.collision["insideOfBlock"] = center["type"]

            temporaryNumber = self.y + (blockSize - self.height + 3)

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



        doPlayerCollision()

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
         # don't let player fall out of the world
        if self.y < blockSize:
            self.yv = 100

         # don't let player go through ceilings
        if self.collision["above"]:
            if self.yv > 0:
                self.y -= self.yv
                self.yv = 0

         # wall collision
         # and block step up (go up blocks without jumping)

        def blockStepUpAndWallCollision(velocity = "xv", side = "right", 
                                        playerInput = right, directionalPushback = "negative"):
            
            aboveSide = "above" + side.capitalize()
            axis = velocity[0]
            
            if self.collision[side]:
                condition1 = self.collision["below"]
                condition2 = self.collision["above"]
                condition3 = self.collision[aboveSide]
                condition4 = playerInput
                condition5 = self.booleans["blockStepUsed"]
                
                if condition1 and not condition2 and not condition3 and condition4 and not condition5:
                    
                    self.y += blockSize
                    
                    self.booleans["blockStepUsed"] = True
                else:    
                    if directionalPushback == "negative":
                        pushback = abs(getattr(self, velocity))
                        thing = getattr(self, axis)
                        setattr(self, axis, (thing - pushback))
                        setattr(self, velocity, 0)

                    if directionalPushback == "positive":
                        pushback = abs(getattr(self, velocity))
                        thing = getattr(self, axis)
                        setattr(self, axis, (thing + pushback))
                        setattr(self, velocity, 0)


         # call function for each side
        self.booleans["blockStepUsed"] = False
        blockStepUpAndWallCollision("xv", "right", right, "negative")
        blockStepUpAndWallCollision("xv", "left", left, "positive")
        blockStepUpAndWallCollision("zv", "up", up, "positive")
        blockStepUpAndWallCollision("zv", "down", down, "negative")


         
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

    def doInventoryThings(self):
        e = pygame.K_e

        # mostly for player inventory goes here now, hooray
        if keysPressed[e]:
            if self.otherInventoryData["open"]:
                self.otherInventoryData["open"] = False
            else:
                self.otherInventoryData["open"] = True

        for slotId, slot in enumerate(self.inventory):
            if slot["contents"] != "empty":
                slot["contents"].slotId = slotId


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

        def changeSelectedHotbarSlot(keyboardInput, slotId):
            if keysPressed[keyboardInput]:
                self.otherInventoryData["currentHotbarSlotSelected"] = slotId
        # there's gotta be a way to do this in a loop with less code, but
        # idk how to do that with the key codes so eh
        changeSelectedHotbarSlot(pygame.K_1, 0)
        changeSelectedHotbarSlot(pygame.K_2, 1)
        changeSelectedHotbarSlot(pygame.K_3, 2)
        changeSelectedHotbarSlot(pygame.K_4, 3)
        changeSelectedHotbarSlot(pygame.K_5, 4)
        changeSelectedHotbarSlot(pygame.K_6, 5)
        changeSelectedHotbarSlot(pygame.K_7, 6)
        changeSelectedHotbarSlot(pygame.K_8, 7)
        changeSelectedHotbarSlot(pygame.K_9, 8)

        def hotbarHeldItemStuff():
            if not self.otherInventoryData["open"]:
                index = self.otherInventoryData["currentHotbarSlotSelected"]
                slotData = self.hotbar[index]
                item = slotData["contents"]

                if item != "empty":
                    # also allow breaking items with fist speed, but
                    # the item will have a breaking speed? or pickaxe power? ect
                    if mouse.buttons["pressed"]["left"]:
                        item.LMBPressedAction()
                    elif mouse.buttons["left"]:
                        item.LMBAction()

                    if mouse.buttons["pressed"]["right"]:
                        item.RMBPressedAction()
                    elif mouse.buttons["right"]:
                        item.RMBAction()
                else:
                    # no item in hand, break items with fist very slowly
                    pass

        hotbarHeldItemStuff()

        def mouseInteractionWithInventory():
            mouse.inPlayerInventory = False
            mouse.inPlayerHotbar = False
            mouse.inASlot = False


            if self.otherInventoryData["open"]:
                mouse.inPlayerInventory = self.otherInventoryData["inventoryRect"].collidepoint(mouse.x, mouse.y)
                mouse.inPlayerHotbar = self.otherInventoryData["hotbarRect"].collidepoint(mouse.x, mouse.y)

                if mouse.inPlayerInventory:
                    for slotId, slot in enumerate(self.inventory):
                        item = slot["contents"]
                            
                        if slot["rect"].collidepoint(mouse.x, mouse.y):
                            # communicate rendering information via the mouse
                            # to rendering
                            mouse.hoveredSlotId = slotId
                            mouse.inASlot = True
                            # interaction for moving around items and stuff
                            if mouse.buttons["pressed"]["left"]:
                                if keys[0][pygame.K_LSHIFT] and item != "empty":
                                    movingItem = item
                                    movingCount = slot["count"]
                                    
                                    movingHasBeenDone = False

                                    for hotbarSlot in self.hotbar:
                                        if hotbarSlot["contents"] == item:
                                            addedCount = movingCount + hotbarSlot["count"]
                                            if addedCount <= maxStackSize:

                                                slot["count"] = 0
                                                slot["contents"] = "empty"

                                                hotbarSlot["count"] = addedCount
                                                hotbarSlot["contents"] = movingItem

                                                movingHasBeenDone = True
                                                break
                                            # may add putting extra stuff
                                                
                                    if not movingHasBeenDone:
                                        for hotbarSlot in self.hotbar:
                                            if hotbarSlot["contents"] == "empty":

                                                hotbarSlot["contents"] = movingItem
                                                hotbarSlot["count"] = movingCount

                                                slot["contents"] = "empty"
                                                slot["count"] = 0
                                                break
                                else:
                                    mouseItem = mouse.heldItem["contents"]
                                    mouseCount = mouse.heldItem["count"]

                                    mouse.heldItem["contents"] = item
                                    mouse.heldItem["count"] = slot["count"]

                                    slot["contents"] = mouseItem
                                    slot["count"] = mouseCount
                
                if mouse.inPlayerHotbar:
                    for slotId, slot in enumerate(self.hotbar):
                        item = slot["contents"]

                        if slot["rect"].collidepoint(mouse.x, mouse.y):
                            # info for rendering stuff
                            mouse.hoveredSlotId = slotId
                            mouse.inASlot = True
                            # interaction for hotbar and mouse stuff
                            if mouse.buttons["pressed"]["left"]:
                                if keys[0][pygame.K_LSHIFT] and item != "empty":
                                    movingItem = item
                                    movingCount = slot["count"]
                                    
                                    movingHasBeenDone = False

                                    for inventorySlot in self.inventory:
                                        if inventorySlot["contents"] == item:
                                            addedCount = movingCount + inventorySlot["count"]
                                            if addedCount <= maxStackSize:

                                                inventorySlot["count"] = addedCount
                                                inventorySlot["contents"] = movingItem
                                                
                                                slot["count"] = 0
                                                slot["contents"] = "empty"

                                                movingHasBeenDone = True
                                                break
                                            # may add putting extra stuff
                                                
                                    if not movingHasBeenDone:
                                        for inventorySlot in self.inventory:
                                            if inventorySlot["contents"] == "empty":

                                                inventorySlot["contents"] = movingItem
                                                inventorySlot["count"] = movingCount

                                                slot["contents"] = "empty"
                                                slot["count"] = 0
                                                break
                                else:
                                    mouseItem = mouse.heldItem["contents"]
                                    mouseCount = mouse.heldItem["count"]

                                    mouse.heldItem["contents"] = item
                                    mouse.heldItem["count"] = slot["count"]

                                    slot["contents"] = mouseItem
                                    slot["count"] = mouseCount
                    

        mouseInteractionWithInventory()        
        
    def handleTimers(self):
        for key, timerValue in self.timers.items():
            if timerValue > 0:
                timerValue -= 1
            if timerValue < 0:
                timerValue += 1
            if timerValue != 0:
                print(str(key) + " " + str(timerValue))

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




            

player = Player()
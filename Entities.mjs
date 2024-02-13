import { blockSize, gravity, maxStackSize, itemEntitySize, Rect } from "./GlobalVariables.mjs";
import { findBlock } from "./Worldgen.mjs";


// base entity with no ai
class Entity {
    constructor(x, y, z, xv, yv, zv) {
        this.x = x || 0; this.xv = xv || 0;
        this.y = y || 0; this.yv = yv || 0;
        this.z = z || 0; this.zv = zv || 0;

        this.deleteThis = false;

        this.width = blockSize;
        this.height = this.width;

        this.rect = Rect(0, 0, this.width, this.height);

        
    }

        this.width = blockSize
        this.height = this.width

        this.rect = pygame.rect.Rect(0, 0, this.width, this.width)

};
# used for items that are on the ground, like after breaking something
class ItemEntity(Entity):
    def __init__(this, itemData, count, x, y, z, xv = 0, yv = 0, zv = 0):
        super().__init__(x, y, z, xv, yv, zv)
        this.itemData = itemData
        this.count = count

        this.width = itemEntitySize
        this.height = itemEntitySize
        this.rect = pygame.rect.Rect(0, 0, this.width, this.height)

        this.maxFallingVelocity = -10

        this.timers = {
            "pickupDelay": 20
        }



    def positionUpdates(this, player):

        a = findBlock(this.x, this.y - this.height, this.z, ignoreWater = True)
        b = findBlock(this.x, this.y - this.height, this.z + this.width, ignoreWater = True)
        c = findBlock(this.x + this.width, this.y - this.height, this.z, ignoreWater = True)
        d = findBlock(this.x + this.width, this.y - this.height, this.z + this.width, ignoreWater = True)
        blockBelow = False
        if a or b or c or d:
            blockBelow = True
        
        if blockBelow:
            # snap to floor
            this.yv = 0
            # normalize y coordinate, should set it to on top of the block
            this.y = math.floor(this.y / blockSize) * blockSize + this.height

            # friction
            this.xv -= this.xv / 15
            this.zv -= this.zv / 15
            if this.xv > -0.1 and this.xv < 0.1:
                this.xv = 0
            if this.zv > -0.1 and this.zv < 0.1:
                this.zv = 0
        else:
            # do gravity
            if this.yv > this.maxFallingVelocity:
                this.yv -= gravity

        # do wall collision, but only if xv/zv is != 0, for performance
        if this.xv != 0:
            if this.xv > 0:
                blockToRight = findBlock(this.x + this.width + 1, this.y, this.z)
                if blockToRight:
                    this.x -= this.xv
                    this.xv = 0
            if this.xv < 0:
                blockToLeft = findBlock(this.x - 1, this.y, this.z)
                if blockToLeft:
                    this.x -= this.xv
                    this.xv = 0

        if this.zv != 0:
            if this.zv > 0:
                blockToUp = findBlock(this.x, this.y, this.z - 1)
                if blockToUp:
                    this.z -= this.zv
                    this.zv = 0
            if this.zv < 0:
                blockToDown = findBlock(this.x, this.y, this.z + this.width + 1)
                if blockToDown:
                    this.z -= this.zv
                    this.zv = 0

        insideABlock = findBlock(this.x + this.width/2, this.y - this.height/2, this.z + this.width/2, ignoreWater = True)
        if insideABlock:
            this.y += blockSize/2
            this.yv = 2
        
        this.x += this.xv
        this.y += this.yv
        this.z += this.zv

        this.rect.x = this.x
        this.rect.y = this.z

    def runTimers(this):
        for key, value in this.timers.items():
            if value > 0:
                value -= 1
            if value < 0:
                value += 1
            this.timers[key] = value

    def playerInteraction(this, player):
        if this.timers["pickupDelay"] == 0:
            
            if this.rect.colliderect(player.rect):

                itemPickedUp = player.giveItem(this.itemData, this.count)
                if itemPickedUp:
                    this.deletethis = True

    def doStuff(this, player):
        
        if not this.deletethis:
            this.positionUpdates(player)
            this.runTimers()

            this.playerInteraction(player)









consoleLog("Entities.mjs initialized");

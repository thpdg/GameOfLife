import sys

colorChart = {}
initialized = False

def defineColors(colorChart:dict, graphics, paletteName="default"):
    # Required Colors
    colorChart["White"] = graphics.create_pen(64, 64, 64)
    colorChart["Black"] = graphics.create_pen(0,0,0)

    if paletteName == "default":
        colorChart["Red"] = graphics.create_pen(255,0,0)
    
    if paletteName == "gameboy":
        colorChart["dark"] = graphics.create_pen(15,56,15)
        colorChart["medium"] = graphics.create_pen(48,98,48)
        colorChart["light"] = graphics.create_pen(139,172,15)
        colorChart["highlight"] = graphics.create_pen(155,188,15)
        colorChart["off"] = graphics.create_pen(170,170,170)

    if paletteName == "red":
        colorChart["dark"] = graphics.create_pen(138,19,16)
        colorChart["medium"] = graphics.create_pen(156,29,25)
        colorChart["light"] = graphics.create_pen(179,36,32)
        colorChart["highlight"] = graphics.create_pen(255,0,0)
        colorChart["off"] = graphics.create_pen(164,140,29)

def clear_board():
     if sys.implementation.name == 'micropython':
         graphics.remove_clip()
         graphics.set_pen(graphics.create_pen(0,0,0))
         graphics.clear()

def initializei75():
    if sys.implementation.name != 'micropython':
        print("Not on i75")
        return
    
    print("Initializing Board")
    
    global colorChart
    global graphics
    global initialized
    global i75

    if sys.implementation.name == 'micropython':
        from pimoroni_i2c import PimoroniI2C
        from pimoroni import HEADER_I2C_PINS  # or PICO_EXPLORER_I2C_PINS or HEADER_I2C_PINS
        from breakout_encoder_wheel import BreakoutEncoderWheel, UP, DOWN, LEFT, RIGHT, CENTRE, NUM_LEDS
        from interstate75 import Interstate75, DISPLAY_INTERSTATE75_32X32

        # Setup Interstate 75 Board
        i75 = Interstate75(display=DISPLAY_INTERSTATE75_32X32)
        graphics = i75.display
        width = i75.width
        height = i75.height

        defineColors(colorChart,graphics,"gameboy")
        initialized = True

def drawBoard(boardData, colorFunction)->bool:
    if not initialized:
        print("LED Board Not Initialized")
        return False
    else:
        print("Updating LED Board")
    
    clear_board()
    
    for y in range(32):
        for x in range(32):
            if boardData[x][y].alive:
                neighbors = colorFunction(boardData,x,y)
                graphics.set_pen(colorChart["highlight"])
                if neighbors < 2 or neighbors > 3:
                    graphics.set_pen(colorChart["dark"])
            else:
                graphics.set_pen(colorChart["Black"])
            graphics.pixel(x,y)
    i75.update()
    print("Board updated")
    return True
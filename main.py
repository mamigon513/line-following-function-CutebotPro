# set variables
lwheel = 10
rwheel = 10
error = 0
# which line are we following:
line = -1 # 0 is left, 1 is right

# set starting speed
CutebotPro.pwm_cruise_control(lwheel, rwheel)
basic.pause(50)

def turn_right():
    global lwheel, rwheel
    lwheel = lwheel + (abs(error)/3000)*50
    rwheel = rwheel - (abs(error)/3000)*50
    # Set the change
    CutebotPro.pwm_cruise_control(lwheel, rwheel)
    #delay 0.05 sec        b
    basic.pause(5)
def turn_left():
    global lwheel, rwheel
    lwheel = lwheel - (abs(error)/3000)*50
    rwheel = rwheel + (abs(error)/3000)*50
    # Set the change
    CutebotPro.pwm_cruise_control(lwheel, rwheel)
    #delay 0.05 sec
    basic.pause(5)

def on_forever():

    global lwheel, rwheel, error, line

    # get the line offset
    error = CutebotPro.get_offset()

    # if detects no line
    if abs(error) == 3000:
        lwheel = 0
        rwheel = 0

        #turn on both headlight (red)
        CutebotPro.color_light(CutebotProRGBLight.RGBL, 0xff0000)
        CutebotPro.color_light(CutebotProRGBLight.RGBR, 0xff0000)
    # if detects a big line
    if error == 0:
        magnet = input.magnetic_force(Dimension.X)
        if abs(magnet) > 0: # magnet detected
            error = 3000
            turn_left()
            # turn on left headlight (green)
            CutebotPro.color_light(CutebotProRGBLight.RGBL, 0x00ff00)
            basic.pause(100)

            #magnet got further away
            if abs(magnet) > input.magnetic_force(Dimension.X):
                error = 3000
                turn_right()
                # turn on right headlight (green)
                CutebotPro.color_light(CutebotProRGBLight.RGBR, 0x00ff00)
                basic.pause(500)
        elif magnet == 0:
            if line == 1: # line is to the left
                turn_right()
                basic.pause(100)
                CutebotPro.color_light(CutebotProRGBLight.RGBR, 0x00ff00)
    # too far left
    if error > 0:
        turn_right()
        line = 1 # line is to the right
        # turn on left headlight (red)
        CutebotPro.color_light(CutebotProRGBLight.RGBL, 0xff0000)  
    # too far right
    if error < 0:
        turn_left()
        line = 0 # line is to the left
        #turn on right headlight (red)
        CutebotPro.color_light(CutebotProRGBLight.RGBR, 0xff0000)


    # reset speed and headlights
    CutebotPro.turn_off_all_headlights()
    lwheel = 10
    rwheel = 10

    CutebotPro.pwm_cruise_control(lwheel, rwheel)
    basic.pause(5)

basic.forever(on_forever)

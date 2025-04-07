
# set variables
lwheel = 10
rwheel = 10
error = 0
# which line are we following:
line = -1 # 0 is left, 1 is right
maxturnspeed = 50

#magnet present
mag = 0

# set starting speed
CutebotPro.pwm_cruise_control(lwheel, rwheel)
basic.pause(50)

def turn_right():
    global lwheel, rwheel, maxturnspeed
    lwheel = lwheel + (abs(error)/3000)*maxturnspeed
    rwheel = rwheel - (abs(error)/3000)*maxturnspeed
    # Set the change
    CutebotPro.pwm_cruise_control(lwheel, rwheel)
    #delay 0.01 sec
    basic.pause(10)
def turn_left():
    global lwheel, rwheel, maxturnspeed
    lwheel = lwheel - (abs(error)/3000)*maxturnspeed
    rwheel = rwheel + (abs(error)/3000)*maxturnspeed
    # Set the change
    CutebotPro.pwm_cruise_control(lwheel, rwheel)
    #delay 0.01 sec
    basic.pause(10)
    
def magnet():
    if abs(input.magnetic_force(Dimension.Y)) >= 500:
        magnet = 1
        # turn headlights green
        CutebotPro.color_light(CutebotProRGBLight.RGBL, 0x00ff00)
        CutebotPro.color_light(CutebotProRGBLight.RGBR, 0x00ff00)

def follow_line():

    global lwheel, rwheel, error, line

    # get the line offset
    error = CutebotPro.get_offset()

    # make the left side of line the center
    error = error + 1000

    # if detects no line
    if abs(error) == 3000:
        lwheel = 0
        rwheel = 0

        #turn on both headlight (red)
        CutebotPro.color_light(CutebotProRGBLight.RGBL, 0xff0000)
        CutebotPro.color_light(CutebotProRGBLight.RGBR, 0xff0000)
    #### Intersection ####
    # if detects a big line (error is less than 100)
    if abs(error) < 100:
        if error > 0: # robot is to the left of intersection (make a big right turn)
            error = 3000/error
            turn_right()
            basic.pause(100)
            #yellow light
            CutebotPro.color_light(CutebotProRGBLight.RGBL, 0xffff00)
        elif error < 0: # robot is to the right of intersection (make a big left turn)
            error = 3000/error
            turn_left()
            basic.pause(100)
            #yellow light
            CutebotPro.color_light(CutebotProRGBLight.RGBR, 0xffff00)
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
    magnet()


# Run line follow till magnet detected then stop
while (mag == 0):
    follow_line()
# stop robot
CutebotPro.pwm_cruise_control(0, 0)
basic.pause(100)
CutebotPro.turn_off_all_headlights()

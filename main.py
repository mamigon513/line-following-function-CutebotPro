#def detect_line():
    #** Description:
        # This function will follow a black line 
        # and stop when it detects a magnet(headlights turn green)
        # The left headlight turns red when it is too far left and 
        # right headlight turn red when it is too far right

    ### set variables ###
error = 0
maxturnspeed = 50

    #magnet present
mag = 0 

    # set starting speed
CutebotPro.pwm_cruise_control(10, 10)
basic.pause(50)

def turn_right(left, right, err):
    left = left + (abs(err)/3000)*maxturnspeed
    right = right - (abs(err)/3000)*maxturnspeed
    # Set the change
    CutebotPro.pwm_cruise_control(left, right)
    #delay 0.01 sec
    basic.pause(10)
def turn_left(left, right, err):
    left = left - (abs(err)/3000)*maxturnspeed
    right = right + (abs(err)/3000)*maxturnspeed
    # Set the change
    CutebotPro.pwm_cruise_control(left, right)
    #turn for 0.01 sec
    basic.pause(10)

def detect_magnet():
    magnet = 0
    if abs(input.magnetic_force(Dimension.Y)) >= 500:
        magnet = 1
        # turn headlights green
        CutebotPro.color_light(CutebotProRGBLight.RGBL, 0x00ff00)
        CutebotPro.color_light(CutebotProRGBLight.RGBR, 0x00ff00)
    return magnet

def follow_line():
    #base speed
    lwheel = 10
    rwheel = 10
    # get the line offset
    error = CutebotPro.get_offset() + 500 # make the left side of line the center
    # if detects no line (both red)
    if error >= 3000:
        lwheel = 0
        rwheel = 0
        #turn on both headlights (red)
        CutebotPro.color_light(CutebotProRGBLight.RGBL, 0xff0000)
        CutebotPro.color_light(CutebotProRGBLight.RGBR, 0xff0000)
        basic.pause(10)
    #### Intersection ####
    # if detects a big line (error is less than 100)
    #if abs(error) < 100:
       # if error > 0: # robot is to the left of intersection (make a big right turn)
       #     error = 3000/error
        #    turn_right(lwheel, rwheel, error)
      #      basic.pause(100)
            #yellow light
      #      CutebotPro.color_light(CutebotProRGBLight.RGBL, 0xffff00)
      #  elif error < 0: # robot is to the right of intersection (make a big left turn)
      #      error = 3000/error
       #     turn_left(lwheel, rwheel, error)
      #      basic.pause(100)
            #yellow light
      #      CutebotPro.color_light(CutebotProRGBLight.RGBR, 0xffff00)
    
    # too far left (left red)
    if error > 0:
        turn_right(lwheel, rwheel, error)
        # turn on left headlight (red)
        CutebotPro.color_light(CutebotProRGBLight.RGBL, 0xff0000)  
    # too far right (right red)
    if error < 0:
        turn_left(lwheel, rwheel, error)
        #turn on right headlight (red)
        CutebotPro.color_light(CutebotProRGBLight.RGBR, 0xff0000)


    # reset speed and headlights
    CutebotPro.turn_off_all_headlights()

    CutebotPro.pwm_cruise_control(10, 10)
    basic.pause(5)

# Run line follow till magnet detected then stop
while (mag == 0):
    follow_line()
    mag = detect_magnet()
# stop robot
CutebotPro.pwm_cruise_control(0, 0)
CutebotPro.stop_immediately(CutebotProMotors.ALL)
basic.pause(100)
CutebotPro.turn_off_all_headlights()
# set variables
lwheel = 10
rwheel = 10
error = 0
# which line are we following:
line = -1 # 0 is left, 1 is right

# set starting speed
CutebotPro.pwm_cruise_control(lwheel, rwheel)
basic.pause(50)

def on_in_background():
    # check if we are at intersection (tracking states 4,5,6,7,10,15)
    if CutebotPro.get_grayscale_sensor_state(TrackbitStateType.TRACKING_STATE_4) or CutebotPro.get_grayscale_sensor_state(TrackbitStateType.TRACKING_STATE_5) or CutebotPro.get_grayscale_sensor_state(TrackbitStateType.TRACKING_STATE_6) or CutebotPro.get_grayscale_sensor_state(TrackbitStateType.TRACKING_STATE_7) or CutebotPro.get_grayscale_sensor_state(TrackbitStateType.TRACKING_STATE_10) or CutebotPro.get_grayscale_sensor_state(TrackbitStateType.TRACKING_STATE_15):
        # left line (go right instead)
        if line == 0:
            lwheel = lwheel + (error/3000)*50
            rwheel = 0
            basic.show_leds("""
            # # . . .
            # # . . .
            # # . . .
            # # . . .
            # # . . .
            """)
        # right line (go left instead)
        elif line == 1:
            rwheel = rwheel + (error/3000)*-50
            lwheel = 0 
            basic.show_leds("""
            . . . # #
            . . . # #
            . . . # #
            . . . # #
            . . . # #
            """)
        elif line == -1:
            basic.show_leds("""
            # # # # #
            # # # # #
            . . . . .
            . . . . .
            . . . . .
            """)
        # Set the change
        CutebotPro.pwm_cruise_control(lwheel, rwheel)

        # turn on headlights to indicate (blue)
        CutebotPro.color_light(CutebotProRGBLight.RGBL, 0x00ffff)
        CutebotPro.color_light(CutebotProRGBLight.RGBR, 0x00ffff)

        basic.pause(100)

        # reset speed and headlights
        CutebotPro.turn_off_all_headlights()
        lwheel = 10
        rwheel = 10


def on_forever():
    
    control.in_background(on_in_background)

    global lwheel, rwheel, line, error
    # check which line we are following:
    if CutebotPro.get_grayscale_sensor_state(TrackbitStateType.TRACKING_STATE_13) or CutebotPro.get_grayscale_sensor_state(TrackbitStateType.TRACKING_STATE_14) or CutebotPro.get_grayscale_sensor_state(TrackbitStateType.TRACKING_STATE_12):
        line = 1 # right side (tracking states 12,13,14)
    elif CutebotPro.get_grayscale_sensor_state(TrackbitStateType.TRACKING_STATE_9) or CutebotPro.get_grayscale_sensor_state(TrackbitStateType.TRACKING_STATE_11) or CutebotPro.get_grayscale_sensor_state(TrackbitStateType.TRACKING_STATE_8):
        line = 0 # left side (tracking states 8,9,11)

    # get the line offset
    error = CutebotPro.get_offset()

    # if detects no line
    if abs(error) == 3000:
        lwheel = 0
        rwheel = 0

        #turn on both headlight (red)
        CutebotPro.color_light(CutebotProRGBLight.RGBL, 0xff0000)
        CutebotPro.color_light(CutebotProRGBLight.RGBR, 0xff0000)
    # too far left
    if error > 0:
        #lasterr = error
        lwheel = lwheel + (error/3000)*50
        
        # turn on left headlight (red)
        CutebotPro.color_light(CutebotProRGBLight.RGBL, 0xff0000)  
    # too far right
    if error < 0:
        rwheel = rwheel + (error/3000)*-50
        lwheel = 0

        #turn on right headlight (red)
        CutebotPro.color_light(CutebotProRGBLight.RGBR, 0xff0000)

    # Set the change     
    CutebotPro.pwm_cruise_control(lwheel, rwheel)
    #delay 0.02 sec
    basic.pause(5)

    # reset speed and headlights
    CutebotPro.turn_off_all_headlights()
    lwheel = 10
    rwheel = 10

    CutebotPro.pwm_cruise_control(lwheel, rwheel)
    basic.pause(5)

basic.forever(on_forever)
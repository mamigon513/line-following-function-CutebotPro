//  set variables
let lwheel = 10
let rwheel = 10
let error = 0
//  which line are we following:
let line = -1
//  0 is left, 1 is right
//  set starting speed
CutebotPro.pwmCruiseControl(lwheel, rwheel)
basic.pause(50)
basic.forever(function on_forever() {
    control.inBackground(function on_in_background() {
        let lwheel: number;
        let rwheel: number;
        //  check if we are at intersection (tracking states 4,5,6,7,10,15)
        if (CutebotPro.getGrayscaleSensorState(TrackbitStateType.Tracking_State_4) || CutebotPro.getGrayscaleSensorState(TrackbitStateType.Tracking_State_5) || CutebotPro.getGrayscaleSensorState(TrackbitStateType.Tracking_State_6) || CutebotPro.getGrayscaleSensorState(TrackbitStateType.Tracking_State_7) || CutebotPro.getGrayscaleSensorState(TrackbitStateType.Tracking_State_10) || CutebotPro.getGrayscaleSensorState(TrackbitStateType.Tracking_State_15)) {
            //  left line (go right instead)
            if (line == 0) {
                lwheel = lwheel + error / 3000 * 50
                rwheel = 0
                basic.showLeds(`
            # # . . .
            # # . . .
            # # . . .
            # # . . .
            # # . . .
            `)
            } else if (line == 1) {
                //  right line (go left instead)
                rwheel = rwheel + error / 3000 * -50
                lwheel = 0
                basic.showLeds(`
            . . . # #
            . . . # #
            . . . # #
            . . . # #
            . . . # #
            `)
            } else if (line == -1) {
                basic.showLeds(`
            # # # # #
            # # # # #
            . . . . .
            . . . . .
            . . . . .
            `)
            }
            
            //  Set the change
            CutebotPro.pwmCruiseControl(lwheel, rwheel)
            //  turn on headlights to indicate (blue)
            CutebotPro.colorLight(CutebotProRGBLight.RGBL, 0x00ffff)
            CutebotPro.colorLight(CutebotProRGBLight.RGBR, 0x00ffff)
            basic.pause(100)
            //  reset speed and headlights
            CutebotPro.turnOffAllHeadlights()
            lwheel = 10
            rwheel = 10
        }
        
    })
    
    //  check which line we are following:
    if (CutebotPro.getGrayscaleSensorState(TrackbitStateType.Tracking_State_13) || CutebotPro.getGrayscaleSensorState(TrackbitStateType.Tracking_State_14) || CutebotPro.getGrayscaleSensorState(TrackbitStateType.Tracking_State_12)) {
        line = 1
    } else if (CutebotPro.getGrayscaleSensorState(TrackbitStateType.Tracking_State_9) || CutebotPro.getGrayscaleSensorState(TrackbitStateType.Tracking_State_11) || CutebotPro.getGrayscaleSensorState(TrackbitStateType.Tracking_State_8)) {
        //  right side (tracking states 12,13,14)
        line = 0
    }
    
    //  left side (tracking states 8,9,11)
    //  get the line offset
    error = CutebotPro.getOffset()
    //  if detects no line
    if (Math.abs(error) == 3000) {
        lwheel = 0
        rwheel = 0
        // turn on both headlight (red)
        CutebotPro.colorLight(CutebotProRGBLight.RGBL, 0xff0000)
        CutebotPro.colorLight(CutebotProRGBLight.RGBR, 0xff0000)
    }
    
    //  too far left
    if (error > 0) {
        // lasterr = error
        lwheel = lwheel + error / 3000 * 50
        //  turn on left headlight (red)
        CutebotPro.colorLight(CutebotProRGBLight.RGBL, 0xff0000)
    }
    
    //  too far right
    if (error < 0) {
        rwheel = rwheel + error / 3000 * -50
        lwheel = 0
        // turn on right headlight (red)
        CutebotPro.colorLight(CutebotProRGBLight.RGBR, 0xff0000)
    }
    
    //  Set the change     
    CutebotPro.pwmCruiseControl(lwheel, rwheel)
    // delay 0.02 sec
    basic.pause(5)
    //  reset speed and headlights
    CutebotPro.turnOffAllHeadlights()
    lwheel = 10
    rwheel = 10
    CutebotPro.pwmCruiseControl(lwheel, rwheel)
    basic.pause(5)
})

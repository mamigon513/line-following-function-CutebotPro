// def detect_line():
// ** Description:
//  This function will follow a black line 
//  and stop when it detects a magnet(headlights turn green)
//  The left headlight turns red when it is too far left and 
//  right headlight turn red when it is too far right
// ## set variables ###
let error = 0
let maxturnspeed = 50
// magnet present
let mag = 0
//  set starting speed
CutebotPro.pwmCruiseControl(10, 10)
basic.pause(50)
function turn_right(left: number, right: number, err: number) {
    left = left + Math.abs(err) / 3000 * maxturnspeed
    right = right - Math.abs(err) / 3000 * maxturnspeed
    //  Set the change
    CutebotPro.pwmCruiseControl(left, right)
    // delay 0.01 sec
    basic.pause(10)
}

function turn_left(left: number, right: number, err: number) {
    left = left - Math.abs(err) / 3000 * maxturnspeed
    right = right + Math.abs(err) / 3000 * maxturnspeed
    //  Set the change
    CutebotPro.pwmCruiseControl(left, right)
    // turn for 0.01 sec
    basic.pause(10)
}

function detect_magnet(): number {
    let magnet = 0
    if (Math.abs(input.magneticForce(Dimension.Y)) >= 500) {
        magnet = 1
        //  turn headlights green
        CutebotPro.colorLight(CutebotProRGBLight.RGBL, 0x00ff00)
        CutebotPro.colorLight(CutebotProRGBLight.RGBR, 0x00ff00)
    }
    
    return magnet
}

function follow_line() {
    // base speed
    let lwheel = 10
    let rwheel = 10
    //  get the line offset
    let error = CutebotPro.getOffset() + 500
    //  make the left side of line the center
    //  if detects no line (both red)
    if (error >= 3000) {
        lwheel = 0
        rwheel = 0
        // turn on both headlights (red)
        CutebotPro.colorLight(CutebotProRGBLight.RGBL, 0xff0000)
        CutebotPro.colorLight(CutebotProRGBLight.RGBR, 0xff0000)
        basic.pause(10)
    }
    
    // ### Intersection ####
    //  if detects a big line (error is less than 100)
    // if abs(error) < 100:
    //  if error > 0: # robot is to the left of intersection (make a big right turn)
    //      error = 3000/error
    //     turn_right(lwheel, rwheel, error)
    //       basic.pause(100)
    // yellow light
    //       CutebotPro.color_light(CutebotProRGBLight.RGBL, 0xffff00)
    //   elif error < 0: # robot is to the right of intersection (make a big left turn)
    //       error = 3000/error
    //      turn_left(lwheel, rwheel, error)
    //       basic.pause(100)
    // yellow light
    //       CutebotPro.color_light(CutebotProRGBLight.RGBR, 0xffff00)
    //  too far left (left red)
    if (error > 0) {
        turn_right(lwheel, rwheel, error)
        //  turn on left headlight (red)
        CutebotPro.colorLight(CutebotProRGBLight.RGBL, 0xff0000)
    }
    
    //  too far right (right red)
    if (error < 0) {
        turn_left(lwheel, rwheel, error)
        // turn on right headlight (red)
        CutebotPro.colorLight(CutebotProRGBLight.RGBR, 0xff0000)
    }
    
    //  reset speed and headlights
    CutebotPro.turnOffAllHeadlights()
    CutebotPro.pwmCruiseControl(10, 10)
    basic.pause(5)
}

//  Run line follow till magnet detected then stop
while (mag == 0) {
    follow_line()
    mag = detect_magnet()
}
//  stop robot
CutebotPro.pwmCruiseControl(0, 0)
CutebotPro.stopImmediately(CutebotProMotors.ALL)
basic.pause(100)
CutebotPro.turnOffAllHeadlights()

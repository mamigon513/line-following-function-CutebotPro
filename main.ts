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
function turn_right() {
    
    lwheel = lwheel + Math.abs(error) / 3000 * 50
    rwheel = rwheel - Math.abs(error) / 3000 * 50
    //  Set the change
    CutebotPro.pwmCruiseControl(lwheel, rwheel)
    // delay 0.05 sec        b
    basic.pause(5)
}

function turn_left() {
    
    lwheel = lwheel - Math.abs(error) / 3000 * 50
    rwheel = rwheel + Math.abs(error) / 3000 * 50
    //  Set the change
    CutebotPro.pwmCruiseControl(lwheel, rwheel)
    // delay 0.05 sec
    basic.pause(5)
}

basic.forever(function on_forever() {
    let magnet: number;
    
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
    
    //  if detects a big line
    if (error == 0) {
        magnet = input.magneticForce(Dimension.X)
        if (Math.abs(magnet) > 0) {
            //  magnet detected
            error = 3000
            turn_left()
            //  turn on left headlight (green)
            CutebotPro.colorLight(CutebotProRGBLight.RGBL, 0x00ff00)
            basic.pause(100)
            // magnet got further away
            if (Math.abs(magnet) > input.magneticForce(Dimension.X)) {
                error = 3000
                turn_right()
                //  turn on right headlight (green)
                CutebotPro.colorLight(CutebotProRGBLight.RGBR, 0x00ff00)
                basic.pause(500)
            }
            
        } else if (magnet == 0) {
            if (line == 1) {
                //  line is to the left
                turn_right()
                basic.pause(100)
                CutebotPro.colorLight(CutebotProRGBLight.RGBR, 0x00ff00)
            }
            
        }
        
    }
    
    //  too far left
    if (error > 0) {
        turn_right()
        line = 1
        //  line is to the right
        //  turn on left headlight (red)
        CutebotPro.colorLight(CutebotProRGBLight.RGBL, 0xff0000)
    }
    
    //  too far right
    if (error < 0) {
        turn_left()
        line = 0
        //  line is to the left
        // turn on right headlight (red)
        CutebotPro.colorLight(CutebotProRGBLight.RGBR, 0xff0000)
    }
    
    //  reset speed and headlights
    CutebotPro.turnOffAllHeadlights()
    lwheel = 10
    rwheel = 10
    CutebotPro.pwmCruiseControl(lwheel, rwheel)
    basic.pause(5)
})

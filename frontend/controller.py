from inputs import get_gamepad
import math
import threading

class XboxController(object):
    # Controls the max limit of triggers and joysticks
    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 8)

    # Inits everything to base position
    def __init__(self):

        self.LeftJoystickY = 0
        self.LeftJoystickX = 0
        self.RightJoystickY = 0
        self.RightJoystickX = 0
        self.LeftTrigger = 0
        self.RightTrigger = 0
        self.LeftBumper = 0
        self.RightBumper = 0
        self.A = 0
        self.X = 0
        self.Y = 0
        self.B = 0
        self.LeftThumb = 0
        self.RightThumb = 0
        self.Back = 0
        self.Start = 0
        self.LeftDPad = 0
        self.RightDPad = 0
        self.UpDPad = 0
        self.DownDPad = 0
        self.ControllerFlag = 1
        self.run = False
        self.lock = threading.Lock()

        # Runs seperately from other processes
        self._monitor_thread = threading.Thread(target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()

    # Return the buttons/triggers state
    def read(self): 
        left_x       = self.LeftJoystickX
        left_y       = self.LeftJoystickY
        left_trigg   = self.LeftTrigger
        left_bumper  = 1 if self.LeftBumper == 1 else -1
        right_x      = self.RightJoystickX
        right_y      = self.RightJoystickY
        right_trigg  = self.RightTrigger
        right_bumper = 1 if self.RightBumper == 1 else -1
        a            = self.A
        b            = self.B
        y            = self.Y
        x            = self.X        
        
        return [left_x, left_y, left_trigg, left_bumper, right_x, right_y, right_trigg, right_bumper, a, b, x, y]
    
    #Enable/Disable the Monitor Controller
    def changeControllerState(self):
        with self.lock:
            self.run = not self.run

    def _monitor_controller(self):
        with self.lock:
            while self.run:
                events = get_gamepad()
                for event in events:
                    if event.code == 'ABS_Y':
                        self.LeftJoystickY = event.state / XboxController.MAX_JOY_VAL # normalize between -128 and 127
                    elif event.code == 'ABS_X':
                        self.LeftJoystickX = event.state / XboxController.MAX_JOY_VAL # normalize between -128 and 127
                    elif event.code == 'ABS_RY':
                        self.RightJoystickY = event.state / XboxController.MAX_JOY_VAL # normalize between -128 and 127
                    elif event.code == 'ABS_RX':
                        self.RightJoystickX = event.state / XboxController.MAX_JOY_VAL # normalize between -128 and 127
                    elif event.code == 'ABS_Z':
                        self.LeftTrigger = event.state 
                    elif event.code == 'ABS_RZ':
                        self.RightTrigger = event.state 
                    elif event.code == 'BTN_TL':
                        self.LeftBumper = event.state
                    elif event.code == 'BTN_TR':
                        self.RightBumper = event.state
                    elif event.code == 'BTN_SOUTH':
                        self.A = event.state
                    elif event.code == 'BTN_NORTH':
                        self.Y = event.state 
                    elif event.code == 'BTN_WEST':
                        self.X = event.state 
                    elif event.code == 'BTN_EAST':
                        self.B = event.state
                    elif event.code == 'BTN_THUMBL':
                        self.LeftThumb = event.state
                    elif event.code == 'BTN_THUMBR':
                        self.RightThumb = event.state
                    elif event.code == 'BTN_SELECT':
                        self.Back = event.state
                    elif event.code == 'BTN_START':
                        self.Start = event.state
                    elif event.code == 'BTN_TRIGGER_HAPPY1':
                        self.LeftDPad = event.state
                    elif event.code == 'BTN_TRIGGER_HAPPY2':
                        self.RightDPad = event.state
                    elif event.code == 'BTN_TRIGGER_HAPPY3':
                        self.UpDPad = event.state
                    elif event.code == 'BTN_TRIGGER_HAPPY4':
                        self.DownDPad = event.state
    
    def calculate_payload(self, current_inputs):
            #print(current_inputs)
            shoulder_left_dxy   = str(current_inputs[0]     // 12 * -1)                  # Normalize to -11 to 10
            shoulder__left_dzy  = str(current_inputs[1]     // 12)                       # Normalize to -11 to 10
            elbow_left          = str((current_inputs[2]    // 25) * -current_inputs[3]) # Normalize to -10 to 10
            shoulder_right_dxy  = str(current_inputs[4]     // 12)                       # Normalize to -11 to 10
            shoulder_right_dzy  = str(current_inputs[5]     // 12)                       # Normalize to -11 to 10
            elbow_right         = str((current_inputs[6]    // 25) * -current_inputs[7]) # Normalize to -10 to 10
            
            payload = "contr," + shoulder_right_dxy + ',' + shoulder_right_dzy + ',' + elbow_right + ',' + shoulder_left_dxy + ',' + shoulder__left_dzy + ',' + elbow_left
            return payload

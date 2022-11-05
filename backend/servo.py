import time

# abstract for a joint
class Joint:
    # each joint contains two servos
    def __init__(self, left_address, right_address) -> None:
        self.left_servo_address = left_address
        self.right_servo_address = right_address
        self.left_servo = 180
        self.right_servo = 0
    
    # returns to the starting position
    def rest(self):
        if self.left_servo != -1:
            self.left_servo = 180
        self.right_servo = 0
    
    # moves the servos to the required angle
    def move(self, angle):
        try:
            self.left_servo = 180 - angle
            self.right_servo = angle
            return 1
        except:
            return 0
    
    # tests the servos functionality
    def test(self) -> int:
        try:
            for i in range(10):
                self.left_servo = 180
                self.right_servo = 0
                print("servo at 180")
                time.sleep(1)

                self.right_servo = 0
                self.left_servo = 180
                print("servo at 0")
                time.sleep(1)

            print("success")
            return 1

        except:
            return 0

# elbow class handles the movement of the elbow joint
class Elbow(Joint):
    def __init__(self) -> None:
        super().__init__(4, 6)
        self.elbow_angle = 0

    # moves the elbow to the desired angle
    def move_elbow(self, angle) -> int:
        try:
            if angle < 180:
                super().move(angle)
                self.elbow_angle = angle
                return 1
        except:
            return 0
    # return the internal angle of the elbow
    def read_elbow(self) -> int:
        return self.elbow_angle
    
    # returns the servo addresses on the board
    def read_elbow_servos(self):
        return self.left_servo_address, self.right_servo_address

# shoulder class handles the movement of the elbow joint
class Shoulder(Joint):
    def __init__(self) -> None:
        super().__init__(0, 15)
        self.shoulder_angle = 0

    # moves the shoulder to the desired angle
    def move_shoulder(self, angle) -> int:
        try:
            if angle < 180:
                super().move(angle)
                self.shoulder_angle = angle
                return 1
        except:
            return 0
    # returns the internal angle of the shoulder
    def read_shoulder(self):
        return self.shoulder_angle
    
    # returns the servo addresses on the board
    def read_shoulder_servos(self):
        return self.left_servo_address, self.right_servo_address

class Gripper(Joint):
    def __init__(self, right_address) -> None:
        super().__init__(-1, right_address)
        self.grippep_pos = 0 
    
    # moves the gripper to the desired position
    def move_gripper(self, angle) -> int:
        try:
            self.move()
            self.grippep_pos = angle
        except:
            print("failed to move the gripper")
    
    # returns the position of the gripper
    def read_gripper(self) -> int:
        return self.grippep_pos

    # returns the servo address on the board    
    def read_gripper_servo(self) -> int:
        return self.right_servo_address

    
# Arm class handles the movement of the entire arm
class Arm:
    def __init__(self) -> None:
        self.elbow = Elbow()
        self.shoulder = Shoulder()

    # moves the arm to the starting position
    def rest(self):
        self.elbow.rest()
        self.shoulder.rest()

    # moves the entire arm to the desired angles
    def move_arm(self, elbow_angle, shoulder_angle) -> int:

        try:
            self.elbow.move_elbow(elbow_angle)
        except:
            print("failed to move elbow")
            return 0

        try:
            self.shoulder.move_shoulder(shoulder_angle)
        except:
            print("failed to move shoulder")
            return 0

        return 1
        
    # moves only the eblow to the required angle
    def move_elbow(self, elbow_angle) -> int:
        try:
            return self.elbow.move_elbow(elbow_angle)
        
        except:
            return 0
    
    # moves only the shoulder to the required angle
    def move_shoulder(self, shoulder_angle) -> int:
        try:
            return self.shoulder.move_shoulder(shoulder_angle)
        except:
            return 0
    
    # tests the movement of the arm
    def test_arm(self) -> int:
        try:
            self.elbow.test()
            self.shoulder.test()
            return 1
        except:
            return 0

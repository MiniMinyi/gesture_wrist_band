import sys
sys.path.append("/Users/panxingyu/gesture_wrist_band/LeapSDK/lib")
import Leap, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import time
import ctypes
import os

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


def draw(frame, ax):
    xs = []
    ys = []
    zs = []
    hand_p = frame[1]
    xs.append(hand_p[0])
    ys.append(hand_p[1])
    zs.append(hand_p[2])
    ax.scatter(xs, ys, zs, c='r', marker='o')
    fingers_ps = frame[2]
    for finger_ps in fingers_ps:
        xs = []
        ys = []
        zs = []
        for finger_p in finger_ps:
            xs.append(finger_p[0])
            ys.append(finger_p[1])
            zs.append(finger_p[2])
        ax.scatter(xs, ys, zs, c='b', marker='o')

class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def on_init(self, controller):
        print ("Initialized")
        self.fig = plt.figure()
        self.ax = fig.add_subplot(111, projection='3d')
        plt.ion()
        self.fig.show()
        self.fig.canvas.draw()

    def on_connect(self, controller):
        print ("Connected")

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print ("Disconnected")

    def on_exit(self, controller):
        print ("Exited")

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        # file_path = "/Users/panxingyu/gesture_wrist_band/gesture_wrist_band/data_collection_system/leap_data/1551483917076"
        # with open(os.path.realpath(file_path), 'rb') as data_file:
        #     data = data_file.read()
        # leap_byte_array = Leap.byte_array(len(data))
        # address = leap_byte_array.cast().__long__()
        # ctypes.memmove(address, data, len(data))
        # frame.deserialize((leap_byte_array, len(data)))


        print ("Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
              frame.id, time.time()*1000, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures())))

        if len(frame.hands) < 1:
            return


        hand = frame.hands[0]
        frame_data = []
        frame_data.append(data_name)
        palm_position = hand.palm_position
        frame_data.append([palm_position[0], palm_position[1], palm_position[2]])

        palm_normal = hand.palm_normal
        hand_direction = hand.direction

        arm = hand.arm
        fingers_points_list = []

        # Get fingers
        for finger in hand.fingers:
            finger_points = []

            # Get bones
            bone = None
            for b in range(0, 4):
                bone = finger.bone(b)
                finger_points.append([bone.prev_joint[0], bone.prev_joint[1], bone.prev_joint[2], ])
            finger_points.append([bone.next_joint[0], bone.next_joint[1], bone.next_joint[2], ])
            fingers_points_list.append(finger_points)
        frame_data.append(fingers_points_list)

        self.ax.clear()
        draw(frame_data, ax)
        ax.set_xlim([-150, 200])
        ax.set_ylim([-150, 200])
        ax.set_zlim([-150, 200])
        self.fig.canvas.draw()


        serialized_tuple = frame.serialize
        serialized_data = serialized_tuple[0]
        serialized_length = serialized_tuple[1]
        data_address = serialized_data.cast().__long__()
        buffer = (ctypes.c_ubyte * serialized_length).from_address(data_address)
        with open("leap_data/%d" % (time.time()*1000), 'wb') as data_file:
            data_file.write(buffer)

        # # Get hands
        # for hand in frame.hands:
        #
        #     handType = "Left hand" if hand.is_left else "Right hand"
        #
        #     print ("  %s, id %d, position: %s" % (
        #         handType, hand.id, hand.palm_position))
        #
        #     # Get the hand's normal vector and direction
        #     normal = hand.palm_normal
        #     direction = hand.direction
        #
        #     # Calculate the hand's pitch, roll, and yaw angles
        #     print ("  pitch: %f degrees, roll: %f degrees, yaw: %f degrees" % (
        #         direction.pitch * Leap.RAD_TO_DEG,
        #         normal.roll * Leap.RAD_TO_DEG,
        #         direction.yaw * Leap.RAD_TO_DEG))
        #
        #     # Get arm bone
        #     arm = hand.arm
        #     print ("  Arm direction: %s, wrist position: %s, elbow position: %s" % (
        #         arm.direction,
        #         arm.wrist_position,
        #         arm.elbow_position))
        #
        #     # Get fingers
        #     for finger in hand.fingers:
        #
        #         print ("    %s finger, id: %d, length: %fmm, width: %fmm" % (
        #             self.finger_names[finger.type],
        #             finger.id,
        #             finger.length,
        #             finger.width))
        #
        #         # Get bones
        #         for b in range(0, 4):
        #             bone = finger.bone(b)
        #             print ("      Bone: %s, start: %s, end: %s, direction: %s" % (
        #                 self.bone_names[bone.type],
        #                 bone.prev_joint,
        #                 bone.next_joint,
        #                 bone.direction))

        # # Get tools
        # for tool in frame.tools:
        #
        #     print ("  Tool id: %d, position: %s, direction: %s" % (
        #         tool.id, tool.tip_position, tool.direction))
        #
        # # Get gestures
        # for gesture in frame.gestures():
        #     if gesture.type == Leap.Gesture.TYPE_CIRCLE:
        #         circle = CircleGesture(gesture)
        #
        #         # Determine clock direction using the angle between the pointable and the circle normal
        #         if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2:
        #             clockwiseness = "clockwise"
        #         else:
        #             clockwiseness = "counterclockwise"
        #
        #         # Calculate the angle swept since the last frame
        #         swept_angle = 0
        #         if circle.state != Leap.Gesture.STATE_START:
        #             previous_update = CircleGesture(controller.frame(1).gesture(circle.id))
        #             swept_angle =  (circle.progress - previous_update.progress) * 2 * Leap.PI
        #
        #         print ("  Circle id: %d, %s, progress: %f, radius: %f, angle: %f degrees, %s" % (
        #                 gesture.id, self.state_names[gesture.state],
        #                 circle.progress, circle.radius, swept_angle * Leap.RAD_TO_DEG, clockwiseness))
        #
        #     if gesture.type == Leap.Gesture.TYPE_SWIPE:
        #         swipe = SwipeGesture(gesture)
        #         print ("  Swipe id: %d, state: %s, position: %s, direction: %s, speed: %f" % (
        #                 gesture.id, self.state_names[gesture.state],
        #                 swipe.position, swipe.direction, swipe.speed))
        #
        #     if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
        #         keytap = KeyTapGesture(gesture)
        #         print ("  Key Tap id: %d, %s, position: %s, direction: %s" % (
        #                 gesture.id, self.state_names[gesture.state],
        #                 keytap.position, keytap.direction ))
        #
        #     if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
        #         screentap = ScreenTapGesture(gesture)
        #         print ("  Screen Tap id: %d, %s, position: %s, direction: %s" % (
        #                 gesture.id, self.state_names[gesture.state],
        #                 screentap.position, screentap.direction ))
        #
        # if not (frame.hands.is_empty and frame.gestures().is_empty):
        #     print ("")

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"

def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print ("Press Enter to quit...")
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import rospy
from rasa_ros.srv import Dialogue, DialogueResponse
from std_msgs.msg import String
from gtts import gTTS
import subprocess
import os

class TerminalInterface:
    '''Class implementing a terminal i/o interface. 

    Methods
    - get_text(self): return a string read from the terminal
    - set_text(self, text): prints the text on the terminal

    '''

    def get_text(self):
        return input("[IN]:  ") 

    def set_text(self,text):
        myVoice = gTTS(text=text,lang="en")
        myVoice.save("tmp.mp3")
        subprocess.call(['mpg321','tmp.mp3','--play-and-exit'])
        #os.remove("./tmp.mp3")

        print("[OUT]:",text)



def callback(data):
    pass

def main():
    rospy.init_node('writing')
    rospy.wait_for_service('dialogue_server')
    dialogue_service = rospy.ServiceProxy('dialogue_server', Dialogue)
    
    terminal = TerminalInterface()

    while not rospy.is_shutdown():
        message = rospy.wait_for_message("spoken_text",String)
        if message == 'exit': 
            break
        try:
            bot_answer = dialogue_service(message.data)
            terminal.set_text(bot_answer.answer)
        except rospy.ServiceException as e:
            print("Service call failed: %s"%e)

if __name__ == '__main__':
    try: 
        main()
    except rospy.ROSInterruptException:
        pass
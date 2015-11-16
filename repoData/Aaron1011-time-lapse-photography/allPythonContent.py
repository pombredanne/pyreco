__FILENAME__ = autorun
#!/usr/bin/env python
import time
import os
import subprocess
import getpass
import argparse
import sys

USER = getpass.getuser()
PACKAGES = ["python-opencv", "mencoder"]

def install_deps():
    subprocess.Popen(["sudo", "apt-get", "install"] + PACKAGES).wait()

try:
    import cv2
except:
    print "OpenCV, a computer vision library which pySnap requires to run, is not installed. Please visit http://opencv.org/ for installation instructions for your platform."
    print "If you are running a Debian-based Linux distribution, pySnap can automatically install OpenCV for you"
    if raw_input("Install OpenCV? [y/n]").lower() == 'y':
        install_deps()
    else:
        print "PySnap will now exit."
        quit()


from PhotoTaker import PhotoTaker

class ConfigFileError:
    pass



def getTime():
    while True:
        try:
            picturetime = raw_input("\nPlease enter the time you would like pySnap to take a picture at each day, in 12-hour format: ")
            time.strptime(picturetime, "%I:%M:%S %p")
            break
        except ValueError:
            print ("Please enter a time in the following format: HH:MM:SS AM/PM: ")
    return picturetime


def on_indie(args):
    return not args.indie and not os.path.exists(os.path.join(os.path.join(os.path.abspath(os.path.dirname(__file__)), '.git')))

def use_indie():
    TERM = os.environ.get("TERM")
    if os.uname()[1] == 'raspberrypi':
        TERM = 'lxterminal'
    subprocess.Popen([TERM, "-e", sys.executable, os.path.abspath(__file__), '-i']).wait()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--indie', action='store_true', help='Run in IndieCity mode')
    parser.add_argument('-cm', '--camera-module', action='store_true', help='Use Raspberry Pi camera module' )
    args = parser.parse_args()
    photo_taker = PhotoTaker(args.camera_module)

    if on_indie(args):
        use_indie()
        quit()

    try:
        print("Welcome to pySnap! pySnap makes it easy to do time lapse photography using your webcam.")
        print("\nThe following time and date has been detected from your computer: \n" + str(time.strftime('%X %x')))
        print("\nIf this is not correct, please exit the program now by pressing Control - C, and change your computer's time and date. Then, re-run this program.")

        print("\n\n\nPress Enter to advance to the next page.")
        raw_input()

        subprocess.call(['clear'])

        print("Press Control - C and any time to exit the program")

        photo_taker.takePicture('./', 'test')

        print("\n\n\nA test image has been taken using your webcam. Look in the location that autorun.py is located for a file named test.jpeg. If you do not see test.jpeg, or it does not contain an image, ensure that your webcam is connected and that it works properly with other programs.")

        print ("\n")
        print ("1) Every \033[31m'x'\033[39m seconds")
        print ("2) Every \033[31m'x'\033[39m minutes")
        print ("3) Every \033[31m'x'\033[39m hours")
        print ("4) Every \033[31m'x'\033[39m days")
        print ("5) Every \033[31m'x'\033[39m weeks")
        print ("6) Every day at \033[31m'x'\033[39m")
        print ("7) Every week at \033[31m'x'\033[39m")
        print('\n')
        print("Enter in the number that corresponds to the frequency that you would like to have pySnap take a picture. You will be prompted to enter \033[31m'x'\033[39m after you make your selection.")

        cont = False

        while not cont:
            try:
                selection = raw_input()
                selection = int(selection)
                if selection in range(1, 8):
                    cont = True
                else:
                    print("Please enter a number from 1 to 7")

            except ValueError:
                print("Please enter a valid selection")

        action = photo_taker.getChoices()[selection - 1]

        if selection == 6:
            photo_taker.start(action, getTime())

        if selection == 7:
            print("\n1)\033[31mSunday\033[39m")
            print("2)\033[31mMonday\033[39m")
            print("3)\033[31mTuesday\033[39m")
            print("4)\033[31mWednesday\033[39m")
            print("5)\033[31mThursday\033[39m")
            print("6)\033[31mFriday\033[39m")
            print("7)\033[31mSaturday\033[39m")
            print("Please enter the number that corresponds to the day that you would like pySnap to take a picture on: ")

            while True:
                try:
                    choice = int(raw_input())
                    if choice in range(1, 8):
                        break
                    else:
                        print("Please enter a number from 1 to 7: ")
                except ValueError:
                    print("Please enter a valid selection: ")
            phototime = getTime()
            photo_taker.start(action, phototime, choice)
        else:

            num = raw_input("Please enter the interval, in " + action.lower() + ", that you would like pySnap to take a picture: ")
            while True:
                try:
                    num = abs(int(num))
                    break
                except ValueError:
                    num = raw_input("Please enter a number: ")
            photo_taker.start(action, num)

    except KeyboardInterrupt:
            print("\nGoodbye!")

if __name__ == "__main__":
    main()

########NEW FILE########
__FILENAME__ = movie
#! /usr/bin/env python
import subprocess
import os
import string


def main():
    try:
        print("Welcome to pySnap's movie-making program! This program allows you to turn the time lapse photography you have taken into a movie\n\n")
        if not os.path.exists("Photos"):
            print("You don't seem to have any pictures yet. Run pySnap first, and then run this program again")
            quit()
        dirs = os.listdir("Photos")
        print("The following picture folders have been detected:")
        i = 1
        for path in dirs:
            print("%s: %s" % (i, path))
            i += 1
        choice = int(raw_input("Enter in the number corresponding the the folder you would like to use: "))
        while not choice - 1 in range(len(dirs)):
            choice = raw_input("Please enter a valid choice: ")

        fps = raw_input("Enter in the frame rate (FPS) for your movie. Hit enter for the default of 20: ")
        if not fps:
            fps = 20
        elif not fps in string.digits:
            fps = 20

        print("Creating movie:")
        subprocess.call(("mencoder mf://%s/*.jpeg -mf w=800:h=600:fps=%s:type=jpeg -ovc lavc -lavcopts vcodec=mpeg4:mbd=2:trell -oac copy -o output.avi" % ("Photos/" + dirs[choice - 1], fps)).split(" "), stdout=subprocess.PIPE)
    except KeyboardInterrupt:
        print("\b\b\nGoodbye!")
        quit()

if __name__ == "__main__":
    main()

########NEW FILE########
__FILENAME__ = PhotoTaker
import getpass
import os
import cv2
import time
import subprocess

class PhotoTaker:
    daysofweek = ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")
    choices = ("Seconds", "Minutes", "Hours", "Days", "Weeks", "Daily", "Weekly")

    def __init__(self, cm=False):
        self.USER = getpass.getuser()
        self.cm = cm
        if cm:
            self.WEBCAM = ['raspistill', '-o']
        else:
            for i in range(11):
                if os.path.lexists("/dev/video" + str(i)):
                    self.WEBCAM = cv2.VideoCapture(i)
                    break
            if not os.path.lexists("Photos"):
                os.mkdir("Photos")
            
    @classmethod
    def getChoices(klass):
        return klass.choices

    @classmethod
    def getDaysofWeek(klass):
        return klass.daysofweek

    def start(self, action, interval, day=None):
        if day:
            getattr(self, action.lower())(interval, day)
        elif action in self.getChoices():
            getattr(self, action.lower())(interval)

    def readConfig(self):
        if os.path.lexists("/home/" + self.USER + "/.pysnap.conf"):
            config = open("/home/" + self.USER + "/.pysnap.conf", "r")
            config = config.readlines()
            for line in config:
                if len(line) > 0:
                    if line[0] is not "#":
                        line2 = line.split("=")
                        if len(line2) == 2:
                            return line2[0], int(line2[1])

    def takePictureCV(self, directory, currtime=None):
        if not currtime:
            currtime = str(time.strftime("%X"))
        rval, img = self.WEBCAM.read()
        cv2.waitKey(20)
        if rval:
            cv2.imwrite(directory + currtime + '.jpeg', img)

    def takePicture(self, *args):
        if self.cm:
            self.takePictureCmd(*args)
        else:
            self.takePictureCV(*args)

    def takePictureCmd(self, directory, currtime=None):
        if not currtime:
            currtime = str(time.strftime("%X"))
        fname = directory + currtime + '.jpeg'
        subprocess.Popen(self.WEBCAM + [fname])

    def removeConfig(self):
        try:
            os.remove("/home" + self.USER + "/.pysnap.conf")
        except Exception:
            pass

    def seconds(self, num):
        try:
            if not os.path.lexists("Photos/Seconds"):
                os.mkdir("Photos/Seconds")
            while True:
                self.takePicture("./Photos/Seconds/")
                time.sleep(float(num))
        except KeyboardInterrupt:
            print("\nGoodbye!")
            quit()

    def minutes(self, num):
        try:
            if not os.path.lexists("Photos/Minutes"):
                os.mkdir("Photos/Minutes")
            num *= 60
            while True:
                self.takePicture("./Photos/Minutes/")
                time.sleep(float(num))

        except KeyboardInterrupt:
            print("\nGoodbye!")
            quit()

    def hours(self, num=None):
        if not os.path.lexists("Photos/Hours"):
            os.mkdir("Photos/Hours")
        num *= 60 ** 2
        while True:
            try:
                self.takePicture("./Photos/Hours/")
                time.sleep(num)
            except KeyboardInterrupt:
                print("\nGoodbye!")
                quit()

    def days(self, num=None):
        if not os.path.lexists("Photos/Weeks"):
            os.mkdir("Photos/Weeks")
        num *= 60 ** 2 * 24
        while True:
            try:
                self.takePicture("./Photos/Days/")
                time.sleep(num)
            except KeyboardInterrupt:
                print("\nGoodbye!")
                quit()

    def weeks(self, num=None):
        if not os.path.lexists("Photos/Weeks"):
            os.mkdir("Photos/Weeks")
        num *= 60 ** 2 * 24 * 7
        while True:
            try:
                self.takePicture("./Photos/Weeks/")
                time.sleep(num)
            except KeyboardInterrupt:
                print("\nGoodbye!")
                quit()

    def daily(self, picturetime):
        if not os.path.lexists("Photos/Daily"):
            os.mkdir("Photos/Daily")
        while True:
            try:
                currtime = time.strftime('%I:%M:%S %p')
                if currtime == picturetime:
                    self.takePicture("./Photos/Daily/", currtime=currtime)
                    time.sleep(5)
            except KeyboardInterrupt:
                print("\nGoodbye!")
                quit()

    def weekly(self, phototime, day):
        if not os.path.lexists("Photos/Weekly"):
            os.mkdir("Photos/Weekly")
        print self.daysofweek[day - 1]
        while True:
            try:
                currtime = time.strftime('%I:%M:%S %p')
                currday = time.strftime('%A')
                if currtime == phototime and currday == self.daysofweek[day - 1]:
                    self.takePicture("./Photos/Weekly/", currtime=currtime)
                    time.sleep(5)

            except KeyboardInterrupt:
                print("\nGoodbye!")
                quit()


########NEW FILE########
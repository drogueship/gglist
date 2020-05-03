import psutil, datetime, time
import win32api

stampsfile = "stamps.csv"
lengthsfile = "lengths.csv"
programslist = "programs.txt"

watched = {}
		
input_file = open(programslist, 'r')
for line in input_file:
	watched[line.replace("\n", "")] = {
		"filename": line.replace("\n", "") + ".exe",
		"open": False,
        "opentime": False,
        "closedtime": False
		}

def reporter(program, event, date):
    f = open(stampsfile,"a")
    print(program + "," + event + "," + date.strftime("%Y-%m-%d") + "," + date.strftime("%H:%M:%S"))
    f.write(program + "," + event + "," + date.strftime("%Y-%m-%d") + "," + date.strftime("%H:%M:%S") + "\n")
    f.close()

def timer(program, event, start, finish, duration):
    f = open(lengthsfile,"a")
    print(program + "," + event + "," + start  + "," +  finish  + "," + duration)
    f.write(program + "," + event + "," + start  + "," +  finish  + "," + duration + "\n")
    f.close()
        
def on_exit(sig, func=None):
    reporter("gglist","closed", str(datetime.datetime.now()) - started)
    time.sleep(1)
	
win32api.SetConsoleCtrlHandler(on_exit, True)

started = datetime.datetime.now()
reporter("gglist","opened",started)

while(True):
    plist = ""
    for proc in psutil.process_iter():
        plist = plist + proc.name() + ","
    for application in watched:
        if(plist.__contains__(watched[application]["filename"])):
            if(not watched[application]["open"]):
                watched[application]["open"] = True
                watched[application]["opentime"] = datetime.datetime.now()
                reporter(application,"opened",watched[application]["opentime"])
        else:
            if(watched[application]["open"]):
                watched[application]["open"] = False
                watched[application]["closedtime"] = datetime.datetime.now()
                reporter(application,"closed",watched[application]["closedtime"])
                timer(application,"openfor",str(watched[application]["opentime"]),str(watched[application]["closedtime"]),str(watched[application]["closedtime"] - watched[application]["opentime"]))
    time.sleep(5)
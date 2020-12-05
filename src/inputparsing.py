import getopt
import sys
import logging


# This function decides wether to print to stdout or stderr depending on if help was called.
def printhelp(helpNeeded):
    message = """Usage: chat [--help] [-v] [-h HOST] [-p PORT] [-n NAME] NETID\n\nArguments:\n NETID The NetID of the user.\n\nOptions:\n --help\n -v, --verbose\n --host HOSTNAME, -h HOSTNAME\n --port PORT, -p PORT\n --name NAME, -n NAME"""
    if helpNeeded:
        print(message, file=sys.stdout)
        sys.exit(0)
    else:
        print(message, file=sys.stderr)
        sys.exit(1)

    return 0


def checkPort(port):
    highestPortNumber = 65353
    lowestPortNumber = 1023
    if (port.isnumeric() == False):
        print("Port must be numeric\n", file=sys.stderr)
        printhelp(False)
    portInt = int(port)
    if(portInt > highestPortNumber or portInt <= lowestPortNumber):
        print("Port number must be below 65354 and above 1023\n", file=sys.stderr)
        printhelp(False)


def checkArguments(numArguments):
    if(numArguments < 1):
        print("NETID argument Required\n", file=sys.stderr)
        printhelp(False)

    if(numArguments > 1):
        print("Unknown Argument Provided", file=sys.stderr)
        printhelp(False)


def mqtt_check_inputs():
    verbose = False
    help = False
    host = "localhost"
    port = "1883"
    name = "TylerClient"
    netId = "NETID"

    argv = sys.argv[1:]
    try:
        opt, args = getopt.getopt(
            argv, "h:p:n:v", ["host=", "port=", "name=", "verbose", "help"])

    except getopt.GetoptError as e:
        print("Option requires an argument", file=sys.stderr)
        printhelp(False)

    for opt, arg in opt:
        if opt in ['--help']:
            printhelp(True)
        elif opt in ['-h', '--host']:
            host = arg
        elif opt in ['-p', '--port']:
            port = arg
        elif opt in ['-n', '--name']:
            name = arg
        elif opt in ['-v']:
            logging.basicConfig(level=logging.DEBUG)
            verbose = True

    checkPort(port)
    checkArguments(len(args))

    netId = argv[-1]

    logging.info('Host: ' + host)
    logging.info('Port: ' + port)
    logging.info('Name: ' + name)
    logging.info('NetID: ' + netId)

    configList = (host, port, name, netId)
    # print(configList)
    return [host, port, name, netId]

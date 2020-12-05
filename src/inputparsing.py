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


def check_inputs():
    verbose = False
    help = False
    host = "localhost"
    port = "1883"
    name = "TylerClient"
    netId = "NETID"

    argv = sys.argv[1:]
    # print(argv)
    try:
        opt, args = getopt.getopt(
            argv, "h:p:n:v", ["host=", "port=", "name=", "verbose", "help"])
        # print(opt)

    except getopt.GetoptError as e:
        print("Option requires an argument", file=sys.stderr)
        printhelp(False)

    # print(len(opt))
    # print((opt))
    # print(len(args))
    # print((args))
    # print(len(argv))
    # print((argv))

    for opt, arg in opt:
        if opt in ['--help']:
            printhelp(True)
        elif opt in ['-h', '--host']:
            host = arg
        elif opt in ['-p', '--port']:
            port = arg
        elif opt in ['-n']:
            name = arg
        elif opt in ['-v']:
            #logging.disable = False
            print("entered")
            logging.basicConfig(level=0)
            verbose = True

    # print(len(opt))
    # print((opt))
    # print(len(args))
    # print((args))
    # print(len(argv))
    # print((argv))
    checkPort(port)
    checkArguments(len(args))

    netId = argv[-1]

    logging.info('Host: ' + host)
    logging.info('Port: ' + port)
    logging.info('Name: ' + name)
    logging.info('NetID: ' + netId)

    print()

    return 0


def mqtt_client_parse_arguments():
    #logging.disable = True
    logging.basicConfig(level=70)
    check_inputs()
    return 0

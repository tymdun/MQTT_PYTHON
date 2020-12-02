import getopt
import sys
import logging


# This function decides wether to print to stdout or stderr depending on if help was called.
def printhelp(helpNeeded):
    message = """Usage: chat [--help] [-v] [-h HOST] [-p PORT] [-n NAME] NETID\n\nArguments:\n NETID The NetID of the user.\n\nOptions:\n --help\n -v, --verbose\n --host HOSTNAME, -h HOSTNAME\n --port PORT, -p PORT\n --name NAME, -n NAME"""
    if helpNeeded:
        print(message, file=sys.stdout)

    else:
        print(message, file=sys.stderr)

    return 0


def check_inputs():
    verbose = False
    help = False
    host = "localhost"
    port = "1883"
    name = "TylerClient"
    netId = "NETID"

    argv = sys.argv[1:]
    # print(argv)
    opt, args = getopt.getopt(
        argv, "h:p:n:v", ["host=", "port=", "name=", "verbose", "help"])
    # print(opt)

    for opt, arg in opt:
        if opt in ['--help']:
            printhelp(True)
        elif opt in ['-h', '--host']:
            host = arg
        elif opt in ['-p']:
            port = arg
        elif opt in ['-n']:
            name = arg
        elif opt in ['-v']:
            verbose = True

    print()

    return 0


def mqtt_client_parse_arguments():
    logging.StreamHandler(sys.stdout)
    check_inputs
    return 0


check_inputs()

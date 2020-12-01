import getopt
import sys
import logging


def check_inputs():
    verbose = False
    help = False
    host = "localhost"
    port = "1883"
    name = "TylerClient"
    netId = "NETID"

    argv = sys.argv[1:]
    # print(argv)
    opt, args = getopt.getopt(argv, "h:p:n:v")
    # print(opt)

    for opt, arg in opt:
        if opt in ['-h']:
            host = arg
        elif opt in ['-p']:
            port = arg
        elif opt in ['-n']:
            name = arg
        elif opt in ['-p']:
            verbose = True

    print()


def mqtt_client_parse_arguments():
    logging.StreamHandler(sys.stdout)
    check_inputs
    return 0


check_inputs()

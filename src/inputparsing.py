import getopt
import sys


def check_inputs():
    verbose = False
    help = False
    host = "localhost"
    port = "1883"
    name = "TylerClient"
    netId = "NETID"

    argv = sys.argv[1:]
    print(argv)


# def mqtt_client_parse_arguments():
#    check_inputs
#    return 0

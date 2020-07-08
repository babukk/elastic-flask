
import os
import sys
import getopt
import configparser

from app import create_app

if __name__ == '__main__':

    _config_name = None
    _port = None
    _usage_msg = "Usage: python " + sys.argv[0] + " -c | --config-name=config_name -p | --port=port_num"

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hc:", ["help", "config-name=", "port=", ])
    except:
        print("Неизвестная опция.\n" + _usage_msg)
        sys.exit(1)

    for oo, a in opts:
        if oo in ("-h", "--help"):
            print(_usage_msg)
            sys.exit( 0 )
        elif oo in ("-c", "--config-name"):
            _config_name = a
        elif oo in ("-c", "--port"):
            _port = a
        else:
            print("Неизвестная опция.\n" + _usage_msg)

    if _config_name is None:
        print("config-name не определён.\n")
        sys.exit(1)

    print("running config:", _config_name)

    app = create_app(_config_name)

    app.run(host="0.0.0.0", port=_port, )

import os
import json
import logging
import atexit
import justpy as jp

import gui as g
from gui import MazeGui

from server import GuiServicer
from server import logger
import maze_model as m


def main():
    configfile = os.environ['CONFIG'] if 'CONFIG' in os.environ else "config.json"
    logger.info("loading config from %s", configfile)
    config = json.load(open(configfile, 'rt'))
    grpcport = config['grpcport']

    R = m.Region(5)
    g.GUI = MazeGui(R)
    server = GuiServicer(grpcport, g.GUI)

    logger.info("Starting server")
    server.start()
    def exit_handler():
        print('Closing down...')
        server.server.stop(2).wait()
        print('Done.')

    atexit.register(exit_handler)
    logger.info("Starting justpy")
    jp.justpy(g.main_page)


if __name__ == "__main__":
    main()

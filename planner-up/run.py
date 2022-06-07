import os
import json
import logging

import aiddl_core.function.default as dfun
from aiddl_core.function.uri import EVAL 

from aiddl_core.container.container import Container
from aiddl_core.representation.sym import Sym
import aiddl_core.parser.parser as parser

from aiddl_core.tools.logger import Logger

from server import UnifiedPlanningServicer
from server import logger


def main():
    configfile = os.environ['CONFIG'] if 'CONFIG' in os.environ else "config.json"
    logger.info("loading config from %s", configfile)
    config = json.load(open(configfile, 'rt'))
    grpcport = config['grpcport']

    server = UnifiedPlanningServicer(grpcport)

    logger.info("starting simulation server on port %s" % grpcport)
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    main()


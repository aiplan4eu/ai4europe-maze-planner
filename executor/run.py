import os
import json
import logging

import aiddl_core.function.default as dfun
from aiddl_core.function.uri import EVAL 

from aiddl_core.container.container import Container
from aiddl_core.representation.sym import Sym
import aiddl_core.parser.parser as parser

from server import ExecutionServicer
from server import logger


def main():
    logger.info("loading AIDDL operators")
    DB = Container()
    freg = dfun.get_default_function_registry(DB)
    m = parser.parse("./aiddl/domain.aiddl", DB, freg, ".")
    f_eval = freg.get_function_or_panic(EVAL)

    operators = f_eval(DB.get_entry(Sym("operators"), module=m).get_value())

    configfile = os.environ['CONFIG'] if 'CONFIG' in os.environ else "config.json"
    logger.info("loading config from %s", configfile)
    config = json.load(open(configfile, 'rt'))
    grpcport = config['grpcport']

    server = ExecutionServicer(grpcport, operators)

    logger.info("starting executor server on port %s" % grpcport)
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    main()

    

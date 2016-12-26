#############################################
#KennyLogger.py
#############################################

import logging
import inspect
import os

class KennyLogger:

    logger = None

    # Since logging.getLogger returns a singleton (static) variable which we are encapsulating (not extending)
    # we only need to call "initialize" the first time the logger is to be used. After that the empty constructor
    # can be called to get a reference to the logger
    def __init__(self):
        pass
    
    def initialize(self, logDirName = "logs", critLogName = "crit.log", errLogName = "err.log",
                   warnLogName = "warn.log",  infoLogName = "info.log", debugLogName = "debug.log"):
        
        #Create / Locate the directory in which we will save logs
        if not os.path.exists(logDirName):
            os.makedirs(logDirName)
        
        KennyLogger.logger = logging.getLogger(__name__)
        KennyLogger.logger.setLevel(logging.DEBUG)
    
        critHandler = logging.FileHandler(logDirName + os.path.sep  + critLogName)
        critHandler.setLevel(logging.CRITICAL)
        critFormatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        critHandler.setFormatter(critFormatter)
    
        errHandler = logging.FileHandler(logDirName + os.path.sep  + errLogName)
        errHandler.setLevel(logging.ERROR)
        errFormatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        errHandler.setFormatter(errFormatter)
        
        warnHandler = logging.FileHandler(logDirName + os.path.sep  + warnLogName)
        warnHandler.setLevel(logging.WARN)
        warnFormatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        warnHandler.setFormatter(warnFormatter)
        
        infoHandler = logging.FileHandler(logDirName + os.path.sep  + infoLogName)
        infoHandler.setLevel(logging.INFO)
        infoFormatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        infoHandler.setFormatter(infoFormatter)
        
        debugHandler = logging.FileHandler(logDirName + os.path.sep  + debugLogName)
        debugHandler.setLevel(logging.DEBUG)
        debugFormatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        debugHandler.setFormatter(debugFormatter)
        
        KennyLogger.logger.addHandler(critHandler)
        KennyLogger.logger.addHandler(errHandler)
        KennyLogger.logger.addHandler(warnHandler)
        KennyLogger.logger.addHandler(infoHandler)
        KennyLogger.logger.addHandler(debugHandler)

    def testLogging(self):
        self.logCritical("Critical Test")
        self.logError("Error Test")
        self.logWarn("Warn Test")
        self.logInfo("Info Test")
        self.logDebug("Debug Test")
    
    def logCritical(self, critStr):
        KennyLogger.logger.critical(critStr + " " + str(inspect.stack()[1][1:3]))
    
    def logError(self, errStr):
        KennyLogger.logger.error(errStr + " " + str(inspect.stack()[1][1:3]))
        
    def logWarn(self, warnStr):
        KennyLogger.logger.warn(warnStr + " " + str(inspect.stack()[1][1:3]))
        
    def logInfo(self, infoStr):
        KennyLogger.logger.info(infoStr + " " + str(inspect.stack()[1][1:3]))
    
    def logDebug(self, debugStr):
        KennyLogger.logger.debug(debugStr + " " + str(inspect.stack()[1][1:3])) 

    
from dxCrashInfoConfig import dxCrashInfoConfig;

class cStackFrame(object):
  def __init__(oSelf, uNumber, uAddress, oModule, uModuleOffset, oFunction, uFunctionOffset):
    oSelf.uNumber = uNumber;
    oSelf.uAddress = uAddress;
    oSelf.oModule = oModule;
    oSelf.uModuleOffset = uModuleOffset;
    oSelf.oFunction = oFunction;
    oSelf.uFunctionOffset = uFunctionOffset;
    if oSelf.oFunction:
      if oSelf.uFunctionOffset > 0:
        oSelf.sAddress = "%s + 0x%X" % (oSelf.oFunction.sName, oSelf.uFunctionOffset);
      elif oSelf.uFunctionOffset:
        oSelf.sAddress = "%s - 0x%X" % (oSelf.oFunction.sName, abs(oSelf.uFunctionOffset));
      else:
        oSelf.sAddress = oSelf.oFunction.sName;
      oSelf.sSimplifiedAddress = oSelf.oFunction.sSimplifiedName;
      if uFunctionOffset in xrange(dxCrashInfoConfig.get("uMaxFunctionOffset", 0xFFF)):
        oSelf.sHashAddress = oSelf.oFunction.sName;
      else:
        # The offset is negative or too large: this is the closest symbol, but probably not the correct symbol.
        # This probably means there are not enough symbols to distinguish different functions. The only thing that
        # can be done to create a unique stack hash for this frame is add the offset. Unfortunately, this offset will
        # likely be different in a different build of the same application, so the stack hash will be different as well.
        oSelf.sHashAddress = oSelf.sAddress;
        oSelf.sAddress += " (this symbol may not be correct)";
    elif oSelf.oModule:
      oSelf.sAddress = "%s + 0x%X" % (oSelf.oModule.sBinaryName, oSelf.uModuleOffset);
      oSelf.sSimplifiedAddress = "%s!(unknown)" % oSelf.oModule.sBinaryName;
      oSelf.sHashAddress = oSelf.oModule.sBinaryName;
    else:
      oSelf.sAddress = "0x%X" % oSelf.uAddress;
      oSelf.sSimplifiedAddress = "(unknown)";
      oSelf.sHashAddress = "";

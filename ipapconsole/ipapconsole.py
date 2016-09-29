# ----------------------------------------------------------------------------
# An IPython profile that provides a CLI to access an Icepap system.
# Copyright (C) 2016  MaxIV Laboratory.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------------

"""An IPython profile that provides a CLI to access an Icepap system."""

import sys

import IPython
from IPython.core.magic import Magics, magics_class, line_magic
from IPython.terminal.ipapp import launch_new_instance

from pyIcePAP import *

from install import install, is_installed


__all__ = ["load_ipython_extension", "run", "load_config"]


@magics_class
class IcepapMagics(Magics):
    """Class defining our magics."""

    # NOTE: Do we really need to export __init__ as a magic?
    def __init__(self, shell):
        super(IcepapMagics, self).__init__(shell)
        self.ice = None
        self.ip = shell

    @line_magic
    def connect(self, parameter_s='', name="connect"):
        split = parameter_s.split()
        host = split[0]
        port = 5000
        if len(split) == 2:
            port = split[1]
        self.ice = EthIcePAP(host, port)
        self.ice.connect()
        # EXPOSE VARIABLE TO USER
        self.ip.user_ns['ice'] = self.ice

    @line_magic
    def disconnect(self, parameter_s='', name="disconnect"):
        self.ice.disconnect()
        self.ice = None

    @line_magic
    def w(self, parameter_s='', name="w"):
        if self.ice is None:
            return 'No connection to any icepap. Use \'connect\''
        command = parameter_s.upper()
        command = command.replace("\\", "")
        print "-> "+command
        try:
            self.ice.sendWriteCommand(command)
        except Exception, e:
            print "!<- Some exception occurred: ", e
            return e

    @line_magic
    def wro(self, parameter_s='', name="wro"):
        if self.ice is None:
            return 'No connection to any icepap. Use \'connect\''
        command = parameter_s.upper()
        command = command.replace("\\", "")
        print "-> "+command
        try:
            ans = self.ice.sendWriteReadCommand(command)
            return ans
        except Exception, e:
            print "!<- Some exception occurred: ", e
            return e

    @line_magic
    def wr(self, parameter_s='', name="wr"):
        print wro(self, parameter_s)

    @line_magic
    def sendfw(self, parameter_s='', name="sendfw"):
        if self.ice is None:
            return 'No connection to any icepap. Use \'connect\''
        try:
            filename = parameter_s

            print "Setting MODE PROG"
            cmd = "#MODE PROG"
            ans = self.ice.sendWriteReadCommand(cmd)
            print ans

            print "Transferring firmware"
            self.ice.sendFirmware(filename)

            time.sleep(5)
            print "Remember Icepap system is in MODE PROG"
            print self.ice.sendWriteReadCommand("?MODE")
        except Exception, e:
            print "!<- Some exception occurred: ", e
            return e

    @line_magic
    def prog(self, parameter_s='', name="prog"):
        if self.ice is None:
            return 'No connection to any icepap. Use \'connect\''
        try:
            print "Setting MODE PROG"
            cmd = "#MODE PROG"
            ans = self.ice.sendWriteReadCommand(cmd)
            print ans

            if parameter_s == '':
                parameter_s = 'ALL FORCE'
            cmd = "#PROG " + parameter_s.upper()
            print "\nProgramming with: " + cmd
            ans = self.ice.sendWriteReadCommand(cmd)
            print ans

            print
            shouldwait = True
            while shouldwait:
                p = self.ice.getProgressStatus()
                if p == 'DONE':
                    shouldwait = False
                elif isinstance(p, int):
                    print 'Programming [%d%%]           \r' % p,
                    sys.stdout.flush()
                    time.sleep(.2)

            print "\nSetting MODE OPER"
            cmd = "#MODE OPER"
            ans = self.ice.sendWriteReadCommand(cmd)
            print ans

            if parameter_s.upper().count('ALL') > 0:
                print '\nWait while rebooting... (25-30) secs'
                self.ice.sendWriteCommand('REBOOT')

                # WE SHOULD WAIT UNTIL CONNECTION IS LOST
                secs = 0
                for i in range(10):
                    time.sleep(1)
                    secs += 1
                    print 'Waiting until icepap system is rebooted. %d secs      \r' % secs ,
                    sys.stdout.flush()
                self.ice.disconnect()

                # WE SHOULD WAIT UNTIL ICEPAP IS RECONNECTED
                while not self.ice.connected:
                    time.sleep(1)
                    secs += 1
                    print 'Waiting until icepap system is rebooted. %d secs      \r' % secs ,
                    sys.stdout.flush()

            print '\nDone!'
            cmd = '0:?VER INFO'
            ans = self.ice.sendWriteReadCommand(cmd)
            print ans

        except Exception, e:
            print "!<- Some exception occurred: ", e
            return e

    @line_magic
    def listversions(self, parameter_s='', name="listversions"):
        if self.ice is None:
            return 'No connection to any icepap. Use \'connect\''
        versions_dict = {}
        ver_cmd = "VER"
        if parameter_s != '':
            ver_cmd = parameter_s.upper()
        sys_status = self.ice.sendWriteReadCommand("?SYSSTAT")
        sys_status = sys_status[sys_status.index("0x"):]
        sys_status = int(sys_status, 16)
        for rack in range(16):
            if (sys_status & (1 << rack)) > 0:
                version = self.ice.sendWriteReadCommand("%d:?%s" % (rack*10, ver_cmd))
                versions_dict[rack*10] = version
                rack_status = self.ice.sendWriteReadCommand("?SYSSTAT %d" % rack)
                rack_status = rack_status[rack_status.index("0x"):]
                rack_status = int(rack_status.split(" ")[1], 16)
                for driver in range(8):
                    if(rack_status & (1 << driver)) > 0:
                        addr = (rack*10+driver+1)
                        version = self.ice.sendWriteReadCommand("%d:?%s" % (addr, ver_cmd))
                        versions_dict[addr] = version
        return versions_dict

    @line_magic
    def getPositionRegisters(self, parameter_s='', name="getPositionRegisters"):
        info = {}
        if self.ice is None:
            return 'No connection to any icepap. Use \'connect\''
        for d in self.ice.getDriversAlive():
            info[d] = {}
            info[d]['indexer'] = self.ice.getIndexer(d)
            info[d]['possrc'] = self.ice.getCfgParameter(d, 'POSSRC')
            info[d]['tgtenc'] = self.ice.getCfgParameter(d, 'TGTENC')
            #for reg in ['AXIS','INDEXER','ENCIN','INPOS','ABSENC','MOTOR','TGTENC','SHFTENC']:
            for reg in ['AXIS', 'INDEXER', 'ENCIN', 'INPOS', 'ABSENC', 'TGTENC', 'SHFTENC']:
                info[d]['POS_'+reg] = self.ice.getPositionFromBoard(d, reg)
                info[d]['ENC_'+reg] = self.ice.getEncoder(d, reg)
        return info

    @line_magic
    def savePositionRegisters(self, parameter_s='', name="savePositionRegisters"):
        """Saves all the position registers in a file
           Syntax:
              savePositionRegisters <file_name>
           Parameters:
              file_name : file in which to store the info
        """
        if self.ice is None:
            return 'No connection to any icepap. Use \'connect\''
        try:
            filename = parameter_s
            f = file(filename, 'w')
            import pickle
            info = ip.magic('getPositionRegisters')
            pickle.dump(info, f)
            f.close()
        except IOError, e:
            msg = 'Unable to write to file \'%s\': %s' % (filename, str(e))
            return msg
        except Exception, e:
            print "!<- Some exception occurred: ", e
            return e
        return info

    @line_magic
    def openPositionRegisters(self, parameter_s='', name="openPositionRegisters"):
        """Recovers all the position registers from a file
           Syntax:
              openPositionRegisters <file_name>
           Parameters:
              file_name : file from which to recover the info
        """
        try:
            filename = parameter_s
            f = file(filename, 'r')
            import pickle
            info = ip.magic('getPositionRegisters')
            info = pickle.load(f)
            f.close()
        except IOError, e:
            msg = 'Unable to write to file \'%s\': %s' % (filename, str(e))
            return msg
        except Exception, e:
            print "!<- Some exception occurred: ", e
            return e
        return info

    @line_magic
    def comparePositionRegisters(self, parameter_s='', name="comparePositionRegisters"):
        """Compares all the position registers from a file with the current hardware values.

           Syntax:
              comparePositionRegisters <file_name>
           Parameters:
              file_name : file from which to recover the info to be compared with the current values
        """

        if self.ice is None:
            return 'No connection to any icepap. Use \'connect\''
        try:
            filename = parameter_s
            info_hw = ip.magic('getPositionRegisters')
            info_file = ip.magic('openPositionRegisters %s' % filename)
            if type(info_hw) != dict or type(info_file) != dict:
                return "Error getting either hardware or file positions"
            diff = set(info_hw.keys()) - set(info_file.keys())
            diffs = {}
            for axis in info_hw.keys():
                try:
                    info_file[axis]
                except KeyError:
                    print 'Info about axis %d is not present in the file. Continuing...' % axis
                    continue
                for param in info_hw[axis].keys():
                    hw_value, file_value = info_hw[axis][param], info_file[axis][param]
                    if hw_value != file_value:
                        msg = "Axis %d param %s: %s %s" % (axis, param, hw_value, file_value)
                        try:
                            diffs[axis]
                        except KeyError:
                            diffs[axis] = {}
                        diffs[axis][param] = [hw_value, file_value]
                        print msg
        except Exception, e:
            print "!<- Some exception occurred: ", e
            return e
        return diffs

    @line_magic
    def setPositionRegisters(self, parameter_s='', name="setPositionRegisters"):
        """Write into the hardware all the position registers from a file.

           Syntax:
              setPositionRegisters <file_name>
           Parameters:
              file_name : file from which to recover the info to be loaded into the harware
        """
        if self.ice is None:
            return 'No connection to any icepap. Use \'connect\''
        filename = parameter_s
        info = ip.magic('openPositionRegisters %s' % filename)
        if type(info) != dict:
            msg = 'Unable to load info from file \'%s\'' % filename
            return msg
        try:
            for axis in info.keys():
                indexer = info[axis]['indexer']
                if indexer != self.ice.getIndexer(axis):
                    print 'SHOULD RESTORE INDEXER'
                possrc = info[axis]['possrc']
                if possrc != self.ice.getCfgParameter(axis, 'POSSRC'):
                    print 'SHOULD RESTORE POSSRC'
                tgtenc = info[axis]['tgtenc']
                if tgtenc != self.ice.getCfgParameter(axis, 'TGTENC'):
                    print 'SHOULD RESTORE TGTENC'
                #for reg in ['AXIS','INDEXER','ENCIN','INPOS','ABSENC','MOTOR','TGTENC','SHFTENC']:
                for reg in ['AXIS', 'INDEXER', 'ENCIN', 'INPOS', 'ABSENC', 'TGTENC', 'SHFTENC']:
                    pos_reg = info[axis]['POS_'+reg]
                    if pos_reg != self.ice.getPositionFromBoard(axis, reg):
                        print 'Axis %d POS_%s: %s' % (axis, reg, pos_reg)
                        try:
                            self.ice.setPosition(axis, int(pos_reg), reg)
                        except Exception, e:
                            print 'ERROR WITH THIS REGISTER', e
                    enc_reg = info[axis]['ENC_'+reg]
                    if enc_reg != self.ice.getEncoder(axis, reg):
                        print 'Axis %d ENC_%s: %s' % (axis, reg, enc_reg)
                        try:
                            self.ice.setEncoder(axis, int(enc_reg), reg)
                        except Exception, e:
                            print 'ERROR WITH THIS REGISTER', e
        except Exception, e:
            print "!<- Some exception occurred: ", e
            return e

        return "Values correctly updated"
# NOTE: %wr can be called by: _ip.magic('wr ...') or ipmagic('wr ...')


def load_ipython_extension(ipython):
    #ip = IPython.get_ipython()
    magics = IcepapMagics(ipython)
    ipython.register_magics(magics)

def unload_ipython_extension(ipython):
    pass

def load_config(config):
    # ------------------------------------
    # InteractiveShellApp
    # ------------------------------------
    i_shell_app = config.InteractiveShellApp
    extensions = getattr(i_shell_app, 'extensions', [])
    extensions.append('ipapconsole')
    i_shell_app.extensions = extensions

def run():
    argv = sys.argv

    if not is_installed():
        install(verbose=False)
    try:
        for i, arg in enumerate(argv[:1]):
            if arg.startswith('--profile='):
                break
            else:
                argv.append("--profile=ipapconsole")
    except:
        pass

    launch_new_instance()

if __name__ == '__main__':
    run()

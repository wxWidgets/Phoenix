import platform
import shlex
import six
import subprocess
import sys
import yaml

# create a list of packages by generic name, assume that the user already has relevant python packages
GENERIC = ["gtk2", "gtk3", "gstreamer", "webkitgtk2", "webkitgtk3", "freeglut", "glu"] 

# package manager action lookup dictionary
PMD = \
{
    "arch"  : {"install" : "pacman -S", "query" : "pacman -Q"},
    "cent"  : {"install" : "yum install", "query" : "rpm -qi"},
    "debian": {"install" : "apt-get install", "query" : "dpkg -s"},
    "ubuntu": {"install" : "apt-get install", "query" : "dpkg -s"}
}

# Indirect OS, to avoid having a large volume of identical entries in the package
# manifest, this dictionary is used to refine necessary configurations
IDOS = \
{
    '' : '',     # python was not able to identify the dist name.
    "arch"  : "arch",
    "CentOS": "cent",
    "CentOS Linux" : "cent",
    
    # until necessity proves otherwise, convert rhel onto cent
    "Red Hat Enterprise Linux Workstation" : "cent",
    "Red Hat Enterprise Linux" : "cent",
    "debian" : "debian",
    "Ubuntu": "ubuntu",
    "elementary" : "debian",
}

class Checker:
    def __init__(self, gtk3):
        # gtk3 boolean value indicating if gtk3 is desired.

        # currently only supports linux:
        if platform.system() != "Linux":
            six.print_("Dependency checker invoked on non-linux OS!", file=sys.stderr)
            sys.exit()  # not worth erroring and halting any other modules.

        # load manifest
        with open("buildtools/lnxdep_manifest.yaml") as fd:
            self.__manifest = yaml.load(fd, Loader=yaml.Loader)

        # grab platform info:
        platinfo = platform.linux_distribution()
        
        # assign distribution:
        try:
            self.__dist = IDOS[platinfo[0]]
            self.__manifest[self.__dist]    # ensures that __dist is configured properly
        except KeyError:
            six.print_("Unknown distribution: %s" % platinfo[0], file=sys.stderr)
            sys.exit(1)

        if not self.__dist:
            six.print_("Unable to identify this distribution.", file = sys.stderr)
            sys.exit(2)

        # load version, on the by and large this will just become  "default"
        self.__ver = platinfo[1]
        try:
            self.__manifest[self.__dist][self.__ver]
        except KeyError:
            self.__ver = "default"

        # can now locate necessary manifest data
        self.__conf = self.__manifest[self.__dist][self.__ver]

        # load require package lists:
        self.__loadpkglists(gtk3)

    def CheckPkgs(self):
        """
        loads package lists and checks for presence, printing results back to user.
        """
        six.print_("Checking for missing packages that are required to build Phoenix.")
        six.print_("This can take some time on some distributions")

        missing = self.__findmissing()
        # report on missing packages
        if len(missing["required"]):
            six.print_("Missing required dependencies:")
            for pkg in missing["required"]:
                six.print_("\t%s" % pkg)
        else:
            six.print_("No missing required dependencies.")

        if len(missing["recommended"]):
            six.print_("Missing recommended packages:")
            for pkg in missing["recommended"]:
                six.print_("\t%s" % pkg)
        else:
            six.print_("No missing recommended packages")

        return (len(missing["required"]))

    def InstallPkgs(self):
        """
        attempts to use the package manager to install missing packages
        this is NOT recommended, as it will require root permission and
        is innately very risky
        """
        missing = self.__findmissing()
        if not (len(missing["required"]) or len(missing["recommended"])):
            six.print_("\nNo missing packages to install.\n")
            return 0    # nothing to do

        # prompt user for a final "are you really really sure?"?
        if  self.__whoami() == "root":
            if not self.__getyn("You are about to use your package manager as root.\n Are you sure this is okay? "):
                six.print_("Okay, exiting now.")
                return 1


        if len(missing["required"]):
            pkgs = " ".join(missing["required"])
            success = self.__runpkgcmd("install", pkgs, True)

            if not success:
                return 1

        if len(missing["recommended"]):
            # do these one by one, as they may not be desired.
            for pkg in missing["recommended"]:
                # check to see if it the package has already been installed
                # by another package
                if not self.__runpkgcmd("query", pkg):
                    six.print_("\n\nInstalling package: %s" % pkg)
                    self.__runpkgcmd("install", pkg, True)
        return 0

    def __findmissing(self):
        """
        returns a dict with fields "required" and "recommended" that are lists of missing packages
        """
        missing = {"required" : [], "recommended" : []}
        
        for item in self.__required:
            if not self.__runpkgcmd("query", item):
                missing["required"].append(item)

        for item in self.__recommended:
            if not self.__runpkgcmd("query", item):
                missing["recommended"].append(item)

        return missing

    def __runpkgcmd(self, command, pkg, showoutput = False):
        """
        runs the provided command type on provided package.
        looks up the command from PMD itself.
        """
        cmd = shlex.split("%s %s" % (PMD[self.__dist][command], pkg))

        out = subprocess.PIPE
        err = subprocess.STDOUT
        if showoutput:
            out = sys.stdout
            err = sys.stderr

        p = subprocess.Popen(cmd, stdout = out, stderr = err)
        while p.poll() is None:
            pass
        return not p.poll()

    def __whoami(self):
        """
        returns the user's name using whoami
        """
        output = subprocess.check_output(["whoami"])
        return output.decode("utf-8").split()[0]

    def __getyn(self, prompt):
        """
        presents prompt to the user and will loop [y/n] until a valid response is
        provided
        returns True for yes, False for no
        """
        response = six.moves.input(prompt + "[y/n] ")
        while response.lower() not in ["yes", "y", "no", "n"]:
            response = six.moves.input("[y/n] ")

        return response[0] == 'y'

    def __loadpkglists(self, gtk3):
        genericpkgs = GENERIC[:]
        if gtk3:
            genericpkgs.remove("gtk2")
            genericpkgs.remove("webkitgtk2")
        else:
            genericpkgs.remove("gtk3")
            genericpkgs.remove("webkitgtk3")

        genericpkgs.append("other")
        self.__required = []
        for item in genericpkgs:
            self.__required += self.__loadpkg(item)

        self.__recommended = self.__loadpkg("recommended")

    def __loadpkg(self, pkgname):
        """
        retrieves a field from the manifest and returns a lists of pkgs from that field
        """
        if self.__ver != "default":
            # check to see if field is available:
            try:
                if self.__manifest[self.__dist][self.__ver][pkgname]:
                    return self.__manifest[self.__dist][self.__ver][pkgname].split()
                else: return []
            except KeyError:
                pass    # fall down to the default lookup block.

        # using default lists.
        # if a key error occurs here it is because the manifest isn't complete
        if self.__manifest[self.__dist]["default"][pkgname]:
            return self.__manifest[self.__dist]["default"][pkgname].split()
        else: return []


if __name__ == "__main__":
    chkr = Checker()
    chkr.CheckPkgs()

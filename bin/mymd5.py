import sys
import glob
import hashlib

def main():
    for arg in sys.argv[1:]:
        for name in sorted(glob.glob(arg)):
            m = hashlib.md5()
            with open(name, 'rb') as fid:
                m.update(fid.read())
            print('%-45s %s' % (name, m.hexdigest()))


if __name__ == '__main__':
    main()

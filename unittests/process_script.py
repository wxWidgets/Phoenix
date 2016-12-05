import sys

if '--stdout' in sys.argv:
    print('process_test')
if '--echo' in sys.argv:
    text = raw_input()
    print("I read '%s'" % text)

sys.exit(0)

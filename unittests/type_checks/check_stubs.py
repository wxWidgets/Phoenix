#!/usr/bin/env python3
#---------------------------------------------------------------------------
# Name:        unittests/type_checks/check_stubs.py
# Purpose:     Sanity checks for the generated wx/*.pyi type stubs
#
# License:     wxWindows License
#---------------------------------------------------------------------------
"""
Checks for the generated wx/*.pyi type stubs. Run this after the etg step,
usually with "python build.py check_stubs". The type checkers used are in the
"typecheck" dependency group (pip install --group typecheck).

The checks are:

  1. Syntax: every stub file must parse cleanly, without even warnings.

  2. Baseline: mypy, pyright, ty and pyrefly are run over the stubs, and the
     number of errors of each kind in each stub file must match what is
     recorded in baseline.json. New errors fail the check, and so do fixed
     ones, so the improvement gets locked in. After an intended change, run
     this script with --update-baseline and commit the new baseline.json.

  3. Cases: the files in the test_cases folder use the stubs like user code
     would, with assert_type() calls and "# type: ignore[...]" comments on
     lines that are expected to fail. ty doesn't honor the error codes of
     the other checkers, so those lines also need a "# ty: ignore[...]".
     All the checkers must accept the cases without any errors, including
     unused ignores.

The settings for each type checker are in the config files in this folder.
To run one by hand, from the top of the source tree, use that file and pass
it the stubs and the cases, for example:

  mypy --config-file unittests/type_checks/mypy.ini wx/*.pyi unittests/type_checks/test_cases
  pyright --project unittests/type_checks/pyrightconfig.json wx/*.pyi unittests/type_checks/test_cases
  ty check --config-file unittests/type_checks/ty.toml wx/*.pyi unittests/type_checks/test_cases
  pyrefly check --config unittests/type_checks/pyrefly.toml wx/*.pyi unittests/type_checks/test_cases
"""

import argparse
import ast
import collections
import glob
import json
import os
import subprocess
import sys
import warnings

HERE = os.path.abspath(os.path.dirname(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
BASELINE = os.path.join(HERE, 'baseline.json')
CASES = os.path.join(HERE, 'test_cases')
# Overrides that don't match their base class are mostly part of the C++ API
# being wrapped, so they are not something that can be fixed in the stubs.
UNTRACKED = {
    'mypy': {'override'},
    'pyright': {'reportIncompatibleMethodOverride',
                'reportIncompatibleVariableOverride'},
    'ty': {'invalid-method-override'},
    'pyrefly': {'bad-override', 'bad-override-param-name',
                'bad-override-mutable-attribute'},
}

Error = collections.namedtuple('Error', 'tool file line code message')

#---------------------------------------------------------------------------

def stubFiles():
    files = sorted(glob.glob(os.path.join(ROOT, 'wx', '*.pyi')))
    if not files:
        sys.exit('No wx/*.pyi files found. Run "python build.py etg" first.')
    return files


def caseFiles():
    return sorted(glob.glob(os.path.join(CASES, '*.py')))


def checkSyntax(files):
    failures = []
    for filename in files:
        with open(filename, encoding='utf-8') as f:
            source = f.read()
        with warnings.catch_warnings():
            warnings.simplefilter('error')
            try:
                ast.parse(source, filename)
            except (SyntaxError, SyntaxWarning) as exc:
                failures.append(f'{os.path.relpath(filename, ROOT)}: {exc}')
    return failures


def displayName(filename):
    """Files are shown relative to ROOT, like wx/core.pyi"""
    return os.path.relpath(os.path.join(ROOT, filename), ROOT).replace(os.sep, '/')


def runTool(cmd):
    try:
        proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True,
                              encoding='utf-8')
    except FileNotFoundError:
        sys.exit(f'Unable to run {cmd[0]}')
    if 'No module named' in proc.stderr:
        sys.exit(f'{proc.stderr.strip()}\n'
                 'Install the type checkers with: pip install --group typecheck')
    return proc


def runMypy(files):
    cmd = [sys.executable, '-m', 'mypy', '--config-file', os.path.join(HERE, 'mypy.ini'),
           '--output', 'json', '--no-error-summary'] + files
    proc = runTool(cmd)
    errors = []
    for line in proc.stdout.splitlines():
        try:
            item = json.loads(line)
        except ValueError:
            continue
        if item['severity'] != 'error':
            continue
        errors.append(Error('mypy', displayName(item['file']), item['line'],
                            item['code'] or 'misc', item['message']))
    if proc.returncode not in (0, 1) or (proc.returncode and not errors):
        sys.exit(f'mypy failed to run:\n{proc.stdout}{proc.stderr}')
    return errors


def runPyright(files):
    cmd = [sys.executable, '-m', 'pyright', '--project', os.path.join(HERE, 'pyrightconfig.json'),
           '--outputjson'] + files
    proc = runTool(cmd)
    try:
        result = json.loads(proc.stdout)
    except ValueError:
        sys.exit(f'pyright failed to run:\n{proc.stdout}{proc.stderr}')
    errors = []
    for item in result['generalDiagnostics']:
        if item['severity'] != 'error':
            continue
        errors.append(Error('pyright', displayName(item['file']),
                            item['range']['start']['line'] + 1,
                            item.get('rule', 'error'), item['message']))
    return errors


def runTy(files):
    # The GitLab Code Quality format is ty's only JSON output
    cmd = [sys.executable, '-m', 'ty', 'check', '--config-file', os.path.join(HERE, 'ty.toml'),
           '--output-format', 'gitlab'] + files
    proc = runTool(cmd)
    try:
        result = json.loads(proc.stdout)
    except ValueError:
        sys.exit(f'ty failed to run:\n{proc.stdout}{proc.stderr}')
    errors = []
    for item in result:
        if item['severity'] not in ('major', 'critical', 'blocker'):
            continue
        code = item['check_name']
        message = item['description'].removeprefix(f'{code}: ')
        location = item['location']
        errors.append(Error('ty', displayName(location['path']),
                            location['positions']['begin']['line'], code, message))
    return errors


def runPyrefly(files):
    cmd = [sys.executable, '-m', 'pyrefly', 'check', '--config', os.path.join(HERE, 'pyrefly.toml'),
           '--output-format', 'json'] + files
    proc = runTool(cmd)
    try:
        result = json.loads(proc.stdout)
    except ValueError:
        sys.exit(f'pyrefly failed to run:\n{proc.stdout}{proc.stderr}')
    errors = []
    for item in result['errors']:
        if item['severity'] != 'error':
            continue
        errors.append(Error('pyrefly', displayName(item['path']),
                            item['line'], item['name'], item['concise_description']))
    return errors


def tally(errors):
    counts = {}
    for e in errors:
        if e.code in UNTRACKED[e.tool]:
            continue
        fileCounts = counts.setdefault(e.tool, {}).setdefault(e.file, {})
        fileCounts[e.code] = fileCounts.get(e.code, 0) + 1
    # sort everything, so the baseline file is stable and diffs are readable
    return {tool: {f: dict(sorted(codes.items())) for f, codes in sorted(files.items())}
            for tool, files in sorted(counts.items())}


def flatten(counts):
    return {(tool, f, code): n
            for tool, files in counts.items()
            for f, codes in files.items()
            for code, n in codes.items()}


def compareBaseline(errors, baseline):
    current = flatten(tally(errors))
    expected = flatten(baseline)
    worse = sorted(k for k in current if current[k] > expected.get(k, 0))
    better = sorted(k for k in expected if expected[k] > current.get(k, 0))

    for key in worse:
        tool, f, code = key
        print(f'\n{tool} {f} [{code}]: {current[key]} errors, '
              f'baseline is {expected.get(key, 0)}')
        matching = [e for e in errors if (e.tool, e.file, e.code) == key]
        for e in matching[:25]:
            print(f'    {e.file}:{e.line}: {e.message}')
        if len(matching) > 25:
            print(f'    ... and {len(matching) - 25} more')
    if better:
        print('\nFewer errors than the baseline expects:')
        for key in better:
            tool, f, code = key
            print(f'    {tool} {f} [{code}]: {current.get(key, 0)} errors, '
                  f'baseline is {expected[key]}')
    if worse or better:
        print('\nIf these changes are expected, run this script with '
              '--update-baseline and commit the result.')
    return not (worse or better)


def printErrors(errors):
    for e in errors:
        print(f'    {e.file}:{e.line}: [{e.tool}:{e.code}] {e.message}')

#---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--update-baseline', action='store_true',
                        help='write the current stub error counts to baseline.json')
    options = parser.parse_args()

    stubs = stubFiles()
    print('Checking stub syntax...')
    failures = checkSyntax(stubs + caseFiles())
    if failures:
        print('\n'.join(failures))
        return 1

    cases = caseFiles()
    errors = []
    for name, run in [('mypy', runMypy), ('pyright', runPyright),
                      ('ty', runTy), ('pyrefly', runPyrefly)]:
        print(f'Running {name}...')
        errors += run(stubs + cases)

    caseNames = {displayName(name) for name in cases}
    caseErrors = [e for e in errors if e.file in caseNames]
    stubErrors = [e for e in errors if e.file.startswith('wx/')]
    otherErrors = [e for e in errors if e not in caseErrors and e not in stubErrors]

    ok = True
    if otherErrors:
        print('\nUnexpected errors:')
        printErrors(otherErrors)
        ok = False

    if options.update_baseline:
        with open(BASELINE, 'w') as f:
            json.dump(tally(stubErrors), f, indent=2)
            f.write('\n')
        print(f'Updated {os.path.relpath(BASELINE, ROOT)}')
    else:
        with open(BASELINE) as f:
            baseline = json.load(f)
        ok = compareBaseline(stubErrors, baseline) and ok

    if caseErrors:
        print('\nErrors in the type checking test cases:')
        printErrors(caseErrors)
        ok = False

    total = sum(1 for e in stubErrors if e.code not in UNTRACKED[e.tool])
    print(f'\n{total} known errors in the stubs, {len(caseErrors)} errors in the cases.')
    print('OK' if ok else 'FAILED')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())

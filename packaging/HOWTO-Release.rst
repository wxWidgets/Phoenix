HOWTO Release wxPython Phoenix
==============================

:note: This is just a note to myself, no need to publish this in the main
       documentation or anything silly like that...

:note: The publish step needs the ``pypi`` environment in the GitHub repo
       settings to have required reviewers, so that it waits for approval.


0. Update the Phoenix/packaging/ANNOUNCE.txt document with details about this
   release. Check-in the file.

1. Make sure CHANGES.rst has a section for this release, with the version
   number as its heading. That section is used as the notes for the GitHub
   Release, and the release build will fail if it can't be found. Also check
   that the version numbers in buildtools/version.py are correct, (VER_FLAGS
   should be empty for a final release.)

2. Ensure that the branch to be built has been pushed to
   github.com/wxWidgets/Phoenix

3. On the Actions page, select the ci-build workflow, click "Run workflow",
   choose the branch, check "Make an official release", and run it.

4. Go do something else for a couple hours...

5. When everything is built the "Publish Python distribution to PyPI" job
   will wait for approval. Download the artifacts from the workflow run and
   do whatever smoke-testing should be done.

6. Approve the deployment with the "Review deployments" button on the
   workflow run. The workflow then uploads the wheels and source archive to
   PyPI, creates the wxPython-{version} tag on the commit that was built, and
   creates a GitHub Release with the release notes, source, docs, demo and pdb
   archives. Fetch the new tag with ``git fetch --tags``.

7. Run the build-linux-wheels workflow on the same branch to build the Linux
   wheels and add them to the GitHub Release.

8. Upload the wxPython-docs-*.tar.gz documentation file to docs.wxpython.org::

        scp wxPython-docs-*.tar.gz wxpython-docs:wxpython-docs/tmp

    TODO: Automate this!
    Go to the site and unpack the new docs into the document root.

9. Bump the version numbers in buildtools/version.py appropriately for the
   next anticipated release, so future snapshot builds will be recognized as
   pre-release development versions for the next official release, not the
   one just completed.

10. If making an announcement about this release, (I think it's okay not to
    for minor releases or smallish bug fixes,) send the text in
    packaging/ANNOUNCE.txt to the email addresses listed at the top of the
    file.

11. Add a news post to the wxPython site about the release.

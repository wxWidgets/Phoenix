HOWTO Release wxPython Phoenix
==============================

:note: This is just a note to myself, no need to publish this in the main
       documentation or anything silly like that...


0. Update the Phoenix/packaging/ANNOUNCE.txt document with details about this
   release. Check-in the file.

1. Ensure the buildbot master and slaves are running, and that
   ~/release-builds on Havok is empty

2. Ensure that the branch to be built has been pushed to github.com/RobinD42/Phoenix

3. Log in to buildbot master

4. On the "Builders" page check the dist-* and the bdist-* builders

5. Set a name/value pair to buildargs/--release

6. If a branch other than master should be used (for testing, etc.) then enter
   that branch name in the Branch field

7. Click the Force Build button

8. This can be done while the other builds are still running. Fetch the source
   tarball when it is finished and put it in Phoenix/dist. Run the following::

        python setup.py build_vagrant --release --upload

9. Go do something else for a couple hours...

10. ...it's still not done, come back later...



11. When the build is done and successful then the release version of the docs
    src and wheel files should be on Havok in ~/release-builds. Do whatever
    smoke-testing should be done.

12. Digitally sign the files with this command::

        cd ~/release-builds
        for f in *.whl *.tar.gz; do gpg --detach-sign -a $f; done

13. Upload to PyPI with::

        cd ~/release-builds
        twine upload wxPython-4*

    (Twine doesn't know what to do with the docs and other files so they need
    to be excluded by the wildcard.)

14. Upload the docs, demos and pdb archive files to wxpython.org/Phoenix/release-extras/::

        VERSION={current release version number}
        ssh wxpython-extras -c "mkdir -p wxpython-extras/$VERSION"
        scp wxPython-[^0-9]* wxpython-extras:wxpython-extras/$VERSION"

15. Tag the released revision in git, using a name like wxPython-4.0.0 (using
    the actual version number of course.) Push the tag upstream.

16. Bump the version numbers in buildtools/version.py appropriately for the
    next anticipated release, so future snapshot builds will be recognized as
    pre-release development versions for the next official release, not the
    one just completed.

17. If making an announcement about this release, (I think it's okay not to
    for minor releases or smallish bug fixes,) send the text in
    packaging/ANNOUNCE.txt to the email addresses listed at the top of the
    file.


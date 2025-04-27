HOWTO Release wxPython Phoenix
==============================

:note: This is just a note to myself, no need to publish this in the main
       documentation or anything silly like that...


0. Update the Phoenix/packaging/ANNOUNCE.txt document with details about this
   release. Check-in the file.

1. Ensure the buildbot master and slaves are running, and that
   ~/release-builds on Havok is empty

2. Ensure that the branch to be built has been pushed to
   github.com/wxWidgets/Phoenix

3. Log in to buildbot master

4. On the "Builders" page click the "trigger-all-dist" builder at the bottom of
   the list. Next, click the force-build button.

5. Add the name of the branch to the appropriate field, and click the "Do a
   release build?" checkbox.

6. Click the Start Build button

7. Building wheel files for selected linux distros can be done while the other
   builds are still running. Fetch the source tarball when it is finished and put
   it in Phoenix/dist. Run the following::

        python build.py build_docker --release --upload

8. Go do something else for a couple hours...

9. ...it's still not done, come back later. Or maybe tomorrow...


10. When the build is done and successful then the release version of the docs
    src and wheel files should be on Havok in ~/release-builds. Do whatever
    smoke-testing should be done.

11. Digitally sign the files with this command::

        cd ~/release-builds
        for f in wxPython-4*; do gpg --detach-sign -a $f; done
        for f in $(find linux -name "*.whl"); do echo $f; gpg --detach-sign -a $f; done

    NOTE: It looks like PyPI does not support gpg signatures any longer, so this step can be skipped/

12. Upload to PyPI with::

        cd ~/release-builds
        twine upload wxPython-4*

    (Twine doesn't know what to do with the docs and other files so they need
    to be excluded by the wildcard.)

13. Upload the wxPython-docs-*.tar.gz documentation file to docs.wxpython.org::

        scp wxPython-docs-*.tar.gz wxpython-docs:wxpython-docs/tmp

    TODO: Automate this!
    Go to the site and unpack the new docs into the document root.

14. Upload the docs, demos and pdb archive files to extras.wxpython.org/wxPython4/extras/::

        VERSION={current release version number}
        ssh wxpython-extras "mkdir -p wxpython-extras/htdocs/wxPython4/extras/$VERSION"
        scp wxPython-[^0-9]* wxpython-extras:wxpython-extras/htdocs/wxPython4/extras/$VERSION

15. Upload the Linux wheels::

        scp -r linux wxpython-extras:wxpython-extras/htdocs/wxPython4/extras/

16. Save a copy of everything to the NAS::

        mkdir /Volumes/STUFF/Development/wxPython/wxPython4/extras/$VERSION
        cp -v wxPython-[^0-9]* /Volumes/STUFF/Development/wxPython/wxPython4/extras/$VERSION
        cp -v wxPython-4* /Volumes/STUFF/Development/wxPython/wxPython4/pypi
        cp -rv linux /Volumes/STUFF/Development/wxPython/wxPython4/extras

17. Tag the released revision in git, using a name like wxPython-4.0.0 (using
    the actual version number of course.) Push the tag to all remotes.

18. Make a release at GitHub. Copy the generated source file into the release,
    and use a message that indicates the source archives created by GitHub are
    not complete.

19. Bump the version numbers in buildtools/version.py appropriately for the
    next anticipated release, so future snapshot builds will be recognized as
    pre-release development versions for the next official release, not the
    one just completed.

20. If making an announcement about this release, (I think it's okay not to
    for minor releases or smallish bug fixes,) send the text in
    packaging/ANNOUNCE.txt to the email addresses listed at the top of the
    file.

21. Add a news post to the wxPython site about the release.


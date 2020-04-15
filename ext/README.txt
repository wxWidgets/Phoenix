What is this?
=============

This folder holds the source for external projects used by Phoenix, (currently
wxWidgets and NanoSVG) as git submodules.  This allows Phoenix to use a specific
revision of the code in the other projects and not depend on the developer
fetching the correct version of the code on their own.

When you first check out the Phoenix source using git you will need to tell git
to also fetch the submodules, like this:

    cd Phoenix
    git submodule init
    git submodule update

To learn more about git submodules, please see the following:

    http://git-scm.com/book/en/v2/Git-Tools-Submodules
    http://blogs.atlassian.com/2013/03/git-submodules-workflows-tips/
    http://www.speirs.org/blog/2009/5/11/understanding-git-submodules.html


Notes to self
=============

 * To clone repositories with submodules:

       git clone <repourl>
       cd <repo>
       git submodule init
       git submodule update

 * To update an existing submodule from its upstream:

       git submodule update --remote <submodule>

   Or you can go into the submodule's folder and use normal git
   fetch/merge or pull operations to update the files in the
   submodule's workspace.  Commit the change in the main repo.

 * To set the submodule to track a specific branch from upstream:

       git config -f .gitmodules submodule.<name>.branch <branch name>

 * To use a different repo URL for a submodule than what others will
   see (in order to make and test local changes to the submodule that
   may be pushed to a different URL) then you can set that with a
   command like:

       git config submodule.MODULE_NAME.url PRIVATE_URL


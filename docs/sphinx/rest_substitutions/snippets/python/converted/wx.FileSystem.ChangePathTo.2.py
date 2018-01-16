
            f = fs.OpenFile("hello.htm") # opens file 'hello.htm'
            fs.ChangePathTo("subdir/folder", True)
            f = fs.OpenFile("hello.htm") # opens file 'subdir/folder/hello.htm' !!

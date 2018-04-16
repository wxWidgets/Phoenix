
        if filetype.GetOpenCommand(MailMessageParameters("foo.txt", "text/plain")):

            # the full command for opening the text documents is in 'command'
            # (it might be "notepad foo.txt" under Windows or "cat foo.txt" under Unix)
            HandleCommand()

        else:

            # we don't know how to handle such files...
            pass

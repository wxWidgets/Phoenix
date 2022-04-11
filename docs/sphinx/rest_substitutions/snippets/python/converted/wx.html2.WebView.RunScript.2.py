    
    success, result = webview.RunScript(
        "document.getElementById('some_id').innderHTML")

    if success:
        ... result contains the contents of the given element ...
    
    else:
        ... the element with self ID probably doesn't exist ...

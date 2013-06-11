# snippet list generation
import os

# list of snippet files
snip_list = [x[:-3] for x in os.listdir (os.path.dirname (__file__))
             if not x.startswith('_') and x.endswith('.py')]
snip_list.sort()

# function used by some or all snippets
def snippet_normalize (ctx, width, height):
    size = min(width, height)
    ctx.scale(size, size)
    ctx.set_line_width (0.04)

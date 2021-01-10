
# For Python the returned GridBlocks object has a __iter__ method so iterating
# in the Python way is possible.
for block in self.grid.GetSelectedBlocks():
    do_something(block)
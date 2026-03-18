
print("Using the contextlib module to create a context manager")
from contextlib import contextmanager

@contextmanager
def manage_resource():
    print("Stated ")
    yield   ##It is used to pause the execution of the function and return control to the caller. The code after the yield statement will be executed when the context block is exited.
    print("Ended")

with manage_resource():
    print("Inside the context")

print("\n Using Class to manually create a caontext manager")

class resource:
    def __enter__(self):
        print("Stated ")

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Ended")
    
with resource() as res:
    print("Inside the context")


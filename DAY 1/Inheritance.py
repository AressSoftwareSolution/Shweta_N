class A:
    def a(self):
        print("This is class A")

class B(A):
    def b(self):
        print("This is class B")

a=A()
b=B()

a.a()
b.b()
b.a()  ## Inheritance allows class B to access method a() from class A
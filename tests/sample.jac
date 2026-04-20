import from os { path }

"""Calculate something."""
def add(a: int, b: int) -> int {
    return a + b;
}

test "math_test" {
    """Test addition."""
    if add(1, 2) != 3 {
        print("Test failed!");
    }
}

"""A person archetype."""
obj Person {
    has name: str;
    has age: int;

    """Greet the world."""
    can greet(prefix: str = "Hello") -> str {
        res = f"{prefix}, my name is {self.name} and I am {self.age} years old.";
        print(res);
        return res;
    }
}

walker say_hello {
    can visit Person {
        here.greet();
    }
}

with entry {
    p = Person(name="Alice", age=30);
    p spawn say_hello;
}

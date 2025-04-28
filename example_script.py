from dataclasses import dataclass
from typing import Protocol


@dataclass(kw_only=True)
class dataclass_one_base:
    """A base class that exposes a dataclass interface."""

    a: int
    b: str

    def method(self) -> None:
        """A method that does something."""
        print(f"Method called with a={self.a}, b={self.b}")


@dataclass(kw_only=True)
class dataclass_one_protocol(Protocol):
    """A protocol that exposes a dataclass interface."""

    a: int
    b: str

    def method(self) -> None:
        """A method that does something."""
        print(f"Method called with a={self.a}, b={self.b}")


@dataclass(kw_only=True)
class dataclass_one(dataclass_one_base):
    """A class that implements the dataclass_one_protocol."""

    pass


@dataclass(kw_only=True)
class dataclass_one_prime(dataclass_one_protocol):
    """A class that implements the dataclass_one_protocol."""

    pass


# An inherited dataclass base types correctly.

instance_one = dataclass_one(a=1, b="example one")
instance_one.method()  # This works

# However, an inherited dataclass protocol does not type correctly although it works as expected.

instance_one = dataclass_one_prime(a=1, b="example one")
instance_one.method()  # This works

# Interestingly, if we create the types dynamically, they both type correctly.
dataclass_one_dynamic = type("dataclass_one_dynamic", (dataclass_one_base,), {})
instance_one_dynamic = dataclass_one_dynamic(a=1, b="example")

# Yet the dynamic protocol version does not actually work as expected, even if it types correctly.
dataclass_one_dynamic_prime = type(
    "dataclass_one_dynamic_prime", (dataclass_one_protocol,), {}
)

try:
    instance_one_dynamic_prime = dataclass_one_dynamic_prime(a=1, b="example")
    # There is no type error here. At runtime, however, it raises:
    # TypeError: dataclass_one_dynamic.__init__() takes exactly one argument (the instance to initialize)
except TypeError as e:
    print(f"Expected TypeError occurred: {e}")

# We can make the dynamic version work by using the dataclass decorator, as it most likely makes a new `__init__`
# method.
dataclass_one_dynamic_prime_prime = dataclass(
    type("dataclass_one_dynamic_prime_prime", (dataclass_one_protocol,), {})
)
instance_one_dynamic_prime_prime = dataclass_one_dynamic_prime_prime(a=1, b="example")


@dataclass(kw_only=True)
class dataclass_two_base:
    """Another base class that exposes a dataclass interface."""

    x: float
    y: str

    def another_method(self) -> None:
        """Another method that does something."""
        print(f"Another method called with x={self.x}, y={self.y}")


@dataclass(kw_only=True)
class dataclass_two_protocol(Protocol):
    """Another protocol that exposes a dataclass interface."""

    x: float
    y: str

    def another_method(self) -> None:
        """Another method that does something."""
        print(f"Another method called with x={self.x}, y={self.y}")


@dataclass(kw_only=True)
class combined_dataclass(dataclass_one_base, dataclass_two_base):
    """A class that combines two protocols."""

    pass


@dataclass(kw_only=True)
class combined_dataclass_prime(dataclass_one_protocol, dataclass_two_protocol):
    """A class that combines two protocols."""

    pass


# Multiple inherited base dataclasses types correctly.

instance_combined = combined_dataclass(a=2, b="example two", x=2.0, y="test")
instance_combined.method()  # This works
instance_combined.another_method()


# Yet, again the combined dataclass protocol does not type correctly

instance_combined_prime = combined_dataclass_prime(
    a=2, b="example two", x=2.0, y="test"
)
instance_combined_prime.method()  # This still works
instance_combined_prime.another_method()

"""
This module defines the Codelet class, which represents a small, self-contained unit of processing.
The Codelet class includes attributes for name, urgency, arguments, and birthdate, and provides
methods for initializing and representing the codelet as a string.

Classes:
    Codelet:
        A class that encapsulates a codelet, including its attributes and methods.
"""

from typing import List


class Codelet(object):
    """
    Represents a codelet, which is a small, self-contained unit of processing.

    Attributes:
        name (str): The name of the codelet.
        urgency (float): The urgency level of the codelet.
        arguments (List): A list of arguments for the codelet.
        birthdate (int): The birthdate of the codelet, representing the time it was created.
    """

    name: str
    urgency: float
    arguments: List
    birthdate: int

    def __init__(self, name: str, urgency: float, arguments: List, current_time: int):
        """Initializes a Codelet instance.

        Args:
            name (str): The name of the codelet.
            urgency (float): The urgency level of the codelet.
            arguments (List): A list of arguments for the codelet.
            current_time (int): The current time, used as the birthdate of the codelet.
        """
        self.name = name
        self.urgency = urgency
        self.arguments = arguments
        self.birthdate = current_time

    def __repr__(self) -> str:
        """Returns a string representation of the Codelet."""
        return f"<Codelet: {self.name}>"

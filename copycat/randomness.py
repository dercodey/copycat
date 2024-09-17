"""
This module provides utility functions and classes for randomness operations.

Functions:
    accumulate(iterable: Iterable) -> Iterator[int]:
        Generates a running total of values from the given iterable.

Classes:
    Randomness:
        A class that encapsulates random operations with an optional seed.
"""

import bisect
import math
import random

from typing import Iterable, Iterator, Optional, Sequence, Union, TypeVar

T = TypeVar("T")  # 'T' is a generic type


def accumulate(iterable: Iterable) -> Iterator[int]:
    """
    Generates a running total of values from the given iterable.

    Args:
        iterable (Iterable): An iterable of numeric values.

    Yields:
        int: The running total of the values.
    """
    total = 0
    for v in iterable:
        total += v
        yield total


class Randomness(object):
    """
    A class that encapsulates random operations with an optional seed.

    Methods:
        coinFlip(p=0.5):
            Returns True with probability p.

        choice(seq):
            Returns a random element from the non-empty sequence seq.
    """

    def __init__(self, seed: Optional[Union[int, float, str, bytes, bytearray]] = None):
        """
        Initializes the Randomness instance with an optional seed.

        Args:
            seed: An optional seed for the random number generator.
        """
        self.rng = random.Random(seed)

    def coin_flip(self, p: float = 0.5) -> bool:
        """
        Returns True with probability p.

        Args:
            p (float): The probability of returning True.

        Returns:
            bool: True with probability p, False otherwise.
        """
        return self.rng.random() < p

    def choice(self, seq: Sequence[T]) -> T:
        """
        Selects a random element from a non-empty sequence.

        Args:
            seq (Sequence): A non-empty sequence (e.g., list, tuple) from
                which to choose an element.

        Returns:
            Any: A randomly selected element from the provided sequence.
        """
        return self.rng.choice(seq)

    def weighted_choice(
        self, seq: Sequence[T], weights: Iterable[float]
    ) -> Optional[T]:
        """
        Selects an item from a sequence based on specified weights.

        Parameters:
            seq (Sequence): A sequence of items to choose from.
            weights (Iterable[float]): A corresponding iterable of weights for
                each item in the sequence.

        Returns:
            The selected item from the sequence based on the weighted probabilities.
            If the sequence is empty, returns None.

        Raises:
            ValueError: If the lengths of `seq` and `weights` do not match.
        """
        if not seq:
            # Many callers rely on this behavior.
            return None

        cum_weights = list(accumulate(weights))
        total = cum_weights[-1]
        return seq[bisect.bisect_left(cum_weights, self.rng.random() * total)]

    def weighted_greater_than(self, first: float, second: float) -> float:
        """
        Determines if a weighted random choice favors the first value over the second.

        This method takes two numerical values, `first` and `second`, and uses a
        coin flip mechanism to decide if the first value is greater than the second
        based on their relative weights. If both values are zero, the method returns
        False.

        Parameters:
            first (float): The weight of the first value.
            second (float): The weight of the second value.

        Returns:
            bool: True if the weighted random choice favors the first value,
                  False otherwise.
        """
        total = first + second
        if total == 0:
            return False
        return self.coin_flip(float(first) / total)

    def sqrt_blur(self, value: float):
        """This is exceedingly dumb, but it matches the Java code."""
        root = math.sqrt(value)
        if self.coin_flip():
            return value + root
        return value - root

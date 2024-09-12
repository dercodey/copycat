#!/usr/bin/env python3
"""
Main Copycat GUI program.
"""
import argparse
import logging

import matplotlib.pyplot as plt

from copycat import Copycat, Reporter

plt.style.use("dark_background")


class SimpleReporter(Reporter):
    """Reports results from a single run."""

    def report_answer(self, answer):
        print(
            f"Answered {answer['answer']:s} (time {answer['time']:d}, "
            f"final temperature {answer['temp']:.1f})"
        )


def main():
    """
    Main function for running the Copycat program with GUI.

    Args:
        --seed (int, optional): Provide a deterministic seed for the RNG.
    
    Returns:
        None
    """


    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        filename="./output/copycat.log",
        filemode="w",
    )

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Provide a deterministic seed for the RNG.",
    )
    options = parser.parse_args()

    copycat = Copycat(reporter=SimpleReporter(), rng_seed=options.seed, gui=True)
    copycat.runGUI()


if __name__ == "__main__":
    main()

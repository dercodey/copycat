#!/usr/bin/env python3
"""
Main Copycat program.

To run it, type at the terminal:

    > python main.py abc abd ppqqrr --interations 10

The script takes three to five arguments. The first two are a pair of strings
with some change, for example "abc" and "abd". The third is a string which the
script should try to change analogously. The fourth (which defaults to "1") is
a number of iterations. One can also specify a defined seed value for the
random number generator.

This instruction produces output such as:

    iiijjjlll: 670 (avg time 1108.5, avg temp 23.6)
    iiijjjd: 2 (avg time 1156.0, avg temp 35.0)
    iiijjjkkl: 315 (avg time 1194.4, avg temp 35.5)
    iiijjjkll: 8 (avg time 2096.8, avg temp 44.1)
    iiijjjkkd: 5 (avg time 837.2, avg temp 48.0)

    wyz: 5 (avg time 2275.2, avg temp 14.9)
    xyd: 982 (avg time 2794.4, avg temp 17.5)
    yyz: 7 (avg time 2731.9, avg temp 25.1)
    dyz: 2 (avg time 3320.0, avg temp 27.1)
    xyy: 2 (avg time 4084.5, avg temp 31.1)
    xyz: 2 (avg time 1873.5, avg temp 52.1)

The first number indicates how many times Copycat chose that string as its
answer; higher means "more obvious". The last number indicates the average
final temperature of the workspace; lower means "more elegant".
"""

import argparse
import logging

from copycat import Copycat, Reporter, plot_answers, save_answers


class SimpleReporter(Reporter):
    """Reports results from a single run."""

    def report_answer(self, answer):
        print(
            f"Answered {answer['answer']:s} (time {answer['time']:d}, "
            f"final temperature {answer['temp']:.1f})"
        )


def main():
    """Program's main entrance point.  Self-explanatory code."""
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
    parser.add_argument(
        "--iterations", type=int, default=1, help="Run the given case this many times."
    )
    parser.add_argument(
        "--plot", action="store_true", help="Plot a bar graph of answer distribution"
    )
    parser.add_argument(
        "--noshow", action="store_true", help="Don't display bar graph at end of run"
    )
    parser.add_argument("initial", type=str, help="A...")
    parser.add_argument("modified", type=str, help="...is to B...")
    parser.add_argument("target", type=str, help="...as C is to... what?")
    options = parser.parse_args()

    copycat = Copycat(reporter=SimpleReporter(), rng_seed=options.seed)
    answers = copycat.run(
        options.initial, options.modified, options.target, options.iterations
    )

    for answer, d in sorted(iter(answers.items()), key=lambda kv: kv[1]["avgtemp"]):
        print(
            f"{answer}: {d['count']} "
            f"(avg time {d['avgtime']:.1f}, "
            f"avg temp {d['avgtemp']:.1f})"
        )

    if options.plot:
        plot_answers(answers, show=not options.noshow)
    save_answers(answers, "output/answers.csv")


if __name__ == "__main__":
    main()

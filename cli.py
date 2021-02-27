#!/usr/local/bin/python3.8

import logging
import argparse
import base

__doc__ = """
An unauthorized command-line interface for uploading scores to conjuguemos.com. 
Use at your own risk (the website may change at any time and break things).
Despite the name, the author would really prefer if you didn't use his hard work to cheat, 
as learning a language is fun and rewarding!

Check out the github repo: https://github.com/2435191/conjuguemos-cheats.
"""

parser = argparse.ArgumentParser(description=__doc__)

parser.add_argument('username', help='Authentication username.')
parser.add_argument('password', help='Authentication password.')
parser.add_argument('id', type=int, help='The integer id of the exercise, usually found at the end of the url.')
parser.add_argument('numCorrect', type=int, help='The number of correct answers (the numerator for the score).')
parser.add_argument('numAttempts', type=int, help='The total number of questions (the denominator for the score).')
parser.add_argument('--time', type=int, default=300, help='Time taken in seconds, default 300.')
parser.add_argument('--mode', default='homework', help='Mode value. Tested only with the default `homework`, use otherwise at own risk.')

# https://stackoverflow.com/questions/18846024/get-list-of-named-loglevels
all_level_names = [logging.getLevelName(x) for x in range(1, 101) if not logging.getLevelName(x).startswith('Level')] \
    + ['OFF']
parser.add_argument('-l', '--loggerLevel', default='INFO', type=str.upper, choices=all_level_names, help="Will only display logging messages at or above this level (default INFO). See Python `logging` package.")

args = parser.parse_args()

if args.loggerLevel == 'OFF':
    logging.disable = True
else:
    logging.basicConfig(level=args.loggerLevel)

ci = base.ConjuguemosInterface()
ci.authenticate(args.username, args.password)
ci.save_score(args.id, args.numCorrect, args.numAttempts, args.time, args.mode)

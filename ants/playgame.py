#!/usr/bin/env python

import sys
from engine import BotThread, run_game, EngineThread

from ants import Ants

def main(argv):
    from optparse import OptionParser
    usage ="Usage: %prog [options] bot1 bot2"
    parser = OptionParser()
    parser.add_option("-o", "--output_file", dest="output_file",
                      help="File to dump game state to.")
    parser.add_option("-m", "--map_file", dest="map",
                      help="Name of the map file")
    parser.add_option("-p", "--players", dest="num_players",
                      default=4, type="int",
                      help="Number of players")

    parser.add_option("--serial", dest="serial",
                      action="store_true",
                      help="Run bots in serial, instead of parallel.")

    parser.add_option("--num_turns", dest="num_turns",
                      default=200, type="int",
                      help="Number of turns in the game")
    parser.add_option("-v", "--verbose", dest="verbose",
                      action="store_true",
                      help="Print out status as game goes.")

    parser.add_option("--timeout_ms", dest="timeout_ms",
                      default=1000, type="int",
                      help="Amount of time to give each bot, in milliseconds")
    parser.add_option("--load_timeout_ms", dest="load_timeout_ms",
                      default=1000, type="int",
                      help="Amount of time to give each bot for load, in milliseconds")

    (opts, args) = parser.parse_args(argv)
    if len(args) < opts.num_players:
        print "Need %s bots in the arguments, got %s %s." % (opts.num_players, len(args), len(args) < opts.num_players)
        return -1
    if opts.map is None:
        print "Please specify a map to start with"
        return -1
    #try:
    game = Ants(opts.map)
    result = "NO RESULT"
    bots = [EngineThread(BotThread(args[n])) for n in range(opts.num_players)]

    result = run_game(game, bots, opts.timeout_ms, opts.load_timeout_ms,
                      output_file=opts.output_file,
                      verbose=opts.verbose,serial=opts.serial)
    #except Exception as ex:
    #    print(ex)

    #finally:
    print()
    print(result)
    for bot in bots:
        bot.stop()
    return 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
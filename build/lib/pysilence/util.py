import time


def time_remaining(iteration, total_iterations, start) -> float:
    delta = time.time() - start
    if delta == 0:
        delta = 1
    iterations_per_sec = (iteration + 1) / delta
    return (total_iterations - (iteration + 1)) / iterations_per_sec


def printv(text, verbose, end='\n', sep=' ', file=None):
    if verbose:
        print(text, end=end, sep=sep, file=file)

import time

import numpy as np

from silence_detection import util, window
from silence_detection.util import printv


# returns a list of silence_detection ranges
# e.g. [[4, 17]] -> from second 4 to second 17 the audio is `silent`
def detect_silence_ranges(
    audio_data,
    sample_rate,
    min_silence_len,
    step_duration,
    silence_threshold,
    verbose=False,
    progress=False
) -> list:
    printv('[i] detecting silence_detection ranges ...', verbose)
    function_start = time.time()

    # converting audio to mono: calculating average of two audio canals
    printv('    - converting audio to mono', verbose)
    mono_audio = np.sum(audio_data, axis=1) / 2

    printv('    - finding maximum amplitude', verbose)
    max_amplitude = np.max(mono_audio)
    max_energy = get_energy([max_amplitude])

    printv('    - finding average energy', verbose)
    avg_energy = get_energy(mono_audio)

    printv(f'    [i] average energy is {avg_energy}', verbose)
    printv(f'    [i] maximum energy is {max_energy}', verbose)

    window_size = int(min_silence_len * sample_rate / 1000)  # size of window in frame count
    step_size = int(step_duration * sample_rate / 1000)  # step size in frame count
    printv(f'[i] window size: {window_size} frames', verbose)
    printv(f'[i] step size: {step_size} frames', verbose)

    printv(f'[i] finding silent ranges', verbose)
    window_generator = window.WindowEnergyIterator(mono_audio, window_size, step_size)

    window_energy = []
    while window_generator.has_next():
        if progress and window_generator.position % 1000:
            window_generator.progress()
        window_energy.append(window_generator.next_window_energy() / avg_energy)

    step_count = len(audio_data) // step_size

    has_silent_audio = _detect_samples_with_silent_audio(window_energy, step_count, silence_threshold)
    ranges = _generate_ranges_from_array(has_silent_audio, window_size, step_size, sample_rate)

    duration = round(time.time() - function_start, 1)
    printv(f'\n[i] took {duration} seconds', verbose)
    return ranges  # in seconds


# calculates the "perceived loudness" in a sample range
def get_energy(samples) -> float:
    return np.sum(np.power(samples, 2)) / float(len(samples))


# detects if frames have silent or loud audio
# returns a binary array
#   0 -> loud
#   1 -> silent
def _detect_samples_with_silent_audio(window_energy, step_count, silence_threshold, progress=False):
    start_loop = time.time()
    has_silent_audio = np.zeros(step_count)
    for i, energy in enumerate(window_energy):
        if i % 1000 == 0:
            remaining = util.time_remaining(i, step_count, start_loop)
            printv(f'\r    {i // 1000}k of {step_count // 1000}k  ETA: {round(remaining, 2)}s    ', progress, end='')
        if energy <= silence_threshold:
            has_silent_audio[i] = 1
    return has_silent_audio


# convert silent/loud array to list of `silence_detection-ranges`
# e.g. [4, 17] -> from second 4 to second 17 the audio is `silent`
def _generate_ranges_from_array(has_silent_audio, window_size, step_size, sample_rate) -> list:
    ranges = []
    last_silent = -1
    for i, silent in enumerate(has_silent_audio):
        if silent == 1:
            if last_silent < 0:  # transition from sound -> silent
                last_silent = i
        else:
            if last_silent >= 0:  # transition from silence_detection -> sound
                padding_size = sample_rate * 1  # one second padding so sound won't be cut off
                start = last_silent * step_size + padding_size
                stop = (i - 1) * step_size - padding_size
                if stop - start >= window_size:
                    ranges.append((start / sample_rate, stop / sample_rate))  # convert to seconds
                last_silent = -1
    return ranges

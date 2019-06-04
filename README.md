# PySilence

PySilence is an silence detection tool

### Install
```pip install pysilence```

### Usage
```python
from pysilence import silence

ranges = silence.detect_silence_ranges(
    audio_data=audio,
    sample_rate=rate,
    min_silence_len=2000,
    step_duration=200,
    silence_threshold=0.1,
    verbose=False,
    progress=False,
)
```
import subprocess
import tempfile

class Recorder:
    def __init__(self, sample_rate=16000):
        self.sample_rate = sample_rate

    def record(self, duration=10):
        temp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        temp_wav_path = temp_wav.name

        cmd = [
            "ffmpeg",
            "-y",
            "-f", "alsa",
            "-ac", "1",
            "-ar", str(self.sample_rate),
            "-i", "plughw:2,0",
            "-t", str(duration),
            temp_wav_path
        ]

        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return temp_wav_path

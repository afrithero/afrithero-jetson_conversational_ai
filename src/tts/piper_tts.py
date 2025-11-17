import subprocess
import os
import tempfile

class PiperTTS:
    def __init__(self, model_path="/app/models/piper/voice.onnx"):
        self.model_path = model_path

    def synthesize(self, text, output_wav=None):

        if output_wav is None:
            tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
            output_wav = tmp.name

        cmd = [
            "piper",
            "--model", self.model_path,
            "--output_file", output_wav
        ]

        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.communicate(text.encode("utf-8"))

        return output_wav


    def play(self, wav_path):
        """
        用 aplay 播放音訊（Jetson 支援 ALSA）。
        """
        subprocess.run(["aplay", wav_path])

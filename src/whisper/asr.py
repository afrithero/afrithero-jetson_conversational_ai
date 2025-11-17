from faster_whisper import WhisperModel

class WhisperASR:
    def __init__(self, model_size="small"):
        self.model = WhisperModel(
            model_size,
            device="cpu",
        )

    def transcribe(self, audio_path):
        result, _ = self.model.transcribe(audio_path)
        text = "".join([segment.text for segment in result])
        return text.strip()

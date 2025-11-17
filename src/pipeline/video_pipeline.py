from audio_input.recorder import Recorder
from whisper.asr import WhisperASR
from llm.llama_cpp_client import LlamaClient
from tts.piper_tts import PiperTTS



class VoicePipeline:
    def __init__(self, whisper_model="small", record_seconds=8):
        self.recorder = Recorder()
        self.asr = WhisperASR(whisper_model)
        self.llm = LlamaClient()
        self.record_seconds = record_seconds
        self.tts = PiperTTS()
        self.enable_tts = True


    def run_once(self):
        print("\nStart recording...")
        wav = self.recorder.record(duration=self.record_seconds)

        print("Transcribing...")
        text = self.asr.transcribe(wav)
        print("User:", text)

        if not text.strip():
            return "[Empty Speech Input]"

        print("LLM thinking...")
        reply = self.llm.chat(text)
        print("Assistant:", reply)

        if self.enable_tts:
            print("Speaking...")
            wav = self.tts.synthesize(reply)
            self.tts.play(wav)

        return reply

    def run_loop(self):
        print("=====================================")
        print("Voice AI - Multi-turn Chat")
        print("=====================================")

        while True:
            try:
                reply = self.run_once()
                print("\n----- Next Round -----\n")

            except KeyboardInterrupt:
                print("\nConversation ended.")
                break

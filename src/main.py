from pipeline.voice_pipeline import VoicePipeline

if __name__ == "__main__":
    pipeline = VoicePipeline(
        whisper_model="small",
        record_seconds=8
    )
    pipeline.run_loop()

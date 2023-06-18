from elevenlabs import generate, play

audio = generate(
  text="Hi! My name is Bella, nice to meet you!",
  voice="Bella",
  model="eleven_monolingual_v1"
)

play(audio)
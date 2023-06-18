import os

import websocket
import pyaudio
import threading

# Set up WebSocket connection
websocket_url = f"wss://api.hume.ai/v0/stream/models?apikey={os.getenv('HUME_API_KEY')}"  # Replace with the Hume API WebSocket URL
ws = websocket.WebSocketApp(websocket_url)

# Set up audio stream from microphone
audio_format = pyaudio.paInt16  # Adjust based on the desired audio format
sample_rate = 44100  # Adjust based on the desired sample rate
chunk_size = 1024  # Adjust based on the desired chunk size

audio_stream = pyaudio.PyAudio().open(format=audio_format,
                                      channels=1,
                                      rate=sample_rate,
                                      input=True,
                                      frames_per_buffer=chunk_size)

# Define WebSocket event handlers
def on_open(ws):
    print("WebSocket connection opened")

def on_close(ws, close_status_code, close_msg):
    print("WebSocket connection closed")

def on_error(ws, error):
    print("WebSocket error:", error)

# Stream microphone input
def stream_microphone_input():
    while ws.sock and ws.sock.connected:
        # Read audio chunk from microphone
        audio_data = audio_stream.read(chunk_size)

        # Send audio chunk over WebSocket
        ws.send(audio_data, opcode=websocket.ABNF.OPCODE_BINARY)

    print("Microphone stream ended")

# Assign event handlers
ws.on_open = on_open
ws.on_close = on_close
ws.on_error = on_error

# Create a separate thread for streaming microphone input
microphone_thread = threading.Thread(target=stream_microphone_input)

# Start the microphone thread
microphone_thread.start()

# Run the WebSocket event loop
ws.run_forever()

# Wait for the microphone thread to finish
microphone_thread.join()

# Close audio stream
audio_stream.stop_stream()
audio_stream.close()

# Close WebSocket connection
ws.close()

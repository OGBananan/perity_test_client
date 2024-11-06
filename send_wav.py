import websockets
import asyncio
import os

async def send_wav(wav_file_path, websocket):
    # Read the WAV file in binary mode
    with open(wav_file_path, 'rb') as wav_file:
        wav_data = wav_file.read()

    # Send the WAV file data over WebSocket (as binary data)
    print(f"Sending {wav_file_path}...")
    await websocket.send(wav_data)
    print(f"{wav_file_path} sent, waiting for FLAC response...")

    # Receive the FLAC data (binary stream) from the server
    flac_data = await websocket.recv()

    # Save the FLAC data to a file with the same name but .flac extension
    flac_file_path = wav_file_path.replace('.wav', '.flac')
    with open(flac_file_path, "wb") as flac_file:
        flac_file.write(flac_data)
    
    print(f"FLAC file saved as {flac_file_path}.")

async def process_folder(folder_path):
    # Get a list of all WAV files in the folder
    wav_files = [f for f in os.listdir(folder_path) if f.endswith('.wav')]

    # Connect to the WebSocket server
    uri = "ws://localhost:3000/ws"  # Replace with your actual WebSocket server URL
    async with websockets.connect(uri) as websocket:
        # For each WAV file in the folder, send it and receive the FLAC
        for wav_file in wav_files:
            wav_file_path = os.path.join(folder_path, wav_file)
            await send_wav(wav_file_path, websocket)

# Replace this with the path to your folder containing WAV files
folder_path = "./wav_files"

# Run the script to process all files in the folder
asyncio.get_event_loop().run_until_complete(process_folder(folder_path))

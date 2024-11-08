import moviepy.editor as mp
import os
import time

def extract_audio(video_path):
    try:
        print(f"[Audio Extraction] Attempting to extract audio from video: {video_path}")
        video = mp.VideoFileClip(video_path)

        if video.audio is None:
            print(f"[Audio Extraction] Error: No audio stream found in video {video_path}.")
            return None

        audio_filename = f"{os.path.splitext(os.path.basename(video_path))[0]}_audio.wav"
        audio_path = os.path.join("Audio_Files", audio_filename)
        
        # Ensure directory exists
        os.makedirs("Audio_Files", exist_ok=True)
        
        video.audio.write_audiofile(audio_path, codec='pcm_s16le')
        print(f"[Audio Extraction] Audio saved to: {audio_path}")

        # Adding a short delay to ensure file write completion
        time.sleep(1)

        return audio_path
    except Exception as e:
        print(f"[Audio Extraction] Error during audio extraction: {str(e)}")
        return None

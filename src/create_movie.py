from moviepy.editor import AudioFileClip, ImageClip
from moviepy.editor import concatenate_videoclips

def create_video_from_audio_image(audio_file, image_file, output_file):
    audio_clip = AudioFileClip(audio_file)
    image_clip = ImageClip(image_file).set_duration(audio_clip.duration)
    video_clip = image_clip.set_audio(audio_clip)
    video_clip.write_videofile(output_file, fps=24)

def create_video_files(config):
    folder_path = config.SeparatePapersFolder
    import os
    files = os.listdir(folder_path)
    audio_files = [f for f in files if f.endswith('.mp3')]
    
    for audio_file in audio_files:
        base_name = audio_file.split('.')[0]
        image_file = f"{base_name}_read-1.png"
        output_file = f"{folder_path}/{base_name}.mp4"
        
        if os.path.exists(f"{folder_path}/{image_file}"):
            create_video_from_audio_image(f"{folder_path}/{audio_file}", f"{folder_path}/{image_file}", output_file)
        else:
            print(f"Image file {image_file} not found.")

def combine_videos(config):
    output_file = config.OutputVideoFile
    folder_path = config.SeparatePapersFolder

    files = os.listdir(folder_path)
    video_files = [f for f in files if f.endswith('.mp4')]
    video_clips = [VideoFileClip(f"{folder_path}/{f}") for f in sorted(video_files)]
    
    final_clip = concatenate_videoclips(video_clips)
    final_clip.write_videofile(output_file)


import argparse
import youtube_dl
import os.path

parser = argparse.ArgumentParser(
    description="Converts a Youtube video to MP3",
    epilog="python youtube_mp3.py --video_url 'https://www.youtube.com/watch?v=CMNry4PE93Y'"
)
parser.add_argument("--video_url", required=True, help="URL of video to be converted")
parser.add_argument("--out_file",  help="Directory to save mp3")
args = parser.parse_args()

def run():
    video_info = youtube_dl.YoutubeDL().extract_info(
        url = args.video_url,download=False
    )
    if not args.out_file:
       filename = f"{video_info['title']}.mp3"
    else:
       if os.path.isdir(args.out_file):
           filename = os.path.join(args.out_file,f"{video_info['title']}.mp3")
       else:
           print(f"{args.out_file} does not exist, try another directory") 
    
    options={
        'format':'bestaudio/best',
        'keepvideo':False,
        'outtmpl':filename,
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video_info['webpage_url']])

    print(f"Download complete... {filename}")

if __name__=='__main__':
    run()

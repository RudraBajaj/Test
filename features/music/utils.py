"""Music player utilities - Optimized for Render free tier"""
import asyncio
import yt_dlp
import os


# yt-dlp options - Download to /tmp with optimization
YDL_OPTIONS = {
    'format': 'bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio',
    'outtmpl': '/tmp/%(id)s.%(ext)s',
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'ytsearch',
    'extract_flat': False,
    'cookiefile': 'cookies.txt',
    # Optimize for low CPU/RAM
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'm4a',
        'preferredquality': '128',  # Lower quality = less CPU/RAM
    }],
}


async def extract_info(search):
    """Extract video info from YouTube"""
    loop = asyncio.get_event_loop()
    
    try:
        await asyncio.sleep(1)  # Rate limiting
        
        ydl = yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True, 'cookiefile': 'cookies.txt'})
        
        if search.startswith('http'):
            data = await loop.run_in_executor(None, lambda: ydl.extract_info(search, download=False))
        else:
            data = await loop.run_in_executor(None, lambda: ydl.extract_info(f"ytsearch:{search}", download=False))
        
        if 'entries' in data:
            data = data['entries'][0]
        
        return data
        
    except Exception as e:
        print(f"Extraction error: {e}")
        return None


async def download_audio(data, video_id):
    """Download audio file to /tmp (optimized)"""
    loop = asyncio.get_event_loop()
    
    try:
        url = data.get('webpage_url') or data.get('url')
        
        ydl = yt_dlp.YoutubeDL(YDL_OPTIONS)
        
        # Download in background
        await loop.run_in_executor(None, lambda: ydl.download([url]))
        
        # Find the downloaded file
        possible_files = [
            f'/tmp/{video_id}.m4a',
            f'/tmp/{video_id}.webm',
            f'/tmp/{video_id}.opus',
        ]
        
        for file_path in possible_files:
            if os.path.exists(file_path):
                return file_path
        
        return None
        
    except Exception as e:
        print(f"Download error: {e}")
        return None

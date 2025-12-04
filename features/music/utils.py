"""Music player utilities - Streaming approach (most reliable for Render)"""
import asyncio
import yt_dlp


# yt-dlp options - Stream audio (no download)
# CRITICAL: Force direct HTTP streams, exclude HLS to prevent segment errors
YDL_OPTIONS = {
    'format': 'bestaudio[protocol^=http][protocol!*=m3u8]/bestaudio/best',
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'ytsearch',
    'extract_flat': False,
    'cookiefile': 'cookies.txt',
}

# FFmpeg options - Force start from 0:00
FFMPEG_OPTIONS = {
    'before_options': '-ss 0 -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn -b:a 128k'
}


async def extract_info(search):
    """Extract video info and stream URL from YouTube"""
    loop = asyncio.get_event_loop()
    
    try:
        await asyncio.sleep(1)  # Rate limiting
        
        ydl = yt_dlp.YoutubeDL(YDL_OPTIONS)
        
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

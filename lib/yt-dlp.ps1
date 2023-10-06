param(
  [Parameter(Mandatory=$true)]
  [string]$dir,
  [Parameter(Mandatory=$true)]
  [string]$videoid,
  [Parameter(Mandatory=$true)]
  [string]$outname
)
$SAMPLE_RATE=16000

# videoid is $videoid
function fetch_clip {

  param (
    [Parameter(Mandatory=$true)]
    [string]$videoid,
    [Parameter(Mandatory=$true)]
    [string]$outname,
    [Parameter(Mandatory=$true)]
    [string]$dir
  )

  echo "INFO fetch_clip() | Fetching clip $videoid..."
  if (Test-Path "$dir/${outname}.wav") {
    echo "Already have it."
    return
  }

  # Download the video and convert to WAV using ffmpeg.
  echo "INFO fetch_clip() | Downloading video..."

  try {
    yt-dlp "https://youtube.com/watch?v=$videoid" --extract-audio --audio-format wav --output "$dir/$outname.%(ext)s"
  } catch {
    echo "ERROR fetch_clip() | yt-dlp failed. Is it installed?"
    exit 1
  }

  if ($? -eq 0) {
    # If we don't pipe `yes`, ffmpeg seems to steal a
    # character from stdin. I have no idea why.
    echo "INFO fetch_clip() | Converting to WAV..."

    ffmpeg -loglevel quiet -i "$dir/$outname.wav" -ar $SAMPLE_RATE "$dir/${outname}_out.wav"
    mv "$dir/${outname}_out.wav" "$dir/$outname.wav"
    #gzip "$dir/$outname.wav"
  } else {
    # Give the user a chance to Ctrl+C.
    sleep 1
  }
}


echo "youtube_download.ps1"
echo "dir: $dir"
echo "videoid: $videoid"
echo "SAMPLE_RATE: $SAMPLE_RATE"

# Invoke the function.
fetch_clip -videoid $videoid -outname $outname -dir $dir


# Test
# .\yt-dlp.ps1 -videoid 9ySNCPfuBYI -dir . -outname fuck
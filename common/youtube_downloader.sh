#!/bin/bash

SAMPLE_RATE=16000

dir=$1

# fetch_clip(videoID, startTime, endTime)
fetch_clip() {
    echo "Fetching $1"
    outname = "$1"
    if [ -f "$dir/${outname}.wav" ]; then
        echo "Already have $1"
        return
    fi

    youtube-dl https://youtube.com/watch?v=$1 -o "$dir/$1.%(ext)s" -f bestaudio --extract-audio --audio-format wav --audio-quality 0 --no-playlist --quiet --output "$dir/$outname.%(ext)s"

    if [ $? -ne 0 ]; then
        echo "Error while downloading $1"
        return
    fi
    if [ $? -eq 0 ]; then
        echo "Successfully downloaded $1"
    fi
}
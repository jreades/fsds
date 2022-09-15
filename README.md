# About this Repository

The *Foundations of Spatial Data Science* (FSDS) module is part of CASA's [MSc degree offering](https://www.ucl.ac.uk/bartlett/casa/programmes) builds on a step-change in our ability to work with large spatial data sets. The design of the module is informed by the dearth of planners and geographers able to *think* computationally using programming, data analysis, and data manipulation skills. There is a severe skills shortage in this domain across all sectors: non-profit, government, corporate, and academic.

The module's objective is to enable students to access, understand, utilise, visualise and communicate data in a spatial context. FSDS is *not* about pushing buttons, but about using logic, programming, and analytical skills to tackle complex real-world problems in a creative, reproducible, and open manner.

## Using this Repository

In order to make use of these materials you will need to download and install the [Spatial Data Science computing environment](https://github.com/jreades/sds_env/).

## To Dos

- Move Debugging Manifesto in Lecture 2.5 and re-render video.
- [Shift away from .values](https://stackoverflow.com/questions/17241004/how-do-i-convert-a-pandas-series-or-index-to-a-numpy-array/54324513#54324513)
- Swap Weeks 8 (Visualising Data) and 9 (Dimensions in Data) + explain rationale to students.
- Shift focus of (new) Week 9 & 10 to review/discussing the final assessment. Content still available to view/practice but not required/delivered.
- Require more active use of GitHub/Git — a submission in which it’s easy to automate checks that they’ve created a repo and populated it with the completed notebooks?
- Refresh Code Camp and make it more self-test oriented. Use the self-test to set expectations about level of effort/preparation required (and whether or not taking the module will be useful).
- Standardise delivery of practical content by TAs: should have consistent approach across practicals.
- Point to cross-module content/recaps.
- Joint reading list?
- Look into automating movie generation. 
  - This code appears to be better-tuend but isn't compatible and generates larger files: [StackOverflow](https://stackoverflow.com/a/73073276/4041902)

```bash
ffmpeg -framerate 30 -i input.jpg -t 15 \
    -c:v libx265 -x265-params lossless=1 \
    -pix_fmt yuv420p -vf "scale=3840:2160,loop=-1:1" \
    -movflags faststart \
    out.mp4
```

- This code appears to generate something that is Mac-compatible from a PNG file:

```bash
ffmpeg -r 0.01 -loop 1 -i image.jpg -i audio.mp3 -c:v libx264 -tune stillimage -preset  ultrafast -ss 00:00:00 -t 00:00:27   -c:a aac  -b:a 96k -pix_fmt yuv420p  -shortest out.mp4 -y
```

### Working FFMPEG code

The below seems to generate an mp4 file with audio track that sounds like what I’d expect. The length seems to be automatically set to the length of the audio track (so `-t 75` is ignored, which is probably for the best). So what we get here is a merger of the two files into one video file. 

```bash
ffmpeg -r 30 -t 75 -loop 1 \
  -i 1.1-Getting_Oriented_19_1280x720.png -i test.m4a \
	-c:v libx264 -tune stillimage -preset ultrafast -pix_fmt yuv420p \
	-c:a aac -b:a 64k \
	out1.mp4
```

We need to repeat this for *every* slide in the deck and *then* merge the videos together into one long video. This approach does *not* re-encode the data so it’s probably faster and less prone to creating artefacts; however it also generates errors and seems to leave a blank spot at the start.

```bash
$ cat list.txt
file 'out2.mp4'
file 'out3.mp4'
ffmpeg -f concat -safe 0 -i list.txt -c copy out4.mp4
```

This looks promising: [Documentation for concat](https://ffmpeg.org/ffmpeg-filters.html#toc-Examples-153):

```bash
ffmpeg -i opening.mkv -i episode.mkv -i ending.mkv -filter_complex \
  '[0:0] [0:1] [0:2] [1:0] [1:1] [1:2] [2:0] [2:1] [2:2]
   concat=n=3:v=1:a=2 [v] [a1] [a2]' \
  -map '[v]' -map '[a1]' -map '[a2]' output.mkv
```

And:

```bash
movie=part1.mp4, scale=512:288 [v1] ; amovie=part1.mp4 [a1] ;
movie=part2.mp4, scale=512:288 [v2] ; amovie=part2.mp4 [a2] ;
[v1] [v2] concat [outv] ; [a1] [a2] concat=v=0:a=1 [outa]
```

*this* seems to work:

```bash
ffmpeg -i out2.mp4 -i out3.mp4 \
-filter_complex "[0:v] [0:a] [1:v] [1:a] concat=n=2:v=1:a=1 [vv] [aa]" \
-map "[vv]" -map "[aa]" out5.mp4
```

This is headed in the right direction… I think:

```bash 
ffmpeg -r 30 \
  -i 1.1-Getting_Oriented_19_1280x720.png -i 1.1-Getting_Oriented_18_1280x720.png \
  -i test.m4a -i test2.m4a \
  -filter_complex "[0:v] [1:v] [0:a] [1:a] concat=n=2:v=1:a=1 [vv] [aa]" \
  -map "[vv]" -map "[aa]" \
  -c:v libx264 -tune stillimage -preset ultrafast -pix_fmt yuv420p \
  -c:a aac -b:a 64k \
  out1.mp4
```

But the only examples I can find involve a [transparent overlay](https://stackoverflow.com/questions/35251122/using-ffmpeg-to-add-overlay-with-opacity). Also this [example](https://stackoverflow.com/questions/55455922/ffmpeg-using-video-filter-with-complex-filter).

### Adding Filters

I think I’ll need to this later: [see docs](https://trac.ffmpeg.org/wiki/FilteringGuide).

Ooooh, and a [cheatsheet](https://gist.github.com/martinruenz/537b6b2d3b1f818d500099dde0a38c5f)

#### New Approach

This approach will join short video segments created from PNG files with audio files not merged. However, there seems to be a keyframe or other issue in the later video – so you can’t scan forward, although it does seem to view properly if you don’t fast forward.

```bash
ffmpeg -r 30 -t 5 -loop 1 \
  -i 1.1-Getting_Oriented_19_1280x720.png \
  -c:v libx264 -tune stillimage -preset ultrafast -pix_fmt yuv420p \
  slide1.mp4
ffmpeg -r 30 -t 5 -loop 1 \
  -i 1.1-Getting_Oriented_20_1280x720.png \
  -c:v libx264 -tune stillimage -preset ultrafast -pix_fmt yuv420p \
  slide2.mp4
ffmpeg \
  -i slide1.mp4 -i slide2.mp4 \
  -i test.m4a -i test2.m4a \
  -filter_complex "[0:v:0][2:a:0][1:v:0][3:a:0] concat=n=2:v=1:a=1[outv][outa]" \
  -map "[outv]" -map "[outa]" \
  -c:v libx264 -tune stillimage -preset ultrafast -pix_fmt yuv420p \
  -c:a aac -b:a 64k \
  out6.mp4
```

#### Also Works

This works well to and may be the easiest: it’s a straightforward concatenation.

```bash
ffmpeg -r 30 -loop 1 \
  -i 1.1-Getting_Oriented_19_1280x720.png -i test.m4a \
	-c:v libx264 -tune stillimage -preset ultrafast -pix_fmt yuv420p \
	-c:a aac -b:a 64k \
	out1.mp4
ffmpeg -r 30 -loop 1 \
  -i 1.1-Getting_Oriented_20_1280x720.png -i test2.m4a \
	-c:v libx264 -tune stillimage -preset ultrafast -pix_fmt yuv420p \
	-c:a aac -b:a 64k \
	out2.mp4
$ cat list.txt
file 'out2.mp4'
file 'out3.mp4'
ffmpeg -f concat -safe 0 -i list.txt -c copy out4.mp4
```

How about:

```bash
ffmpeg \
  -r 30 -t 50 -loop 1 -i 1.1-Getting_Oriented_19_1280x720.png \
  -r 30 -t 30 -loop 1 -i 1.1-Getting_Oriented_20_1280x720.png \
  -i test.m4a -i test2.m4a \
  -filter_complex "[0:v:0][2:a:0][1:v:0][3:a:0] concat=n=2:v=1:a=1[outv][outa]" \
  -map "[outv]" -map "[outa]" \
  -c:v libx264 -tune stillimage -preset ultrafast -pix_fmt yuv420p \
  -c:a aac -b:a 64k \
  out7.mp4
```

**Something** happening here and in other ones where I try to merge PNG images into one video: at about 3:39 the preview goes black and if you fast forward or rewind in that area you get no picture.

*Failing *OK**! So this problem disappears if the `-t` option is longer than the audio file for input>0. But then you get video with no audio past the point where the recording stopped. So you kind of need to set the time to the length of the related audio file.

Consider also adding filters on audio and video channeles:

- atadenoise denoising [here](https://www.ffmpeg.org/ffmpeg-filters.html#toc-atadenoise)
- blend for blending one layer into another (watermarking?) [here](https://www.ffmpeg.org/ffmpeg-filters.html#toc-blend-1)
- chromakey for green-screening [here](https://www.ffmpeg.org/ffmpeg-filters.html#toc-blend-1) (also has useful thing for overlaying on a static black background)
- colorize is  [here](https://www.ffmpeg.org/ffmpeg-filters.html#toc-colorize)
- colortemperature is [here](https://www.ffmpeg.org/ffmpeg-filters.html#toc-colortemperature)
- coreimage to make use of Apple's CoreImage API [here](https://www.ffmpeg.org/ffmpeg-filters.html#toc-coreimage-1)
- crop is [here](https://www.ffmpeg.org/ffmpeg-filters.html#toc-crop)
- dblur for directional blur could be fun on intro/outro [here](https://www.ffmpeg.org/ffmpeg-filters.html#toc-dblur)
- decimate is [here](https://www.ffmpeg.org/ffmpeg-filters.html#toc-decimate-1)
- displace (probably a bad idea but...) is [here](https://www.ffmpeg.org/ffmpeg-filters.html#toc-displace)
- drawtext (for writing in date/year) is [here](https://www.ffmpeg.org/ffmpeg-filters.html#toc-drawtext-1) (requires libfreetype)
- fade (to fade-in/out the input video) is [here](https://www.ffmpeg.org/ffmpeg-filters.html#toc-fade)
- frames per second is [here](https://www.ffmpeg.org/ffmpeg-filters.html#toc-fps-1) not sure how it differs from [framerate](https://www.ffmpeg.org/ffmpeg-filters.html#toc-framerate)
- Gaussian blur is [here](https://www.ffmpeg.org/ffmpeg-filters.html#toc-gblur)
- Hue/saturation/intensity is [here](https://www.ffmpeg.org/ffmpeg-filters.html#toc-huesaturation)
- Colour adjustment is [here](https://www.ffmpeg.org/ffmpeg-filters.html#toc-Color-adjustment)
- Loop is [here](https://www.ffmpeg.org/ffmpeg-filters.html#toc-loop)
- Monochrome is [here](https://www.ffmpeg.org/ffmpeg-filters.html#toc-monochrome) and could be used with colourisation on live video, for instance
- Normalise is [here](https://www.ffmpeg.org/ffmpeg-filters.html#toc-normalize) for mapping input histogram on to output range
- Overlay is [here](https://www.ffmpeg.org/ffmpeg-filters.html#toc-overlay-1) and will be useful for adding an intro/outro
- Perspective correction i s[here](https://www.ffmpeg.org/ffmpeg-filters.html#toc-perspective)
- Scale is [here](https://www.ffmpeg.org/ffmpeg-filters.html#toc-scale-1) to rescale inputs.
- Trim is [here](https://www.ffmpeg.org/ffmpeg-filters.html#toc-trim)
- Variable blur i s[here](https://www.ffmpeg.org/ffmpeg-filters.html#toc-varblur) and could be useful for background blurring behind a talking head.
- Vibrance to increase/change saturation is [here](https://www.ffmpeg.org/ffmpeg-filters.html#toc-vibrance)
- Vstack as faster alternative to Overlay and Pad is [here](https://www.ffmpeg.org/ffmpeg-filters.html#toc-vstack)
- Xfade to perform cross-fading between input streams is [here](https://www.ffmpeg.org/ffmpeg-filters.html#toc-xfade)
- Zoom and pan is [here](https://www.ffmpeg.org/ffmpeg-filters.html#toc-zoompan)

Currently available video sources are [here](https://www.ffmpeg.org/ffmpeg-filters.html#toc-Video-Sources)



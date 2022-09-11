# About this Repository

The *Foundations of Spatial Data Science* (FSDS) module is part of CASA's [MSc degree offering](https://www.ucl.ac.uk/bartlett/casa/programmes) builds on a step-change in our ability to work with large spatial data sets. The design of the module is informed by the dearth of planners and geographers able to *think* computationally using programming, data analysis, and data manipulation skills. There is a severe skills shortage in this domain across all sectors: non-profit, government, corporate, and academic.

The module's objective is to enable students to access, understand, utilise, visualise and communicate data in a spatial context. FSDS is *not* about pushing buttons, but about using logic, programming, and analytical skills to tackle complex real-world problems in a creative, reproducible, and open manner.

## Using this Repository

In order to make use of these materials you will need to download and install the [Spatial Data Science computing environment](https://github.com/jreades/sds_env/).

## To Dos

- [Shift away from .values](https://stackoverflow.com/questions/17241004/how-do-i-convert-a-pandas-series-or-index-to-a-numpy-array/54324513#54324513)
- Swap Weeks 8 (Visualising Data) and 9 (Dimensions in Data) + explain rationale to students.
- Shift focus of (new) Week 9 & 10 to review/discussing the final assessment. Content still available to view/practice but not required/delivered.
- Require more active use of GitHub/Git — a submission in which it’s easy to automate checks that they’ve created a repo and populated it with the completed notebooks?
- Refresh Code Camp and make it more self-test oriented. Use the self-test to set expectations about level of effort/preparation required (and whether or not taking the module will be useful).
- Standardise delivery of practical content by TAs: should have consistent approach across practicals.
- Point to cross-module content/recaps.
- Joint reading list?
- Look into automating movie generation. This code appears to generate something that is Mac-compatible from a PNG file:

```bash
ffmpeg -r 0.01 -loop 1 -i image.jpg -i audio.mp3 -c:v libx264 -tune stillimage -preset  ultrafast -ss 00:00:00 -t 00:00:27   -c:a aac  -b:a 96k -pix_fmt yuv420p  -shortest out.mp4 -y
```


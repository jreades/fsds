# Overview 

We have 'flipped' the classroom for this module so we expect you to come to 'lecture' (***except*** in Week 1!) having already watched the assigned videos and completed the assigned readings. This means that there is a mix of 'asynchronous' (work that you do in your own time) and 'synchronous' (work that we do during scheduled hours) interaction. For those unable to attend a 'synchronous' activity because of Time Zone issues we *intend* to make a recording available afterwards, but we expect that a 2-hour recording of a group discussion and live coding session will be rather less educational and informative than actually *being there* so recordings should not be used as a substitute for attendance.

### Preparation

The nature and amount of preparation will vary from week to week, but may include:

- Readings from both academic and non-academic sources.
- Recorded lectures from CASA staff.
- Recorded videos from non-CASA staff.
- Short Moodle quizzes to test your completion of readings and videos.
- Contributions to a weekly '[Padlet](https://en-gb.padlet.com/)' that will be used to guide the 'synchronous' sessions.

### 'Lecture'

The 'lecture' in your timetable will be used for a mix of discussion and 'live coding' (eeek!) using the following framework:

- We will review questions and issues arising from the previous week's practical session.
- We will use ***your*** contributions to the week's Padlet to prioritise discussion around concepts and readings with which students are struggling or wish to engage further.
- We will have a 'live coding' session following an 'I do/We do' format: we will employ concepts covered in the week's preparation activities, as well as approaches that will be explored further in the practical, to look a real-world data set *together* using code.

So we're going to call these **workshops** instead! These will take place on Zoom and can be accessed using the 'activity' specified on the [Lectures and Workshop Material](https://moodle.ucl.ac.uk/course/view.php?id=11291&section=2) page.

### Practical

There are two timetabled practical sessions; we will inform you of your assigned session. These will also take place on Zoom and can *also* be accessed using the 'activity' specified on the [Lectures and Workshop Material](https://moodle.ucl.ac.uk/course/view.php?id=11291&section=2) page of Moodle.

# Week 1: Setting Up

This week is focussed on getting you set up for the rest of the course in terms of having the requisite software installed and accounts configured so that you can keep track of your work, write code, and track changes.

### Preparation

Although none of these activities are *compulsory* in advance of the first session, getting your computer set up to code *does* take time and most of these preparatory activites are fairly straightforward... with a few exceptions noted below. If you are able to get these tools installed in advance then you can focus on the taught content in the first two practicals rather than also wrestling with an installation. This will also give us more time to help you if you discover that you're one of the unlucky people for whom installation is a lot more work!

#### Computer Health Check-up

Please ensure that your computer is fully up-to-date with Operating System and application updates. Also, please make a note of the following three things:

- What Operating System and Version is your _main_ computer running? [Help for Windows](https://support.microsoft.com/en-gb/help/13443/windows-which-version-am-i-running). [Help for Mac](https://support.apple.com/en-gb/HT201260).
- How much RAM does your _main_ computer have? [Help for Windows](https://www.howtogeek.com/435644/how-to-see-how-much-ram-is-in-your-pc-and-its-speed/). [Help for Mac](https://www.macworld.co.uk/how-to/mac/much-ram-need-more-3793418/).
- How much free disk space does your _main_ computer have? [Help for Windows](https://www.lifewire.com/how-to-check-free-hard-drive-space-in-windows-2619187). [Help for Mac](https://www.macworld.com/article/2972775/how-to-check-a-mac-free-hard-drive-space.html).

This information will be very useful during the first few weeks when you are most likely to encounter problems with the programming environment. *Generally* speaking, the things to watch out for are:

1. Your operating system is Windows 10 Home, or something older than Windows 10 (*e.g.* Windows 8 or ealier), or MacOS older than 10.13 (High Sierra).
2. Your computer has less than 8GB of RAM.
3. Your computer has less than 15GB of free disk space remaining.

#### Installing Command Line Tools 

If you want to get a *little* bit ahead of things, then you should try to install one of:

- **Mac:** the Xcode Command Line Tools, which can be done [directly from the Terminal](https://osxdaily.com/2014/02/12/install-command-line-tools-mac-os-x/).
- **Windows:** WSL 2, for which you can follow [these instructions](https://www.digitalocean.com/community/tutorials/how-to-install-the-windows-subsystem-for-linux-2-on-microsoft-windows-10).

#### Installing the Programming Environment

If you want to get even *more* ahead of things, then the single most important thing you can do is to install the programming environment. This is the stage where you're most likely to encounter problems that will need our assistance, so knowing that you need our help here means that you ask for it much sooner!

We previously experimented with four approaches to installation: VirtualBox; Vagrant; Docker; and Anaconda Python directly. Each of these has pros and cons, but after careful consideration we have come to the conclusion that **Docker** is the most robust way to ensure a consistent experience in which all students end up with the same versions of each library, difficult-to-diagnose hardware/OS issues are minimised, and running/recovery is the most straightforward. Successful tests have been conducted using the **Docker**-based installation approach using macOS and Windows operating systems, however some small issues have arise which we plan to solve soon, so don't despair.

__To install the Programming Environment follow the instructions in Practical 1 [here](https://github.com/jreades/fsds/blob/master/practicals/Practical-01-Getting_Started.ipynb)__ (Task 5, but 4 and 3 are recommended)

##### Known issues

We've found issues running Docker using Windows that when closing down the Docker image the files you created are not saved and you cannot access any files on your current system. If this appears for you, a solution that could work is replacing:

`-v "$WORK_DIR":/home/jovyan/work`

with:

`--mount type=bind,source="$(pwd)",target=/home/jovyan/work`

and trying to load up the Docker image again. In doing so you should be able to see any existing files that you have, while also being able to save any files that you create in JupyterLab.

### Workshop

In this weeks workshop we will introduce modules aims, learning outcomes and expectations with a general introduction to the course

N.B. Workshop material and all other resources for this module are on the Moodle

### Practical

If you have already installed the programming environment then the practical can be downloaded from [GitHub](https://github.com/jreades/i2p/blob/master/practicals/Practical-01-Getting_Started.ipynb) (Click on `Raw` and then `Save File As...`) and viewed by saving it to your `Documents/CASA/...` folder, or you can just [view it online](https://github.com/jreades/i2p/blob/master/practicals/Practical-01-Getting_Started.ipynb) in your web browser.

# Week 2: Foundations (Part 1)

This week we will be (briefly) reviewing the basics of Python with a view to recapping the more complex aspects of simple data structures. And yes, that's a bit of an oxymoron! We will be contextualising this within the longer history of the study of geography through computation. If you are new to Python and have not yet completed Code Camp you are very strongly encouraged to complete Notebooks 1–7 as soon as possible.

### Preparation

#### Installing Command Line Tools 

If you didn't get to this during the practical then *please* do it before we get to Week 2's practical! You need to install one of:

- **Mac:** the Xcode Command Line Tools, which can be done [directly from the Terminal](https://osxdaily.com/2014/02/12/install-command-line-tools-mac-os-x/).
- **Windows:** WSL 2, for which you can follow [these instructions](https://www.digitalocean.com/community/tutorials/how-to-install-the-windows-subsystem-for-linux-2-on-microsoft-windows-10).

#### Installing the Programming Environment

See the [previous week's instructions](#installing-the-programming-environment). It is *vital* that you try to get this installed **before this week's practical**. If you encounter difficulties we will need time to help you, so the sooner you know that you need help, the faster we can help you.

#### Code Camp

If you have ***not* completed [Code Camp](https://kingsgeocomputation.org/teaching/code-camp/code-camp-python/)**, then we would strongly recommend that you tackle *Notebooks 3–5* as preparation for the week's class.

#### Optional: Git & GitHub

If you would like to have more time to focus on coding, please try to get your local computer and GitHub synchronising your *Introduction to Programming* (suggested name: `i2p`) project. Click on the still below to access the video on Streams.

[![Screen Grab from Git and GitHub](https://raw.githubusercontent.com/jreades/i2p/master/practicals/img/Git_GitHub.png)](https://web.microsoftstream.com/video/29a31977-ff9e-4b53-92d3-ee3bb2a769f6)

There are written instructions in the Week's practical.

#### Lectures

As we're working in a 'flipped' environment, you should watch these videos *before* class so that the 'live' workshop can focus on demonstration, discussion, and clarification. This week is very busy because we need to cover off the basics for those of you who were unable to engage with [Code Camp](https://kingsgeocomputation.org/teaching/code-camp/code-camp-python/), while recapping only the crucial bits for those of you who *were* able to do so: 

- Watch: [Python: the Basics](https://web.microsoftstream.com/video/dc5951ed-33fb-43a7-8e30-19ec2b41cb1f) ([Notes](https://github.com/jreades/i2p/blob/master/lectures/2.3-Python_the_Basics.md))
- Watch: [Lists](https://web.microsoftstream.com/video/21ef45cf-c432-4882-be54-e9bdbdaf7a3b) ([Notes](https://github.com/jreades/i2p/blob/master/lectures/2.4-Lists.md))
- Watch: [Iteration](https://web.microsoftstream.com/video/ecbf2b2b-6d11-4df0-a28b-caed2badbea1) ([Notes](https://github.com/jreades/i2p/blob/master/lectures/2.5-Iteration.md))
- Watch: [The Command Line](https://web.microsoftstream.com/video/5cd2a59c-ab53-4e75-a607-dd5de5e61681) ([Notes](https://github.com/jreades/i2p/blob/master/lectures/2.6-The_Command_Line.md))
- Watch: [Getting Stuck Into Git](https://web.microsoftstream.com/video/aa0f7893-4fb5-4af1-ad44-af8e352f4d52) ([Notes](https://github.com/jreades/i2p/blob/master/lectures/2.7-Git.md))

#### Readings

- [@Burton:1963] (Expand title)[DOI](https://doi.org/10.1111/j.1541-0064.1963.tb00796.x)
- [@ArribasBel:2018] [DOI](https://doi.org/10.1111/gec3.12403)

#### Contribution

- Padlet: [Collaborative Agenda]

#### Quiz!

- Complete the [short Moodle quiz](https://moodle.ucl.ac.uk/mod/quiz/view.php?id=2388403) associated with this week's activities.

### Workshop

- Review of **Collaborative Agenda** 

- Discussion of **Readings** 

- **Live Coding**

### Practical

This week's practical requires you to have **completed installation of the programming environment**. The practical can be downloaded from [GitHub](https://github.com/jreades/i2p/raw/master/practicals/Practical-02-Foundations_1.ipynb).

# Week 3: Foundations (Part 2)

### Preparation

#### Code Camp

*All* students should complete/revisit [Code Camp](https://mybinder.org/v2/gh/kingsgeocomp/code-camp-env/notebook-v1.0?urlpath=git-pull%3Frepo%3Dhttps%253A%252F%252Fgithub.com%252Fkingsgeocomp%252Fcode-camp%26urlpath%3Dtree%252Fcode-camp%252F%26branch%3Dmaster) Notebooks 8–11.

**Note:** there is an issue with the GeoJSON tasks in Notebooks 8 and 9. We can discuss in the Workshop.

#### Lectures

This week we start to move beyond [Code Camp](https://kingsgeocomputation.org/teaching/code-camp/code-camp-python/). So although you should recognise many of the _parts_ that we discuss,  you'll see that we start to put them together in a new way:

- Watch: [Dictionaries](https://web.microsoftstream.com/video/041f9734-9368-429c-8f91-2208f9c2ba07) ([Notes](https://github.com/jreades/i2p/blob/master/lectures/3.1-Dictionaries.md))
- Watch: [LOLs](https://web.microsoftstream.com/video/129b862b-cb1b-41ab-a6ad-d526eff3fd20) ([Notes](https://github.com/jreades/i2p/blob/master/lectures/3.2-LOLs.md))
- Watch: [DOLs to Data](https://web.microsoftstream.com/video/28266460-26b2-4455-ab42-1456f483a412) ([Notes](https://github.com/jreades/i2p/blob/master/lectures/3.3-DOLs_to_Data.md))
- Watch: [Functions](https://web.microsoftstream.com/video/3bd3fe3a-5dea-4ac8-a3e2-49ab50b862aa) ([Notes](https://github.com/jreades/i2p/blob/master/lectures/3.4-Functions.md))
- Watch: [Packages](https://web.microsoftstream.com/video/0ef82489-8c35-4532-a459-596d8e8f9633) ([Notes](https://github.com/jreades/i2p/blob/master/lectures/3.5-Packages.md))

#### Readings

- [@Etherington:2016] [DOI](https://doi.org/10.1080/03098265.2015.1086981)
- [@Donoho:2017] [DOI](https://doi.org/10.1080/10618600.2017.1384734)
- [@Unwin:1980] [DOI](https://doi.org/10.1080/03098268008708772)

#### Contribution

- Padlet: [Collaborative Agenda]

#### Quiz!

- Complete the [short Moodle quiz](https://moodle.ucl.ac.uk/mod/quiz/view.php?id=24300940) associated with this week's activities.

### Workshop

- Reviewing the **Collaborative Agenda** 
- Discussion of **Readings** 
- **Live Coding** 

### Practical

The practical can then be downloaded from [GitHub](https://github.com/jreades/i2p/raw/master/practicals/Practical-03-Foundations_2.ipynb).

# Week 4: Object-Oriented Programming

### Preparation

#### Lectures

- Watch: [Methods](https://web.microsoftstream.com/video/d953bec3-667d-4330-88ca-07deb9c68c9a) ([Notes](https://github.com/jreades/i2p/blob/master/lectures/4.1-Methods.md))
- Watch: [Classes](https://web.microsoftstream.com/video/8727d485-199e-4f49-ab87-0848366a55ea) ([Notes](https://github.com/jreades/i2p/blob/master/lectures/4.2-Classes.md))
- Watch: [Design](https://web.microsoftstream.com/video/caade180-3e55-463c-a5b9-4572dd2cd2f3) ([Notes](https://github.com/jreades/i2p/blob/master/lectures/4.3-Design.md))
- Watch: [Exceptions](https://web.microsoftstream.com/video/ab802229-9eb2-46c3-8fa6-a6dec56a6828) ([Notes](https://github.com/jreades/i2p/blob/master/lectures/4.4-Errors.md))

#### Readings

- [@Cox:2016] [PDF](http://insideairbnb.com/reports/how-airbnbs-data-hid-the-facts-in-new-york-city.pdf)
- [@dignazio:2020, chap. 5] **Unicorns, Janitors, Ninjas, Wizards, and Rock Stars** [Pre-review Chapter URL](https://bookbook.pubpub.org/pub/fcshwhq6)

#### Contribution

- Padlet: [Collaborative Agenda]

#### Quiz!

- Complete the [early feedback questionnaire](https://moodle.ucl.ac.uk/mod/questionnaire/view.php?id=2429914) please!

### Workshop

- Reviewing the **Collaborative Agenda** 
- Discussion of **Readings** 
- **Live Coding** 

### Practical

The practical can be [downloaded from GitHub](https://github.com/jreades/i2p/blob/master/practicals/Practical-04-Objects.ipynb).

# Week 5: Numeric Data

### Preparation

#### Lectures

- Watch: [Logic](https://web.microsoftstream.com/video/b9684684-5210-4917-8066-c7c247872051) ([Notes](https://github.com/jreades/i2p/blob/master/lectures/5.1-Logic.md))
- Watch: [Randomness](https://web.microsoftstream.com/video/18ee48e3-81d9-42d2-9e24-d434a9aa06ce) ([Notes](https://github.com/jreades/i2p/blob/master/lectures/5.2-Randomness.md))
- Watch: [Data Files](https://web.microsoftstream.com/video/465db9d5-fc82-42f7-ada4-089a01de1d7b) ([Notes](https://github.com/jreades/i2p/blob/master/lectures/5.3-Files.md))
- Watch: [Pandas](https://web.microsoftstream.com/video/ce84fd59-b44f-40cb-804b-593613053e24) ([Notes](https://github.com/jreades/i2p/blob/master/lectures/5.4-Pandas.md))

#### Readings

- [@dignazio:2020, chap. 4] **What Gets Counted Counts** in *Data Feminism*; [Pre-review URL](https://bookbook.pubpub.org/pub/rykaknh1)
- [@Wachsmuth:2018] [DOI](https://doi.org/10.1177%2F0308518X18778038)
- [@Harris:2018] [URL](https://www.theguardian.com/commentisfree/2018/feb/12/profiteers-killing-airbnb-erode-communities)

#### Contribution

- Padlet: [Collaborative Agenda]

### Workshop

- Brief Discussion of **Assessments* 
- Reviewing the **Collaborative Agenda** 
- Discussion of **Readings** 
- **Live Coding** 

### Practical

The practical can be [downloaded from GitHub](https://github.com/jreades/i2p/blob/master/practicals/Practical-05-Numeric_Data.ipynb).

# Reading Week

You should be doing the readings that will support your answers to Assessment #2. And, looking ahead to the Final Assessment and where you might find ideas or literature to support your thinking, I'd suggest having a browse of the [Full Bibliography](https://github.com/jreades/i2p/blob/master/bib/Bibliography.md). This is a working document and I will add more items as and when I come across them or new works are published!

### Readings

In addition to looking for relevant content in [@dignazio:2020] ([URL](https://bookbook.pubpub.org/data-feminism)), you will also want to check consider:

- [@Elwood:2017] [DOI](https://doi.org/10.1080/13658816.2017.1334892)
- [@Elwood:2018] [DOI](https://doi.org/10.1080/0966369X.2018.1465396)
- [@Bemt:2018] [DOI](https://doi.org/10.1080/03098265.2018.1436534)
- [@Amoore:2019] [DOI](https://doi.org/10.1177%2F0263276419851846)
- [@Crawford:2015] [DOI](https://doi.org/10.1007/s10708-014-9597-z)

# Week 6: Spatial Data

### Preparation

#### Lectures

- Watch: [Mapping](https://web.microsoftstream.com/video/74559a29-4214-4f79-8d41-06293ba1bade) ([Notes](https://github.com/jreades/i2p/blob/master/lectures/6.1-Mapping.md))
- Watch: [GeoPandas](https://web.microsoftstream.com/video/b79dab45-1390-40e9-b97b-ffd3c63e55d6) ([Notes](https://github.com/jreades/i2p/blob/master/lectures/6.2-Geopandas.md))
- Watch: [EDA](https://web.microsoftstream.com/video/bf4b47c4-2bbc-4989-a11c-cc3be529cef1) ([Notes](https://github.com/jreades/i2p/blob/master/lectures/6.3-EDA.md))
- Watch: [ESDA](https://web.microsoftstream.com/video/5c0a28b2-eb42-4ace-baed-a0fa9131aa4a) ([Notes](https://github.com/jreades/i2p/blob/master/lectures/6.4-ESDA.md))

#### Readings

- [@dignazio:2020, chap. 6] **The Numbers Don't Speak for Themselves** in *Data Feminism*; [Pre-review URL](https://bookbook.pubpub.org/pub/6ui5n4vo)
- [@Elwood:2017] [DOI](https://doi.org/10.1080/13658816.2017.1334892) 

#### Contribution

- Padlet: [Collaborative Agenda]

#### Quiz!

- Complete the [short Moodle quiz](https://moodle.ucl.ac.uk/mod/quiz/view.php?id=2532856) associated with this week's activities.

### Workshop

- Reviewing the **Collaborative Agenda** 
- Discussion of **Readings** 
- **Live Coding** 

### Practical

The practical can be [downloaded from GitHub](https://github.com/jreades/i2p/blob/master/practicals/Practical-06-Spatial_Data.ipynb).

# Week 7: Textual Data 

### Preparation

#### Lectures

- Watch: [Notebooks as Documents](https://web.microsoftstream.com/video/fa80e0b3-a14a-44dd-b9b5-1774dde219ba) ([Notes](https://github.com/jreades/i2p/blob/master/lectures/7.1-Notebooks_as_Documents.md))
- Watch: [Patterns in Text](https://web.microsoftstream.com/video/9e419529-f1d7-40a9-94e3-3adf8c4608f6) ([Notes](https://github.com/jreades/i2p/blob/master/lectures/7.2-Patterns_in_Text.md))
- Watch: [Cleaning Text](https://web.microsoftstream.com/video/3a7ad210-31fb-4d15-8e33-3bea705042e2) ([Notes](https://github.com/jreades/i2p/blob/master/lectures/7.3-Cleaning_Text.md))
- Watch: [Analysing Text](https://web.microsoftstream.com/video/edcbccdd-15b9-49da-b84a-691b5cc41b88) ([Notes](https://github.com/jreades/i2p/blob/master/lectures/7.4-Analysing_Text.md))


#### Readings

- [@Ladd:2020] [Web Page](https://programminghistorian.org/en/lessons/common-similarity-measures)
- [@Lavin:2019] [Web Page](https://programminghistorian.org/en/lessons/analyzing-documents-with-tfidf)

#### Contribution

- Padlet: [Collaborative Agenda]

#### Quiz!

- Complete the [short Moodle quiz](https://moodle.ucl.ac.uk/mod/quiz/view.php?id=2555003) associated with this week's activities.

### Workshop

- Reviewing the **Collaborative Agenda** 
- Discussion of **Readings** 
- **Live Coding** 

### Practical

The practical can then be [downloaded from GitHub](https://github.com/jreades/i2p/blob/master/practicals/Practical-07-Textual_Data.ipynb).

# Week 8: Visualising Data

### Preparation

#### Lectures

- Watch: [Linking Data](https://web.microsoftstream.com/video/05759776-10b9-4476-9949-c7c0fbeef298) ([Notes](https://github.com/jreades/i2p/blob/master/lectures/8.1-Linking_Data.md))
- Watch: [Linking Spatial Data](https://web.microsoftstream.com/video/4bf27eaa-90d8-4628-81ba-e673816e691f) ([Notes](https://github.com/jreades/i2p/blob/master/lectures/8.2-Linking_Spatial_Data.md))
- Watch: [Grouping Data](https://web.microsoftstream.com/video/7f8df345-7339-466c-be60-a65be1ad6b57) ([Notes](https://github.com/jreades/i2p/blob/master/lectures/8.3-Grouping_Data.md))
- Watch: [Data Visualisation](https://web.microsoftstream.com/video/4cc8c5a2-5881-4342-adda-32b39a989d90) ([Notes](https://github.com/jreades/i2p/blob/master/lectures/8.4-Visualising_Data.md))

#### Readings

- [@dignazio:2020, chap. 3] On Rational, Scientific, Objective Viewpoints from Mythical, Imaginary, Impossible Standpoints in Data Feminism; [Pre-review URL](https://bookbook.pubpub.org/pub/8tjbs2x5)
- [@badger:2019] The Neighborhood Is Mostly Black. The Home Buyers Are Mostly White. [URL](https://www.nytimes.com/interactive/2019/04/27/upshot/diversity-housing-maps-raleigh-gentrification.html)

#### Contribution

- Padlet: [Collaborative Agenda]

#### Quiz!

- Complete the [short Moodle quiz](https://moodle.ucl.ac.uk/mod/quiz/view.php?id=2579101) associated with this week's activities.

### Workshop

- Reviewing the **Collaborative Agenda** 
- Discussion of **Readings** 
- **Live Coding** 

### Practical

The practical can then be downloaded from GitHub.

# Week 9: Dimensions in Data 

### Preparation

#### Lectures

- Watch: [The Data Space](https://web.microsoftstream.com/video/9c365da5-81b4-43f8-8296-16086f3f5887) ([Notes](https://github.com/jreades/i2p/blob/master/lectures/9.1-Data_Space.md))
- Watch: [Transformation](https://web.microsoftstream.com/video/070225ac-285b-4408-8c2a-35e223b79845) ([Notes](https://github.com/jreades/i2p/blob/master/lectures/9.2-Transformation.md))
- Watch: [Dimensionality](https://web.microsoftstream.com/video/9b47ffbb-de09-4538-bf84-66decfd1250b) ([Notes](https://github.com/jreades/i2p/blob/master/lectures/9.3-Dimensionality.md)) 

#### Readings

- [@Bunday:0000] A Final Tale or You Can Prove Anything with Figures [URL](https://www.ucl.ac.uk/~ucahhwi/AFinalTale.pdf)
- [@Harris:2019] The Certain Uncertainty of University Rankings [URL](https://rpubs.com/profrichharris/uni-rankings)
- [@Cima:2014] The Most and Least Diverse Cities in America, Priceonomics [URL](https://priceonomics.com/the-most-and-least-diverse-cities-in-america/) ([PDF with Figures](https://github.com/jreades/i2p/blob/master/docs/The_Least_Segregated_Cities_in_America.pdf))
- [@lu:2013] Are statisticians cold-blooded bosses? a new perspective on the ‘old’ concept of statistical population [DOI](https://doi.org/10.1111/j.1467-9639.2012.00524.x)

#### Contribution

- Padlet: [Collaborative Agenda]

#### Quiz!

- Complete the [short Moodle quiz](https://moodle.ucl.ac.uk/mod/quiz/view.php?id=2621322) associated with this week's activities.

### Workshop

- Reviewing the **Collaborative Agenda** 
- Discussion of **Readings** 
- **Live Coding** 

### Practical

The practical can then be [downloaded from GitHub](https://github.com/jreades/i2p/blob/master/practicals/Practical-09-Dimensions_in_Data.ipynb).

# Week 10: Grouping Data 

### Preparation

#### Lectures

- Watch: [Classification](https://web.microsoftstream.com/video/1a88749d-2dca-4bc6-9990-3227a253bfb0) ([Notes](https://github.com/jreades/i2p/blob/master/lectures/10.1-Classification.md))
- Watch: [Clustering](https://web.microsoftstream.com/video/77b1ad5c-bece-4154-89b3-cb1e42877cae) ([Notes](https://github.com/jreades/i2p/blob/master/lectures/10.2-Clustering.md))

#### Readings

- Shapiro, W. and Yavuz, M. (2017) Rethinking 'distance' in New York City Medium [URL](https://medium.com/topos-ai/rethinking-distance-in-new-york-city-d17212d24919)
- Wolf, L. *et al.* (2020) Quantitative geography III: Future challenges and challenging futures, *Progress in Human Geography* [DOI](https://doi.org/10.1177%2F0309132520924722)
- Arribas-Bel, D. and Singleton, A. (2019) Geographic Data Science, *Geographical Analysis* [DOI](https://doi.org/10.1111/gean.12194)


#### Contribution

- Padlet: [Collaborative Agenda]

#### Quiz!

- Complete the short Moodle quiz associated with this week's activities.

### Workshop

- Reviewing the **Collaborative Agenda** 
- Discussion of **Readings** and **Reflections** 

### Practical

The practical can then be [downloaded from GitHub](https://github.com/jreades/i2p/blob/master/practicals/Practical-10-Grouping_Data.ipynb).

Bibliography
============

::: {#refs}
:::

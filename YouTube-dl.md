## Using YouTube-dl

YouTube-dl is a command line YouTube downloader application, but it can also download videos from other websites.
Here is a good website to use to install or learn to use via examples: https://ostechnix.com/youtube-dl-tutorial-with-examples-for-beginners/

# How we used it

First, we got a list of all the available formats:

$ youtube-dl --list-formats https://www.twitch.tv/videos/832507786

This returns a list of all the formats:

![Alt text](https://github.com/JustinTienken-Harder/DeepLearningOfDynamics/blob/master/Images/README_Images/Screen%20Shot%202020-12-14%20at%204.20.18%20PM.png)

From the above, we now choose a format, i.e. 360p, 480p, etc....:

$ youtube-dl -f 360p -g https://www.twitch.tv/videos/832507786


This command returns a string:

![Alt text](https://github.com/JustinTienken-Harder/DeepLearningOfDynamics/blob/master/Images/README_Images/return_string.png)
  

Now, to put everything together and download the portion of the video we specifially want, we use ffmpeg. For ffmpeg, we give the -i command then the string we got from above. Next, we use the -ss command and pass in the starting time we want to start downloading from the video follwed by the -to command with an end time. Finally, we just use the -c copy command and give the output a file name (preferably an mp4 file).


ffmpeg -i <paste string from prev. command here> -ss <start time in 00:00:00 format>  -to <end time in 00:00:00 format> -c copy <file_name>
  
Example: ffmpeg -s https://dqrpb9wgowsf5.cloudfront.net/b637e79f891b3bbd02d1_crittervision_40901217998_1607623227/360p30/index-dvr.m3u8 -ss 7:00:00 -to 10:30:00 -c output.mp4

This starts the download from 7 hours into the video and stops 10 hours and 30 minutes into the video.

This is how we scrapped the video data for this project.

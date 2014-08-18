Team City Launch Button
===========

TeamCity deploys IRL! It's a bummer to work on a project with a team full of people who don't get to have the joy of deploying to prod. I wanted to add a bit of pomp and circumstance to our deployment process, so I made a rig to launch a deploy by pressing a big red button.

The rig includes a button for branch switching, an arming switch to prevent accidental launch, and a few indicator lights that help you determine the progress of the launch and the target branch.

The launch is kicked off by making a CURL call to the [TeamCity API](http://confluence.jetbrains.com/display/TCD8/REST+API). You'll need to add login creds for TC and the branch IDs that you want to target. There are two XML files that have the build IDs in them, you'll need to update those as well.

The .conf file is there if you want to have this script run on boot/reboot of the Raspberry Pi. You can find out more about that [here](http://www.raspberrypi.org/forums/viewtopic.php?f=37&t=49153)

Check out a video of the project [on YouTube](https://www.youtube.com/watch?v=wxBtHvDUVHk).

Hit me up on [Twitter](https://twitter.com/justinSmithChi) with any questions or comments - I'd love to see if anyone else implements this. This is my first run at Python, so any suggestions for improving the code are more than welcome.
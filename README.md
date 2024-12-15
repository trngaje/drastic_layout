### drastic_layout

resolution | description
---------- | -----------------
640x480  | images worked on by the @steward-fu.
1024x768 | resizing the 640x480 image and using it again.
720x720 | images worked on by @duncanyoyo1.
1280x720 | This image is pre-applied by crossmix.
854x480 | not defined
7204480 | not defined
480x320 | not defined

#### The description of layout.json is as follows.

> The format is still in development. It may be deleted at any time.

"type" : 0 (default,normal),1:trasparent,2:vertical,3:high resolution,4:single <br>
"rotate" : 0, 90, 270 for vertical layout <br>
"bg" : "[file name of bg image]" <br>
"_x" : positon x of screen <br>
"_y" : position y of screen <br>
"_w" : width of screen <br>
"_h" : height of screen <br>

example <br>
type : normal
~~~
{
    "index":10,
    "name":"vh_s2",
    "bg":"bg_vh_s2.png",

    "screen0_x":240,
    "screen0_y":0,
    "screen0_w":160,
    "screen0_h":120,

    "screen1_x":80,
    "screen1_y":120,
    "screen1_w":480,
    "screen1_h":360
},
~~~

I'm not good at graphics work tools, so I'm always welcome to reflect on this git hub after someone changes the bg image.

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/G2G5DV6J4)

# CardTuber: Animated Avatar On a Business Card.

People who post videos on Youtube are called Youtubers.
Youtubers who use animated avatars are called V-tubers.
V-tubers who only use 4 png images as avatars are called Pngtubers.
What about, what about, what about people who talk through animated avatars in real life?

Introducing CardTuber: an animated avatar on a business card.

## The Story

Let's rewind a bit to the beginning.
First the earth cooled. And then came the CircuitPython.
I made an online IDE for CircuitPython (circuitpy.online) and consider myself as a maker.
I demoed it on phili maker faire in 2022,
and LI maker faire in 2023.
I was also planning to go to the LI maker faire in 2024.
One thing that I always want for the maker faire is a maker badge,
a fun and powerful one like the supercon one.
So I decided to make one for this year.

While I was thinking about how to design a maker badge,
I came across this Business Card Contest on Hackaday.
I just realized this is the perfect form factor of a badge:
- Business card size
- introducing myself
- doing something cool

## The design

Of course this is a business card / badge,
so it need to have my name on it,
together with a little bit intro of my self.
On the other side, people usually have a logo or photo of there business.

I can put my youtube avatar there, but that is too boring.
In one of my recent videos, I made an animated avatar by drawing 4 png images.
(which is based on the Character Izutsumi in Dungeon Meshi)
So I think It would be a good idea to put that avatar here.

Of course this is a maker badge for LI Maker Faire,
The light house on the LI Maker Faire logo is an actual light house at Montauk.
As a Long Islander, I have been there several times and like it a lot.
So I found a good photo of that light house on MTA's website,
and draw a sketch of it.

## The hardware

Because the avatar need to talk when I talk,
I need a MIC module to capture the sound.
This made Seeed Xiao the perfect choice for micro controller board.
In a small package it includes a
- powerful computing unit
- MIC
- batter management circuit

It also has a acceleration meter and BLE, which I didn't use in this project

The screen I choose is Sharp.
I mean it is really Sharp (bad pon)....
Sharp memory LCD are power efficient and also very good in image quality.
Unlike the OLED screens that are flicking all the time,
images on Sharp memory LCDs are still which makes it much better when moved a lot.

If I tell you this array of resistors are all 1M ohm,
you probably already know that they are used for capacitive touch.
And yes, the whole right side of the business card is a linear touch pad.
Because I don't have too much on the board, I can hide all the traces to the back of the PCB.
The only thing in the front are the touch pads.


## The Software

The code is written in CircuitPython,
which is not only because I am the author of CircuitPython Online IDE,
but also because it has well support for 52840 microcontrollers, mic and Sharp memory displays.

### Blink and Speak

The mechanism is very similar to the mechanism of the PNG tuber.
Basically I have 4 images as the combination of mouse open/close and eyes open/close.
And the system will pick one of the images depending on the status of the eys and mouse.

And the avatar will blink randomly every 2~5 seconds.
This is just achieved by a timer with random time duration.

The avatar will speak when the volume picked up from the mic is higher than the threshold.
And when speaking, the avatar will raise a little bit and come back when stop speaking to look more lively.

The volume is picked up as the log of the amplitude of the sound wave.
Threshold is just a number.
However, Maker Faire is a quite busy environment,
so I actually cannot rely on a pre-set fox number threshold level
because I don't have any idea of the background noise level.
I did a bit adaptive algorithm:
first I keep record of all the volume with a time window,
and set the threshold to be a little above the minimum volume within the the time window.
This adaptive threshold actually worked very well.

### QR code

The Business Card should function as a business card: giving contact information.
Even though I have a lot written on the card,
I still want to do that in a fancier way.
When People ask me about my social/github,
I can swipe up the texts to bring up the qr code.

## The show

There are hole on the badge for me to ware it stand alone,

However, to ware this as a make badge to gether with the badge of the Maker Faire,
I 3D printed a case for the badge, which can be fixed to the Maker Faire badge by a twisted wire.
There are also holes on the case so the mic is not blocked.

Here is how it looked on the Maker Faire day!

## The bonus

And of course, how can such a thing be complete without games.

## The end

Developer: Jeremy Springston
Project: End-to-End House Environmental Analysis
Version 1.0

Intro: First, thank you for taking the time to read through this! It's my first attempt at something like
this so bear with me as I screw up one thing after another. Don't hesitate to let me know how I can do
better, but at the same time, don't be a dick. That's all I ask. 

Background: My house tends to get a bit toasty in the summer and cold in the winter, which, naturally, 
means my power bill fluctuates wildly. Since I'm not a fan of paying a crap ton of money for anything
not fun, I decided to put my education and professional experience to the test for a solution. The goal 
is to set up a data pipeline to wirelessly transfer temperature, air pressure, and humidity data from my 
Arduino to a SQLite database on my computer, then have it run through a machine learning model. This
should help me optimize air flow in the house, save money on peak month power bills, and let me buy more
fun sensors and whatever else I can use to make more fun stuff.

Project Components:
- Hardware 
 - Arduino Uno WIFI
 - Grove DHT-11
 - Grove LED
- Software
 - Arduino IDE 2.2.1
 - Python 3.9
 - SQLite 3.4.4
 
System Architecture:

Arduino Uno WIFI
      |------------>WIFI<------->Flask------->SQLite-------->Analysis scripts---->Output
      |                                         ^                      |
      |                                         |                      v
      |                                         |----------------------|
    __|__
   |     |
DHT-11  BMP-280

Update (11 Sep 23): I've made some significant revisions to parts of the code that revolve around its analytical and data-logging capabilities. One issue I have seen that is unrelated to the Python pipeline is with the Arduino. For some reason, I have to manually toggle the reset switch once every twelve hours or it will stop transmitting data. I'm digging into the issue but if anyone out there understands the problem, don't hesitate to throw out a solution. A second, but minor, issue I'm seeing is that the Spyder console output sometimes shows four df.describe() calls and I cannot figure out why. It doesn't impact anything important, but it would be nice to solve. 

Final Thoughts: I'm not exactly sure what's supposed to go in a README file, so hit me with your knowledge.
Thanks again for taking a look and I'm looking forward to collaborating with folks toward the goal of making
something simultaneously functional and cool!

# New York Food List

Food is essential to everyday life. Trying out new restaurants and exploring different kinds of cuisine is something I truly enjoy. Being able to shock my tastebuds and delve into the unknwon helps me to learn more about a country's cusine and gives insight as to how other people live around the world. Since I can't travel aroudn the world constantly, trying new cusine has become a substitute for this. Thus, I created this program to keep me updated on new restaurants that pop up in NYC, so that I can try them out whenever possible. I only hope that my stomach and wallet can handle all these restuarants.

## Why specifically NYC?
I read in an article somewhere that eating at all the restaurants in New York City would take an average of 22.7 years. Besides being a melting hotpot of culture and with no shortage of restaurants, I decided to choose New York City as it perfectly aligned with my agenda of finding and trying various types of restaurants. Additionally, the websites that I use to find the restaurants also provided plenty of data on these restaurants. 

Edit: Found the article! https://bit.ly/2RqVagq

## So what does this repo do?
This repo scrapes both the Eater and The Infatuation websites for their monthly hot and essential recommended restaurants in New York City and then finds additonal data on the restaurants using the yelp api to gather their ratings, location and website, etc. It is then compiled into a large excel file which is then sent automatically to an email address which can be used for further "analysis" purposes. When compiling the excel file, users are able to choose between having an excel file with ONLY the feautured restaurants for this month AND/OR an excel file which updates the popular restaurants every time you run the program. The idea is to create a constant update to notify users of new restaurants and places one should try.

## How do I run it?
Besides making several minor changes, all you have to do is to download this repo, ensure that the command directory is linked to the proper spot and just run it as a regular python program! The changes that you need to make are simple: Just input a forwarding and receiving email (same email works) in fromaddr and toaddr respectively, and replace the stars with your email password in "s.login(fromaddr, "******")" (line 191). You might also need to change some security settings related to your email to receive this as an email. If you dont want it as an email, then ignore the send_email function and just use the convert_to_xl function. You also need to get a yelp-api key via https://bit.ly/3mkSizM


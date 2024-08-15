# Introduction
This is a bot that automatically (periodically):
1. Crawls products from e-commerce websites such as Shopee, Lazada
2. Crawls product's affiliate url from the product's original url from the third-party website that provides affiliate service
3. Generate marketing content based on pre-designed templates
4. Publish marketing content and product photos on social media such as Facebook

# Disclaimer
This software is for educational purposes only. Do not risk money and credit (relationship) against the websites that you crawl. 

USE THE SOFTWARE AT YOUR OWN RISK. I AND ALL AFFILIATES ASSUME NO RESPONSIBILITY FOR YOUR ACTIONS.

I strongly recommend you to have coding and Python knowledge. Do not hesitate to read the source code and understand the mechanism of this bot.

# Quick Start
I suggest that you should expect some runtime errors the first time running the bot. It is more convenient for a user to have prior knowledge of Python, MongoDB and Docker for investigating and fixing the bugs.
1. Run the Makefile to run the bot
2. Run docker-compose to start the monitoring

# Design Overview
As it has been a while since I stopped developing the bot, this documentation only resembles knowledge pieces that are still retained in my memory.
- The bot runs by scheduling the unit of the job called "flow". Each flow represents an end2end business flow
- A flow, when invoked by the scheduler, triggers the schedules for sub-flows like product flow and publishing flow. 
- In product flow, the bot craw the products from e-commerce websites, crawls the affiliate links, generates marketing content, and saves all of them to the MongoDB database. 
- In publishing flow, the bot retrieves products from the database and publishes content on social media
![affiliate-bot-design](https://github.com/user-attachments/assets/7c8e34a6-c705-4d95-b59f-94d7428843b1)

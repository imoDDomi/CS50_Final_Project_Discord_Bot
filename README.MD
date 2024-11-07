# Final Project Discord Bot

## CS50 informations
- Video Demo: [here](https://youtu.be/JW6xTww-7J0)

## Description

This Discord Bot contains 2 COGs

- Memes
  - pulls images from Reddit, you can specify from which subreddit
- Expenses
  - collects data from a Discord channel where people put in their expenses in the format "10€ Fortnite" or "5€ clash of clans


## Getting Started

### Dependencies

- You can either run your program locally on a computer or in a cloud
- COGs are developed for the [Red-Discord Bot](https://github.com/Cog-Creators/Red-DiscordBot)
- create Reddit account and add an App to get the ID and secret


### Installing

Install Red-Discord Bot from https://docs.discord.red/en/stable/install_guides/index.html

Download the COGs

Run through the setup program:
```
redbot-setup
```
Create a .env file in the project folder
add following lines

```
CLIENT_ID=<your_id>
CLIENT_SECRET=<your_secret>
USER_AGENT=<your_agent>
```
### Executing program

run through the installation process of red discord bot <br>
Set a specific prefix [p] that you later have to write before your commands, e.g. 
```
!post <subreddit>
```
https://docs.discord.red/en/stable/install_guides/windows.html#installing-red

Command to run the bot in windows terminal:
```
redbot <name_of_your_bot>
```

## Commands

Commands available within the COGs

*Memes*

```
[p]post <subreddit> pulls a random picture from the subreddit
[p]delete deletes all messages the bot send in this channel

Set a channel ID in order to run the automatic post every 24h
```

*Expenses*

```
[p]broke <username> generates an overview with all expenses described in this channel in format xxx€ <game>
[p]compare compares all user inputs from this channel for a summary
```

## Authors

Contributors names and contact info

Dominik Polo

## Version History

* v0.1 Initial Release
* v0.2 fixed some bugs

## License

This project is licensed under the MIT License - see the LICENSE.md file for details

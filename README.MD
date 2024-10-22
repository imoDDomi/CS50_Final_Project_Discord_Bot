# Final Project Discord Bot



## Description

This Discord Bot contains of 2 COGs

- Memes
  - pulls images from subreddit, you can specify from which channel
- Expenses
  - collects data from a Discord channel where people put in their expenses in the format "10€ Fortnite" or "5€ clash of clans


## Getting Started

### Dependencies

- You can either run your program locally on a computer or in a cloud
- COGs are based on the Red-Discord Bot
- create Reddit account and add an App to get the ID and secret


### Installing

Install Red-Discord Bot from https://docs.discord.red/en/stable/install_guides/index.html

Download the COGs

Run through the setup program:
```
redbot-setup
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

## License

This project is licensed under the MIT License - see the LICENSE.md file for details

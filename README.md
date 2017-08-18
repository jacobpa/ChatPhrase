# ChatPhrase

ChatPhrase is a discord bot which utilizes [discord.py](https://github.com/Rapptz/discord.py) as well as the [Datamuse API](https://www.datamuse.com/api/) in order to emulate Hasboro's [Catch Phrase](https://en.wikipedia.org/wiki/Catch_Phrase_(game)) party game.

## Dependencies
ChatPhrase depends on:
* [discord.py](https://github.com/Rapptz/discord.py)
* [Requests](https://github.com/requests/requests)

## Setup
After installing the necessary dependencies, rename or copy `config.py.example` to `config.py`. Make sure to replace the `BOT_TOKEN` and `CLIENT_ID` values with the appropriate token and ID provided in the Discord API control panel.

## Commands
All commands must begin with the prefix you define in the `config.py` file to use.
* `newgame "category"` - Starts a new game with a pool of 100 words related to the given category.
* `newword` - If used by the player describing a word, will message the user with a new word.
* `vote` - Allow's users to vote to start a new game, the minimum amount of votes (including the player who started the game) can be defined in the `config.py` file.
* `correct` - If used by the player describing a word, will give the next player a word.
* `namecategory` - Makes the bot tell you the current category of words.
* `fstop` - Force ends the game, must have the administrator role to use.
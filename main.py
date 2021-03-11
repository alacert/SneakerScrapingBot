import discord
import lxml.html
import json
import aiohttp
import validators
import time
import random
from discord.ext import commands
from discord.utils import get
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from bs4 import BeautifulSoup

TOKEN = "ODExNTE1MTc5NTQzNTYwMjEz.YCzUaA.m46HDxACdKShtq75WZtQrf3TEog"
PREFIX = "."
COLOR = 0xb17bff

# The location of the firefox binary, NOTE: Will be different on different systems, will need to change!
binary = FirefoxBinary('C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe')
# Create the Selenium Browser to get our HTML
driver = webdriver.Firefox(firefox_binary=binary)

# Initialize the discord bot
bot = commands.Bot(command_prefix=PREFIX)
bot.remove_command('help')

async def update_data(users, user,server):
    if not str(server.id) in users:
        users[str(server.id)] = {}
        if not str(user.id) in users[str(server.id)]:
            users[str(server.id)][str(user.id)] = {}
            users[str(server.id)][str(user.id)]['experience'] = 0
    elif not str(user.id) in users[str(server.id)]:
        users[str(server.id)][str(user.id)] = {}
        users[str(server.id)][str(user.id)]['experience'] = 0


async def add_experience(users, user, exp, server):
    users[str(user.guild.id)][str(user.id)]['experience'] += exp


async def check_assign_level(users, user, server):
    num_of_messages = users[str(server.id)][str(user.id)]['experience']

    if num_of_messages >= 25:
        role = get(server.roles, name="Pink")
        await user.add_roles(role)
    if num_of_messages >= 100:
        role = get(server.roles, name="Green")
        await user.add_roles(role)


async def level_system(message):
    with open('level.json', 'r') as f:
        users = json.load(f)

    await update_data(users, message.author, message.guild)
    await add_experience(users, message.author, 1, message.guild)
    await check_assign_level(users, message.author, message.guild)

    with open('level.json', 'w') as f:
        json.dump(users, f)



async def create_embed(top_list, bottom_list, title, url, ctx):
    # Create an embed with the two lists supplied and the title


    # Create the embed
    embed = discord.Embed(title=title, url=url, color=COLOR)

    # Iterate through each item in the list
    for index in range(len(top_list)):
        # Add field to the embed with the list with the value of top_list[index] and bottom_list [index]
        embed.add_field(name=top_list[index], value=bottom_list[index], inline=True)

    # Send the embed
    await ctx.channel.send(embed=embed)


async def create_embed_image(top_list, bottom_list, title, url, image_url, ctx):
    # Create an embed with the two lists supplied and the title

    # Create the embed
    embed = discord.Embed(title=title, url=url, color=COLOR)

    embed.set_thumbnail(url=image_url)

    # Iterate through each item in the list
    for index in range(len(top_list)):
        # Add field to the embed with the list with the value of top_list[index] and bottom_list [index]
        embed.add_field(name=top_list[index], value=bottom_list[index], inline=True)

    # Send the embed
    await ctx.channel.send(embed=embed)


def get_html(url):
    # Gets HTML from the URL

    # Checks to see if the user entered a URL
    if url == "":
        return False

    # Checks to see if the URL is valid, if not then return
    if validators.url(url) is not True:
        return False

    # Sends Selenium to the link and grabs the HTML, and sets up the bs4 parser
    driver.get(url)
    return driver.page_source


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


async def good_morning(message):
    response_text = [
        "Rise and shine",
        "Top of the morning to you",
        "Good day to you",
        "Have a great day",
        "Hello there",
        "Wishing you the best for the day ahead",
        "How are you this fine morning",
        "Isn’t it a beautiful day today",
        "Wakey, wakey, eggs and bakey",
        "Look alive",
        "Good morning, sleepy head/wakey wakey, sleepy head",
        "Look at what the cat dragged in"
        "What a pleasant morning we are having",
        "How is your morning going so far",
        "Morning"
    ]
    response = response_text[random.randint(0, len(response_text) - 1)]
    await message.channel.send(response + ", " + message.author.mention)



async def good_night(message):
    response_text = [
        "Nighty Night",
        "Sweet dreams",
        "Sleep well",
        "Have a good sleep",
        "Dream about me",
        "Go to bed, you sleepy head",
        "Sleep tight",
        "Time to ride the rainbow to dreamland",
        "Don’t forget to say your prayers",
        "Goodnight, the little love of my life",
        "Night Night",
        "Lights out",
        "See ya’ in the morning",
        "I’ll be right here in the morning",
        "I’ll be dreaming of you",
        "Sleep well, my little prince/princess",
        "Jesus loves you, and so do I",
        "Sleep snug as a bug in a rug",
        "Dream of me",
        "Until tomorrow",
        "Always and forever",
        "I’ll be dreaming of your face",
        "I’m so lucky to have you, Sweetheart",
        "I love you to the stars and back",
        "I’ll dream of you tonight and see you tomorrow, my love",
        "I can’t imagine myself with anyone else",
        "If you need me, you know where to find me",
        "Goodnight, the love of my life",
        "Can’t wait to wake up next to you"
    ]
    response = response_text[random.randint(0, len(response_text) - 1)]
    await message.channel.send(response + ", " + message.author.mention)


@bot.command(
    name="8ball",
    brief="Ask 8 ball questions"
)
async def eight_ball(ctx):
    response_text = [
        "As I see it, yes",
        "Ask again later",
        "Better not tell you now",
        "Cannot predict now",
        "Concentrate and ask again",
        "Don’t count on it",
        "It is certain",
        "It is decidedly so",
        "Most likely",
        "My reply is no",
        "My sources say no",
        "Outlook not so good",
        "Outlook good",
        "Reply hazy, try again",
        "Signs point to yes",
        "Very doubtful",
        "Without a doubt",
        "Yes",
        "Yes – definitely",
        "You may rely on it"
    ]

    response = response_text[random.randint(0, len(response_text) - 1)]
    await ctx.channel.send(response + ", " + ctx.author.mention)


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    await level_system(message)

    if bot.user.mentioned_in(message):
        if "gm" in message.content.lower():
            await good_morning(message)
        if "gn" in message.content.lower():
            await good_night(message)

    await bot.process_commands(message)


@bot.command(
    name="ping",
    brief="Prints pong back to the channel"
)
async def ping(ctx, *, arg=""):
    await ctx.channel.send("pong")


@bot.command(name="help")
async def help(ctx):
    embed = discord.Embed(title="help", color=COLOR)

    embed.add_field(name="help", value="Shows this menu", inline=True)
    embed.add_field(name="ping", value="Pong", inline=True)
    embed.add_field(name="stockx", value="Get prices for each size from a stockx link. \nUsage: `.stockx [url]`", inline=True)
    embed.add_field(name="goat", value="Same but with goat. \nUsage: `.goat [url]`", inline=True)
    embed.add_field(name="ebay", value="Displays list of items with prices for a search term on ebay. \nUsage:`.ebay [search-term]`", inline=True)
    embed.add_field(name="ebay-ping", value="Pings ebay x amount of times. \nUsage: `.ebay-ping [url] [amount of times]`", inline=True)

    await ctx.channel.send(embed=embed)


@bot.command(
    name="stockx",
    brief="Get prices for each size from a stockx link. Usage: .stockx [url]"
)
async def stockx(ctx, url=""):
    # Sends an embed of all the prices and sizes of the shoes on stockx with the link specified by the user
    # USAGE: .stockx [url]

    await ctx.channel.send("Processing...", delete_after=5)

    # Get the html from the URL
    html = get_html(url)
    if not html:
        await ctx.channel.send("Error: You didn't enter a valid URL! Usage: `.stockx [url]`")
        return

    soup = BeautifulSoup(html, "html.parser")

    # Gets the name of the sneaker, and the list of all the sneaker elements
    sneaker_name = soup.find_all('h1', class_="name")[0].text
    sneaker_list = soup.find_all('ul', class_="sneakers")[0].find_all('li')

    sneaker_image_url = soup.find_all('div', class_="image-container")[0].find_all("img")[0]["src"]

    # Creates an array that holds all the sizes and prices of the sneakers
    size_list = []
    price_list = []

    for sneaker in sneaker_list:
        # Gets the Sneaker Size (and removes the "US" text at the start), and Gets the price
        sneaker_size = sneaker.find_all("div", class_="title")[0].text.strip()
        sneaker_price = sneaker.find_all("div", class_="subtitle")[0].text.strip()

        print(sneaker_size)

        # Omits the sneaker size with the value "All"
        if sneaker_size == "All":
            continue

        if sneaker_size in size_list:
            continue

        # Append the sneaker_size and sneaker_price to size_list and price_list respectively
        size_list.append("Size " + sneaker_size)
        price_list.append("**Lowest ask: **" + sneaker_price)

    # Creates the embed with the values we just scraped
    await create_embed_image(size_list, price_list, sneaker_name, url, sneaker_image_url, ctx)


@bot.command(
    name="goat",
    brief="Get prices for each size from a goat link. Usage: .goat [url]"
)
async def goat(ctx, url=""):
    # Sends an embed of all the prices and sizes of the shoes on goat with the link specified by the user
    # Usage: .goat [url]

    await ctx.channel.send("Processing...", delete_after=5)

    # Get the html from the URL
    html = get_html(url)
    if not html:
        await ctx.channel.send("Error: You didn't enter a valid URL! Usage: `.goat [url]`")
        return

    # Create bs4 instance and lxml parser as bs4 doesn't support xpaths
    soup = BeautifulSoup(html, "html.parser")
    parse = lxml.html.fromstring(html)

    # Grab the contents of the script element that contains the JSON with the data we need, strip the whitespace,
    # Then remove the first 21 characters as we dont need them, and then feed the result into a json
    data = json.loads(parse.xpath('/html/body/script/text()')[2].lstrip()[21:])

    # Get the part of the JSON that contains the data about the sneakers
    sneakers = (data['default_store']['product-templates']['slug_map'])
    # Get the item ID which we need to go further down the tree
    item_id = list(sneakers.keys())[0]
    # Finally get to the part of the JSON that contains the data about the sneakers
    sneakers = (sneakers[item_id]['productVariants'])

    try:
        sneaker_image_url = soup.find_all("div", class_="ProductImageCarousel__Wrapper-yzm2o0-0")[0].find_all("img")[0]["src"]
    except IndexError:
        sneaker_image_url = "https://icon-library.com/images/no-image-icon/no-image-icon-0.jpg"

    # Try and get the Sneaker name, sometimes this fails so we'll use item_id as a backup

    try:
        name = soup.find_all('h1', class_="ProductTitlePane__Title-sc-17vgpmb-4")[0].text
    except IndexError:
        name = item_id

    # Create a list to hold the sizes and prices of the sneaker
    size_list = []
    price_list = []

    for sneaker in sneakers:
        # Get the size and the price in dollars
        size = str(sneaker['size'])
        price = str(int((sneaker['lowestPriceCents']['amount']) / 100))

        size = "Size " + size
        price = "**Lowest ask:** " + "$" + price

        if size in size_list:
            continue

        # Append these to size_list and price_list respectively
        size_list.append(size)
        price_list.append(price)

    # Create embed with the information we just scraped
    await create_embed_image(size_list, price_list, name, url, sneaker_image_url, ctx)



@bot.command(
    name="ebay",
    brief="Get prices for sold listing on ebay. Usage: .ebay [search term]"
)
async def ebay(ctx, *, arg=""):
    # Sends an embed of length 15 of the ebay search results with the search term specified by the user
    # USAGE: .ebay [search term]

    # If the user hasn't entered a search term then tell them the usage then return
    if arg == "":
        await ctx.channel.send("Error: no search term entered! Usage: `.ebay [search term]`")
        return

    # Replace spaces in string with +
    search_term = arg.replace(" ", "+")

    url = f"https://www.ebay.com/sch/i.html?_nkw={search_term}&_in_kw=1&_ex_kw=&_sacat=0&LH_Sold=1&_udlo=&_udhi=&_samilow=&_samihi=&_sargn=-1%26saslc%3D1&_salic=3&_sop=12&_dmd=1&_ipg=50&LH_Complete=1&_fosrp=1"

    # Create a aiohttp session and HTML GET the Ebay link with the search term send by the user
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            html = await resp.text()

    # Create the HTML parser
    soup = BeautifulSoup(html, "html.parser")

    # Grab the Element that contains the list of search term results
    item_list = soup.find(id="ListViewInner")

    try:
        # Try to get the list of search term results. If throws an AttributeError then we have been rate limited
        item_list = item_list.find_all('li', class_="sresult")
    except AttributeError:
        # Tell the user that we have been rate limited, and return
        await ctx.reply("Rate limited, please wait a second and try again")
        return

    # Create lists to hold the item names and prices
    item_names = []
    item_prices = []

    # Iterate through item_list and extract the data
    for item in item_list:
        # Get the elements that hold the name and price, and extract the text, and strip the whitespace
        name = item.find_all('a', class_="vip")[0].text.strip()
        price = item.find_all('span', class_="bidsold")[0].text.strip()

        # Append these values to the lists
        item_names.append(name)
        item_prices.append(price)

    # Create embed with the values we scraped, only send the first 15 items of each array
    await create_embed(item_names[:15], item_prices[:15], "Ebay results for: " + arg, url, ctx)


@bot.command()
async def fees(ctx, value: int):
    embed = discord.Embed(title="Fees", color=0xffff00)

    feeList = {
        "PayPal": f"${(value - (value * 0.029)) - 0.30}",
        "StockX Level 1": f"${value - (value * (0.095 + 0.03))}",
        "StockX Level 2": f"${value - (value * (0.09 + 0.03))}",
        "StockX Level 3": f"${value - (value * (0.085 + 0.03))}",
        "StockX Level 4": f"${value - (value * (0.08 + 0.03))}",
        "eBay": f"${value - (0.35 + (value * 0.10) + (value * 0.029) + 0.30)}",
        "Mercari": f"${value - (value * 0.10) - (value * 0.029) - 0.30}"
    }

    for key, value in feeList.items():
        embed.add_field(name=f'{key}', value=f'{value}')

    embed.set_footer(text="These fees are estimates and are subject to change.")
    await ctx.send(embed=embed)


@bot.command(
    name="ebay-ping",
    brief="Pings an ebay URL x amount of times. Usage: .ebay [url] [number of times]"
)
async def ebay_ping(ctx, url="", count=0):
    # Pings an Ebay listing the user specifies X amount of times
    # Usage: .ebay-ping [URL] [number_of_times]

    max_pings = 10

    # Check if the link or the count is empty, if so then display the usage and return
    if url == "" or count == "":
        await ctx.reply("Error: Wrong Arguments. Usage: `.ebay-ping [url] [number of times]`")
        return

    try:
        int(count)
        await ctx.reply("Error: " + count + " is not a valid number!")
    except:
        return

    if int(count) > max_pings:
        await ctx.reply("Error: " + max_pings + " is the maximum number of pings allowed")
        return

    # Check if url is a valid URL, if not return
    if validators.url(url) is not True:
        await ctx.reply("Error: " + url + " is not a valid URL!")
        return

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
    }

    await ctx.channel.send("Pinging...")

    # Create a aiohttp session and ping the URL count amount of times
    async with aiohttp.ClientSession() as session:
        for index in range(int(count)):
            await session.get(url, headers=headers)
            time.sleep(0.01)

    await ctx.reply("Done!")


if __name__ == "__main__":
    bot.run(TOKEN)

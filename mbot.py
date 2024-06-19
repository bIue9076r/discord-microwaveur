import json
import os.path
import discord

tok = str(open('tok.txt').read())

intents = discord.Intents.default()
intents.message_content = True
intents.emojis = True

client = discord.Client(intents=intents)

# global tables
prefixes = [
	"~","+","!",
	"=","$",
	"%","&",
	"-",":",
	".","?",
	"\\","/","]",
	"|","}"
]

def splitStr(s):
	ret = [""]
	o = ""
	index = 0
	literal = False
	escape = False
	
	for i in range(0,len(s)):
		if (s[i] == " " and not literal):
			if (o != ""):
				o = ""
				ret.append("")
				index = index + 1
		elif (s[i] == '\\' and not escape):
			escape = True
		elif (s[i] == '"' and not escape):
			literal = not literal
		else:
			o = o + s[i]
			ret[index] = o
			escape = False
	
	return ret;

def dictlog(d):
	print(json.dumps(d, indent=4))

async def b_help(message,args):
	await message.channel.send(
	"```txt\n"+
	"echo:    ~echo    ...\n"+
	"echok:   ~echok   ...\n"+
	"about:   ~about\n"+
	"```"
	)

async def b_help_d(message,args):
	await message.channel.send("comand in progress")
	await b_help(message,args)

async def b_echo(message,args):
	if (len(args) < 1):
		await message.channel.send("Usage: ~echo ...")
		return;
	p = ""
	for i in range(0,len(args)):
		p = p + args[i] + " "
	await message.channel.send(p)
	await message.delete()

async def b_echo_k(message,args):
	if (len(args) < 1):
		await message.channel.send("Usage: ~echo ...")
		return;
	p = ""
	for i in range(0,len(args)):
		p = p + args[i] + " "
	await message.channel.send(p)

async def b_about(message,args):
	await message.channel.send(
	f"```txt\n"+
	f"Version:   0.0\n"+
	f"Prefixes:  ~!=#$%&-.>?\n"+
	f"user:      {client.user}\n"+
	f"channel:   {message.channel.id}\n"+
	f"guild:     {message.guild.id}\n"+
	f"```"
	)

cmds = {
	"help":		b_help,
	"echo":		b_echo,
	"echok":	b_echo_k,
	"about":	b_about,
	"h":		b_help,
}

async def pmes(message):
	if (message.content[0] in prefixes):
		mtbl = splitStr(message.content[1:])
		comand = mtbl[0]	# string
		args = mtbl[1:]		# table
		
		if (comand in cmds):
			await cmds[comand](message,args)
		else:
			await message.channel.send(f"invalid command")

@client.event
async def on_ready():
	print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
	if (message.author == client.user):
		return;
	
	await pmes(message)

client.run(tok)

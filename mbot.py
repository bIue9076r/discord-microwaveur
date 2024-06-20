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

board = {
    "turns": 1,
    "board": [
        [0,0,0],
        [0,0,0],
        [0,0,0],
    ],
}

ntoe = {
    "1":    ":x:",
    "0":    ":black_large_square:",
    "-1":   ":o:",
}

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
    "ttt:     ~ttt\n"+
    "tttx:    ~tttx\n"+
    "ttto:    ~ttto\n"+
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
	f"Version:   1.0.1\n"+
	f"Prefixes:  ~+!=$%&-:.?\\\n"+
	f"user:      {client.user}\n"+
	f"channel:   {message.channel.id}\n"+
	f"guild:     {message.guild.id}\n"+
	f"```"
	)

async def b_ttt(message, args):
    await message.channel.send("New Board Created\ntttx to play as x\nttto to play as o\n")
    board["board"] = [
	    [0,0,0],
	    [0,0,0],
	    [0,0,0],
    ]
    board["turns"] = 1
    await message.channel.send(
        ntoe[str(board["board"][0][0])]+ntoe[str(board["board"][0][1])]+ntoe[str(board["board"][0][2])]+"\n"+
        ntoe[str(board["board"][1][0])]+ntoe[str(board["board"][1][1])]+ntoe[str(board["board"][1][2])]+"\n"+
        ntoe[str(board["board"][2][0])]+ntoe[str(board["board"][2][1])]+ntoe[str(board["board"][2][2])]
    )
    return 

async def b_tttx(message, args):
    # check colition and display board
    if len(args) > 2:
        await message.channel.send("What?")
        await message.channel.send("Usage: tttx [x] [y]")
        return

    if len(args[0]) > 1:
        await message.channel.send("Usage: tttx [x] [y]")
        return

    if len(args[1]) > 1:
        await message.channel.send("Usage: tttx [x] [y]")
        return

    if not args[0] in "123":
        await message.channel.send("Error [x] is not a valid number")
        return

    if not args[1] in "123":
        await message.channel.send("Error [y] is not a valid number")
        return

    ix = int(args[0]) - 1
    iy = int(args[1]) - 1

    if ix < 0 or ix > 2:
        await message.channel.send("Error [x] out of range")
        return

    if iy < 0 or iy > 2:
        await message.channel.send("Error [y] out of range")
        return

    if not board["board"][iy][ix] == 0:
        await message.channel.send("Slot Occupied")
        return

    board["board"][iy][ix] = 1
    board["turns"] = board["turns"] + 1
    await message.channel.send(
        ntoe[str(board["board"][0][0])]+ntoe[str(board["board"][0][1])]+ntoe[str(board["board"][0][2])]+"\n"+
        ntoe[str(board["board"][1][0])]+ntoe[str(board["board"][1][1])]+ntoe[str(board["board"][1][2])]+"\n"+
        ntoe[str(board["board"][2][0])]+ntoe[str(board["board"][2][1])]+ntoe[str(board["board"][2][2])]
    )
    if board["turns"] > 5:
        h1 = board["board"][0][0] + board["board"][0][1] + board["board"][0][2]
        h2 = board["board"][1][0] + board["board"][1][1] + board["board"][1][2]
        h3 = board["board"][2][0] + board["board"][2][1] + board["board"][2][2]

        v1 = board["board"][0][0] + board["board"][1][0] + board["board"][2][0]
        v2 = board["board"][0][1] + board["board"][1][1] + board["board"][2][1]
        v3 = board["board"][0][2] + board["board"][1][2] + board["board"][2][2]

        d1 = board["board"][0][0] + board["board"][1][1] + board["board"][2][2]
        d2 = board["board"][0][2] + board["board"][1][1] + board["board"][2][0]

        if (h1 == 3) or (h2 == 3) or (h3 == 3):
            await message.channel.send("X wins")
            return
        if (v1 == 3) or (v2 == 3) or (v3 == 3):
            await message.channel.send("X wins")
            return
        if (d1 == 3) or (d2 == 3):
            await message.channel.send("X wins")
            return
    return 

async def b_ttto(message, args):
    # check colition and display board
    if len(args) > 2:
        await message.channel.send("What?")
        await message.channel.send("Usage: ttto [x] [y]")
        return

    if len(args[0]) > 1:
        await message.channel.send("Usage: ttto [x] [y]")
        return

    if len(args[1]) > 1:
        await message.channel.send("Usage: ttto [x] [y]")
        return

    if not args[0] in "123":
        await message.channel.send("Error [x] is not a valid number")
        return

    if not args[1] in "123":
        await message.channel.send("Error [y] is not a valid number")
        return

    ix = int(args[0]) - 1
    iy = int(args[1]) - 1

    if ix < 0 or ix > 2:
        await message.channel.send("Error [x] out of range")
        return

    if iy < 0 or iy > 2:
        await message.channel.send("Error [y] out of range")
        return

    if not board["board"][iy][ix] == 0:
        await message.channel.send("Slot Occupied")
        return

    board["board"][iy][ix] = -1
    board["turns"] = board["turns"] + 1
    await message.channel.send(
        ntoe[str(board["board"][0][0])]+ntoe[str(board["board"][0][1])]+ntoe[str(board["board"][0][2])]+"\n"+
        ntoe[str(board["board"][1][0])]+ntoe[str(board["board"][1][1])]+ntoe[str(board["board"][1][2])]+"\n"+
        ntoe[str(board["board"][2][0])]+ntoe[str(board["board"][2][1])]+ntoe[str(board["board"][2][2])]
    )
    if board["turns"] > 5:
        h1 = board["board"][0][0] + board["board"][0][1] + board["board"][0][2]
        h2 = board["board"][1][0] + board["board"][1][1] + board["board"][1][2]
        h3 = board["board"][2][0] + board["board"][2][1] + board["board"][2][2]

        v1 = board["board"][0][0] + board["board"][1][0] + board["board"][2][0]
        v2 = board["board"][0][1] + board["board"][1][1] + board["board"][2][1]
        v3 = board["board"][0][2] + board["board"][1][2] + board["board"][2][2]

        d1 = board["board"][0][0] + board["board"][1][1] + board["board"][2][2]
        d2 = board["board"][0][2] + board["board"][1][1] + board["board"][2][0]

        if (h1 == -3) or (h2 == -3) or (h3 == -3):
            await message.channel.send("O wins")
            return
        if (v1 == -3) or (v2 == -3) or (v3 == -3):
            await message.channel.send("O wins")
            return
        if (d1 == -3) or (d2 == -3):
            await message.channel.send("O wins")
            return
    return 

cmds = {
	"help":		b_help,
	"echo":		b_echo,
	"echok":	b_echo_k,
	"about":	b_about,
    "ttt":      b_ttt,
    "tttx":     b_tttx,
    "ttto":     b_ttto,
	"h":		b_help,
    "e":        b_echo,
    "t":        b_ttt,
    "tx":       b_tttx,
    "to":       b_ttto,
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

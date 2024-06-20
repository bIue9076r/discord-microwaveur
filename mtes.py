import json
import os.path

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

def echo(m,a):
    print(a)
    return

def ttt(m,a):
	print("New Board Created\ntttx to play as x\nttto to play as o\n")
	board["board"] = [
		[0,0,0],
		[0,0,0],
		[0,0,0],
	]
	board["turns"] = 1
	print(board["board"])

def tttx(m,a):
	print(a)
	# check colition and display board
	if len(a) > 2:
		print("what?")
		return
	
	if len(a[0]) > 1:
		print("what? first")
		return
	
	if len(a[1]) > 1:
		print("what? second")
		return
	
	if not a[0] in "0123456789":
		print("what? not a number")
		return
	
	if not a[1] in "0123456789":
		print("what? not a number 2")
		return
	
	if (int(a[0]) - 1) < 0 or (int(a[0]) - 1) > 2:
		print("what? out of range")
		return
	
	if (int(a[1]) - 1) < 0 or (int(a[1]) - 1) > 2:
		print("what? out of range 2")
		return
	
	if not board["board"][(int(a[1]) - 1)][(int(a[0]) - 1)] == 0:
		print("Occupied")
		return
	
	board["board"][(int(a[1]) - 1)][(int(a[0]) - 1)] = 1
	board["turns"] = board["turns"] + 1
	print(board["board"])
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
			print("Player X wins")
			return
		if (v1 == 3) or (v2 == 3) or (v3 == 3):
			print("Player X wins")
			return
		if (d1 == 3) or (d2 == 3):
			print("Player X wins")
			return
	return

def ttto(m,a):
	print(a)
	# check colition and display board
	if len(a) > 2:
		print("what?")
		return
	
	if len(a[0]) > 1:
		print("what? first")
		return
	
	if len(a[1]) > 1:
		print("what? second")
		return
	
	if not a[0] in "0123456789":
		print("what? not a number")
		return
	
	if not a[1] in "0123456789":
		print("what? not a number 2")
		return
	
	if (int(a[0]) - 1) < 0 or (int(a[0]) - 1) > 2:
		print("what? out of range")
		return
	
	if (int(a[1]) - 1) < 0 or (int(a[1]) - 1) > 2:
		print("what? out of range 2")
		return
	
	if not board["board"][(int(a[1]) - 1)][(int(a[0]) - 1)] == 0:
		print("Occupied")
		return
	
	board["board"][(int(a[1]) - 1)][(int(a[0]) - 1)] = -1
	board["turns"] = board["turns"] + 1
	print(board["board"])
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
			print("Player X wins")
			return
		if (v1 == -3) or (v2 == -3) or (v3 == -3):
			print("Player X wins")
			return
		if (d1 == -3) or (d2 == -3):
			print("Player X wins")
			return
	return

cmds = {
        "echo":echo,
        "ttt":ttt,
        "tttx":tttx,
        "ttto":ttto,
}

def pmes(message):
        if (message[0] in prefixes):
                mtbl = splitStr(message[1:])
                comand = mtbl[0]        # string
                args = mtbl[1:]         # table
				
                if (comand in cmds):
                        cmds[comand](message,args)
                else:
                        print(f"invalid command")

pmes("!echo hello world")
pmes("!ttt")
pmes("!tttx 1 1")
pmes("!ttto 2 2")
pmes("!tttx 2 2")
pmes("!tttx 1 3")
pmes("!ttto 2 1")
pmes("!tttx 1 2")
pmes("!ttt")

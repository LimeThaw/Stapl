#!/usr/bin/env python3

import sys
import re
from errors import *
import os
import subprocess

output = "\
#include <cstdlib>\n\
#include <stdio.h>\n\
#include <iostream>\n\
#include <math.h>\n\
#include \"stack.cpp\"\n\
#include <map>\n\
#include <string>\n\
#include <random>\n\
#include <time.h>\n\
using namespace std;\n\
stack<long double> main_stack;\n\
map<string, long double> vars;\n\
\n\
int main(){\n\
long double ret = 0.0;\n\
long double tmp = 0.0;\n\
int tmpi = 0;\n\
string tmps = \"\";\n\
srand(time(NULL));\n\
"

if len(sys.argv) < 2:
	raise InputError("Please specify a source file")

instructions = re.split(" |\t|\n", open(sys.argv[1]).read())

# The variables defined in the program - don't try to get anything not in here.
variables = []
stacks = []

rip = 0
tmp = []
while rip < len(instructions):
	inst = instructions[rip]

	if inst == "": # Ignore whitespaces
		pass
	elif inst[0] == '%': # Ignore comments
		if inst == "%":
			rip += 1
		while instructions[rip][-1] != '%' and rip < len(instructions):
			rip += 1
	else:
		tmp.append(inst)
	rip += 1
instructions = tmp

for rip in range(len(instructions)):
	if instructions[rip] == "stack":
		name = instructions[rip+1]
		output += "stack<long double> " + name + ";\n"
		stacks.append(name)

rip = 0
while rip < len(instructions):
	inst = instructions[rip]

	if inst == "add": # Arithmetic functions
		output += "main_stack.push(main_stack.pop() + main_stack.pop());\n"
	elif inst == "sub":
		output += "\
			tmp = -main_stack.pop();\n\
			main_stack.push(main_stack.pop() + tmp);\n\
			"
	elif inst == "mul":
		output += "main_stack.push(main_stack.pop() * main_stack.pop());\n"
	elif inst == "div":
		output += "main_stack.push((1.0/main_stack.pop()) * main_stack.pop());\n"
	elif inst == "mod":
		output += "main_stack.push(fmod(main_stack.pop(), main_stack.pop()));\n"

	elif inst == "push": # stack operations
		expr = instructions[rip + 1]
		if expr[0] == '"':
			string = expr
			i = rip + 2
			while string[-1] != '"' and i < len(instructions):
				string = string + " " + instructions[i]
				i += 1
			rip = i - 2
			string = string[-2:0:-1]
			output += "main_stack.push(0.0);\n"
			for c in string:
				tmp = str(float(ord(c)))
				output += "main_stack.push(" + tmp + ");\n"
		else:
			output += "main_stack.push(" + expr + ");\n"
		rip += 1
	elif inst == "pop":
		output += "main_stack.pop();\n"
	elif inst == "pops":
		output += "\
			do {\n\
				tmp = main_stack.pop();\n\
			} while (tmp != 0.0);\n\
		"
	elif inst == "cpy":
		output += "tmp = main_stack.pop(); main_stack.push(tmp); main_stack.push(tmp);\n"
	elif inst == "stof":
		output += "\
			tmpi = (int) main_stack.pop();\n\
			tmp = 0;\n\
			while(tmpi != 0) {\n\
				tmp = 10*tmp + (tmpi - 48);\n\
				tmpi = (int) main_stack.pop();\n\
			}\n\
			main_stack.push(tmp);\n\
		"
	elif inst == "rand":
		output += "main_stack.push(((double)rand()) / RAND_MAX);\n"

	elif inst == "fun": # Function calls
		output += instructions[rip+1] + ":\n"
		rip += 1
	elif inst == "call":
		output += "goto " + instructions[rip+1] + ";\n"
		rip += 1

	elif inst == "if": # Control
		mode = instructions[rip+1]
		if mode != "eq" and mode != "lt" and mode != "gt" and mode != "empty":
			raise ArgumentError("Invalid if comparison mode \"" + mode + "\"")
		if mode == "empty":
			output += "if(main_stack.length() == 0) {\n"
		else:
			op = {
				"eq": "==",
				"lt": ">", # Operators reverted because of argument order on the stack
				"gt": "<",
			}.get(mode)
			output += "if(main_stack.end()[-1] " + op + " main_stack.end()[-2]) {\n"
	elif inst == "end":
		output += "}\n"
	elif inst == "ret":
		output += "\
			ret = main_stack.length() > 0 ? main_stack.pop() : 0;\n\
			printf(\"Program returned with value %Lf.\\n\", ret);\n\
			exit(ret);\n\
		"

	elif inst == "set": # Storage
		name = instructions[rip+1]
		if not name in variables:
			variables.append(name)
		output += "vars[\"" + name + "\"] = main_stack.pop();\n"
		rip += 1
	elif inst == "get":
		name = instructions[rip+1]
		if not name in variables:
			raise UnknownLabelError("Unknown variable name \"" + instructions[rip+1] + "\"")
		output += "main_stack.push(vars[\"" + name + "\"]);\n"
		rip += 1
	elif inst == "store":
		name = instructions[rip+1]
		if not name in stacks:
			raise UnknownLabelError("Unknown stack name \"" + name + "\" - Please declare all stacks before usage.")
		output += name + ".push(main_stack.pop());\n"
	elif inst == "load":
		name = instructions[rip+1]
		if not name in stacks:
			raise UnknownLabelError("Unknown stack name \"" + name + "\" - Please declare all stacks before usage.")
		output += "main_stack.push(" + name + ".pop());\n"
	elif inst == "size":
		name = instructions[rip+1]
		if not name in stacks:
			raise UnknownLabelError("Unknown stack name \"" + name + "\" - Please declare all stacks before usage.")
		output += "main_stack.push(" + name + ".length());\n"


	elif inst == "print": # Interaction
		output += "printf(\"%Lf\\n\", main_stack.peek());\n"
	elif inst == "prints":
		output += "\
			for(vector<long double>::iterator it = main_stack.end()-1; it >= main_stack.begin(); it--) {\n\
				if(*it == 0.0) break;\n\
				printf(\"%c\", (char)(int) *it);\n\
			}\n\
			printf(\"\\n\");\n\
		"
	elif inst == "printstack":
		output += "\
			for(vector<long double>::iterator it = main_stack.begin(); it < main_stack.end(); ++it) {\n\
				printf(\"%Lf\\n\", *it);\n\
			}\n\
		"
	elif inst == "read":
		output += "\
			getline(cin, tmps);\n\
			main_stack.push(0.0);\n\
			for(string::iterator it = tmps.end()-1; it >= tmps.begin(); it--){\n\
				main_stack.push((long double)(int) *it);\n\
			}\n\
		"

	else: # What is that brah? Like, honestly, are you foreal right now?
		pass
		#raise UnknownInstructionError("Instruction \"" + inst + "\" is unknown")

	rip += 1 # Next instruction please

output += "}"
with open("out.cpp", "w") as f:
	f.write(output)

msg = subprocess.check_output(["g++", "out.cpp", "--std=c++11"]+sys.argv[2:])
print("Compiled successfully.")
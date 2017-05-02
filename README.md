# Stapl - A **STA**ck based **P**rogramming **L**anguage

This is the official documentation and specification for a little language I invented called
Stapl. As the name suggests, the concept of a [stack][link_stack] is the basis for (almost) all operations.
Each program has a main stack, on which all operations are carried out. The stack contains
only floating point numbers, which are internally represented as [long double][link_long_double] values. The
compiler translates the source into [C++][link_c++] code and calls [gcc][link_gcc] to compile it into an
executable.


## Stack operations

The basics on manipulating the main stack.

- push

	Must be followed by a value. If the value is a number (any number representable as a double),
	then it will be pushed to the top of the main stack. If it is a string (surrounded by quotes),
	the ascii values for each letter will be pushed on the stack followed by a zero, so all strings
	are represented on the stack as zero-terminated number sequences.

	  push 3.141593

	  push "hello, world."

- pop

	Removes the value on top of the stack.

- pops (pop string)

	Removes numbers from the top of the stack until it reaches a zero. If a string has been pushed,
	it will be removed by this command.

	  push "hello, world."

	  pops

- cpy (copy)

 	Duplicates the value on top of the stack. The stack will be one entry larger and the top two
	entries will be the same.

	  push 42

	  cpy

- stof (string to float)

	Reads a string from the top of the stack by reading numbers until it encounters a zero and
	converting them to characters, and then converts the string to a floating point number it
	pushes on top of the stack.

	  push "3.141593"

	  stof

- rand (random)

	Pushes a random number between 0 and 1 on top of the stack.


## Arithmetic

Basic mathematic functions.

- add

	Pops two numbers from the stack, adds them together and pushes the result.

- sub (subtract)

	Subtracts the number last pushed to the stack from the one pushed before. Then removes those
	numbers from the stack and pushes the result.

- mul (multiply)

	Pops two numbers from the stack, multiplies them together and pushes the result.

- div (divide)

	Divides the number second from the top through that on top of the stack. Then removes those
	numbers from the stack and pushes the result.

- mod (modulo)

	Pushes the second to last push modulo the last push to the stack after popping those numbers.


## Comments

Now that you can write some basic code it is time to tell you how to document it properly.
Comments are delimited by the character %. Make sure you have whitespace characters immediately
before the first and after the last %.

	push 3.141593 % Push PI to the stack %
	pop %And delete it again%
	push "WOW" %WOW%
	% Now that's what i call code brah! %


## Function calls

Haters will tell you it is just a simple goto, but this feature is, in fact, the most advanced
function calling system in the industry. Use at own risk!

- fun *name* (function)

	Marks the begin of the function with the given *name*. The details are incredibly complicated,
	but you can use it just like a label in c like languages or assembly.

	  fun myfunction

	      push "This is my function."

- call *name*

	Executes the function with the given *name*. Our engineers have worked hard on this, and it is
	not only brilliant but also simple to use: Just pretend it is a simple goto instruction.

	  call myfunction


## Program flow

A few functions to give you control over your program flow. I guess technically the function calls
would belong in here... Oh well.

- if *cond* [...] end

	A classic if struct. *cond* must be *eq*, *gt*, *lt* or *empty*. If the condition is true, the
	code in [...] will be executed. Otherwise execution resumes at *end*. With a1 being the second
	to last number on the stack and a2 being the last, the conditions are:<br/>
	*eq*: a1 == a2<br/>
	*lt*: a1 < a2<br/>
	*gt*: a1 > a2<br/>
	*empty*: The stack is currently empty

	  push 3
	  push 4

	  if gt

		push "3 > 4"

	  end

- ret (return)

	Exits the program and returns the top value of the stack.


## Storage

Now this is where things get interesting. These function allow you to store values outside of the
stack. This allows for a lot of programs and techniques that would be hard or impossible to
implement with only a single stack.

- set *var*

	This sets the vale of the variable *var* to the value stored on top of the stack and pops once.
	The variable does not have to be declared before assignment. If the variable held a value
	before, it will be overwritten.

- get *var*

	Pushes the value of the variable *var* on top of the stack. *var* must be *set* before.

	<!-- Separator -->

	push 3
	set var
	get var

- stack *name*

	Creates an extra stack with the given *name*. You can make as many of them as you want. These
	stacks can hold multiple values (up to the size limit for stacks), but no operations can be
	performed on them.

- store *name*

	Pops the top from the main stack and pushes the value to the storage stack with the given
	*name*. The stack must be initialized somewhere in the code.

- load *name*

	Pops the top from the storage stack with the given *name* and pushes it to the mains stack -
	basically the inversion of *store*. Again, the stack must be initialized somewhere in the code.

- size *name*

	Pushes the length of the given storage stack to the main stack. Blah, blah, initialize, blah.

	<!-- Separator -->

	stack mystack

	push 1
	push 2

	store mystack
	store mystack
	load mystack
	size mystack

	if eq
		push "Now only 2 is in mystack."
	end


## Interaction

Now non-interactive programs are fine, but kind of boring. Let's spice it up with some cool
features!

- print

	Prints the value on top of the stack.

- prints (print string)

	Reads from the stack until it reaches a zero, converts the values to characters and prints
	the resulting string.

- printstack

	Goes through the entire stack (bottom to top) and prints all values.

- read

	Reads a string from the standard input and pushes it to the main stack in zero-terminated
	form (just like *push* with a string).

	<!-- Separator -->

	push "Please input a number: "
	prints
	pops

	read
	stof

	push "Your number is: "
	prints
	pops

	print

  	<!-- Separator -->

	push "What's your name?"
	prints
	pops

	read

	push "Hello "
	pops
	prints


## Building

Okay, so that's the core language. To test it you can write some code and compile it using my little
compiler. I have cheated a little bit: The compiler just converts the program to C++ and has
[gcc][link_gcc] do the rest. To use it for compiling test.stapl within the directory of the compiler, open
a terminal, navigate to the relevant folder and type:

	./staplc.py test.stapl

You can also use some [options][link_options]. All options will be relayed to gcc. The intermediate
C++ code is saved in the file out.cpp. You can have a look at it if you are interested or having
trouble compiling your code.

## Misc

I also included some example codes. root.stapl takes a number and computes its square root,
sort.stapl generates an array of random numbers and sorts it, euklid.stapl takes two numbers and
uses the euklidean algorithm to find their greatest common divisor, and primes.stapl takes an upper
bound and lists all prime numbers smaller than this bound.

If you have any further questions message me or shoot me an email to laudit@student.ethz.ch.


[link_stack]: https://en.wikipedia.org/wiki/Stack_(abstract_data_type)
[link_gcc]: https://gcc.gnu.org/
[link_options]: https://gcc.gnu.org/onlinedocs/gcc/Invoking-GCC.html
[link_c++]: https://en.wikipedia.org/wiki/C%2B%2B
[link_long_double]: http://www.cplusplus.com/doc/tutorial/variables/
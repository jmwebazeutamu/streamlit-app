import json
from pathlib import Path

cells = []

def md(text):
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in text.strip("\n").split("\n")],
    })

def code(src):
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in src.strip("\n").split("\n")],
    })

md('''
# Module 6 Notebook: Python Functions (Review + Practice)

This notebook was developed from: **Module_6_Python_Functions_Reusable_Code_Guide.pdf**.

## PDF review highlights
- Clear progression from function basics to advanced argument passing.
- Strong emphasis on scope, return values, and common mistakes.
- Repeated `Try It` prompts are good for quick checks.
- A few slide text artifacts/typos exist (for example stray symbols), but concept flow is solid.

Use this notebook in order: **read text cells -> run examples -> attempt exercises -> complete debugging tasks**.
''')

md('''
## 1) What is a function?

A function is a named, reusable block of code that performs a specific task.

Why functions matter:
- **Modularity**: break complex programs into smaller parts.
- **Reuse**: write once, call many times.
- **Readability**: code becomes easier to understand and maintain.
''')

code('''
# Example: built-in function usage
print("Hello, World!")
print(len("function"))
''')

md('''
### Exercise 1
Write your own function named `say_hi()` that prints `Hi there!`, then call it twice.
''')

code('''
# Exercise 1 - your code
# TODO: define say_hi()

# TODO: call it twice
''')

md('''
### Debugging 1 (Syntax)
The code below contains syntax issues similar to the ones discussed in the PDF.
Fix it so it runs.
''')

code('''
# Debugging 1
# Fix: missing parentheses, colon, and indentation

def start_engine
print("Vroom!")
''')

md('''
## 2) Function definition syntax

Pattern:
```python
def function_name(parameters):
    "Optional docstring"
    # indented body
```

Key points:
- Use `def` keyword.
- Use snake_case function names.
- Include parentheses and a trailing colon.
- Indent body consistently (typically 4 spaces).
''')

code('''
# Example: valid function definition with docstring

def say_hello():
    """Prints a friendly greeting."""
    print("Hello there!")

say_hello()
''')

md('''
### Exercise 2
Create a function `favorite_game(game)` that prints: `My favorite game is <game>.`
Call it with at least two different games.
''')

code('''
# Exercise 2 - your code
''')

md('''
### Debugging 2 (Order of execution)
Fix this `NameError` by arranging lines correctly.
''')

code('''
# Debugging 2
# Problem: function is called before it is defined

greet()

def greet():
    print("Welcome!")
''')

md('''
## 3) Control flow and function calls

Execution model:
1. Main program runs top-to-bottom.
2. When a function is called, control jumps to the function definition.
3. Function body executes.
4. Control returns to the line after the call.
''')

code('''
# Example: observe order of output

def say_hello():
    print("Hi")

print("Start")
say_hello()
print("End")
''')

md('''
### Exercise 3
Predict the output before running:
1. `First`
2. `Inside`
3. `Last`

Then run to verify.
''')

code('''
def inside():
    print("Inside")

print("First")
inside()
print("Last")
''')

md('''
## 4) Scope: local vs global variables

- **Local variable**: created inside a function; exists only while that function runs.
- **Global variable**: created outside functions; visible broadly.
- To modify a global inside a function, use `global` (use sparingly).
''')

code('''
# Example: local scope

def set_score():
    score = 100
    print("Inside function:", score)

set_score()
# print(score)  # Uncomment to see NameError
''')

code('''
# Example: global modification

total = 0

def add_point():
    global total
    total = total + 1

add_point()
print("Total:", total)
''')

md('''
### Exercise 4
1. Create a global variable `visits = 0`.
2. Write `record_visit()` to increment it.
3. Call it three times and print the final count.
''')

code('''
# Exercise 4 - your code
''')

md('''
### Debugging 3 (Scope)
The code tries to modify a global variable but fails.
Fix it.
''')

code('''
# Debugging 3
counter = 0

def increment():
    counter = counter + 1

increment()
print(counter)
''')

md('''
## 5) Parameters vs arguments

- **Parameter**: variable name in function definition.
- **Argument**: actual value passed when calling the function.
''')

code('''
# Example

def greet(name):  # name is a parameter
    print("Hello,", name)

greet("Alice")  # "Alice" is an argument
''')

md('''
### Exercise 5
Define `square(n)` and return `n * n`. Call it with `2`, `5`, and `10`.
''')

code('''
# Exercise 5 - your code
''')

md('''
## 6) Mutability and function arguments

Python passes references to objects:
- Immutable types (`int`, `str`, `tuple`) cannot be changed in place.
- Mutable types (`list`, `dict`, `set`) can be changed in place.
''')

code('''
# Example: mutable list changes outside function

def modify_list(items):
    items[0] = 99

numbers = [1, 2, 3]
modify_list(numbers)
print(numbers)  # [99, 2, 3]
''')

code('''
# Example: immutable string behavior

def try_change(text):
    text = "Changed"

word = "Original"
try_change(word)
print(word)  # still "Original"
''')

md('''
### Exercise 6
Write a function `append_item(lst, value)` that appends `value` to `lst`.
Test it with an empty list.
''')

code('''
# Exercise 6 - your code
''')

md('''
## 7) Return values

- `return` sends a value back to the caller and ends the function.
- If no `return` is used, Python returns `None`.
''')

code('''
# Example: explicit return

def add(x, y):
    return x + y

sum_val = add(5, 3)
print(sum_val)
''')

code('''
# Example: implicit None

def announce(msg):
    print(msg)

result = announce("Hi")
print("Returned:", result)
''')

md('''
### Exercise 7
Define `circle_area(radius)` and return area using `3.14159 * radius * radius`.
Call it for `radius = 2` and `radius = 4.5`.
''')

code('''
# Exercise 7 - your code
''')

md('''
### Debugging 4 (Missing return)
The function calculates a value but returns `None`. Fix it.
''')

code('''
# Debugging 4

def multiply(a, b):
    product = a * b

answer = multiply(3, 4)
print(answer)
''')

md('''
## 8) Positional, keyword, and default arguments

- Positional arguments match by position.
- Keyword arguments match by parameter name.
- Default values are used when an argument is omitted.
- Positional arguments must come before keyword arguments.
''')

code('''
# Example: positional + keyword + default

def describe_pet(animal, name, mood="happy"):
    print(f"I have a {animal} named {name} who is {mood}.")

describe_pet("hamster", "Harry")
describe_pet(name="Milo", animal="cat", mood="sleepy")
''')

md('''
### Exercise 8
Call this function in three ways:
1. Positional only
2. Keyword only
3. Mixed positional + keyword (valid order)
''')

code('''
def calc_total(price, tax=0.06):
    return price * (1 + tax)

# Exercise 8 - your calls
''')

md('''
### Debugging 5 (Argument order)
Fix the invalid call.
''')

code('''
# Debugging 5

def greet(name, msg="Hello"):
    print(msg, name)

greet(msg="Hi", "Bob")
''')

md('''
## 9) Final challenge: mini refactor + debugging

Goal: remove repetition with functions and fix hidden bugs.

Tasks:
1. Run the cell and observe errors/unexpected behavior.
2. Refactor repeated print logic into functions.
3. Correct scope and return issues.
4. Add one test call that demonstrates correct output.
''')

code('''
# Final Challenge
points = 0

# repeated behavior blocks (refactor these into functions)
print("Player A scored")
points = points + 1
print("Player A scored")
points = points + 1


def bonus_round():
    points = points + 5   # bug: scope


def report_total():
    total = points
    # bug: missing return

bonus_round()
final_score = report_total()
print("Final score:", final_score)
''')

nb = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {
            "name": "python",
            "version": "3.x",
        },
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

out = Path('/Users/johnsonmwebaze/Documents/codex/output/notebooks/module_6_functions_review_workbook.ipynb')
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(nb, indent=2), encoding='utf-8')
print(out)

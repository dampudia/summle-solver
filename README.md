# Summle Solver

This is a tree-based approach to solve [Summle] (https://summle.net/) . A very similar challenge was part of a popular Spanish game show called "Cifras y Letras" that was broadcast some years ago.

The scripts generates and grows a set of binary trees where each node represent a basic arithmetic operation or a number. The search stops when a set of operations returning the target is found.

## Usage

The script receives two parameters, the target number and a set of numbers (separated by commas) to reach the target using the four basic arithmetic operators.

For example, if the target is 649 and the set of numbers is [1, 1, 2, 10, 12, 100], you can execute the script with

`python summel-solver.py 649 1,1,2,10,12,100`

and, after a while, it will return the solution, if it exists:

`solution:((((1+12)*100)/2)-1)`

This script uses a brute-force approach, so it is not very efficient, but it is guaranteed to return the result with the minimum of arithmetic operations (i.e. if there is a solution with four operators and another with five, it will return the four one).


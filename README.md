# OOP_Ex4
![image](https://github.com/ChenLipschitz/OOP_Ex4/blob/main/logo.jpg)


This project presents the final assignment for the OOP course (CS.Ariel 2021).
In this assignment we designed a “Pokémon game” in which given a weighted graph, a set of “Agents” should be located on it so they could “catch” as many “Pokémon” as possible.
The pokémons are located on the graph’s (directed) edges, therefore, the agent needs to take (aka walk) the proper edge to “grab” the pokémon. The goal is to maximize the overall sum of weights of the “grabbed” pokémons.

## Classes:
* Node - Represents the graph's vertices
* Edge - Represents the graph's edges
* DiGraph - Represents the graph
* GraphAlgo - Algorithems that can be execute on the graph
* TestGraph - Test class
* GraphInterface - An abstract class which represents an interface of a graph
* GraphAlgoInterface - An abstract class which represents an interface of a graph
* Client - Represents the server
* Student_code - Represents the GUI class
* Button - Represents the buttons on the screen
* Pokémon - Represents the pokémons
* Agent - Represents the players
* Main - Represents the main class

## How To Run:
Download the project.
Open the projectm, in the terminal command write the following line:

java -jar Ex4_Server_v0.0.jar 2

Notaion: for the example, 2 is the number of the case. There are [0-15] cases.

![image](https://github.com/ChenLipschitz/OOP_Ex4/blob/main/Screenshot%202022-01-09%20145046.png)

## UML
![image](https://github.com/ChenLipschitz/OOP_Ex4/blob/main/UMLScreenshot%202022-01-09%20151330.png)

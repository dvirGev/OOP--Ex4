
# OOP--Ex4
# POKEMON GAME – PYTHON
![image](https://user-images.githubusercontent.com/92378800/148260320-c740a7f5-ddf1-498e-bd29-94911c4e2d84.png)

![image](https://user-images.githubusercontent.com/92378800/148351388-344d199a-f285-49c2-b19f-62b6376ef919.png)


## Written by Dvir Biton , Dvir Gev and Danielle Musai.

## PROJECT EXPLANATION

In this assignment  we were asked to create a Pokemons Game in which given a weighted graph, a set of “Agents” that located on it so they could “catch” as many “Pokemons” as possible.
An important detail is that every pokemon has a different value of points  and we need to collect as many points as possible .
The pokemons are located on the graph’s (directed) edges, therefore, the agent needs to take (aka walk) the proper edge to “grab” the pokemon .
As we can see we are given a specific and limited time and moves ,clearly the moves are dependents on the distance of the pokemons from the agents.(edges and weights).
Our mission is to maximize the overall sum of weights of the “grabbed” pokemons.

---
## classes

### 1.DiGraph - 
            contains dictionary of all the nodes in the graph(Node) and all the edges() and the mc(changing in the graph).

### 2.GraphAlgo - this class get DiGraph and can calculate the next list of algorithms:

             * A shorted path between 2 verticals.
             * The ideal center of the graph.
             * Tsp problem for a group of verticals in the graph
             * load graph from json file.
             * save the graph to new json file.
             * plot the graph(crate visual display of the graph(GUI)).

### 3.Node - this class save information about each vertical:

             * its exclusive id.
             * location information.
             * tag(using for the algorithms).
             * dictionary for all the edges from this node to another.
             * dictionary for all the edges that getting to this node.

### 4.gameAlgo- this class is charge of the game algorithm and the cmd

            * update the details about the agents and Pokemons in the graph
            * pokemon_src_dest-calculate which edge the pokemon standes(src, dest).
            * isEdge-return if their are edge between src and dest
            * distanceNodes-calculate the distance between two verticals.
            * distancePokNode-  calculate the distance between pokemon and verticals.
            * calc- calculate the distance between the agent and the pokemon.
            * allocateAgen-  alloctae for every agent match pokemon.
            * allocateAllagent- for every agent call to allocateAgen func.
            * CMD
            * the shortest path between 2 verticals using Dijkstra's Algorithm.

### 5.client-*start connection

           * send messege- to start a new connection to the game server
           * get agents
           * adding an agent
           * getting a graph
           * get info- the current game information
           * get the current pokemon state.
           * running the project - check if the game still running.
           * time to end in mili-sec.
           * starting the game 
           * move
           * choose next edge means choosing the next destination for a specific agent.
           * login
           * stop connection

### 6.classes include: 

          * agent & pokemon


## GUI
This classes generate a windows that show the game.

We have the exit and music buttoms also a results of the moves ,time and grade. 


![image](https://user-images.githubusercontent.com/92378800/148246637-1c7fe8ac-5531-4a0b-8d05-651b6a56c333.png)

----

## Algorithms

The algorithm is very simple.
After all, the goal of the game is to maximize the overall sum of weights of the "grabbed" pokemons.
The solution is simple. To each agent we match Pokemon without saving anything and as soon as we find a match between the two of them we send to the next station.
The main advantage is that it is very dynamic, which means that if a Pokemon is created close to it, the agent simply changes the route again to catch the same Pokemon.


---

## UML

![image](https://user-images.githubusercontent.com/92378800/148247697-b445d322-1915-443b-a8a2-eecd0fc4496c.png)

----
## Algorithms Results
you can see the results in our wiki
https://github.com/dvirGev/OOP--Ex4/wiki

----
## How to run the project
Open the floder of the project and write this line in the terminal command:

* python codes./Ex4.py 11(11 is one of the cases)

![image](https://user-images.githubusercontent.com/92378800/148261828-9a3d3395-09b4-4c0e-a500-e3ff06c1ad0c.png)




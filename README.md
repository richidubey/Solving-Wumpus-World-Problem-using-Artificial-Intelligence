# Solving-Wumpus-World-Problem-using-Artificial-Intelligence
A program that simulates an agent's behaviour in a wumpus world that has exactly one wumpus and one pit. The rules regarding wumpus and pit can be changed in run.py and the world can be changed in agent.py.

The figure below shows a Wumpus world containing one pit and one Wumpus. 

![World Image](https://github.com/richidubey/Solving-Wumpus-World-Problem-using-Artificial-Intelligence/blob/master/world.png?raw=true)

There is an agent in room [1,1]. The goal of the agent is to exit the Wumpus world alive. The agent can exit the Wumpus world by reaching room [4,4].  
--- 
## Rules:  
The wumpus world contains exactly one Wumpus and one pit.  
There will be a breeze in the rooms adjacent to the pit, and there will be a stench in the rooms adjacent to Wumpus.  
The logical agent can take four actions: Up, Down, Left and Right. These actions help the agent move from one room to an adjacent room.   
The agent can perceive two things: Breeze and Stench.
--- 
run.py is a python program that uses propositional logic sentences to check which rooms are safe. The inference is drawn using the DPLL algorithm. 
--- 
   
   
## Assumptions:  
Assume that there will always be a safe path that the agent can take to exit the Wumpus world.  
   
   
---
DPLL ALgorithm from : Artificial Intelligence A Modern Approach Third Edition by Stuart Russell and Peter Norvig.

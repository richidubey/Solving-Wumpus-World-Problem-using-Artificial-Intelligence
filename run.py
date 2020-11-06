#!/usr/bin/env python3
from Agent import * # See the Agent.py file
import copy

#### All your code can go here.

#### You can change the main function as you wish. Run this program to see the output. Also see Agent.py code.


# Player position denoted by :
#
# 12 , 22 , 32 , 42
# 11 , 21 , 31 , 41

# Breeze by 111
# Stench by 211
# Pit by 311
# Wumpus by 411.
#Goal is to reach 44, or to make 44 true = a part of our model.
 
#Returns false if any clause is false or not determined(ambiguous)	

TotalCount=0	
def checkEveryClauseTrue(clauses, model):

	if(len(clauses)==0):
		return True;		#Empty clauses means all the clauses have atleast one positive literal.
	count=0;
	
	for clause in clauses:
		for literal in clause:
			if( literal in model ):
				count=count+1;
				break;
				
	if( count == len(clauses)):
		return True;
	
	return False;

#Returns True if any clause is false and False if none of the clause is trully false	
	
def checkAnyFalseClause(clauses, model):
	for clause in clauses:
		if(len(clause)==0):
			return True;		#Empty clause means all the literals have been negated.
		for literal in clause:
			if( literal in model ):
				break;
	
		fcount=0;
		
		for literal in clause:		#By previous check, if no true literal lies in model
			if( -1*literal in model ):	#So,existence of negation of all false literal means the clause is false 
				fcount=fcount+1;
		
		if(fcount == len(clause)):
			return True;
		
	return False;
	
	
def FindPureSymbol(clauses,symbols, model):

	for literal in symbols:
		count = 0;
		
		for clause in clauses:
			if( (literal in clause) or ( (-1*literal) not in clause)):
				count = count+1;
			
			else:
				break;
				
		if (count == len(clauses)):
			return literal;
	
	#Check for negation of each literal:
	
	for literal in symbols:
		count = 0;
		
		nliteral = -1*literal
		
		for clause in clauses:
			if( (nliteral in clause) or ( (-1*nliteral) not in clause)):
				count = count+1;
			
			else:
				break;
				
		if (count == len(clauses)):
			return nliteral;
			
	#Neither symbols nor negation of symbols present as pure. Return 0
	return 0;  

def FindUnitClause(clauses, model):
	for clause in clauses:
		
		if (len(clause) == 1) and ((clause[0] not in model) and ((-1*clause[0]) not in model)):	#If no valuation is present for the literal in the model, then it is a unit clause
			return clause[0]
		
		#Check if all literal but one already assigned false
		newclause= copy.deepcopy(clause)
		
		for literal in clause:
			if(-1 * literal in model ): 	
				newclause.remove(literal)	 
		
		if( (len(newclause)==1) and  ( (newclause[0] not in model) and ( (-1*newclause[0]) not in model ) ) ):			#Check if all literal but one already assigned false
			return newclause[0]
				
	return 0;
	
def DPLL(clauses, symbols, model):
	global TotalCount
	TotalCount=TotalCount+1;
#	print("Current model: ",model," and symbols: ",symbols)
	if( checkEveryClauseTrue( clauses, model ) ):	#if(every clause in clauses is true in model):
		return True;
	
	if( checkAnyFalseClause( clauses, model ) ):					#if(some clause in clauses is false in model):
		return False; #TODO: Check if this is correct. Check the order of True and False properly.
	
	#print("Hi there")
	
	#P,value <- FIND-PURE-SYMBOL(symbols,clauses,model)
	#if P is non-null then return DPLL(clauses, symbols - P, model U {P=value} )
	
	Pure = FindPureSymbol(clauses,symbols, model) #P,value <- FIND-UNIT-CLAUSE(clauses,model)
	if(Pure != 0 ):
		#print(" Yay ")
		
		symbols.remove(abs(Pure))
		model.append(Pure)
		#Remove all the clauses that have this literal.
		
		for clause in clauses:
			if(Pure in clause):
				clauses.remove(clause)
				
				 
		return DPLL(clauses, symbols, model) 		#  if P is non-null then return DPLL(clauses, symbols - P, model U {P=value} )
		
	Unit = FindUnitClause(clauses, model) #P,value <- FIND-UNIT-CLAUSE(clauses,model)
	if(Unit != 0 ):
	#	print("Found Unit symbol: ",Unit)
	#	print("And current symbols are: ", symbols)
	#	print("And current model is: ", model)
		
		symbols.remove(abs(Unit))
		model.append(Unit)
		#Remove all the clauses that have this literal.
		
		for clause in clauses:
			if(Unit in clause):
				clauses.remove(clause)
				
				 
		return DPLL(clauses, symbols, model) 		#  if P is non-null then return DPLL(clauses, symbols - P, model U {P=value} )
	
	first=copy.deepcopy(symbols[0])
	symbols.remove(first)

	firstModel=copy.deepcopy(model)
	secondModel=copy.deepcopy(model)
	
	firstModel.append(first)
	secondModel.append(-1*first)
	
	firstSymbols=copy.deepcopy(symbols)
	secondSymbols=copy.deepcopy(symbols)
	
	return DPLL(clauses,firstSymbols,firstModel) or DPLL(clauses,secondSymbols,secondModel)
	
def populateKB(KB):
#####Rule for exactly one wumpus and exactly one pit:

	##Add rule that there is atleast one wumpus
	clause=[411,412,413,414,421,422,423,424,431,432,433,434,441,442,443,444]
	KB.append(clause)
  
	##Add rule that there is atmost one wumpus:
  
	for i in range(len(clause)):
		for j in range(i+1,len(clause)):
			KB.append([ -1*clause[i],-1*clause[j] ])
  
	##Add rule that there is atleast one pit
	clause=[]
	clause=[311,312,313,314,321,322,323,324,331,332,333,334,341,342,343,344]
	KB.append(clause)
  
	##Add rule that there is atmost one pit:
  
	for i in range(len(clause)):
	  	for j in range(i+1,len(clause)):
	  		KB.append([ -1*clause[i],-1*clause[j] ])

#####Cover Pits and Stench that Affect 2 Adjacent Squares:	

#Add Breeze Rules:
# Add condition B11 <-> (P12 V P21)
	clause2 = [-111,312,321]
	KB.append(copy.deepcopy(clause2))  #~B11 V P12 V P21
	clause2 = [-312,111]
	KB.append(copy.deepcopy(clause2))  # B11 V ~P12
	clause2 = [-321,111]
	KB.append(copy.deepcopy(clause2))  # B11 V ~P21
	
# Add condition B14 <-> (P13 V P24)

	clause2 = [-114,313,324]
	KB.append(copy.deepcopy(clause2))  #~B14 V P13 V P24
	clause2 = [-313,114]
	KB.append(copy.deepcopy(clause2))  # B14 V ~P13
	clause2 = [-324,114]
	KB.append(copy.deepcopy(clause2))  # B14 V ~P24
	
# Add condition B41 <-> (P31 V P42)

	clause2 = [-141,331,342]
	KB.append(copy.deepcopy(clause2))  #~B41 V P31 V P42
	clause2 = [-331,141]
	KB.append(copy.deepcopy(clause2))  # B41 V ~P31
	clause2 = [-342,141]
	KB.append(copy.deepcopy(clause2))  # B41 V ~P42

# Add condition B44 <-> (P34 V P43)

	clause2 = [-144,334,343]
	KB.append(copy.deepcopy(clause2))  #~B41 V P34 V P43
	clause2 = [-334,144]
	KB.append(copy.deepcopy(clause2))  # B41 V ~P34
	clause2 = [-343,144]
	KB.append(copy.deepcopy(clause2))  # B41 V ~P43

#Add Stench Rules:
# Add condition S11 <-> (W12 V  W21)

	clause2 = [-211,412,421]
	KB.append(copy.deepcopy(clause2))  #~S11 V W12 V W21
	clause2 = [-412,211]
	KB.append(copy.deepcopy(clause2))  # S11 V ~W12
	clause2 = [-421,211]
	KB.append(copy.deepcopy(clause2))  # S11 V ~W21

# Add condition S14 <-> (W13 V W24)

	clause2 = [-214,413,424]
	KB.append(copy.deepcopy(clause2))  #~S14 V W13 V W24
	clause2 = [-413,214]
	KB.append(copy.deepcopy(clause2))  # S14 V ~W13
	clause2 = [-424,214]
	KB.append(copy.deepcopy(clause2))  # S14 V ~W24
	
# Add condition S41 <-> (W31 V W42)

	clause2 = [-241,431,442]
	KB.append(copy.deepcopy(clause2))  #~S41 V W31 V W42
	clause2 = [-431,241]
	KB.append(copy.deepcopy(clause2))  # S41 V ~W31
	clause2 = [-442,241]
	KB.append(copy.deepcopy(clause2))  # S41 V ~W42

# Add condition S44 <-> (W34 V W43)

	clause2 = [-244,434,443]
	KB.append(copy.deepcopy(clause2))  #~S41 V W34 V W43
	clause2 = [-434,244]
	KB.append(copy.deepcopy(clause2))  # S41 V ~W34
	clause2 = [-443,244]
	KB.append(copy.deepcopy(clause2))  # S41 V ~W43
	
#####Cover Pits and Stench that Affect 3 Adjacent Squares:

#Add Breeze Rules:
# Add condition B21 <-> (P11 V P31 V P22)

	clause2 = [-121,311,331,322]
	KB.append(copy.deepcopy(clause2))  #~B21 V P11 V P31 V P22
	clause2 = [-311,121]
	KB.append(copy.deepcopy(clause2))  # B21 V ~P11
	clause2 = [-331,121]
	KB.append(copy.deepcopy(clause2))  # B21 V ~P31
	clause2 = [-322,121]
	KB.append(copy.deepcopy(clause2))  # B21 V ~P22

# Add condition B31 <-> (P21 V P32 V P41)

	clause2 = [-131,321,332,341]
	KB.append(copy.deepcopy(clause2))  #~B31 V P21 V P32 V P41
	clause2 = [-321,131]
	KB.append(copy.deepcopy(clause2))  # B31 V ~P21
	clause2 = [-332,131]
	KB.append(copy.deepcopy(clause2))  # B31 V ~P32
	clause2 = [-341,131]
	KB.append(copy.deepcopy(clause2))  # B31 V ~P41

# Add condition B12 <-> (P11 V P13 V P22)

	clause2 = [-112,311,313,322]
	KB.append(copy.deepcopy(clause2))  #~B12 V P11 V P13 V P22
	clause2 = [-311,112]
	KB.append(copy.deepcopy(clause2))  # B12 V ~P11
	clause2 = [-313,112]
	KB.append(copy.deepcopy(clause2))  # B12 V ~P13
	clause2 = [-322,112]
	KB.append(copy.deepcopy(clause2))  # B12 V ~P22

# Add condition B13 <-> (P12 V P14 V P23)

	clause2 = [-113,312,314,323]
	KB.append(copy.deepcopy(clause2))  #~B13 V P12 V P14 V P23
	clause2 = [-312,113]
	KB.append(copy.deepcopy(clause2))  # B13 V ~P12
	clause2 = [-314,113]
	KB.append(copy.deepcopy(clause2))  # B13 V ~P14
	clause2 = [-323,113]
	KB.append(copy.deepcopy(clause2))  # B13 V ~P23


# Add condition B24 <-> (P14 V P34 V P23)

	clause2 = [-124,314,334,323]
	KB.append(copy.deepcopy(clause2))  #~B24 V P14 V P34 V P23
	clause2 = [-314,124]
	KB.append(copy.deepcopy(clause2))  # B24 V ~P14
	clause2 = [-334,124]
	KB.append(copy.deepcopy(clause2))  # B24 V ~P34
	clause2 = [-323,124]
	KB.append(copy.deepcopy(clause2))  # B24 V ~P23

# Add condition B34 <-> (P24 V P44 V P33)

	clause2 = [-134,324,344,333]
	KB.append(copy.deepcopy(clause2))  #~B34 V P24 V P44 V P33
	clause2 = [-324,134]
	KB.append(copy.deepcopy(clause2))  # B34 V ~P24
	clause2 = [-344,134]
	KB.append(copy.deepcopy(clause2))  # B34 V ~P44
	clause2 = [-333,134]
	KB.append(copy.deepcopy(clause2))  # B34 V ~P33
	
# Add condition B43 <-> (P42 V P44 V P33)

	clause2 = [-143,342,344,333]
	KB.append(copy.deepcopy(clause2))  #~B43 V P42 V P44 V P33
	clause2 = [-342,143]
	KB.append(copy.deepcopy(clause2))  # B43 V ~P42
	clause2 = [-344,143]
	KB.append(copy.deepcopy(clause2))  # B43 V ~P44
	clause2 = [-333,143]
	KB.append(copy.deepcopy(clause2))  # B43 V ~P33
	
# Add condition B42 <-> (P41 V P43 V P32)

	clause2 = [-142,341,343,332]
	KB.append(copy.deepcopy(clause2))  #~B42 V P41 V P43 V P32
	clause2 = [-341,142]
	KB.append(copy.deepcopy(clause2))  # B42 V ~P41
	clause2 = [-343,142]
	KB.append(copy.deepcopy(clause2))  # B42 V ~P43
	clause2 = [-332,142]
	KB.append(copy.deepcopy(clause2))  # B42 V ~P32


#Add Stench Rules:
# Add condition S21 <-> (W11 V W31 V W22)

	clause2 = [-221,411,431,422]
	KB.append(copy.deepcopy(clause2))  #~S21 V W11 V W31 V W22
	clause2 = [-411,221]
	KB.append(copy.deepcopy(clause2))  # S21 V ~W11
	clause2 = [-431,221]
	KB.append(copy.deepcopy(clause2))  # S21 V ~W31
	clause2 = [-422,221]
	KB.append(copy.deepcopy(clause2))  # S21 V ~W22

# Add condition S31 <-> (W21 V W32 V W41)

	clause2 = [-231,421,432,441]
	KB.append(copy.deepcopy(clause2))  #~S31 V W21 V W32 V W41
	clause2 = [-421,231]
	KB.append(copy.deepcopy(clause2))  # S31 V ~W21
	clause2 = [-432,231]
	KB.append(copy.deepcopy(clause2))  # S31 V ~W32
	clause2 = [-441,231]
	KB.append(copy.deepcopy(clause2))  # S31 V ~W41

# Add condition S12 <-> (W11 V W13 V W22)

	clause2 = [-212,411,413,422]
	KB.append(copy.deepcopy(clause2))  #~S12 V W11 V W13 V W22
	clause2 = [-411,212]
	KB.append(copy.deepcopy(clause2))  # S12 V ~W11
	clause2 = [-413,212]
	KB.append(copy.deepcopy(clause2))  # S12 V ~W13
	clause2 = [-422,212]
	KB.append(copy.deepcopy(clause2))  # S12 V ~W22

# Add condition S13 <-> (W12 V W14 V W23)

	clause2 = [-213,412,414,423]
	KB.append(copy.deepcopy(clause2))  #~S13 V W12 V W14 V W23
	clause2 = [-412,213]
	KB.append(copy.deepcopy(clause2))  # S13 V ~W12
	clause2 = [-414,213]
	KB.append(copy.deepcopy(clause2))  # S13 V ~W14
	clause2 = [-423,213]
	KB.append(copy.deepcopy(clause2))  # S13 V ~W23


# Add condition S24 <-> (W14 V W34 V W23)

	clause2 = [-224,414,434,423]
	KB.append(copy.deepcopy(clause2))  #~S24 V W14 V W34 V W23
	clause2 = [-414,224]
	KB.append(copy.deepcopy(clause2))  # S24 V ~W14
	clause2 = [-434,224]
	KB.append(copy.deepcopy(clause2))  # S24 V ~W34
	clause2 = [-423,224]
	KB.append(copy.deepcopy(clause2))  # S24 V ~W23

# Add condition S34 <-> (W24 V W44 V W33)

	clause2 = [-234,424,444,433]
	KB.append(copy.deepcopy(clause2))  #~S34 V W24 V W44 V W33
	clause2 = [-424,234]
	KB.append(copy.deepcopy(clause2))  # S34 V ~W24
	clause2 = [-444,234]
	KB.append(copy.deepcopy(clause2))  # S34 V ~W44
	clause2 = [-433,234]
	KB.append(copy.deepcopy(clause2))  # S34 V ~W33
	
# Add condition S43 <-> (W42 V W44 V W33)

	clause2 = [-243,442,444,433]
	KB.append(copy.deepcopy(clause2))  #~S43 V W42 V W44 V W33
	clause2 = [-442,243]
	KB.append(copy.deepcopy(clause2))  # S43 V ~W42
	clause2 = [-444,243]
	KB.append(copy.deepcopy(clause2))  # S43 V ~W44
	clause2 = [-433,243]
	KB.append(copy.deepcopy(clause2))  # S43 V ~W33
	
# Add condition S42 <-> (W41 V W43 V W32)

	clause2 = [-242,441,443,432]
	KB.append(copy.deepcopy(clause2))  #~S42 V W41 V W43 V W32
	clause2 = [-441,242]
	KB.append(copy.deepcopy(clause2))  # S42 V ~W41
	clause2 = [-443,242]
	KB.append(copy.deepcopy(clause2))  # S42 V ~W43
	clause2 = [-432,242]
	KB.append(copy.deepcopy(clause2))  # S42 V ~W32
	

#####Cover Pits and Stench that Affect 4 Adjacent Squares:

#Add Breeze Rules:
# Add condition B22 <-> (P12 V P23 V P21 V P32)

	clause2 = [-122,312,323,321,332]
	KB.append(copy.deepcopy(clause2))  #~B22 V P12 V P23 V P21 V P32
	clause2 = [-312,122]
	KB.append(copy.deepcopy(clause2))  # B22 V ~P12
	clause2 = [-323,122]
	KB.append(copy.deepcopy(clause2))  # B22 V ~P23
	clause2 = [-321,122]
	KB.append(copy.deepcopy(clause2))  # B22 V ~P21
	clause2 = [-332,122]
	KB.append(copy.deepcopy(clause2))  # B22 V ~P32

# Add condition B32 <-> (P22 V P33 V P31 V P42)

	clause2 = [-132,322,333,331,342]
	KB.append(copy.deepcopy(clause2))  #~B32 V P22 V P33 V P31 V P42
	clause2 = [-322,132]
	KB.append(copy.deepcopy(clause2))  # B32 V ~P22
	clause2 = [-333,132]
	KB.append(copy.deepcopy(clause2))  # B32 V ~P33
	clause2 = [-331,132]
	KB.append(copy.deepcopy(clause2))  # B32 V ~P31
	clause2 = [-342,132]
	KB.append(copy.deepcopy(clause2))  # B32 V ~P42
	
# Add condition B23 <-> (P13 V P22 V P24 V P33)

	clause2 = [-123,313,322,324,333]
	KB.append(copy.deepcopy(clause2))  #~B23 V P13 V P22 V P24 V P33
	clause2 = [-313,123]
	KB.append(copy.deepcopy(clause2))  # B23 V ~P13
	clause2 = [-322,123]
	KB.append(copy.deepcopy(clause2))  # B23 V ~P22
	clause2 = [-324,123]
	KB.append(copy.deepcopy(clause2))  # B23 V ~P24
	clause2 = [-333,123]
	KB.append(copy.deepcopy(clause2))  # B23 V ~P33

# Add condition B33 <-> (P23 V P32 V P34 V P43)

	clause2 = [-133,323,332,334,343]
	KB.append(copy.deepcopy(clause2))  #~B33 V P23 V P32 V P34 V P43
	clause2 = [-323,133]
	KB.append(copy.deepcopy(clause2))  # B33 V ~P23
	clause2 = [-332,133]
	KB.append(copy.deepcopy(clause2))  # B33 V ~P32
	clause2 = [-334,133]
	KB.append(copy.deepcopy(clause2))  # B33 V ~P34
	clause2 = [-343,133]
	KB.append(copy.deepcopy(clause2))  # B33 V ~P43

#Add Stench Rules:
# Add condition S22 <-> (W12 V W23 V W21 V W32)

	clause2 = [-222,412,423,421,432]
	KB.append(copy.deepcopy(clause2))  #~S22 V W12 V W23 V W21 V W32
	clause2 = [-412,222]
	KB.append(copy.deepcopy(clause2))  # S22 V ~W12
	clause2 = [-423,222]
	KB.append(copy.deepcopy(clause2))  # S22 V ~W23
	clause2 = [-421,222]
	KB.append(copy.deepcopy(clause2))  # S22 V ~W21
	clause2 = [-432,222]
	KB.append(copy.deepcopy(clause2))  # S22 V ~W32

# Add condition S32 <-> (W22 V W33 V W31 V W42)

	clause2 = [-232,422,433,431,442]
	KB.append(copy.deepcopy(clause2))  #~B32 V W22 V W33 V W31 V W42
	clause2 = [-422,232]
	KB.append(copy.deepcopy(clause2))  # S32 V ~W22
	clause2 = [-433,232]
	KB.append(copy.deepcopy(clause2))  # S32 V ~W33
	clause2 = [-431,232]
	KB.append(copy.deepcopy(clause2))  # S32 V ~W31
	clause2 = [-442,232]
	KB.append(copy.deepcopy(clause2))  # S32 V ~W42
	
# Add condition S23 <-> (P13 V P22 V P24 V P33)

	clause2 = [-223,413,424,422,433]
	KB.append(copy.deepcopy(clause2))  #~S23 V W13 V W22 V W24 V W33
	clause2 = [-413,223]
	KB.append(copy.deepcopy(clause2))  # S23 V ~W13
	clause2 = [-424,223]
	KB.append(copy.deepcopy(clause2))  # S23 V ~W22
	clause2 = [-422,223]
	KB.append(copy.deepcopy(clause2))  # S23 V ~W24
	clause2 = [-433,223]
	KB.append(copy.deepcopy(clause2))  # S23 V ~W33

# Add condition S33 <-> (P23 V P32 V P34 V P43)

	clause2 = [-233,423,432,434,443]
	KB.append(copy.deepcopy(clause2))  #~S33 V W23 V W32 V W34 V W43
	clause2 = [-423,233]
	KB.append(copy.deepcopy(clause2))  # S33 V ~W23
	clause2 = [-432,233]
	KB.append(copy.deepcopy(clause2))  # S33 V ~W32
	clause2 = [-434,233]
	KB.append(copy.deepcopy(clause2))  # S33 V ~W34
	clause2 = [-443,233]
	KB.append(copy.deepcopy(clause2))  # S33 V ~W43

	
def main():
    ag = Agent()
    
    KB=[]
    populateKB(KB)

    symbols=[111,112,113,114,121,122,123,124,131,132,133,134,141,142,143,144, 211,212,213,214,221,222,223,224,231,232,233,234,241,242,243,244, 311,312,313,314,321,322,323,324,331,332,333,334,341,342,343,344, 411,412,413,414,421,422,423,424,431,432,433,434,441,442,443,444]
   
    visited=[]
    safe=[]
    print("Percept is printed only for newly visited states. Revisiting a state is printed without 2 line breaks")
    

	
	
    while True:
    
    	safe=[]
    	print()
    	print('curLoc',ag.FindCurrentLocation())
    	curx = (ag.FindCurrentLocation())[0]
    	cury = (ag.FindCurrentLocation())[1]
    	
    	if(curx==4 and cury==4):
    		print("Success");
    		print("Total call to DPLL", TotalCount)
    		return
    		
    	visited.append(curx*10+cury)
    	
    	print('Percept [breeze, stench] :',ag.PerceiveCurrentLocation())
    	
    	pBreeze = ag.PerceiveCurrentLocation()[0]
    	pStench = ag.PerceiveCurrentLocation()[1]
    	
    	if pBreeze:
    		KB.append([100+(curx*10+cury)])
    	else:
    		KB.append([-1*(100+(curx*10+cury))])
    		
    	if pStench:
    	#	print("Added stench location")
    		KB.append([200+(curx*10+cury)])
    	else:
    		KB.append([-1*(200+(curx*10+cury))])
    		
   #	print("Current KB: ")
    #	for clause in KB:
    #		print(clause)
    		
    	#Find all the safe places that can be visited (which is not already visited):
    	for i in range(4):
    		for j in range(4):
    			if(((i+1)*10+(j+1)) not in visited):
    			#	print("Checking if",i+1,j+1," is safe: ")
    				sent=[]
    				sent = copy.deepcopy(KB)	#sent is the sentence that we are passing to DPLL
    				sent.append([(300+(i+1)*10+(j+1)),(400+(i+1)*10+(j+1))])			#Add pit or wumpus
    				
    				sentsym=copy.deepcopy(symbols)
    				res=DPLL(sent, sentsym, [])
    			
    				if not res:
    					safe.append((i+1)*10+(j+1))
    					
    	#Check for a path to safe place from visited state, so find a visited place which has a safe place in its immediate neighbourhood:
    	
    	#print("Number of current safe states: ",len(safe))
    	#print("Which are: ")
    	#for state in safe:
    	#	print(state)
    	goalFound=False
    	
    	goalx=0
    	goaly=0
    	safex=0
    	safey=0
    	for state in safe:
    		if(goalFound):
    			break;
    			
    		safex=(int)(state/10)
    		safey=state%10
    		
    		if(safex!=1 and ((safex-1)*10+(safey)) in visited):
    			goalx=safex-1
    			goaly=safey
    			#print("Goal found: ",goalx,",",goaly)
    			goalFound=True;
    			break;
    		
    		if(safey!=1 and ((safex)*10+(safey-1)) in visited):
    			goalx=safex
    			goaly=safey-1
    			#print("Goal found: ",goalx,",",goaly)
    			goalFound=True;
    			break;
    		
    		if(safex!=4 and ((safex+1)*10+safey) in visited):
    			goalx=safex+1
    			goaly=safey
    			#print("Goal found: ",goalx,",",goaly)
    			goalFound=True;
    			break;
    		
    		if(safey!=4 and (safex*10+(safey+1)) in visited):
    			goalx=safex
    			goaly=safey+1
    			#print("Goal found: ",goalx,",",goaly)
    			goalFound=True;
    			break;
    				
    	
    	#Now go to goalx goaly, which are visited states and then take 1 step to reach safex, safey
    	#print("Plan is: Goal: ",goalx,",",goaly," and Safe: ",safex,",",safey)
    	
    	#We would use BFS algorithm to generate a path from curx, cury to goalx,goaly:
    	
    	pathqueue=[]
    	curpath=[]
    	pathqueue.append([curx*10+cury])
    	
    	while len(pathqueue)!=0:
    		curpath=pathqueue[0]
    		
    		pathqueue.remove(curpath)
    		
    		node=curpath[len(curpath)-1]
    		
    		nodex=(int)(node/10)
    		nodey=node%10
    		
    		if(node==(goalx*10+goaly)):
    			break;
    		
    		for state in visited:
    			if(state not in curpath):
    				statex=(int)(state/10)
    				statey=state % 10;
    				
    				if( ( abs(statex-nodex)==0 and abs(statey-nodey)==1 ) or ( abs(statex-nodex)==1 and abs(statey-nodey)==0 ) ):
    				
    					newpath=copy.deepcopy(curpath)
    					newpath.append(state)
    					pathqueue.append(newpath)
    	curpath.remove(curx*10+cury)
      	
    	while(curx!=goalx or cury!=goaly):
    		
    		
    		statex = (int)(curpath[0]/10)
    		statey = curpath[0]%10
    		
    		curpath.remove(statex*10+statey)

    		if(statex>curx):		
    			ag.TakeAction('Right')
    		
    		elif(statex<curx):
    			ag.TakeAction('Left')
    			
    		elif(statey>cury):
    			ag.TakeAction('Up')
    		
    		elif(statey<cury):
    			ag.TakeAction('Down')
    		
    		curx=(ag.FindCurrentLocation())[0]
    		cury=(ag.FindCurrentLocation())[1]
    	
    	
    	#We have reached goalx, goaly, now we would take a step to reach Safex, safey and retry the entire search process:
    	
    	if(safex>curx):
    		ag.TakeAction('Right')
    		
    	elif (safex<curx):
    		ag.TakeAction('Left')
    			
    	elif (safey>cury):
    		ag.TakeAction('Up')
    	
    	elif (safey<cury):
    		ag.TakeAction('Down')


if __name__=='__main__':
    main()

{testcost(1..10,1..20,1..40)}=1.

#minimize {X@1 : testcost(X,_,_)}.
#maximize {Y@2 : testcost(_,Y,_)}.
#minimize {Z@3 : testcost(_,_,Z)}.

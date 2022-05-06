item(1,price(5),weight(6)).
item(2,price(8),weight(10)).
item(3,price(2),weight(2)).
item(4,price(6),weight(8)).
item(5,price(7),weight(3)).
item(6,price(6),weight(7)).
item(7,price(18),weight(9)).
item(8,price(5),weight(12)).
item(9,price(3),weight(2)).
item(10,price(21),weight(15)).


{choose(I) : item(I,_,_)}.
sum_w(S) :- S= #sum{W : item(I,_,weight(W)),choose(I)}. % Sum of weight
sum_i(S) :- S= #sum{1,I :choose(I)}.                    % Sum of # item

:- sum_w(S), S>41.
:- sum_w(S), S<35.


#show sum_w/1.
#show sum_i/1.
#show choose/1.

#minimize {  I@1 : sum_i(I)}.
#maximize {  W@2 : sum_w(W)}.


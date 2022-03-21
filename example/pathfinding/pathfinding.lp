direction(0,1).
direction(0,-1).
direction(1,0).
direction(-1,0).
direction(0,0).

time(1..9).

position(X,Y,0) :- init(X,Y).


1{move(DX,DY,T): direction(DX,DY)}1 :- time(T).


position(X+DX,Y+DY,T) :- 
    position(X,Y,T-1), 
    node(X+DX,Y+DY), 
    move(DX,DY,T).


endreached(T) :- position(X,Y,T), end(X,Y).

:- endreached(T), not move(0,0,T'), time(T'), T'>T.
:- position(X,Y,_), wall(X,Y).
:- move(_,_,T), not position(_,_,T).


endreached :- endreached(_).
:- not endreached.

position(X,Y) :- position(X,Y,_).

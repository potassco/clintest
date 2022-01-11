#program base.
test(1..5).
% :-test(1).
#program clintest.
% clintest(sat).
clintest(trueInAll,test(1),test(2),test(6)).
% clintest(trueInAll,test(N)) :- test(N).


% clintest(contain,test(2),test(8),test(9)).
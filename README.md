   My high-level approach for solving Wordle was to maintain a list of valid guesses and randomly make selections from it, 
using the results to adjust the list as appropriate. While in actual Wordle games it is sometimes advantageous to guess 
a completely incorrect word to rule out common letters, I chose to go with my method since it would be much easier to 
implement. To do this, my code randomly picks a word from the list, removes it from the list, and submits it as a guess 
using the sendMsg() method. If the word was right, I’m done; if not, I call the updateWordList() method, which uses the 
info in the guess to cross invalid words off the list. This method is well-optimized; once a character of the final word 
is known, it is removed from the “unknown” list so that we never check that slot again. Then, we repeat until we win.
   As for testing, I’m afraid I’ve disappointed my Logic and Comp professor. My testing consisted of dozens and dozens 
of executions of the program, with various valid and invalid values in each argument. While not logically foolproof, 
I’m confident that my random testing didn’t miss any significant cases. One thing I was sure to check for was runs where 
the correct word was the last word in the list, since that was a likely edge case.
   I faced a few major challenges in writing this code. My first was the fact that I didn’t know Python before this 
assignment, which led to a lot of delays for researching commands and resolving syntax errors. I also initially used 
another guessing approach in which I repeatedly picked random words from the list and checked that individual word against 
all previous guesses. The method was inefficient and buggy, and I wasted a good amount of time fixing it. With all that 
said, I’m confident in the quality of my final result, and I’m glad I made and learned from those mistakes.

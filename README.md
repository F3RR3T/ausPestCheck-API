# ausPestCheck-API
Scripts for API clients


## Quick start

* create a text file called 'mykeys.txt' in the same folder as the script.
* copy your subscription key as line 1 and particiapnt key as line 2.
* save and close the file
* Using a python interactive console, execute the script.
* This loads the functions as objects.
* invoke 'uploadObs(createPayload())' at the prompt
* this will upload 3 medfly obs in WA.
* default arguments are: num = 3, state = 'WA', pestID='C'
* Change the num, state and pestIDs as desired.

You can also print the observations as a list using 'writeObs(payload)'
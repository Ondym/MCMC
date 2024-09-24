## Usage of chaos-game-ext.py
__How to edit the program to try your own configurations__

This is a program simulating the chaos game (https://en.wikipedia.org/wiki/Chaos_game), which is a generalized version
of our Sierpinski triangle. Since there are many versions of the chaos game and it depends on various factors - number 
of vertices, lerp (Linear intERPolation) coefficient, rule for selecting vertices (this one makes the most interesting)...
You can find all the details on the Wikipedia page.

You can try making some basic changes to the parameters, like in the setup() function, or experiment with the vertex
selection rule on line 122 (v_index - it is higlightet via a comment). However, if you're not completely sure or if you
want the animation to be a certain way, I’d definitely recommend just copying the code and asking ChatGPT to modify it.
If you’re looking for inspiration, I suggest experimenting with the number of vertices, the lerp coefficient (I recommend
playing around with the colors, reducing the number of points generated in each round, and setting erase=False)...

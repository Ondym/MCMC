## Usage of chaos-game-ext.py
__How to edit the program to try your own configurations__

Tohle je program simulujici chaos game (https://en.wikipedia.org/wiki/Chaos_game), coz je generalizovana verze
naseho Sierpinskiho trojuhelniku. Jelikoz je mnoho verzi chaos game a zalezi, cim se bude ridit (pocet vertexu,
koeficient lerpu, pravidlo vybirani vrcholu...), vsechno je na ty strance na Wikipedii.

Muzete se pokusit o nejaky zakladni zmeny parametru, treba ve funkci setup(), nebo o pravidlo vyberu vrcholu na 
radku 74 (v_index), ale pokud si nejste uplne jisty a nebo chcete aby to bylo/nebylo nejak animovany, urcite doporucuju
proste to zkopirovat a napsat ChatGPT, protoze tak jsem delal animace ja kdyz jsem je chtel nejak videt. Kdyby jste chteli
nejakou inspiraci, tak ja jsem se treba koukal jak se to meni s poctem vrcholu, koeficientem lerpu (doporucuju menit
ho, snizit pocet bodu generovanych v kazdym kole a nastavit erase=False)...

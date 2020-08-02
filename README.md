# ticket2ride

## ticket2ride custom board creation
Ticket to Ride is a fan-made expansion to the Days of Wonder, Inc. Ticket to Ride series created by Alan R. Moon. 
Published by permission for non-commercial use. All rights to the Ticket to Ride name, gameplay, mechanics, and imagery are reserved by Days of Wonder, Inc., who have not endorsed or playtested this expansion.
Unofficial Fan made expansion - Symbols & Graphics Copyright 2004-2016 Days of Wonder, Inc. Produced with permission of Days of Wonder, for non-commercial use only.

## Code to create custom ticket to ride game board colouring and tickets.

#### Game board:
Based on your gameboard place and track placements, the code will generate random colours for each section of track, based on probabilites from the Europe board game. Locamotive and tunnel random placement also returned (will be improved in future version).

#### Ticket generation:
Using network X, a full graph network is created for the map. Using this all shortest path distances between places (nodes) can be easily calculated. Based on the approximate distribution of ticket lengths in the European version of the game.

#### Example code:
Full example for creation of 'Singapore ticket to ride' game. I wrote this code to speed up the ticket generation and ensure more randomness in the board track colouring. Code can be reused for other custom board creations.

## Other
##### Making the board

I created the board using an image editor (Photoshop), and then extracted the coordinates for each of my places to a .csv file. This can then be read into python easily.
I laid the tracks (without colours) to calculate the best placement on the board, then wrote the length of these track segments to a second .csv file.

The track scoring image came from: https://boardgamegeek.com/boardgame/9209/ticket-ride/expansions

#### font
The 'shangri-la' font can be downloaded from:https://www.fontsquirrel.com/fonts/shangrilanf

#### Print the tickets
The mailmerge option in word can be used to write multiple .png ticket images to one A4 sheet for printing. 

### Packages required
Networkx, Numpy, Pandas, Matplotlib

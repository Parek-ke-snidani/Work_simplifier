# Work repository

Code I managed to write to simplify my tasks. :-)

## Download_IMG_Napojse

I got products with EAN codes in excel file and I had to download images which supplier shared through Napojse.cz

### Little overview

Open browser (Firefox) -> search website (napojse.cz) -> sign in with email and password -> copy ean from excel -> search ean on the website -> download image (if image not found write it to excel) and name it after name of the product on website-> repeat and save excel every 10th loop

## TORcountry

This project provides a somewhat user-friendly GUI tool to customize the torrc configuration file for Tor Browser. Using this tool, you can easily update the list of exit nodes, specifying which countries' IP addresses you want Tor to use for outgoing traffic. (code should be in the topmost folder of Tor browser or specify the path to the torrc file)

This tool modifies the torrc file and may affect your Tor network behavior. Use responsibly

### Little overview

Load torrc File -> opens GUI -> Select Countries -> If path is correct (code should be in first folder - Tor Browser) it updates the exit nodes (if file is not found it will ask for new path to the torrc file and save it in .json file)
![alt text](https://i.imgur.com/SonSxEP.png)

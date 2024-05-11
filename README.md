## Author
Lorenzo Springer-Giamartino

## Project Title
No Scroll - a personalized stylist which optimizes your wardrobe and wallet

## Project Description
The generation and sharing of digital content via the internet is somewhat fragmented and discoordinated, creating much redundancy, smothering shoppers. Meanwhile, shopping is increasinly moving online. This has made it quite difficult to use quality reference points in order to discern what an optimal purchase is. Therefore, I propose an application which draws upon the fashion brands a user follows on their X account, in order to identify a user's style preferences. With these data, a reccomendation algorithm which is designed to reccomend the most efficient purchase will be implemented. 

This will involve integrating with the X api to pull the most recent posts of the fashion brands they follow, and then run an image classifier on the images in order to identify how certain articles are co-styled. Then a reccomendation algorithm is implemented to reccomend the items which optimize the users wardrobe - those items that create the greatest number of pleasing outfits. 

The package is in progress and contains code for the first implementation of the reccomendation algorithm in the file 'reccomend.py", the gathering of twitter data in 'get_x.py', and a main file to call them. 





# How To Run
<details>
  <summary><h3>Install all the dependencies:</h3></summary>
  <li>matplotlib</li>
  <li>requests</li>
  <li>json</li>
  <li>scipy</li>
  <li>numpy</li>
</details>


Run the python script called **BeatSaberHeightBeatLeader.py**. (*python BeatSaberHeightBeatLeader.py*)

Next you will be asked to enter the Map Id, to get the Map Id all you have to do is:
- Go to [BeatLeader](https://www.beatleader.xyz/leaderboards)
- Find a map that you are interested in, and click on it
- The Map Id is the few characters at the end of the URL, just like on this image:
![BeatLeaderMapId](https://user-images.githubusercontent.com/69699046/177191315-8ff5add2-6083-4096-b0e9-378f3ed62a5d.png)
- Paste the Id into the console, press enter and voilà. Now you have to wait up to few minutes (depends on your pc specs and internet bandwidth)
- After some time has passed, a graph with all the data should pop up.


# Sample Graphs
#### There are provided 2 additional sample files that the script uses, if you choose the correct Map Id.

<details>
  <summary><h3>Graphs created using this tool:</h3></summary>

![image](https://user-images.githubusercontent.com/69699046/177191448-f27b27ae-4cb0-46aa-8831-abf9f6e7fe4c.png)

![image](https://user-images.githubusercontent.com/69699046/177191565-f9fbeff7-2730-4da6-94f8-45e6debf58dc.png)

</details>

# My Thoughts
Though the data looks cool and all, it's **very inconclusive**, which is probably caused by a marginal difference in peoples' height and the fact that you can **manually set the height** yourself in beatsaber settings.

# Note
Like I have mentioned earlier, you can manually adjust the height yourself. This causes some rather interesing numbers like **players** that are more that **3 meters tall, or that are shorter than a toddler**. To *combat* this I just added a code to filter out those values, you can find it [here](https://github.com/AndyFilter/BeatSaberHeightAnalysis/blob/9dbc7900f486baeabe7840dafd4bfed25f423c3c/BeatSaberHeightBeatLeader.py#L178). *The values were picked arbitrarily.* It's also *interesing* to run the code without this filter.

# Requirements
- Python 3.10 (I couldn't install Matplotlib on older versions)

# SelfDrivinCarTobi
This is a small Unity Project. 
This Part was for learning some basic Unity Concepts and refreshing these concepts.

The second part of the Project was a Python Rest Server which should give the car commands if it drives in the 'autonomous mode'.
The Machine Learning Model  I tried first was a Naive Bayes Classifier, which classified if the car should Turn Left, TurnRight, ShouldAccelerate.
I will Implement a lot of other supervised learning methods and may if I have time also start a Reinforcement Learning approach on this application

## Getting Started
Just Clone the repository start the server with Python 3, after you downloaded the needed libraries.
If I am finished with the project I will create a requirements.txt file, which inlcudes all the modules for the project to make the installation easier with pip. <br>
<b> Introduction will follow </b> <br>
<br>
<b>How you use the application:</b> <br>
1.   First of all run the server.py script in the Server Directory 
  The server.py starts a server, which is collecting the data of the car in Unity.
  The server is running on localhost on the Port 80. It is a simple Rest Implementation, that accepts POST requests on 2 paths.</li> 
  <ul>
      <li>'/sendDrivingData': Rest response will be the command for the car in autonomous mode. The command will be predicted with
      a certain ML-Supervised Method (SVM, NaiveBayes, NNs,...) and send back to the car. </li>
      <li> '/getDrivingData': On this path the server receives the data from the car and saves it, in order to learn from it for the        predcition </li>
  </ul>
2.   After you run the server, start the Unity Project and open the MainMenu Scene.
  Click on Play and choose the Training Mode first. <br>
3.   After you have collected enough data, simply try out the autonomous mode and see how your car solves the autonomous driving task.


## Some Impressions
TODO: Add pictures here and maybe a video how the car is driving autonomously and how it works.


## Code Explanation



## Theory Explanation <br>

### Unity Project
The Unity Project has 3 Scenes. I will describe the 2 important ones. <br>
The <b>MainMenu Scene</b> has 2 Buttons, which start the Game either in Training or Autonomous Mode.
<img src="GitHubRes/MainMenu.PNG" height="200px" title="Main Menu with 2 Buttons"><br>
Therefore they use the functions of the GameManager Object with the GameManagerScript.cs and set the 2 methods of the GameManagerScript as the onClick Methods.<br>

The GameCntrollable Scene is the actual Game with the Parcour and the predefined end of the track. Just try to reach the pizza store without crashing against a wall. <br>

First of all 2 Pictures of it, so you see, how this scene actually looks like:<br>
<ul> 
  <li> This is the View of the GameControllable Scene in Unity, you can see all GameObjects, and the Properties of the Car
    <img src="GitHubRes/GameControllable_Unity_View.PNG" height="200px" title="GameControllable in Editor View">
  </li>
  <li> This is the View of the GameControllable Scene actually if you play it
    <img src="GitHubRes/GameControllable_GameView.PNG" height="200px" title="GameControllable in Game View"> <br>
  </li>
 </ul>
 
 In the first picture you can already see the important Game Objects on the left side and what scripts are used by the Car GameObject.
 <br>
 
The Car Game OBject contains 4 Scripts:
<ul>
  <li> The CarControll Script: enables the moovement of the car, interacts with the other scripts aswell and somehow defines the lifecycle and doings of the car (autonomousMode, CollisionHandling, Init InformationHandling, ...)
  </li>
  <li> The LevelManager Script in the CarControllScript Block is just the reference to the GameObject "GameManager" and called, when you fail or reach thedestination. (levelManager.showMenu())
  </li>
    <li> The SensorData Script: Uses the Sensor in the front of the car ("Radar"- measures distances to objects maybe half a meter over the ground). After the start of the Game this script enables the "Radar" with the checkDistancesMethod(float time). <br></li>
     ```
  
       while (!CarControll.isFinished)
        {
            yield return new WaitForSeconds(time);
            //Debug.Log("Time: " + Time.time);
            forwardDistance = CheckForwardSensorDistance();
            leftDistance = CheckLeftwardSensorDistance();
            rightDistance = CheckRightWardSensorDistance();
            leftRightRatio = calculateLeftRightRatio(leftDistance, rightDistance);
            //Debug.Log("LR-Ratio: " + leftRightRatio);
        }
     
     ``` 
  It will also create a InformationList (addInformationList()), that collects the data in a list and serializes the data and makes a JSON Object out of it, to send it to the server later.

  
  



  

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details 


















The Unity project (Car and C# part) is based on this project, I rebuilded there code and tried to understand it, in order to get a feeling for it.
https://github.com/MCKapur/SPCSAISelfDrivingCar.

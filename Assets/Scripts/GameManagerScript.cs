﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GameManagerScript : MonoBehaviour {

	

    public  void testTheCar()
    {
        CarControll.isControlledByAI = true;
        Application.LoadLevel("EasyParkour");
    }

    public  void trainTheCar()
    {
        CarControll.isControlledByAI = false;
        Application.LoadLevel("EasyParkour");
    }
}

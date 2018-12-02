using System.Collections;
using System.Collections.Generic;
using System.Text;
using UnityEngine;

public class DataTransfer : MonoBehaviour {

    //Data Delay for collecting Data in creating InformationList
    public  float dataDelay;

    private SensorData sensorData;

    private void Awake()
    {
        sensorData = this.GetComponent<SensorData>();
    }

    // Use this for initialization
    void Start () {
	}
	
	// Update is called once per frame
	void Update () {
		
	}

    //This is only a one time thing
    public  void SendDataToServer()
    {
        //If human is controlling, we want to send human's data for training
        //Print accumulated data
        if (sensorData == null)
        {
            sensorData = this.GetComponent<SensorData>();
        }
        Debug.Log(sensorData.SerializeList());

        string url = "http://localhost:80/sendDrivingData";
        Dictionary<string, string> postHeaders = new Dictionary<string, string>();
        postHeaders.Add("Content-Type", "application/json");
        byte[] bytes = Encoding.UTF8.GetBytes(sensorData.SerializeList());
        WWW www = new WWW(url, bytes, postHeaders);
        // Debug.Log("We sent data correctly...");
        List<string> keyList = new List<string>(www.responseHeaders.Keys);
        List<string> valueList = new List<string>(www.responseHeaders.Values);

        Debug.Log("Respnse from Server:");
        debugListValues(keyList);
        debugListValues(valueList);

        //StartCoroutine (WaitForRequest (www));  
    }

    //AI-Methods
    //Sent by MoveCar
    public IEnumerator GetDataFromServerRequest()
    {
        Debug.Log("GetDataFromServerRequestMethod called!!!");
        //If AI is controlling, then we want it to send wall input data
        //&& !CarControll.isFinished
        while (CarControll.isControlledByAI )
        {
            yield return new WaitForSeconds(dataDelay);
            //Debug.Log("Sending distance from wall");
            string url = "http://localhost:80/getDrivingData";
            //First send distance from wall data
            Dictionary<string, string> postHeaders = new Dictionary<string, string>();
            postHeaders.Add("Content-Type", "application/json");
            byte[] bytes = Encoding.UTF8.GetBytes(sensorData.GetDistanceToObject());
            WWW www = new WWW(url, bytes, postHeaders);
            //Receive data
            StartCoroutine(WaitForRequest(www));
        }
    }


    IEnumerator WaitForRequest(WWW www)
    {
        Debug.Log("WaitForRequest called!!!");

        //If www is null, return
        yield return www;
        //Debug.Log ("we are receiving requests");
        if (www.error == null)
        {
            Debug.Log("WaitForRequest and no error:");
            string receivedText = www.text;
            Debug.Log("Received Command from Server: " +  receivedText);
            JSONObject jsonReceived = new JSONObject(receivedText);
            Dictionary<string, string> dict =  jsonReceived.ToDictionary();
            CarControll.isTurningLeft = float.Parse(dict["isTurningLeft"]);
            CarControll.isTurningRight = float.Parse(dict["isTurningRight"]);
            CarControll.isNotTurning = float.Parse(dict["isKeepingStraight"]);
            CarControll.isAccelerating = float.Parse(dict["isAccelerating"]);
            Debug.Log("Commands arrived at Car: " + jsonReceived.ToString());


            //accessData(serializedList);

        }
    }

    /*
    void accessData(JSONObject obj)
    {
        for (int i = 0; i < obj.list.Count; i++)
        {
            string key = (string)obj.keys[i];
            float number = obj.list[i].n;
            switch (key)
            {
                case "shouldAccelerate":
                    //If we are moving straight and we are in front of the wall, override and break
                    if (sensorData.scaledForward < 0.2f && number == 1 && MoveCar.shouldNotTurn == 1 && MoveCar.mySpeed > 30f)
                    {
                        number = 0;
                    }
                    MoveCar.shouldAccelerate = number;
                    break;
                case "shouldTurnLeft":
                    MoveCar.shouldTurnLeft = number;
                    break;
                case "shouldTurnRight":
                    MoveCar.shouldTurnRight = number;
                    break;
                case "shouldKeepStraight":
                    MoveCar.shouldNotTurn = number;
                    break;
            }
        }
    }
    */

    public void debugListValues(List<string> list)
    {
        string temp = "";
        foreach (string str in list)
        {
            temp += str + ","; //maybe also + '\n' to put them on their own line.
        }

        Debug.Log("List: " + temp);
    }



}

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
        dataDelay = 0.2f;
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
        Debug.Log("Response from Server:  " + www.responseHeaders.ToString());
        //StartCoroutine (WaitForRequest (www));  
    }

}

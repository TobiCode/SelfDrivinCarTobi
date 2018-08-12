using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SensorData : MonoBehaviour
{

    //Location of the Sensor at the Car
    public Transform sensorLocation;

    //Visualisation where teh sensors hit
    public GameObject leftwardRayHitPoint, forwardRayHitPoint, rightwardRayHitPoint;

    public float rayAngle;

    //Car Variables
    CarControll carControll;
    //Data Transfer Script
    DataTransfer dataTransfer;

    //Sensor Data
    float leftRightRatio;
    float leftDistance;
    float rightDistance;
    float forwardDistance;

    //Cam--> Needed to moove UI Elements to hitpoints
    public Camera cam;

    //store multiple variables in one list
    public static List<Values> informationList;

    //Object that will be sent to server on Finish
    private static JSONObject _serializedObject;

    // Use this for initialization
    private void Awake()
    {
        dataTransfer = GetComponent<DataTransfer>();
        leftwardRayHitPoint = GameObject.Find("LeftRay");
        forwardRayHitPoint = GameObject.Find("CenterRay");
        rightwardRayHitPoint = GameObject.Find("RightRay");
        cam = Camera.main;

        //Init & So that this does not reset every turn
        if (informationList == null)
        {
            informationList = new List<Values>();
        }
    }

    private void Start()
    {
        StartCoroutine(checkDistances(0.1f));
    }

    // Update is called once per frame
    void Update()
    {

    }

    //This prints data to the game view itself...
    void OnGUI()
    {
        //Left ray
        GUI.Button(new Rect(10, 20, 200, 30), "ScaledLR: " + leftRightRatio);
        GUI.Button(new Rect(Screen.width / 2 - 100, 50, 200, 30), "Forward distance: " + forwardDistance);

        GUI.Button(new Rect(10, 80, 150, 30), "Speed: " + Mathf.Round(CarControll.currentSpeed) + " km/h");
        GUI.Button(new Rect(10, 50, 200, 30), "AI is Driving: " + CarControll.isControlledByAI);
    }


    IEnumerator checkDistances(float time)
    {
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

    }

    float calculateLeftRightRatio(float left, float right)
    {
        return (leftDistance / (leftDistance + rightDistance));
    }

    float CheckForwardSensorDistance()
    {
        RaycastHit hit;
        Vector3 fwd = sensorLocation.TransformDirection(Vector3.forward);

        if (Physics.Raycast(sensorLocation.position, fwd, out hit, Mathf.Infinity))
        {
            if (hit.transform.tag == "Wall")
                Debug.DrawRay(sensorLocation.position, sensorLocation.TransformDirection(Vector3.forward) * hit.distance, Color.blue);
            //Debug.Log("Did Hit Forwar: " + hit.distance);

            //Set Sensor GUI to the hitpoint
            forwardRayHitPoint.transform.position = cam.WorldToScreenPoint(hit.point);
            //forwardRayHitPoint.transform.position.z = 0;


            return hit.distance;
        }

        return 1.0f;
    }

    float CheckLeftwardSensorDistance()
    {
        RaycastHit hit;
        Vector3 leftWard = Quaternion.AngleAxis(-rayAngle, sensorLocation.up) * sensorLocation.forward;

        if (Physics.Raycast(sensorLocation.position, leftWard, out hit, Mathf.Infinity))
        {
            if (hit.transform.tag == "Wall")
                Debug.DrawRay(sensorLocation.position, leftWard * hit.distance, Color.red);
            // Debug.Log("Did Hit Leftward: " + hit.distance);

            //Set Sensor GUI to the hitpoint
            leftwardRayHitPoint.transform.position = cam.WorldToScreenPoint(hit.point);
            //forwardRayHitPoint.transform.position.z = 0;


            return hit.distance;
        }


        return 1.0f;
    }

    float CheckRightWardSensorDistance()
    {
        RaycastHit hit;
        Vector3 rightWard = Quaternion.AngleAxis(rayAngle, sensorLocation.up) * sensorLocation.forward;

        if (Physics.Raycast(sensorLocation.position, rightWard, out hit, Mathf.Infinity))
        {
            if (hit.transform.tag == "Wall")
                Debug.DrawRay(sensorLocation.position, rightWard * hit.distance, Color.green);
            // Debug.Log("Did Hit Rightward: " + hit.distance);

            //Set Sensor GUI to the hitpoint
            rightwardRayHitPoint.transform.position = cam.WorldToScreenPoint(hit.point);
            //forwardRayHitPoint.transform.position.z = 0;


            return hit.distance;
        }


        return 1.0f;
    }


    //Build Information List after gameStart
    public IEnumerator addInformationList()
    {
        while (!CarControll.isControlledByAI && !CarControll.isFinished)
        {
            yield return new WaitForSeconds(dataTransfer.dataDelay);
            //Send data only when the person starts accelerating
            informationList.Add(new Values
            {
                sentScaledSpeed = CarControll.currentSpeed,
                sentScaledForward = forwardDistance,
                sentScaledLRRatio = leftRightRatio,
                isAccelerating = CarControll.isAccelerating,
                isTurningLeft = CarControll.isTurningLeft,
                isTurningRight = CarControll.isTurningRight,
                isNotTurning = CarControll.isNotTurning
            });
            //Just for DEBUG
            SerializeList();
            //Debug.Log("InfoList: " + SerializeList());
        }
    }

    //Recording human data for training
    public string SerializeList()
    {
        _serializedObject = new JSONObject(JSONObject.Type.OBJECT);
        JSONObject data = new JSONObject(JSONObject.Type.ARRAY);
        foreach (Values v in informationList)
        {
            JSONObject trainingCase = new JSONObject(JSONObject.Type.OBJECT);
            //trainingCase.AddField("normalizedSpeed", MoveCar.normalizedSpeed);
            trainingCase.AddField("scaledForward", v.sentScaledForward);
            trainingCase.AddField("scaledLeftRightRatio", v.sentScaledLRRatio);
            trainingCase.AddField("isAccelerating", v.isAccelerating);
            trainingCase.AddField("scaledSpeed", v.sentScaledSpeed);

            trainingCase.AddField("isTurningLeft", v.isTurningLeft);
            trainingCase.AddField("isTurningRight", v.isTurningRight);
            trainingCase.AddField("isKeepingStraight", v.isNotTurning);
            data.Add(trainingCase);
            //Debug.Log("New Training Case: " + trainingCase.Print());
        }
        _serializedObject.AddField("data", data);
        JSONObject types = new JSONObject(JSONObject.Type.ARRAY);
        types.Add("motion");
        types.Add("steering");
        _serializedObject.AddField("types", types);
        return _serializedObject.Print();
    }


    public struct Values
    {
        public float sentScaledSpeed;
        public float sentScaledForward;
        public float sentScaledLRRatio;
        public float isAccelerating;
        public float isTurningLeft;
        public float isTurningRight;
        public float isNotTurning;
    }


    //AI-Methods
    //Server sending server data to 3d environment
    public string GetDistanceToObject()
    {
        _serializedObject = new JSONObject(JSONObject.Type.OBJECT);
        JSONObject trainingCase = new JSONObject(JSONObject.Type.OBJECT);
        trainingCase.AddField("scaledSpeed", CarControll.currentSpeed);
        trainingCase.AddField("scaledForward", forwardDistance);
        trainingCase.AddField("scaledLeftRightRatio", leftRightRatio);
        _serializedObject.AddField("data", trainingCase);
        return _serializedObject.Print();
    }



}


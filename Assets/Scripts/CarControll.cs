using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class CarControll : MonoBehaviour {

    //Level Manager-- Restarting, Swtiching to AI Mode, Etc.
    public LevelManager levelManager;
    private SensorData sensors;
    private DataTransfer dataTransfer;


    //GUI variables
    public Text successInfoText;

    //Car physics variables
    public float maxMotorTorque;
    public float maxBrakeTorque;
    public float maxSteeringAngle; //maximum steering Angle the wheel can have
    public List<AxleInfo> axleInfos; // the information about each individual axle

    private Rigidbody rb;
   [SerializeField] public static float currentSpeed;
    public float maxSpeed;

    //Sound variables
    public AudioClip movingCarSound;
    private AudioSource audioSource;

    //Game State Variables
    public static bool isFinished;
    private bool alreadyAccelerated;

    //isControlledByAI
    public static bool isControlledByAI;

    private bool dataSentOnce;

    private bool crashed;

    //Initia position-Starting position
    private Vector3 initialPosition;
    private Quaternion initialRotation;
    //Default COM is 0, 0.3, 0
    private Vector3 centerOfMass = new Vector3(0, 0, 0);

    //Car moove variables --> Used in Fixed Update to moove the car
    //Accelerating
    public static float isAccelerating;
    //Turning
    public static float isTurningLeft;
    public static float isTurningRight;
    public static float isNotTurning;


    public void Awake()
    {
        dataSentOnce = false;
        initialPosition = transform.position;
        initialRotation = transform.rotation;
        rb = GetComponent<Rigidbody>();
        rb.centerOfMass = centerOfMass;
        audioSource = GetComponent<AudioSource>();

        sensors = this.GetComponent<SensorData>();
        dataTransfer = this.GetComponent<DataTransfer>();

        startingSettingsGame();


        //Ai Mode:
        if (isControlledByAI)
        {
            //Change to IEnumerator
            StartCoroutine(dataTransfer.GetDataFromServer());

        }
    }

    //After Crash or maybe at the restart
    public void startingSettingsGame()
    {
        alreadyAccelerated = false;
        isFinished = false;
        //ResetCarPosition
        transform.position = initialPosition;
        transform.rotation = initialRotation;
    }

    
	
	// Update is called once per frame
	void Update () {
        if (!isFinished && !isControlledByAI)
        {   
            //Hold the speed of the car: Without not able to steer 
            currentSpeed = rb.velocity.magnitude * 3.6f;

            float moveForward = Input.GetAxisRaw("Vertical");
            float moveSideWards = Input.GetAxisRaw("Horizontal");
            //Accelerating/Braking DATA
            if (moveForward == 1)
            {
                if (!alreadyAccelerated)
                {
                    OnFirstAccelerate();
                    alreadyAccelerated = true;
                }
                isAccelerating = 1f;
            }
            else if (moveForward <= 0)
            {
                isAccelerating = 0f;
            }

            //Turning DATA
            if (moveSideWards == 1)
            {
               // Debug.Log("Sidewards-Debug: Right: " + isTurningRight.ToString());
                isTurningRight = 1f;
                isNotTurning = 0f;
                isTurningLeft = 0f;
            }
            else if (moveSideWards == 0)
            {
                isTurningRight = 0f;
                isNotTurning = 1f;
                isTurningLeft = 0f;
            }
            else if (moveSideWards == -1)
            {
               // Debug.Log("Sidewards-Debug: Left:  " + isTurningLeft.ToString());

                isTurningRight = 0f;
                isNotTurning = 0f;
                isTurningLeft = 1f;
            }
        }

        playSound();

    }

    public void FixedUpdate()
    {
       if (!isFinished)
        {
            float motor = maxMotorTorque * isAccelerating;
            float brake = maxBrakeTorque * (1 - isAccelerating);

            // Maps current speed from 1 to 0.5f
            //This makes it harder to turn at faster speeds and able to turn anyways at faster speeds
            //Needed becasue otherwise steering is calcualted with a speed of 450 -> steering would get weird values
            float mappedSpeed = Map(0, maxSpeed, 1f, 0.3f, currentSpeed);


            //my speed goes above max speed sometimes so we need to fix that later on...
            if (currentSpeed > maxSpeed && motor > 0)
            {
                motor = 0;
            }

            //calculate possible steering, when turning horizontal
            float steering = 0f;
            if (isTurningLeft > 0)
            {
                steering = maxSteeringAngle * -isTurningLeft * mappedSpeed;
            }
            else if (isTurningRight > 0)
            {
                steering = maxSteeringAngle * isTurningRight * mappedSpeed;
            }
            else if (isNotTurning > 0)
            {
                steering = 0;
            }


            foreach (AxleInfo axleInfo in axleInfos)
            {
                if (axleInfo.steering)
                {
                    //Debug.Log("Sidewards-Debug: Steering:" + steering);
                    axleInfo.leftWheel.steerAngle = steering;
                    axleInfo.rightWheel.steerAngle = steering;
                }
                if (axleInfo.motor)
                {
                    axleInfo.leftWheel.motorTorque = motor;
                    axleInfo.rightWheel.motorTorque = motor;
                }
                if (axleInfo.braking)
                {
                    axleInfo.leftWheel.brakeTorque = brake;
                    axleInfo.rightWheel.brakeTorque = brake;
                }
            }



        } 
    }

    public float Map(float OldMin, float OldMax, float NewMin, float NewMax, float OldValue)
    {
        float OldRange = (OldMax - OldMin);
        float NewRange = (NewMax - NewMin);
        float NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin;

        if (NewValue < NewMin)
        {
            return NewMin;
        }
        if (NewValue > NewMax)
        {
            return NewMax;
        }
        //Debug.Log("New Value (mappedSpeed): " + NewValue);
        return NewValue;
    }

    private void playSound()
    {
        if (isAccelerating == 1)
        {
            //slowly turn on engine sound
            audioSource.volume = Mathf.Lerp(audioSource.volume, 1, 0.1f);
        }
        else
        {
            //slowly turn off engine sound
            audioSource.volume = Mathf.Lerp(audioSource.volume, 0, 0.1f);
        }

        if (!audioSource.isPlaying)
        {
            audioSource.Play();
        }
    }
    
    public void OnCollisionStay(Collision collision)
    {
        
        if(collision.gameObject.tag == "Finish" && !isControlledByAI)
        {
            if (!dataSentOnce)
            {
                dataTransfer.SendDataToServer();
                dataSentOnce = true;
            }
            else
            {
                successInfoText.text = "Succesfull trained, Data is sent to Server";
                StartCoroutine(WaitTimeAndShowMenu(3.0f));
            }
            //Debug.Log("Debug OnCollisionStay: " + "Should be called only once");
        }

        else if (collision.gameObject.tag == "Finish" && isControlledByAI)
        {
            successInfoText.text = "Succesfull Autonomous Car, Well Done!";
            StartCoroutine(WaitTimeAndShowMenu(3.0f));
            //Debug.Log("Debug OnCollisionStay: " + "Should be called only once");
        }


    }

    public void OnCollisionEnter(Collision collision)
    {
        if (collision.gameObject.tag == "Wall" && !isControlledByAI)
        {
            successInfoText.text = "Failed, restart Training!";
            StartCoroutine(WaitTimeAndShowMenu(3.0f));

        }
        else if (collision.gameObject.tag == "Finish" && isControlledByAI)
        {
            successInfoText.text = "Failed, go Back To Menu!";
            StartCoroutine(WaitTimeAndShowMenu(3.0f));

        }

    }

    IEnumerator WaitTimeAndShowMenu(float time)
    {
        yield return new WaitForSeconds(time);
        levelManager.showMenu();

    }


    //Build Data for Training
    private void OnFirstAccelerate()
    {
        if (!CarControll.isControlledByAI)
        {
           StartCoroutine(sensors.addInformationList());
        }
    }

}

//Variables for each wheel
[System.Serializable]
public class AxleInfo
{
    public WheelCollider leftWheel;
    public WheelCollider rightWheel;
    public bool motor; // is this wheel attached to motor?
    public bool steering; // does this wheel apply steer angle?
    public bool braking;
}

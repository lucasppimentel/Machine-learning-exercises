using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Obstacle_velocity : MonoBehaviour
{

    public Rigidbody rb;
    public float obsVelocity = 2000f;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void FixedUpdate()
    {
        rb.AddForce(obsVelocity * Time.deltaTime, 0, 0);
    }
}

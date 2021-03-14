using System;
using System.Collections;
using System.Collections.Generic;
using Unity.MLAgents;
using UnityEngine;
using Unity.MLAgents.Sensors;
using Unity.MLAgents.Actuators;

public class MSControl : Agent {

    public Rigidbody rb;
    public Transform tf;
    public float velocity = 100f;
    private Vector3 startingPosition;
    private Quaternion startingRotation;

    public event Action OnReset;
    // Start is called before the first frame update

    public override void Initialize()
    {
        startingPosition = tf.position;
        startingRotation = tf.rotation;
    }

    public override void OnActionReceived(ActionBuffers actions)
    {
        if (actions.DiscreteActions[0] == 1)
        {
            rb.AddForce(0, 0, velocity * Time.deltaTime);
        }

        if (actions.DiscreteActions[0] == 2)
        {
            rb.AddForce(0, 0, -velocity * Time.deltaTime);
        }

    }

    public override void OnEpisodeBegin()
    {
        reset();
    }

    [Obsolete]
    public override void Heuristic(float[] actionsOut)
    {
        actionsOut[0] = 0;
    }


    // Update is called once per frame
    void FixedUpdate()
    {
        if (Input.GetKey("d"))
        {
            rb.AddForce(0, 0, velocity * Time.deltaTime);
        }

        if (Input.GetKey("a"))
        {
            rb.AddForce(0, 0, -velocity * Time.deltaTime);
        }
    }


    public void OnCollisionEnter(Collision collision)
    {
        if (collision.gameObject.CompareTag("obs"))
        {
            AddReward(-1.0f);
            EndEpisode();
        }
    }

    public void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag("score"))
        {
            AddReward(0.1f);
        }
    }

    private void reset()
    {
        tf.position = startingPosition;
        rb.velocity = new Vector3(0, 0, 0);
        tf.rotation = startingRotation;
        OnReset();
    }

}

using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Random = UnityEngine.Random;
using System;

public class Spawner : MonoBehaviour
{

    public GameObject ob;
    public GameObject trigger;
    private float minSpawnIntervalInSeconds = 3;
    private float maxSpawnIntervalInSeconds = 4;
    private List<bool> positions = new List<bool>() {true, true, true, true, true, true , true, true};
    private Vector3 comp = new Vector3(0, 0, 2f);
    private Vector3 atraso = new Vector3(-1f, 0, 0);
    private List<GameObject> spawnedObjects = new List<GameObject>();
    public MSControl player;
  
    // Start is called before the first frame update
    private void Awake()
    {
        
        //Subscribes to Reset of Player
        player.OnReset += DestroyAllSpawnedObjects;

        StartCoroutine(nameof(spawn));
    }

    public IEnumerator spawn()
    {
        for (int t = 0; t < 2; t = t + 1)
        {
            int d = Random.Range(0, 5);
            positions[d] = false;
        }

        for (int a = 0; a < 6; a = a + 1)
        {
            if (positions[a] == true)
            {
                var spawned_trigger = Instantiate(ob, transform.position + a*comp, transform.rotation, transform);
                spawnedObjects.Add(spawned_trigger);
            }
        }

        for (int c = 0; c < 5; c = c + 1)
        {
            positions[c] = true;
        }

        var spawned = Instantiate(trigger, transform.position + atraso, transform.rotation, transform);
        spawnedObjects.Add(spawned);

        yield return new WaitForSeconds(Random.Range(minSpawnIntervalInSeconds, maxSpawnIntervalInSeconds));
        StartCoroutine(nameof(spawn));
    }

    private void DestroyAllSpawnedObjects()
    {
        for (int i = spawnedObjects.Count - 1; i >= 0; i--)
        {
            Destroy(spawnedObjects[i]);
            spawnedObjects.RemoveAt(i);
        }
    }

}

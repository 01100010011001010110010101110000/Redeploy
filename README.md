# Kubernetes Rolling Update Trigger
This is a simply Python 3 script that takes a deployment and namespace as environment variables
and triggers a rolling redeploy of that deployment by appending or updating the `restartedAt` annotation

# Testing

The unit test may be run in the usual way via your IDE or `python -m unittest` from the project root 

## Note
The tests require a running `docker-desktop` kubernetes context
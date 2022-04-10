# Lab1 Iot Devices Networking

This repository simulate the mqtt publisher and subscriber.

`subscriber_simulator.py` is the subscriber simulator that listen for the topic and write to mysql database.

## Setup

1. Copy `.env.example` to `.env` and update the values.
2. Run the docker container by running the `docker composer up -d` command.

Run the subscriber_simulator.py script to start the subscriber simulator.

```bash
python subscriber_simulator.py
```

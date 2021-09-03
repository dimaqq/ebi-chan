# Exponential Backoff Iotaservice

Nicknamed Ebi-chan 🦐

Full description: TBD

#### Quick start

```
git clone git@github.com:ORG/ebi-chan.git
poetry shell
poetry install
adev runserver -p 7890 src/ebi/main.py
```

#### Test

```
pytest
```

#### Tasks

##### GIP level

You may notice that `State.names` continues to grow.
Develop an efficient, timely, Pythonic cleanup for `State`.

##### Mid-career level

Imagine there are so many users of this microservice, that it's set up to auto-scale (wording?)
This means that there are many `ebi` containers running in parallel.
Additionally, these containers may come and go as load changes throughout the day.
A given business logic node will hit a random container.
We want the `ebi` cluster to behave as a logically single entity.
That is, no matter which of the containers the service hits, the result is same.
Assume that deployment provides a fully-qualified domain names that resolves to ip addressed of all containers running at that time.

[Mandatory]
Extend `ebi` to implement this functionality: design algorithms and/or protocols and implement them.

[Optional]
Estimate the total cost of running this service in the public cloud of your choice, in JPY or USD per million requests.

[Optional]
The business logic node may ask for a back-off with a timeout.
 Support this in the code: timed-out request should not increase the delay.

[Optional]
Let's say business logic nodes run in several availability zones, and so will `ebi` containers.
Develop an approach that allows the `ebi` system to survive network partitions.

[Optional]
`terraform` (or other tool) it, for the public cloud of your choice.

[Optional]
Implement HTTP/2 endpoint for this service.

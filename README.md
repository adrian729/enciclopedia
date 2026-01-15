# system-design


## Recognizing systems

- Breaking down system design problem into steps
    - Understanding what the stakeholders need to know 
    - Asking the right questions to clarify requirements
- Level of detail needed
    - features being build
    - requirements
    - accessibility
- The right solution should be logical and achieving the end goal
- Diagram important to break down the requirements and communicate the system flow

Important to make sure the requirements and scope (boundaries) are clear and well defined

### Distributed Systems

- Components separated
- Need to work together
- Design needs to handle **failure** and **scale** across multiple locations

### Common System Components

- **Client**: sends requests, displays data to users
- **Database**: stores, updates, and retrieves data
- **Server**: processes requests, business logic
- **Load** balancer: distributes incomming traffic to keep things running smoothly
- **Cache**: makes things faster by temp storing data


## Requirements

### Core elements

- Translating business requirements
    - What are we trying to solve?
- Designing API and architecture
- Understanding technology and trade-offs

#### Example: TODO app Requirements

    - create todo
    - read todo
    - update todo
    - delete todo

- But, what core features do we need to support?
    - Is it for myself? For several users?
    - Do we need persisting data or it's just for the moment?

#### Strategy

1. Scope the problem (REALLY IMPORTANT!)
2. Design the high-level architecture
3. Address key challenges and trade-offs (Details)

#### Functional Requirements

Describes WHAT the system should do.

- Understant the problem we want to fix
- Understant the scope, what are our boundaries.

1. What are the core features? What should the user be able to do?
2. Who are the users? Are there different kind of users?
3. How do users interact with the system? Phone? Website? App?
4. Any edge cases to consider?
5. What constraints do we have?

##### TODO App Functional Requirements

- Tasks can be only text
- Users should be able to read their todos
- ... create new todos
- ... edit todos
- ... delete todos
- ... re-order todos
- ... archive todos
- ... create a list of todos
- ... edit a list
- ... filter and sort a list
- ... delete a list
- ~~... sharing a list~~ (maybe not this one, adds a lot of complexity)
- ... create account and login with email and password

#### CAP Theorem

CAP theorem is about distributive systems and trade-offs you make

##### Quality

- **Reliability**: the hability of a system to function correctly `over time`
    - **Availability**: the proportion of `time` the system is `operational` and `accessible`
    - **Resiliency**: how well does the system handle `failures`
    - **Consistency**: how well does the system ensure that `all` users see the `same data` at the `same time`

###### `C`onsistency

Every read receives the most recent write or error

###### `A`vailability

Every request receives a (non-error) response

###### `P`artition Tolerance

The system continues to operate even if messages are delayed or lost

##### CAP Theorem Problem

Any distributed system can only `guarantee` 2 out of the 3 -  `C` `A` `P` - at the same time

##### Trade-offs

- ~~**C + A**: only works without network issues~~ -> single server: NOT REALISTIC! Not a distributed system anymore
- **C + P**: always show the latest data but unreliable performance
- **A + P**: always works but might show outdated data

##### Scenarios

1. Banking App -> `C + P`
2. A link shortening service -> `A + P` / `C + P`, it depends, does the link ALWAYS need to redirect somewhere, or is it really important that it redirects to the right place even if sometimes it doesn't work?)
3. An online store -> `C + P` (transactions)
4. A medical team TODO app -> `C + P` / `A + P`, depends on the assumptions taken and how critical the tasks are. If some dosis is given twice that could be a really big issue, but also not knowing what needs to be done. Maybe `A + P` since eventual consistency can be achieved
5. Social TODO app -> `A + P`

##### Takeaways

- In distributed systems, network failures will happen -> ~~`C + A`~~
- You must decide:
    - Latest data
    - Always available
- No perfect system exists, trade-offs are necessary

#### System Quality

- Reliability
    - Availability
    - Resiliency
    - Consistency
- Observability
- Security
- Scalability
- 

#### Non-Functional Requirements

Describe HOW the system should behave/perform.

- How many users do we expect?
    - What is the average RPS?
    - Does this number change in time?
- How consistent does the system need to be?
    - Is it acceptable that some users see slightly outdated data?
- What metrics are important?
    - What is the maximum latency?
- What data needs to be protected?

##### Key Metrics / Requirements

- RPS (requests per second)
- Latency (ms)
- Availability (measured in "nines")
- Back-ups
- Security (encryption, auth, etc)
- Compliance requirements:
    - PII (Personally Identifiable Information)
    - GDPR (General Data Protection Regulation)
- Read / Write heavy (f.e. banking system, lot of reads and not so many writes)
- More...

##### TODO App Non-Functional Requirements

- Only authenticated users can access tasks
- Task operations must complete within 1000ms
- The system must support a total of 1000 registered users, and 10 concurrent users
- All user data must be transmitted over HTTPS

## Modeling

1. `Requirements`: functional / non-functional
2. `Entity Modeling`: define the main functional elements
3. `API Design`: define the actions and operations of the system
4. `Endpoints (Optional)`: 

### TODO App Modeling

1. `Requirements`
    - Tasks can be only text
    - Users should be able to read their todos
    - ... create new todos
    - ... edit todos
    - ... delete todos
    - ... re-order todos
    - ... archive todos
    - ... create a list of todos
    - ... edit a list
    - ... filter and sort a list
    - ... delete a list
    - ~~... sharing a list~~ (maybe not this one, adds a lot of complexity)
    - ... create account and login with email and password
2. `Entities`
    - `user` -> {
            userId,
            username,
            password
    }
    - `task` -> {
        taskId,
        contents,
        status
    }
    - `list` -> {
        listId,
        description,
        tasks
    }
3. `API`


## Protocols

### HTTP

`H`yper`T`ext `T`ransport `P`rotocol

#### Characteristics

- simple
- human readable
- supported by all browsers
- stateless

#### Common Use Cases

- Web Browsers

### WebSockets

#### Characteristics

- bi-directional communication
- persistent connection
- low-latency
- stateful

#### Common Use Cases

- chat apps
- live dashboards
- collaborative editing

### Server-Sent Events 

#### Characteristics

- one-way communication (server to client)
- human readable

#### Common Use Cases

- news feeds
- status updates
- stock tickers

### gRPC

`R`emote `P`rocedure `C`all

#### Characteristics

- binary protocol (HTTP/2)
- strongly-typed contracts (proto buffs)
- requires code generation

#### Common Use Cases

- microservice communication
- performance critical systems
- IoT devices

### REST

`RE`presentational `S`tate `T`ransfer

#### Characteristics

- multiple endpoints
- human readable
- supported by all browsers
- stateless

#### Common Use Cases

- single-sources of data
- CRUD apps
- easily cached data

### GraphQL

`Graph` `Q`uery `L`anguage

#### Characteristics

- single endpoint
- precise data retrieval
- self-documenting API
- strongly typed

#### Common Use Cases

- complex or multiple sources of data (Facebook Homepage)
- apps supporting multiple client types
- decoupling FE from BE development

### Protocol Cheat Sheet

Advice on chosing the proper protocol

- Internal service-to-service communication?
    - `gRPC`

- Need real time updates?
    - Bi-directional communication?
        - `WebSockets`
    - `Server-Sent Events`

- Complext data from many sources?
    - `GraphQL`
- `REST`



# questions / things to check

- pros/cons using int IDs
- pros/cons generate and use UIDs
- pros/cons/why use slugs
    - how to generate them
- SQL basic things (multi-keys, intermediate tables to link other tables f.e. Employee - EmployeeLocation - Location)
- Why cache and split Locations (geo)
    - lat/long
- Types of allocation of data
    - DB
    - File
    - Memory (redys etc)
- 
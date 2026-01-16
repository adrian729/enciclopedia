<!-- vscode-markdown-toc -->
* 1. [Recognizing systems](#Recognizingsystems)
	* 1.1. [Distributed Systems](#DistributedSystems)
	* 1.2. [Common System Components](#CommonSystemComponents)
* 2. [Requirements](#Requirements)
	* 2.1. [Core elements](#Coreelements)
		* 2.1.1. [Example: TODO app Requirements](#Example:TODOappRequirements)
		* 2.1.2. [Strategy](#Strategy)
		* 2.1.3. [Functional Requirements](#FunctionalRequirements)
		* 2.1.4. [CAP Theorem](#CAPTheorem)
		* 2.1.5. [System Quality](#SystemQuality)
		* 2.1.6. [Non-Functional Requirements](#Non-FunctionalRequirements)
* 3. [Modeling](#Modeling)
	* 3.1. [TODO App Modeling](#TODOAppModeling)
* 4. [Protocols](#Protocols)
	* 4.1. [HTTP](#HTTP)
		* 4.1.1. [Characteristics](#Characteristics)
		* 4.1.2. [Common Use Cases](#CommonUseCases)
	* 4.2. [WebSockets](#WebSockets)
		* 4.2.1. [Characteristics](#Characteristics-1)
		* 4.2.2. [Common Use Cases](#CommonUseCases-1)
	* 4.3. [Server-Sent Events](#Server-SentEvents)
		* 4.3.1. [Characteristics](#Characteristics-1)
		* 4.3.2. [Common Use Cases](#CommonUseCases-1)
	* 4.4. [gRPC](#gRPC)
		* 4.4.1. [Characteristics](#Characteristics-1)
		* 4.4.2. [Common Use Cases](#CommonUseCases-1)
	* 4.5. [REST](#REST)
		* 4.5.1. [Characteristics](#Characteristics-1)
		* 4.5.2. [Common Use Cases](#CommonUseCases-1)
	* 4.6. [GraphQL](#GraphQL)
		* 4.6.1. [Characteristics](#Characteristics-1)
		* 4.6.2. [Common Use Cases](#CommonUseCases-1)
	* 4.7. [Protocol Cheat Sheet](#ProtocolCheatSheet)

<!-- vscode-markdown-toc-config
	numbering=true
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->

# <a name='SystemDesign'></a>system-design

##  1. <a name='Recognizingsystems'></a>Recognizing systems

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

###  1.1. <a name='DistributedSystems'></a>Distributed Systems

- Components separated
- Need to work together
- Design needs to handle **failure** and **scale** across multiple locations

###  1.2. <a name='CommonSystemComponents'></a>Common System Components

- **Client**: sends requests, displays data to users
- **Database**: stores, updates, and retrieves data
- **Server**: processes requests, business logic
- **Load** balancer: distributes incomming traffic to keep things running smoothly
- **Cache**: makes things faster by temp storing data


##  2. <a name='Requirements'></a>Requirements

###  2.1. <a name='Coreelements'></a>Core elements

- Translating business requirements
    - What are we trying to solve?
- Designing API and architecture
- Understanding technology and trade-offs

####  2.1.1. <a name='Example:TODOappRequirements'></a>Example: TODO app Requirements

    - create todo
    - read todo
    - update todo
    - delete todo

- But, what core features do we need to support?
    - Is it for myself? For several users?
    - Do we need persisting data or it's just for the moment?

####  2.1.2. <a name='Strategy'></a>Strategy

1. Scope the problem (REALLY IMPORTANT!)
2. Design the high-level architecture
3. Address key challenges and trade-offs (Details)

####  2.1.3. <a name='FunctionalRequirements'></a>Functional Requirements

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

####  2.1.4. <a name='CAPTheorem'></a>CAP Theorem

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

####  2.1.5. <a name='SystemQuality'></a>System Quality

- Reliability
    - Availability
    - Resiliency
    - Consistency
- Observability
- Security
- Scalability
- 

####  2.1.6. <a name='Non-FunctionalRequirements'></a>Non-Functional Requirements

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

##  3. <a name='Modeling'></a>Modeling

1. `Requirements`: functional / non-functional
2. `Entity Modeling`: define the main functional elements
3. `API Design`: define the actions and operations of the system
4. `Endpoints (Optional)`: 

###  3.1. <a name='TODOAppModeling'></a>TODO App Modeling

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


##  4. <a name='Protocols'></a>Protocols

###  4.1. <a name='HTTP'></a>HTTP

`H`yper`T`ext `T`ransport `P`rotocol

####  4.1.1. <a name='Characteristics'></a>Characteristics

- simple
- human readable
- supported by all browsers
- stateless

####  4.1.2. <a name='CommonUseCases'></a>Common Use Cases

- Web Browsers

###  4.2. <a name='WebSockets'></a>WebSockets

####  4.2.1. <a name='Characteristics-1'></a>Characteristics

- bi-directional communication
- persistent connection
- low-latency
- stateful

####  4.2.2. <a name='CommonUseCases-1'></a>Common Use Cases

- chat apps
- live dashboards
- collaborative editing

###  4.3. <a name='Server-SentEvents'></a>Server-Sent Events 

####  4.3.1. <a name='Characteristics-1'></a>Characteristics

- one-way communication (server to client)
- human readable

####  4.3.2. <a name='CommonUseCases-1'></a>Common Use Cases

- news feeds
- status updates
- stock tickers

###  4.4. <a name='gRPC'></a>gRPC

`R`emote `P`rocedure `C`all

####  4.4.1. <a name='Characteristics-1'></a>Characteristics

- binary protocol (HTTP/2)
- strongly-typed contracts (proto buffs)
- requires code generation

####  4.4.2. <a name='CommonUseCases-1'></a>Common Use Cases

- microservice communication
- performance critical systems
- IoT devices

###  4.5. <a name='REST'></a>REST

`RE`presentational `S`tate `T`ransfer

####  4.5.1. <a name='Characteristics-1'></a>Characteristics

- multiple endpoints
- human readable
- supported by all browsers
- stateless

####  4.5.2. <a name='CommonUseCases-1'></a>Common Use Cases

- single-sources of data
- CRUD apps
- easily cached data

###  4.6. <a name='GraphQL'></a>GraphQL

`Graph` `Q`uery `L`anguage

####  4.6.1. <a name='Characteristics-1'></a>Characteristics

- single endpoint
- precise data retrieval
- self-documenting API
- strongly typed

####  4.6.2. <a name='CommonUseCases-1'></a>Common Use Cases

- complex or multiple sources of data (Facebook Homepage)
- apps supporting multiple client types
- decoupling FE from BE development

###  4.7. <a name='ProtocolCheatSheet'></a>Protocol Cheat Sheet

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
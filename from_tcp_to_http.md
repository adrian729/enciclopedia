# From TCP to HTTP

## Table of Contents

- [1. TCP](#1-tcp)
  - [1.1. Reading from a file example](#11-reading-from-a-file-example)
  - [1.2. Reading from the internet](#12-reading-from-the-internet)
  - [1.3. Protocols](#13-protocols)
  - [1.4. Transmission Control Protocol (TCP)](#14-transmission-control-protocol-tcp)
  - [1.5. TCP vs UDP](#15-tcp-vs-udp)
- [2. HTTP](#2-http)


## 1. TCP

### 1.1. Reading from a file example

Imagine we have a really large file.

How can we:

1. Read from the file.
2. Send that information.

What we will be doing most of the time is:

1. Deciding a `chunck` size.
2. Read and send one `chunck` at a time, until we are finished with the file.
3. Close / free the file so others can interact with it!

### 1.2. Reading from the internet

The file reading example is similar to how an internet connection will work.

A file represents some contiguous `piece` of data. An internet connection is also a contiguous `stream` of data!

The difference is, working with a file, we determine how much you read from the file. A connection in the other hand `pushes` data towards you.

- You `pull` data from a file.
- An internet connection `pushes` data towards you.

### 1.3. Protocols

A protocol is a `design` or `spec` for one computer or device to communicate to another.

It descrives how you break down the data, how exactly is it formatted, the header packets, etc... so that the other side can re-construct messages sent across the wire.

### 1.4. Transmission Control Protocol (TCP)

[TCP](https://en.wikipedia.org/wiki/Transmission_Control_Protocol) is a primary communication protocol of the internet, though that is changing with [HTTP3](https://www.cloudflare.com/learning/performance/what-is-http3/) (which is not built on TCP) gaining adoption.

TCP is great because it allows ordered data to be safely sent across the internet.

When data is sent over a network, it is sent in [packets](https://en.wikipedia.org/wiki/Packet_switching). Each message is split into packets, the packets are sent, they arrive (potentially) out of order, and they are reassembled on the other side. And without a protocol like TCP, you can't guarantee that the order is correct...

**TCP example**

Having 8 packets `[1, 2, 3, 4, 5, 6, 7, 9]`, with TCP we would have a `sliding window` that will contain how many packets can we have out in flight at one time.

Let's pretend we have a sliding window of 4.

1. `[1, 2, 3, 4]` <- 4 packets in the `sliding window` can be sent to destination.
2. `1` will be sent. When the receiver needs to send an acknowledgement (ACK).
3. When the `ACK` for packet `1` is received by the sender, the `sliding window` can proceed further [2, 3, 4, 5], so now packet `5` can also be send.

This is how TCP is in order and reliable:

- The window allows to send several packets at once.
- Packets will have some kind of ID so that the receiver can reconstruct the message in order.
- With the ID we are also able to know if we are missing some packet, and if the sender doesn't get an `ACK` it can try re-sending it.

### 1.5. TCP vs UDP

User Datagram Protocol (UDP) is often compared to TCP, as they are both transport layer protocols. Here are the high-level differences between the two:

|                | TCP | UDP |
| :---           | :-- | :-- |
| Connection     | Yes | No  |
| Handshake      | Yes | No  |
| In Order       | Yes | No  |
| Blazingly Fast | No  | Yes |

TCP establishes a connection between sender and receiver with a [handshake](https://en.wikipedia.org/wiki/Handshake_(computing)), and ensures that all the data is sent in order. UDP yeets the data to the receiver and hopes they can make sense of it.

UDP is faster, but also a lot more complex. You need to decide:

- How to break up the data.
- How to organize it.
- How to reconstruct it at destination.
- How does the receiver know it's missing a packet and send a `NACK` so that the sender sends it again.

That's the same reason it is more performant:

- With TCP we need to wait for ACK to continue sending data.
- With UDP we can just send all at once and only care when we get a `NACK` back.

## 2. HTTP


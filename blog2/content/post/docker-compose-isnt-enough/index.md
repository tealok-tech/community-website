---
date: 2024-11-07
draft: false
params:
  author: eliribble
title: "Docker Compose Isn't Enough"
weight: 10
description: "Docker Compose solves real problems in getting applications deployed. It causes problems when deploying many applications. We can do better."
categories:
  - "Engineering"
  - "Ideas"
tags:
  - "Self-Hosting"

# Theme-Defined params
lead: "Docker Compose creates problems as you scale a single server to many applications. We should learn from it and build something better."
comments: false # Enable Disqus comments for specific page
authorbox: true # Enable authorbox for specific page
pager: true # Enable pager navigation (prev/next) for specific page
toc: true # Enable Table of Contents for specific page
mathjax: true # Enable MathJax for specific page
sidebar: "right" # Enable sidebar (on the right side) per page
widgets: # Enable sidebar widgets in given order per page
  - "search"
  - "recent"
  - "taglist"
---
## Summary

<code>[Docker-compose](https://docs.docker.com/compose/)</code> is a tool for working with Docker containers. It solves very real problems with deploying complex applications. By itself it is not enough to make self-hosting applications simple enough for the mass-market. What we need is something like docker-compose, but at a higher level of abstraction that has a concept of SQL databases, local caches, durable storage, service discovery, and resource management.


## What does docker do?

I’m actually going to assume that you’re already familiar with [containerization](https://www.docker.com/resources/what-container/) as popularized by Docker. Metaphorically, you can think of some host system with an unknown configuration like a ship. The ship can be large or small, efficient or not. It has a method for holding some number of containers. It doesn’t need to care what’s in them, only that they are a standard shape and strength.

A basic system diagram running containers looks like this:

![A stacked-block diagram. At the bottom is the system hardware. Above that is the operating system. Above that is the container runtime, reverse web proxy, and database which run on the operating system. Above the container runtime are containers for an application, including a webapp container and an API container](containers-without-compose.png "If I had an artist on staff I would have put these blocks into a happy whale-shaped container ship for hopefully obvious reasons.")

You've got some hardware with an operating system and a container runtime. Containers run within the runtime and talk to some other services like databases or a webserver.

## What does docker-compose do?

<code>[Docker-compose](https://docs.docker.com/compose/)</code> is a tool for specifying groups of containers that work together. I’m also going to assume in this article that you’re familiar with the basics. <code>Docker-compose</code> kinda breaks our metaphor - within shipping there’s no reason a given ship would need to position some number of containers together and let them communicate with each other.

This may seem like a minor point, but I want to expand upon it. The entire point of containers is simplifying operations by standardizing the interface. `Docker-compose` breaks the standardization and recreates the problems that containers originally solved. Within shipping there is the concept of the [intermodal freight system](https://en.wikipedia.org/wiki/Intermodal_freight_transport). `Docker-compose` should have been like intermodal freight - standardizing interactions between commonly used tools and reducing the cost of switching carrying networks.

That said, `docker-compose` has been extremely popular as a tool for specifying how to deploy self-hosted applications. It’s declarative and makes it possible to get multiple separate processes (web server, database, cache, background workers, API) to communicate with each other. In order explain where `docker-compose` falls short it’s useful to build up to an example.


### Pihole

Let’s look at an application that lots of people want to self-host: [Pihole](https://pi-hole.net/). Here’s [an example docker-compose file](https://github.com/pi-hole/docker-pi-hole/blob/master/examples/docker-compose.yml.example):


```
# https://github.com/pi-hole/docker-pi-hole/blob/master/README.md

services:
  pihole:
    container_name: pihole
    image: pihole/pihole:latest
    # For DHCP it is recommended to remove these ports and instead add: network_mode: "host"
    ports:
      - "53:53/tcp"
      - "53:53/udp"
      - "67:67/udp"
      - "80:80/tcp"
    environment:
      TZ: 'America/Chicago'
      # WEBPASSWORD: 'set a secure password here or it will be random'
    # Volumes store your data between container upgrades
    volumes:
      - './etc-pihole:/etc/pihole'
      - './etc-dnsmasq.d:/etc/dnsmasq.d'
    #   https://github.com/pi-hole/docker-pi-hole#note-on-capabilities
    cap_add:
      - NET_ADMIN
    restart: unless-stopped # Recommended but not required (DHCP needs NET_ADMIN)  
```


This is pretty complex because pihole is a DNS server. We have the `name` and the `image` to use, then a slew of ports to open up (53 for the DNS queries, 67 for DHCP, 80 for the web admin interface). There’s some `environment` that gets passed to the container, including the timezone we are running in and the ability to set a password. `Volumes` mounts some data from the host into the container, in this case it’s two different directories that store configuration data that can be changed from the web interface. `Cap_add` grants additional capabilities to the container, `NET_ADMIN` specifies the ability to configure network interfaces. Finally, `restart` specifies the behavior when the container crashes. In this case we bring it back up since our entire network is going to depend on it.

Whew! That’s a lot of stuff! And this is running just one container for pihole. It could, in theory, have a separate container for the web admin interface, a separate database, a batch processing container, and on and on.

Pihole could be more like Jitsi Meet


### Jitsi Meet

[Jitsi Meet](https://jitsi.org/jitsi-meet/) is complex software. It comes with [a system](https://jitsi.github.io/handbook/docs/devops-guide/devops-guide-docker/) for *generating* a `docker-compose` configuration. That configuration involves 4 different containers in a single network, 7 volumes, 9 ports, and 200+ lines of environment configuration.

I won’t reproduce it here.

This is a bit extreme, but not very much.

Let’s look at some others.


### Other Applications

I’m going to choose a few applications that are popular in the self-hosting community, and that I’m familiar with. Some have a single `docker-compose` configuration, others use scripts to generate it, others have a menu of configurations that you choose from.


<table>
  <tr>
   <td>Software
   </td>
   <td>Containers
   </td>
   <td>Ports
   </td>
   <td>Volumes
   </td>
  </tr>
  <tr>
   <td><a href="https://docs.goauthentik.io/docs/install-config/install/docker-compose">Authentik</a>
   </td>
   <td>Postgres, redis, server, worker
   </td>
   <td>Http, https
   </td>
   <td>Database, redis
   </td>
  </tr>
  <tr>
   <td><a href="https://github.com/nextcloud/all-in-one/blob/main/compose.yaml">Nextcloud</a>
   </td>
   <td>Master, caddy (optional)
   </td>
   <td>Http (main), http (service), https
   </td>
   <td>master
   </td>
  </tr>
  <tr>
   <td><a href="https://immich.app/docs/install/docker-compose/">Immich</a>
   </td>
   <td>Server, machine-learning, redis, postgres, 
   </td>
   <td>2283 (?)
   </td>
   <td>Upload, localtime, cache, postgres-data
   </td>
  </tr>
  <tr>
   <td><a href="https://jellyfin.org/docs/general/installation/container/">Jellyfin</a>
   </td>
   <td>jellyfin
   </td>
   <td>None - host networking
   </td>
   <td>Config, cache, media1, media2, fonts
   </td>
  </tr>
  <tr>
   <td><a href="https://docs.paperless-ngx.com/setup/">Paperless NGX</a>
   </td>
   <td>redis, db, webserver
   </td>
   <td>http
   </td>
   <td>Cache, postgres-data, data, media, export, consume
   </td>
  </tr>
</table>


On the positive side `docker-compose` is **far** **easier than raw docker commands.** Each of these configurations would take dozens, if not hundreds of `docker` commands to reproduce. `Docker-compose` is a huge improvement over the existing alternatives.


## The Problem

The problem is that `docker-compose` is **too flexible**, **too detailed,** and **operates at the wrong layer of abstraction**. Each of the applications above have some kind of HTTP-handling process. Each of them have a cache or a database (or both). Every single one has one or more volumes for dealing with persistent data.

These applications leave database backup as an exercise for the system operator. Getting back to the shipping metaphor, let’s pretend databases are our railway lines. If you run multiple container workloads on a single host using `docker-compose` it’s like hand building a crane out of wood to move your container to your rail lines rather than enjoying the benefits of [container cranes](https://en.wikipedia.org/wiki/Container_crane).

The problem is best detailed by looking closely at the number #1 issue when using `docker-compose` - reverse http(s) proxies.


### Reverse HTTP proxies

A reverse HTTP proxy is a program that receives incoming HTTP requests and forwards them on to another program. It stands in as a proxy for the program itself on *incoming* requests. The fact that it’s incoming instead of outgoing is what makes it a “reverse” proxy.

Each of the programs above have some kind of administrative or user interface that is served over HTTP. 

For each program the developers must decide: do we include a web server or not?

Frankly, you’re damned if you do. You’re also damned if you don’t.


#### Included Web Server

If you include a web server then your program will work, including the browser-based interface. It will only work on a particular port, and unless you use host networking, a specific container-only IP address.

If you run IPv4 networking and more than one container with a web server, you’ll need to remap their ports on the host. Then you’ll need a reverse proxy, with its bespoke configuration, to pass web requests to this web server. You have at least two web servers to serve one application.

If every program does this we end up deploying multiple redundant programs doing approximately the same work, taking up compute resources.


#### No Web Server

If you don’t include a web server then at least you aren’t wasting resources through redundant server processes. Instead, you have to configure the application without an administrative interface (config files, environment variables) so that it can communicate with the web server you provide. This may include generating static assets (HTML, CSS), setting headers (CORS, Authentication), and breaking requests out to different ports based on their path.


#### DNS

Your web interface is going to have an address, whether it’s available on the public internet or not. If you want TLS ([and you do](https://smallstep.com/blog/use-tls/)) then you’ll need a name, not just an IP address. If you run multiple services on a single host you’ll need to route requests either by domain name or by path (please choose domain name).

If your service is publicly addressable, you can register a domain name and use [Let’s Encrypt](https://letsencrypt.org/). If your service is not publicly addressable, you can [run your own certificate authority](https://smallstep.com/docs/step-ca/). Either way, you’re going to need an automated system for getting new certificates, or you’re going to need incredible patience for toil.


#### Ports

Really, the problem is ports. `Docker-compose` allows for exposing and remapping ports. This is great if you want arbitrarily complex networking setups.

We want to be able to support arbitrarily complex networking setups.

We don’t want applications to actually use them.

What we want is for an application like Immich not to say “I expose some networked service on port 2283, read the manual and find out what it is and how dangerous it might be!” What we want is for Immich to say “I need an HTTPS proxy in front of me to handle client requests. Please let me know what domain name it's using so I can configure myself internally accordingly.”


### Databases

Okay, I said reverse proxies are the #1 issue. Databases are issue #1 ½

Docker [says](https://docs.docker.com/get-started/docker-concepts/running-containers/persisting-container-data/):

“When a container starts, it uses the files and configuration provided by the image. Each container is able to create, modify, and delete files and does so without affecting any other containers. When the container is deleted,** these file changes are also deleted**.” (emphasis mine)

So a `docker-compose` file says it needs a database. By nature, that database container is going to delete everything when the database stops. The smart developer then adds a volume to the `docker-compose` file to store the database contents.

What happens if I hit the machine with a sledgehammer?

Your volume won’t save you.


#### N+1=2 or something

You can save your database from my sledgehammer, or at least the resulting consequences to your application, by having an off-site backup.

Do you know how to backup Authentik?

Me neither.

I could probably do okay by iterating over all of the volumes on the service and copying the files in the volume. That may be wasteful and capture files I don’t care about. It may also produce corruption unless I take the service offline.

You could modify the `docker-compose` configuration and add in a sidecar that stops the database server and exports its databases into a backup-friendly format, then export that from the cluster.

You could also do some [crazy stuff ](https://www.howtoforge.com/tutorial/how-to-use-snapshots-clones-and-replication-in-zfs-on-linux)with filesystem-level replication.

There be dragons.


#### Waste

Did you know that one database server can service many logical databases? It can! So, if each of your services bundles a separate database server process we are wasting compute resources, just like a reverse proxy. Nobody needs 5 copies of Postgres fighting for context switches on the same system. Run one Postgres, have it manage 5 databases.

Can one learn this power? Not from `docker-compose`

### In Pictures

To summarize the problem I drew this pretty diagram of services running with docker-compose:

![Another block diagram that starts with hardware, an operating system, and a container runtime. This time we have multiple database containers in the container runtime talking to volumes and a port remapper between the webapp containers and the reverse proxy. There's duplicate containers for everything.](containers-with-compose.png "This image really understates how annoying it is to have dozens of services that need manual port remapping and how annoying it is to figure out what the hell any given application is doing with each of the 5 ports they want to expose.")


## The Solution

Okay, maybe not “the” solution, not yet, but certainly **a solution**.

Let’s move up a layer of abstraction. Instead of talking about meaningless interchangeable container images and opaque network protocols let’s add some semantics. Our semantics are going to delimit the kinds of containers that we can depend on: databases, reverse web proxy, cache, static web assets, etc.


### An Example in Semantics

Here’s a configuration for a pretend web app  in `docker-compose`:


```
services:
 web:
   build: .
   ports:
     - "8000:5000"
 redis:
   image: "redis:alpine"
```


From the view of docker this is just two containers on the same network (which is implied) and exposing a single port. The actual type of containers and the protocol of the port is meaningless.

Now I’m going to introduce a new configuration format for my higher-level semantic constructs. I’m not using YAML, [it’s garbage](https://news.ycombinator.com/item?id=12423733). I’m going to use TOML


```
service = "mywebapp"
build = "."

[https]
reverse-proxy = true

[cache]
variant = "redis"
```


In this snippet I’m providing a name for the application. I’m still building a container image from the current directory. I’m specifying that I want an https-capable reverse proxy. I don’t specify a port - the container will always use a standard port for incoming requests from the reverse proxy. That’s because I didn’t tell you, but each of these containers gets an IPv6 address within a specific subnet, so all the containers on a host don’t have to fight for the same pool of ports. I also specify I want a caching service, one that specifically speaks “redis”, but the actual provider is up to the runtime.


### Solution #1

This already solves most of the reverse proxy problems: 



* Each program requests a reverse proxy, it doesn’t instantiate one. No duplication, no waste.
* That reverse proxy provides the DNS name the program runs at on a standard environment variable. It’s not configurable on purpose.
* The reverse proxy can be informed by the container of assets that should be extracted from the container image and made available by the reverse proxy. The runtime handles the extraction.
* The reverse proxy forwards all paths (that aren’t static assets) to the program without the need for configuration in the reverse proxy. The application will need to conform to this rather than doing whatever the developers think of and being a snowflake.


### Solution #1.5

Okay, so what about databases?


```
service = "myphotoapp"
image = "github.com/eliribble/iminurphotos"

[https]
reverse-proxy = true

[database]
variant = "sql:2023"
permissions = "full"
```


The only new items here are the `database` section. It specifies we need a database that complies with the 2023 version of the SQL standard and that the program expects “full” permissions. This means the applications will create the schema and populate the tables and will take no care to coordinate with other programs within the database.

If an application needs a specific database it can specify a given variant. In general, I’d encourage app developers to be standards-compliant and avoid requiring specific database variants. This allows operators the freedom to choose a database that’s best for them.

With this configuration - database owned outside the application - operators are free to stream replication to a second host, create backups, and store those backups however they see fit. This only needs to be configured once and any number of applications can benefit.


### What About Ports?

Like I said before, each program gets its own IPv6 address that’s routable over the network the host is on. This means I can run Jellyfin and Paperless NGX on the same host and they can both use [well-known port numbers](https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers) for HTTP (80). Since we care about security, we’re going to use a firewall to prevent anything but the reverse proxy from accessing that port.

Applications that bind to port 443 are expected to terminate their own TLS and have a facility for handling certificates. This doesn’t need to be negotiated or configured. If the application binds to that well-known port, it’s expected they are using the corresponding protocol, and they are responsible for it.

Pihole should still bind port 53, which is the standard for DNS. Since it has a valid IP address on the network, it can receive DHCP on port 67 and respond properly.

In a lot of ways we got here because containers default to IPv4. This meant there was contention between containers for the host’s port numbers. This meant we couldn’t use standard port numbers. Then we had to communicate what we were doing on non-standard port numbers out-of-band through product documentation.

If you start with IPv6 you can have multiple addresses on a single adapter. Then you can have an address per container. Then you can use standard port numbers. Then you can add semantics to your runtime about the right ways to handle the different protocols. Adding all of this together makes it possible to have a single runtime that can run all your applications with standardized interfaces.

### Moar Pictures

!["Another block diagram. Hardware and operating system on the bottom. The container runtime has just one block - the Tealok runtime. Within that runtime is the webproxy, database, and storage volumes. It also has an arrow out to offsite backups. Above the Tealok runtime is a number of application containers."](containers-with-tealok.png "I haven't decided yet whether or not Tealok should enforce an application having a single container. I'm leaning toward doing it. It certainly makes the diagram cleaner.")

## Tealok - A New Container Runtime

Tealok is a runtime we’re building for running containers. It’s like an [intermodal freight transport system](https://en.wikipedia.org/wiki/Intermodal_freight_transport) in the [ongoing extended metaphor](https://www.docker.com/resources/what-container/) Docker started over a decade ago. Tealok imposes certain constraints on containers and provides standardized interfaces. 

Tealok runs on Linux hosts. You tell it what applications you want to run and it runs them. The applications tell Tealok what they need and Tealok supplies it to the application. Tealok gets TLS certificates, runs a reverse proxy, sets up DNS records, and makes backups. For operators it helps avoid waste, ensure consistent good practices, and reduces the burden of managing individual snowflake deployment configurations. For application developers it makes it easier to make decisions about how their application is deployed.

Tealok’s designed to make hosting applications operationally simple. So simple, in fact, that anyone who can use a phone can have a Tealok and own their own cloud computing. This means owning your data, owning your services, and owning your destiny. Join us by subscribing to our mailing list, preordering some hardware, or contributing to the project.


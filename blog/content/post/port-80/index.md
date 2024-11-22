---
date: 2024-11-21
draft: false
params:
  author: eliribble
title: "Port 80"
weight: 10
description: "Problems I faced trying to run simple web applications on port 80 on my residential internet service."
categories:
  - "Engineering"
  - "Internet Service Providers"
tags:
  - "Self-Hosting"
  - "Blocking"

# Theme-Defined params
lead: "Handling requests on port 80 is a basic building block of web applications. Too bad we can't all just...do that."
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
I live in Gilbert Arizona. I have access to fiber-to-the-home. The fiber is owned by Cox. This means that even though I hate them, Cox is the best option for my home Internet service.

Recently I was working on [Tealok](https://github.com/tealok-tech/tealok/), specifically trying to figure out if it’s possible to run a group of containers within [Docker Swarm](https://docs.docker.com/engine/swarm/) on a single node using IPv6 for incoming traffic. The goal is for [Traefik](https://traefik.io/traefik/) to terminate TLS and run as a reverse proxy for a number of different services that have a web frontend.

IPv6 support in Docker Swarm has [a still-open bug from 2016 around IPv6 networking](https://github.com/moby/moby/issues/24379). The long and short of it is: you can’t run a container inside the swarm that can receive incoming traffic on an IPv6 address on the host.

What does this have to do with port 80? I’ll get there.

Before I do, I want to thank several people who posted workarounds on that Docker Swarm bug. [Msva](https://github.com/msva) had the best comment about using `systemd-socket-proxyd` as a workaround due to its architectural consistency. Unfortunately for me, I’m running NixOS which, for some unknown-to-me reason, does[ not include systemd-socket-proxyd](https://search.nixos.org/packages?channel=24.05&from=0&size=50&sort=relevance&type=packages&query=systemd-socket-proxyd). [Benz0li](https://github.com/benz0li) gets a shout-out for authoring [docker-swarm-ipv6-nftables](https://github.com/b-data/docker-swarm-ipv6-nftables) which has a detailed breakdown of a setup doing exactly what I want (though I couldn’t use it directly). Final thanks goes to [MatthieuBarthel](https://github.com/MatthieuBarthel) for a `socat`-based solution, since NixOS *does *have `socat`.

At this point I spun up Traefik and got a certificate and everything was fine and I went on with my life.

I’m kidding, it didn’t work, of course. Turns out [Let’s Encrypt](https://letsencrypt.org/) couldn’t reach my web server to confirm I owned my domain and give me a TLS certificate.


# Are you there port 80?

I rent a VM in a Las Vegas datacenter. I’m hard-core that way. I disabled the IPv6 firewall on my home router and started testing ports. I started [netcat](https://linux.die.net/man/1/nc) on the server on a [random](https://xkcd.com/221/) [non-system-so-above-1024](https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers#Well-known_ports) port:


```
nc -6 -l 5454
```


On the VM we connect up using my IPv6 address


```
nc  -zv 2001:0DB8::1 5454
Connection to 2001:0DB8::1 5454 port [tcp/*] succeeded!
```


Okay, so at this point I know that most of the pipe is working. The address is correct, the router is forwarding correctly. Must be a port thing. I tested port 443, which is standard for HTTPS connections. It worked fine.

In a grand epiphany I even [disabled the web admin interfac](https://help.mikrotik.com/docs/spaces/ROS/pages/103841820/Services)e on port 80 of my router.

Did it work? No, it didn’t work.


# Building a Table Stochastically

I’m an engineer now, but in high-school I liked to[ pretend to be a scientist](https://www.soinc.org/). As a retired junior pretend scientist I ran a bunch of tests and built up a table of ports that worked and ports that didn’t. It looked like this:


| Port | Works |
| ---- | ----- |
| 5454 | yep   |
| [443](https://en.wikipedia.org/wiki/HTTPS)  | Uh, yeah. WTH |
| 81   | Yes   |
| [80](https://en.wikipedia.org/wiki/HTTP)   | No.   |
| [23](https://en.wikipedia.org/wiki/Telnet) | Yes?! |
| [25](https://en.wikipedia.org/wiki/Simple_Mail_Transfer_Protocol) | No, WTF! |


I’m really just rebuilding the [official Internet Ports Blocked or Restricted by Cox page](https://www.cox.com/residential/support/internet-ports-blocked-or-restricted-by-cox.html).

Are there good reasons to block ports by default? [Yes](https://en.wikipedia.org/wiki/Timeline_of_computer_viruses_and_worms). Is there a good reason that you can’t tell Cox that you pinky-swear you know what you’re doing and you want the port unblocked? No.

Is this a mechanism for Cox to sell Business-class Internet?

Oh, very yes.


# To Business or Not To Business

Thankfully, Cox publishes enough information for me to do some price comparison without having to speed-up my cellular ennui by talking to their salesdrones. I pay $100/month for 250 Mbps symmetric fiber without a data cap on the residential plan. I can pay $90/month for 300 Mbps symmetric without a data cap and **a 2 year agreement**. The last time I had an agreement with Cox it cost me because they renewed the full term of the agreement contrary to what their representative told me and I got to pay for a bunch of months I couldn’t use.

I hate Cox.

I also love fiber.

Here’s the thing though. Tealok is about fighting for the user. Lots of users are going to be stuck with residential fiber, which means they won’t be able to use port 80 because Cox decides it’s in their business interests to behave that way. If I just sidestep this whole issue I won’t be building for our users.

So I’ll need to find another way.


# Non-Standard Ports

We could in theory just configure services on a non-standard port. There are 65526 ports that aren’t blocked by Cox and for any service we could specify the port: https://service.my.tld:8123. This has some serious drawbacks:



* We can’t use straightforward [HTTP-01 challenge mode](https://letsencrypt.org/docs/challenge-types/) to get TLS certificates. DNS-01 could still work. [Traefik](https://doc.traefik.io/traefik/https/acme/#tlschallenge) and [Caddy](https://caddy.community/t/caddy-supports-the-acme-tls-alpn-challenge/4860/2) both support TLS-ALPN-01, which will work.
* When you type “service.my.tld” into any browser it’s going to default to a request to port 80. You can be specific and type “https://service.my.tld” and it’ll go straight to port 443, which will work, but if you forget the prefix you’ll see an ugly error. We can mitigate this to some extent with [HSTS](https://www.chromium.org/hsts/).
* Webcrawlers will never find the service. This can be a pro and a con, depending on what services you want to run. Your photo collection? Fine. Your influencer blog? Not-fine.

Ultimately non-standard ports are going to artificially limit our users. We fight for the user. Cox started this problem, but we should be able to work around it.


# More Proxying

Ultimately we could just [add another layer of indirection](https://en.wikipedia.org/wiki/Fundamental_theorem_of_software_engineering). We run a service in a datacenter that is highly available and has no restrictions on port 80. DNS records for our service point at this service. The service then forwards the connection on to the user’s Tealok using an outbound-only connection that the Tealok made to the service.

There are plenty of solutions for creating network tunnels in the [awesome-tunneling list](https://github.com/anderspitman/awesome-tunneling). These are all self-hostable, if you happen to rent (or own!) a server in a datacenter with a public IP address and no blocks on port 80 and port 443.

Alternatively we could use a provider. Tunneling is cheap enough that it’s actually free from some places. [Cloudflare offers this service for free](https://blog.cloudflare.com/tunnel-for-everyone/). The problem is that Cloudflare will only configure tunnels for DNS entries they are managing. I don’t want to Cloudflare-ify my entire setup just to get this one thing, so here’s a list of providers that also do free tunneling **without** owning your DNS:



* [https://localhost.run/](https://localhost.run/)
* [https://serveo.net/](https://serveo.net/)
* [https://telebit.cloud/](https://telebit.cloud/)

There are also a bunch of providers you can pay for tunnels. Here’s a few I found:



* [https://burrow.io](https://burrow.io)
* [https://pagekite.net](https://pagekite.net)
* [https://ngrok.com](https://ngrok.com)

If you want to host this yourself in a datacenter, I’d recommend the standout at ~85k stars: [frp](https://github.com/fatedier/frp). It’s listed as a “comprehensive open alternative to [ngrok](https://ngrok.com/).” Apache 2.0 [license](https://github.com/fatedier/frp/blob/dev/LICENSE). Works for me. I got what I needed:

On the datacenter system at `/etc/frps.yaml`:


```
bindPort = 7000
vhostHTTPPort = 80
```


Then run `frps -c /etc/frps.yaml`.

On the blocked-network system at `/etc/frpc.yaml`:


```
serverAddr = "insert public IP of datacenter system"
serverPort = 7000

[[proxies]]
name = "web"
type = "http"
localIP = "127.0.0.1"
localPort = 80
customDomains = ["domain1.com", "domain2.com"]
```


Then run `frpc -c /etc/frpc.yaml`.

At that point you can create a DNS entry for `domain1.com` that points to the public datacenter server. Requests for `domain1.com` that come to that server on port 80 will then be forwarded on to the blocked-network system.

Neat.


# No Datacenter Server, No Problem!

Okay, but the whole point of Tealok is to *not need to rent datacenter systems*. For that we’ll use one of the free hosted options. I picked [localhost.run](https://localhost.run). From their landing page, just run this:


```
ssh -R 80:localhost:80 nokey@localhost.run
```


You’ll be given a URL like [https://48f572f458b266.lhr.life](https://48f572f458b266.lhr.life)

Open that in your browser and you’ll see the response from Traefik which is proxying for Tealok.

There’s just a few problems with this:



* Ssh-based tunnels [aren’t stable](https://localhost.run/docs/faq#my-connection-is-unstable-tunnels-go-down-often) without some configuring.
* Individual applications may [need some configuring](https://localhost.run/docs/faq#i-can-see-requests-to-localhost8080-when-browsing-my-site-thru-localhostrun) as well to understand they are being tunneled.
* Unless you pay, localhost.run (reasonably) [constantly shifts your domain name](https://localhost.run/docs/faq#my-tunnel-name-changes-every-time-i-connect).


# I Thought You Said ‘No Problem’

Okay, they aren’t *problems*, they are just…the kind of bumps we frequently encounter when self-hosting. It’s actually incredibly generous that several companies provide free, temporary tunnels for the public to use. If you need something running in a datacenter because your ISP is monopolistic garbage, then you have to pay for it.


# What Are We Going to Do About It?

We’re developing Tealok in the open, and it will stay open. We also have a company, Gleipnir, which will provide services to self-hosters to overcome these kinds of issues. The goal is to be a single service that will help you overcome arbitrary limits, skills issues, and unknown-unknows to make you successful running Tealok.

At this point, we're still developing the kinds of services that Gleipnir will offer. We're not offering any services yet. If you've got services you'd like to see us offer, [send us an email](mailto:contact@tealok.tech), join [our mailing list](https://mailing-list.tealok.tech/subscription/form) for updates or [contribute to the project](https://github.com/tealok-tech/tealok).

Tealok’s designed to make hosting applications operationally simple. So simple, in fact, that anyone who can use a phone can have a Tealok and own their own cloud computing. This means owning your data, owning your services, and owning your destiny. 

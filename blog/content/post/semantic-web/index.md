---
date: 2024-12-17
draft: false
params:
  author: benjaminsperry
title: "Tealok: Building the Semantic Web They Promised Us in 1989"
weight: 10
description: "Hey Internet, where's my Semantic Web?"
categories:
  - "Vision"
tags:
  - "Solutions"

# Theme-Defined params
lead: "Tim-Berner's Lee personally promised me I could have a semantic web. This was back when I was 7. I'm still waiting."
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
In 1989, [Tim Berners-Lee](https://en.wikipedia.org/wiki/Tim_Berners-Lee), one of the original inventors of the [World Wide Web](https://en.wikipedia.org/wiki/World_Wide_Web) (that big internet thing you may have heard of), described his vision of the internet as a *[semantic web](https://en.wikipedia.org/wiki/Semantic_Web) of data*.


## What is the Semantic Web?

At Berners-Lee's time, the[ web](https://en.wikipedia.org/wiki/Web_2.0#Web_1.0) was a group of interconnected pages. This structure still forms the foundation of the internet today. However, there is a limitation: linking only connects pages without giving machines any understanding of the actual information contained on those pages. For a page to be understood, a human has to read it.

This approach worked when the web was small, but in today’s world of endless information, it’s no longer practical. Berners-Lee’s vision was to [link data itself](https://en.wikipedia.org/wiki/Linked_data), not just pages. Imagine reading a recipe on one webpage and instantly seeing nutritional information, alternative ingredient suggestions, or similar recipes from other sites. Or consider a research paper that links directly to related studies, datasets, or visualizations. Such interconnected data would transform web navigation into a fluid experience, where information builds upon itself, saving time and enhancing usability.


---


## Where Are We Today?

So, where are we nearly 35 years later? We’ve made progress—baby steps, really—but the web remains a patchwork of disconnected islands.

Google leads the charge. As the de facto search engine, their influence has persuaded millions of website creators to tag their data with [semantic markers](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data), incentivised by improved search rankings. This has had an interesting side effect: Google can now understand that data well enough to deliver special insights, even before you click on a page.

Take recipes, for example. Search for a recipe, and Google doesn’t just point you to a list of links—it gives you the basic ingredients, instructions, and cooking times right there in the search results. That’s not magic. It’s the result of recipe sites using semantic tags to describe their content in a way machines can understand. Google aggregates all of that data to produce a clean, generalized recipe that matches your search.

Microsoft, too, has worked hard to realize some of the benefits of the semantic web. Behind every Office365 organization, there is a semantic [graph](https://learn.microsoft.com/en-us/graph/overview) that maps the relationships between documents, email, and Teams messages. This is how they can suggest documents to attach to your email and provide you with universal search across your work-related items.

The offerings from Google and Microsoft provide value to the user—but it’s a double-edged sword. They also provide value to Google and Microsoft, often at the expense of the user. And all of the value they create is trapped inside their respective ecosystems. One project that provides value in a more public way is **[DBpedia](https://www.dbpedia.org/)**, an effort by volunteers to semantically enhance Wikipedia articles. DBpedia enables links between individual data elements, which is why Wikipedia articles feature helpful summary tables and interlinked content.

When it comes down to it, though, users are still not receiving the full benefit of what the semantic web promised.


---


## Why Don’t We Have It?

"If it’s so great, why don’t we have it? Don’t Google, Apple, and Microsoft love me and want to help?"

Google, Apple, Microsoft, and Facebook love you the way a rancher loves cows. You are a resource, not a person. They love you most at slaughter time when you’re being divided up to be sold to advertisers and other paying customers.

They are only interested in providing value to you when it aligns with higher sales of your personal data. Building a truly open semantic web would mean breaking down walls and filling in moats—steps that no SaaS provider wants to take.If big tech ever implements a broader semantic web, it won’t be for *your* benefit.

So, there is no business reason for the semantic web to be realized, and it won’t be on a large scale until we change the incentives. Instead of waiting for everyone else to semantically define data for us, we’re going to have to start with our own data pile and build our *own* personal semantic webs.

The answer is to take control of your data. By self-hosting your own server and creating a personal knowledge graph, you unlock the full potential of your data and prepare to make the world a better place.


---


## How Does It Work?

Fortunately, there has been a lot of effort and brainpower invested in solving this problem over the years, so we aren’t starting from scratch. The real innovation is the idea that all information can be broken down into atomic statements—representations of information at its smallest possible level without losing meaning. These statements typically take the form of [subject : predicate : object]. For example:



* [Benjamin : has the surname : Sperry]
* [Benjamin : has the eye color : blue]

It’s the collection of these statements taken together that defines an entity. When data is organized this way, it can be reassembled into more complex structures to serve a variety of purposes.

Tealok takes data from any application and defines an ontology and a schema for it—a map of what the data means and how it relates to other pieces of information. Using this framework, Tealok breaks the data into [triple](https://en.wikipedia.org/wiki/Semantic_triple) statements and stores them in a Universal Data Layer (UDL)—a new foundational layer that encompasses *all* data attributed to you, not just the knowledge you create or consume. Just as the Resource Description Framework ([RDF](https://en.wikipedia.org/wiki/Resource_Description_Framework)) serves as the semantic layer for the semantic web, the UDL transforms your data into a fluid, interconnected resource. Once the data resides in the UDL, it can be searched, compared, or reconstructed—not just for the app that created it, but for any other app you choose to share it with.

Because your data is stored as atomic statements instead of complex, rigid structures, sharing becomes more powerful and flexible. Imagine setting rules like: “Make all my landscape photos that don’t include people public,” or “Share this list of party guests with all invitees, but exclude their phone numbers, addresses, and nicknames.”


## **Conclusion**

The semantic web is a vision of interconnected data that works for you, not corporations. While big tech hoards this capability, solutions like **[Tealok](https://tealok.tech/)** give you the power to build your own semantic web. By taking control of your data, you unlock smarter connections, better insights, and seamless usability.

You never knew you wanted the semantic web, but once you experience its potential, you’ll wonder how you lived without it.


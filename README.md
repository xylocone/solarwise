## Introduction

As part of our DSC-15 course titled _Software Engineering_, we are required to submit an academic project in the form of our practical assignment.

In this document, we present the **Problem Statement**, the **Team** and a general **Overview** of the way in which we will proceed with a solution to the problem.

---

## Problem Statement

The problem we will be addressing is **1590 of Smart India Hackathon 2024**. The following is the text of the problem:

> Innovative ideas that help manage and generate renewable/sustainable sources more efficiently.

### Interpretation

As is evident from its text, the above-stated problem is quite vague; several sub-problems can fall under its ambit. We have, therefore, in the interest of focused clarity, narrowed down its scope and interpreted it to mean the following:

> **Objective**: The objective of this hackathon challenge is to develop a comprehensive application that can allow consumers to _assess potential benefits_ associated with adopting _solar energy_ as a source of electricity at their homes.
>
> **Potential Features**:
>
> 1. User-friendly interface for inputting relevant information such as _geo-location, roof area, type of Photovoltaic technology_, with the option to add additional configuration such _azimuth orientation, slope of the panels etc._
> 2. Illustrative output, with charts and infographics, that showcases the _potential power generation, savings in electricity costs, carbon offsets etc._ associated with adoption of solar power for the input location and other parameters.
>
> **Deliverable**: A web-based solution (mobile and web application) that implements the features and achieves the objective stated above.

---

## Overview of Solution

### Deliverables

We propose to build:

- A [PWA](https://en.wikipedia.org/wiki/Progressive_web_app) that takes in certain inputs regarding the location and configuration for the solar panels that the user wishes to install at their property, and outputs such information as potential power, savings etc.

Essentially, we'll be delivering a single application, accessible both as a web application and as a native Android application.

### Approach

These are some high-level markers highlighting our proposed approach:

- We'll use a map application's API (for e.g. _OpenStreetMap_) to map user's input address to a Latitude-Longitude coordinate.
- We'll use an existing family of datasets called _SARAH_ for finding out the historical long-wave solar insolation at that particular Latitude-Longitude coordinate, which will be in units of $W/m^2$.
- We'll use a _Regression Model_ to predict sunlight intensity over that coordinate for years in the future.
- We'll make a few simple calculations once we have all the factors down, and display the result in an easily digestible format.

#### Datasets

Based on the approach stated above, the following datasets can be listed as dependencies for our application:

1. _OpenStreetMap_'s geolocation dataset, used by our application through its API
2. _SARAH_, an open dataset of long-wave solar insolation
3. _Solar panel subsidies_ dataset
4. _Solar panel types_ dataset
5. _Discom electricity rates_ dataset

The bottom three datasets need to be maintained by the application, as they are not readily available anywhere else. They are also susceptible to frequent change, in the wake of changing government policies and the launch of new products in the market. That is a why a **DEO (Data Entry Operator)** is supposed maintain their accuracy on a frequent basis.

---

## Team

The following are the members:

1. Rakshit Rabugotra (_Team Leader_)
2. Arjun Singh
3. Subhajit Das
4. Deepanshu
5. Jasmehar Kaur
6. Saumya Kapoor

All members belong to Practical Group 1 of the class, except Saumya, who belongs to Practical Group 2.

We will be showcasing our progress with the project every **Tuesday**, in the designated Software Engineering lab.

---

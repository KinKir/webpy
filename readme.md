# WebPy
A web-based python interpreter

Sean Debroni, Evan Wilde, Navdeep Bahia

## Description

This is our self-adaptive systems project, using the information from the
various users to limit CPU quota to ensure fair sharing among users.


![Webapp image](https://raw.githubusercontent.com/etcwilde/webpy/master/webpy.png)

## Policy Driven

We allow the use of policies to change how the system behaves for the various
user types. Users with accounts will be given more CPU quota, while users
without accounts will be given less CPU quota. Furthermore, users with accounts
will have longer computation time than their anonymous counterparts.

## Core

### Flask
The project is implemented in Python using the Flask micro-framework to
simplify things.

## Installation

### Install Requirements
`pip install -r requirements.txt1`

### Run

Front-end server:
`python run_server.py`

Backend CPU Scheduler:
`python run_scheduler.py`

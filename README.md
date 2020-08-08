# CollabRobot-DQN
Master Thesis work @htwsaar. 

Implementation of mobile robots using Reinforcement Learning. Robots are able to avoid dynamic obstacles, plan their tasks based on their location and
work together to lift a heavy object.

## Repository

This repository contains two projects:

- The RL source code
- The graphical user interface for simulating the agents' behavior.

Navigate to the respective submodule to learn more about their content.

## Abstract

Many real-world applications require robots to collaboratively work on the sametask to achieve certain goals, e.g. lifting heavy objects and transporting it to a targetlocation. However, programming mobile robots can consume a lot of resources andtime since random obstacles and physical constraints often have to be consideredprior deployment. Recent advances have shown that machine learning methods andtheir research can be adjusted for applications in robotics.In this thesis, we investigate the feasibility of Reinforcement Learning (RL)algorithms to reinforce desired behavior for mobile robots on warehouse packagetransportation scenarios. Our models were trained and tested using variousexisting algorithms, such as Double Deep Q-Network, Dueling Deep Q-Networkand Prioritized Experience Replay, based on the renowned Deep Q-Network(DQN). In addition, the idea of partial observability is evaluated by using sensorinformation that are often equipped on modern robots. We apply our approach onseveral environments that evaluates critical robotic tasks such as static or dynamicobstacle  avoidance,  path-planning  and  collaborative  work  capabilities.  Ouranalyses show that DQN has diverse applications in package transportation usingrobots and can aid in finding the most optimal behavior policy with sufficientexperiences.

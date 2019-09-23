# cqrs_es
To Run. All the set up in done in __main__.py
```python
python -m cqrs_es 
```

__Domain-Driven Design (DDD)__ is an approach to software development for complex needs by connecting the implementation to an evolving model. The premise of Domain-Driven Design is the following:

placing the project's primary focus on the core domain and domain logic
basing complex designs on a model of the domain
initiating a creative collaboration between technical and domain experts to iteratively refine a conceptual model that addresses particular domain problems
The term was coined by Eric Evans in his book of the same title.

__Command Query Responsibility Segregation (CQRS)__ is simply the creation of two objects where there was previously only one. The separation occurs based upon whether the methods are a command or a query (the same definition that is used by Meyer in Command and Query Separation, a command is any method that mutates state and a query is any method that returns a value).

__Event Sourcing__ the fundamental idea of Event Sourcing is that of ensuring every change to the state of an application is captured in an event object, and that these event objects are themselves stored in the sequence they were applied for the same lifetime as the application state itself. As a side effect of this you can do __*time travel*__ through object change history.

A simple diagram to display the control flow

![alt text](https://camo.githubusercontent.com/ab394787f0caa609e7fe7f18c2f3c29e6930daa4/687474703a2f2f7777772e682d6f6e6c696e652e636f6d2f646576656c6f7065722f696d67732f38302f392f382f322f382f362f302f6371727330322d623461306163313665373062633766362e706e67)

__Unsure about DDD__ If you are new to the world of DDD and CQRS, [see this](https://github.com/heynickc/awesome-ddd). Its a collection of videos, books and articles
 

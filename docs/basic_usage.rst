Basic Usage
===========

.. toctree:: 
   :maxdepth: 1
   :hidden:

   basic_usage/prepare_ingredients
   basic_usage/cooking_ingredients

How pypotage works?
-------------------

**Pypotage** is a python package that makes it easier for developers to use **Dependency Injection** in their code. 

**Pypotage** simplifies the integration of **Dependency Injection** into developers' Python projects. It operates on the principle of a **container**, acting as a **central repository for all required dependencies**. These dependencies are subsequently **injected into the codebase** using this container.

.. note::
   In the context of this package, we will refer to the container as the **pot** and the dependencies as the **ingredients**. 

Preparing the Ingredients
-------------------------

To use **pypotage**, you need to **prepare the ingredients** that you will be using in your code. These ingredients are the dependencies that you will be injecting into your codebase. So let's **prepare the ingredients** first.

This is achieved by using the **@pypotage.prepare** decorator.

.. code-block:: python3
   
   import logging
   import pypotage

   @pypotage.prepare
   def my_logger():
       return logging.Logger(__name__)

.. note:: 
   The **@pypotage.prepare** can be used to prepare any type of ingredient, be it a function or a class.

.. warning::
   To check the type of the ingredient, **pypotage needs to execute the function if no specific type is provided**. Annotating the function prevents this behaviour.

Now we have a Logger prepared to use in any part of our codebase.

Cooking the Ingredients
-----------------------

To **inject the ingredients** into the codebase, you need to use the **pypotage.cook** function.

In the following example, we will inject the ingredient into a function of another class.

.. code-block:: python3

   import logging
   import pypotage

   def my_function():
      print(pypotage.cook(logging.Logger))

Now when this function is called, the ingredient will be injected into the function.

**Full Example**

`__init__.py`

.. code-block:: python3

   import logging
   import pypotage

   from my_module import my_function

   @pypotage.prepare
   def my_logger():
      return logging.Logger(__name__)

   my_function()

`my_module.py`

.. code-block:: python3

   import logging
   import pypotage

   def my_function():
      print(pypotage.cook(logging.Logger).take_out())

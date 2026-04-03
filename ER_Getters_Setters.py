"""
Below are the 8 classes defined in the current version of the ER diagram for Kintable.
These classes only have getter and setter functions, not intializers.
Conditional logic can be applied to the setter methods in the future.
These functions should not interfere with how you normally access class attributes in Python.
"""

#Home class
class Home:
    #Attributes: id (PK), address, location, name
    
    #Getters
    @property
    def id(self):
        return self._id
    @property
    def address(self):
        return self._address
    @property
    def location(self):
        return self._location
    @property
    def name(self):
        return self._name
    
    #Setters
    @id.setter
    def set_id(self, new_id):
        self._id = new_id
    @address.setter
    def set_address(self, new_address):
        self._address = new_address
    @location.setter
    def set_location(self, new_location):
        self._location = new_location
    @name.setter
    def set_name(self, new_name):
        self._name = new_name

#Table class
class Table:
    #Attributes: id (PK), name, capacity

    #Getters
    @property
    def id(self):
        return self._id
    @property
    def name(self):
        return self._name
    @property
    def capacity(self):
        return self._capacity
    
    #Setters
    @id.setter
    def set_id(self, new_id):
        self._id = new_id
    @name.setter
    def set_name(self, new_name):
        self._name = new_name
    @capacity.setter
    def set_capacity(self, new_capacity):
        self._capacity = new_capacity

#Seat class
class Seat:
    #Attributes: id (PK), is_available

    #Getters
    @property
    def id(self):
        return self._id
    @property
    def is_available(self):
        return self._is_available
    
    #Setters
    @id.setter
    def set_id(self, new_id):
        self._id = new_id
    @is_available.setter
    def set_is_available(self, new_is_available):
        self._is_available = new_is_available

#User class
class User:
    #Attributes: id (PK), name, role, active

    #Getters
    @property
    def id(self):
        return self._id
    @property
    def name(self):
        return self._name
    @property
    def role(self):
        return self._role
    @property
    def active(self):
        return self._active
    
    #Setters
    @id.setter
    def set_id(self, new_id):
        self._id = new_id
    @name.setter
    def set_name(self, new_name):
        self._name = new_name
    @role.setter
    def set_role(self, new_role):
        self._role = new_role
    @active.setter
    def set_active(self, new_active):
        self._active = new_active

#Dependent class
class Dependent:
    #Attributes: id (PK), name, age

    #Getters
    @property
    def id(self):
        return self._id
    @property
    def name(self):
        return self._name
    @property
    def age(self):
        return self._age
    
    #Setters
    @id.setter
    def set_id(self, new_id):
        self._id = new_id
    @name.setter
    def set_name(self, new_name):
        self._name = new_name
    @age.setter
    def set_age(self, new_age):
        self._age = new_age

#Meal class
class Meal:
    #Attributes: id (PK), title, description, date_prepared

    #Getters
    @property
    def id(self):
        return self._id
    @property
    def title(self):
        return self._title
    @property
    def description(self):
        return self._description
    @property
    def date_prepared(self):
        return self._date_prepared
    
    #Setters
    @id.setter
    def set_id(self, new_id):
        self._id = new_id
    @title.setter
    def set_title(self, new_title):
        self._title = new_title
    @description.setter
    def set_description(self, new_description):
        self._description = new_description
    @date_prepared.setter
    def set_date_prepared(self, new_date_prepared):
        self._date_prepared = new_date_prepared

#CuisineStyle class
class CuisineStyle:
    #Attributes: id (PK), name, region

    #Getters
    @property
    def id(self):
        return self._id
    @property
    def name(self):
        return self._name
    @property
    def region(self):
        return self._region
    
    #Setters
    @id.setter
    def set_id(self, new_id):
        self._id = new_id
    @name.setter
    def set_name(self, new_name):
        self._name = new_name
    @region.setter
    def set_region(self, new_region):
        self._region = new_region

#ConversationTopic class
class ConversationTopic:
    #Attributes: id (PK), topic, category

    #Getters
    @property
    def id(self):
        return self._id
    @property
    def topic(self):
        return self._topic
    @property
    def category(self):
        return self._category
    
    #Setters
    @id.setter
    def set_id(self, new_id):
        self._id = new_id
    @topic.setter
    def set_topic(self, new_topic):
        self._topic = new_topic
    @category.setter
    def set_category(self, new_category):
        self._category = new_category
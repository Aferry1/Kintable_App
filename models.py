# models.py
//  Created by jackdanielrobinson@hotmail.com on 4/5/26.
from datetime import date
from typing import List, Optional

class Home:
    """
    Home class
    Attributes: id (PK), address, location, name
    """

    def __init__(self, id: str, address: str, location: str, name: str):
        self.id = id
        self.address = address
        self.location = location
        self.name = name

        # Relationships
        self.users: List["User"] = []
        self.table: Optional["Table"] = None

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, new_id):
        self._id = new_id

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, new_address):
        self._address = new_address

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, new_location):
        self._location = new_location

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    def __repr__(self):
        return f"Home(id={self.id!r}, name={self.name!r}, location={self.location!r})"
        
    
class Table:
    """
    Table class
    Attributes: id (PK), name, capacity
    """

    def __init__(self, id: str, name: str, capacity: int):
        self.id = id
        self.name = name
        self.capacity = capacity

        # Relationships
        self.home: Optional["Home"] = None
        self.seats: List["Seat"] = []
        self.meals: List["Meal"] = []

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, new_id):
        self._id = new_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, new_capacity):
        self._capacity = new_capacity

    def __repr__(self):
        return f"Table(id={self.id!r}, name={self.name!r}, capacity={self.capacity!r})"
        
        
class Seat:
    """
    Seat class
    Attributes: id (PK), is_available
    """

    def __init__(self, id: str, is_available: bool = True):
        self.id = id
        self.is_available = is_available

        # Relationships
        self.table: Optional["Table"] = None
        self.meal: Optional["Meal"] = None
        self.guest: Optional["User"] = None
        self.child_guest: Optional["Dependent"] = None

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, new_id):
        self._id = new_id

    @property
    def is_available(self):
        return self._is_available

    @is_available.setter
    def is_available(self, new_is_available):
        self._is_available = new_is_available

    def __repr__(self):
        return f"Seat(id={self.id!r}, is_available={self.is_available!r})"
        
        
class User:
    """
    User class
    Attributes: id (PK), name, role, active
    """

    def __init__(self, id: str, name: str, role: str, active: bool):
        self.id = id
        self.name = name
        self.role = role
        self.active = active

        # Relationships
        self.homes: List["Home"] = []
        self.dependents: List["Dependent"] = []
        self.favorite_users: List["User"] = []
        self.recent_visits: List["User"] = []
        self.hosted_home: Optional["Home"] = None

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, new_id):
        self._id = new_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, new_role):
        self._role = new_role

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, new_active):
        self._active = new_active

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, role={self.role!r}, active={self.active!r})"
        
        
class Dependent:
    """
    Dependent class
    Attributes: id (PK), name, age
    """

    def __init__(self, id: str, name: str, age: int):
        self.id = id
        self.name = name
        self.age = age

        # Relationships
        self.users: List["User"] = []

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, new_id):
        self._id = new_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, new_age):
        self._age = new_age

    def __repr__(self):
        return f"Dependent(id={self.id!r}, name={self.name!r}, age={self.age!r})"
        
        
class Meal:
    """
    Meal class
    Attributes: id (PK), title, description, date_prepared
    """

    def __init__(self, id: str, title: str, description: str, date_prepared):
        self.id = id
        self.title = title
        self.description = description
        self.date_prepared = date_prepared

        # Relationships
        self.table: Optional["Table"] = None
        self.cuisine_styles: List["CuisineStyle"] = []
        self.conversation_topics: List["ConversationTopic"] = []
        self.seats: List["Seat"] = []

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, new_id):
        self._id = new_id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, new_title):
        self._title = new_title

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, new_description):
        self._description = new_description

    @property
    def date_prepared(self):
        return self._date_prepared

    @date_prepared.setter
    def date_prepared(self, new_date_prepared):
        self._date_prepared = new_date_prepared

    def __repr__(self):
        return f"Meal(id={self.id!r}, title={self.title!r}, date_prepared={self.date_prepared!r})"
        
        
class CuisineStyle:
    """
    CuisineStyle class
    Attributes: id (PK), name, region
    """

    def __init__(self, id: str, name: str, region: str):
        self.id = id
        self.name = name
        self.region = region

        # Relationships
        self.meals: List["Meal"] = []

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, new_id):
        self._id = new_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @property
    def region(self):
        return self._region

    @region.setter
    def region(self, new_region):
        self._region = new_region

    def __repr__(self):
        return f"CuisineStyle(id={self.id!r}, name={self.name!r}, region={self.region!r})"
        
        
class ConversationTopic:
    """
    ConversationTopic class
    Attributes: id (PK), topic, category
    """

    def __init__(self, id: str, topic: str, category: str):
        self.id = id
        self.topic = topic
        self.category = category

        # Relationships
        self.meals: List["Meal"] = []

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, new_id):
        self._id = new_id

    @property
    def topic(self):
        return self._topic

    @topic.setter
    def topic(self, new_topic):
        self._topic = new_topic

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, new_category):
        self._category = new_category

    def __repr__(self):
        return f"ConversationTopic(id={self.id!r}, topic={self.topic!r}, category={self.category!r})"

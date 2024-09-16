from typing import Optional
from pydantic import BaseModel
"""

This module contains the serializers for the User model.

Classes:
- UserBase: Represents the base properties of a user.
- UserBaseInDB: Represents the base properties of a user stored in the database.
- UserCreate: Represents the properties of a user received via API on creation.
- UserUpdate: Represents the properties of a user received via API on update.
- SpecificUserUpdate: Represents the specific properties of a user received via API on update.
- User: Represents the additional properties to return via API.
- UserInDB: Represents the additional properties stored in the database.
- SuperuserCreate: Represents the properties of a superuser received via API on creation.

"""

# Shared properties
class UserBase(BaseModel):
  email:            Optional[str]           = None
  is_active:        Optional[bool]          = True
  full_name:        Optional[str]           = None

class UserBaseInDB(UserBase):
  id:               int                     = None

# Properties to receive via API on creation
class UserCreate(UserBaseInDB):
  username:         str
  email:            str
  password:         str

# Properties to receive via API on update
class UserUpdate(UserBaseInDB):
  password:         Optional[str]           = None

class SpecificUserUpdate(UserBaseInDB):
  username:        Optional[str]           = None
  email:            Optional[str]           = None
  is_active:        Optional[bool]          = None
  created_by:       Optional[str]           = None
  updated_by:       Optional[str]           = None

# Additional properties to return via API
class User(UserBaseInDB):
  pass

# Additional properties stored in DB
class UserInDB(UserBaseInDB):
  hashed_password:  str

class SuperuserCreate(UserBaseInDB):
  username:         str                     = 'Super User'
  email:            str                     = 'test@gmail.com'
  password:         str                     = 'password'

from sqlalchemy.orm import Session
from typing import List, Optional
from math import ceil
import io

from src.core.security import get_password_hash, verify_password
from src.models import User
from src.serializers.user_serializer import UserCreate, UserUpdate, SpecificUserUpdate
from sqlalchemy.sql.functions import current_timestamp

from src.ai.generate_sample_sales_data import generate_csv
from src.services.inventory_forecasting_service import forecasting

def authenticate(db_session: Session, *, email: str, password: str) -> Optional[User]:
    """
    Authenticates a user by checking if the provided email and password match a user in the database.

    Args:
        db_session (Session): The database session.
        email (str): The email of the user.
        password (str): The password of the user.

    Returns:
        Optional[User]: The authenticated user if the email and password match, otherwise None.
    """

    # Get the user by email
    user = get_by_email(db_session, email=email)

    # If user does not exist, return None
    if not user:
        return None

    # Verify the password
    if not verify_password(password, user.hashed_password):
        return None

    # Return the authenticated user
    return user

def get_by_email(db_session: Session, *, email: str) -> Optional[User]:
    """
    Retrieve a user from the database by email.
    Args:
        db_session (Session): The database session.
        email (str): The email of the user to retrieve.
    Returns:
        Optional[User]: The user object if found, None otherwise.
    """
    
    return db_session.query(User).filter(User.email == email).first()

def get(db_session: Session, *, user_id: int) -> Optional[User]:
    """
    Retrieve a user from the database based on the provided user ID.
    Args:
        db_session (Session): The database session object.
        user_id (int): The ID of the user to retrieve.
    Returns:
        Optional[User]: The retrieved user object, or None if no user is found.
    """
    
    user = db_session.query(User).filter(User.id == user_id).first()
    return user

def is_active(user) -> bool:
    """
    Check if the user is active.
    Args:
        user: The user object.
    Returns:
        bool: True if the user is active, False otherwise.
    """
    
    return user.is_active

def is_superuser(user) -> bool:
    """
    Check if the user is a superuser.
    Args:
        user: The user object to check.
    Returns:
        bool: True if the user is a superuser, False otherwise.
    """
    
    return user.role == 0

def get_multi(db_session: Session, page: int, limit: int) -> List[Optional[User]]:
    """
    Retrieves a list of users from the database based on the specified page and limit.
    Args:
        db_session (Session): The database session object.
        page (int): The page number to retrieve.
        limit (int): The maximum number of users to retrieve per page.
    Returns:
        dict: A dictionary containing the list of users, total number of pages, and current page.
    Comments:
        - The function queries the total number of users in the database.
        - It calculates the total number of pages based on the total number of users and the specified limit.
        - The function retrieves the users from the database, ordered by their creation date in descending order.
        - The offset and limit are used to retrieve the users for the specified page.
        - The function returns a dictionary containing the list of users, total number of pages, and current page.
        - If the total number of pages is less than 1, it is set to 1 to avoid division by zero errors.
    """
    
    total_users = db_session.query(User).count()
    total_pages = ceil(total_users / limit)
    users = db_session.query(User).order_by(User.created_at.desc()).offset((page - 1) * limit).limit(limit).all()

    return {"users": users, "total_pages": max([total_pages, 1]), "current_page": page}

def create(db_session: Session, user_in: UserCreate) -> User:
    """
    Create a new user in the database.
    Args:
        db_session (Session): The database session.
        user_in (UserCreate): The user data to be created.
    Returns:
        User: The created user object.
    """
    # Create a new User object with the provided data
    # Add the user to the database session
    # Commit the changes to the database
    # Refresh the user object to get the updated values from the database
    # Return the created user object
    
    user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        username=user_in.username,
        is_active=True,
        created_at=current_timestamp(),
        updated_at=current_timestamp()
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user

def update(db_session: Session, user_in: UserUpdate, current_user) -> User:
    """
    Update the user information in the database.

    Args:
        db_session (Session): The database session.
        user_in (UserUpdate): The updated user information.
        current_user: The current user object.

    Returns:
        User: The updated user object.
    """

    if user_in.full_name:
        current_user.full_name = user_in.full_name
    if user_in.password:
        passwordhash = get_password_hash(user_in.password)
        current_user.hashed_password = passwordhash

    db_session.add(current_user)
    db_session.commit()
    db_session.refresh(current_user)

    return current_user

def update_user(db_session: Session, user_in: SpecificUserUpdate, current_user, user) -> User:
    """
    Update the user with the provided information.

    Args:
        db_session (Session): The database session.
        user_in (SpecificUserUpdate): The updated user information.
        current_user: The current user performing the update.
        user: The user to be updated.

    Returns:
        User: The updated user.
    """

    user.updated_by = current_user.id
    if user_in.full_name:
        user.full_name = user_in.full_name
    if user_in.email:
        user.email = user_in.email
    if not user_in.is_active == None:
        user.is_active = user_in.is_active

    db_session.commit()
    db_session.refresh(user)

    return user


def genrate_fake_sales_data():
    """
    Generates fake sales data and returns it as a buffer.
    Returns:
        io.StringIO: A buffer containing the generated sales data in CSV format.
    """
    # Generate a CSV file with fake sales data
    # Create a buffer to store the CSV data
    # Write the DataFrame to the buffer as CSV
    # Move the buffer's position to the beginning
    # Return the buffer containing the generated sales data
    
    df = generate_csv()
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)
    
    return buffer

async def train_and_save_model(file):
    """
    Trains and saves a model using the provided file.
    Parameters:
    file (str): The file path to the data used for training.
    Returns:
    The result of the forecasting function.
    """
    return await forecasting(file)

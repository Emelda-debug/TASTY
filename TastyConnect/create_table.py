import os
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Get the absolute path of the directory containing the create_table.py file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Specify the relative path to the database file
database_filename = 'recipes.db'

# Construct the full path to the database file
database_path = os.path.join(current_dir, database_filename)

# Create the engine to connect to the SQLite database
engine = create_engine(f'sqlite:///{database_path}')

# Define the base class for declarative models
Base = declarative_base()

# Define the table schema
class RecipeTable(Base):
    __tablename__ = 'recipe'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    ingredients = Column(String)
    instructions = Column(String)

# Create the table in the database
Base.metadata.create_all(engine)
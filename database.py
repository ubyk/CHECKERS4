from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

Base = declarative_base()

class GameResult(Base):
    __tablename__ = 'game_results'
    
    id = Column(Integer, primary_key=True)
    game_id = Column(String, unique=True, nullable=False)
    winner = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Use SQLite for the initial prototype
engine = create_engine('sqlite:///checkers_game.db')
Session = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)

def save_game_result(game_id, winner):
    session = Session()
    result = GameResult(game_id=game_id, winner=winner)
    session.add(result)
    session.commit()
    session.close()

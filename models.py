from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    
    bookings = relationship("Booking", back_populates="user")

class VM(Base):
    __tablename__ = "vms"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    
    nodes = relationship("Node", back_populates="vm", cascade="all, delete-orphan")
    bookings = relationship("Booking", back_populates="vm")

class Node(Base):
    __tablename__ = "nodes"
    id = Column(Integer, primary_key=True, index=True)
    vm_id = Column(Integer, ForeignKey("vms.id"))
    name = Column(String)
    
    vm = relationship("VM", back_populates="nodes")
    bookings = relationship("Booking", back_populates="node")

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    vm_id = Column(Integer, ForeignKey("vms.id"))
    node_id = Column(Integer, ForeignKey("nodes.id"), nullable=True) # Tomt = Hela VM bokad
    start_time = Column(DateTime)
    end_time = Column(DateTime)

    user = relationship("User", back_populates="bookings")
    vm = relationship("VM", back_populates="bookings")
    node = relationship("Node", back_populates="bookings")
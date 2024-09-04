import os
import enum
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, Enum, Float, Text, Date,DateTime, Boolean, func 
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship


from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()


class UserRoleEnum(enum.Enum):
    Shipper = "Shipper"
    Driver = "Driver"
    Admin = "Admin"

class Role(Base):
    __tablename__ = 'Roles'

    roleId = Column(Integer, primary_key=True, autoincrement=True, index=True)
    role = Column(Enum(UserRoleEnum), unique=True, nullable=False)

    user_roles = relationship('UserRole', back_populates='role')

class User(Base):
    __tablename__ = 'Users'

    userId = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    verifiedUser = Column(Boolean, nullable=False)

    roles = relationship('UserRole', back_populates='user')

class UserRole(Base):
    __tablename__ = 'User_roles'

    userRoleId = Column(Integer, primary_key=True, autoincrement=True, index=True)
    userId = Column(Integer, ForeignKey('Users.userId'), nullable=False)
    roleId = Column(Integer, ForeignKey('Roles.roleId'), nullable=False)

    user = relationship('User', back_populates='roles')

    role = relationship('Role', back_populates='user_roles')
class OrderStatusEnum(enum.Enum):
    pending = "pending"
    completed = "completed"
    cancelled = "on-going"

class VehicleTypeEnum(enum.Enum):
    car = "car"
    truck = "truck"
    van = "van"

class Order(Base):

    __tablename__ = "Orders"

    orderId = Column(Integer, primary_key=True, autoincrement=True)
    # SET THE NULLABLE TO FALSE AND ADD ForeignKey('User.Id')
    customerId = Column(Integer, nullable=True)
    driverId = Column(Integer, nullable=True)
    pickupLocation = Column(String, nullable=False)
    dropoffLocation = Column(String, nullable=False)
    orderStatus = Column(Enum(OrderStatusEnum), nullable=False)
    paymentAmount = Column(Float, nullable=False)
    vehicleType = Column(Enum(VehicleTypeEnum), nullable=False)
    dimensions = Column(Text, nullable=False)
    weightValue = Column(String, nullable=False)
    deliveryTime = Column(Date, nullable=False)
    createdAt = Column(DateTime, default=func.now())
    updatedAt = Column(DateTime, default=func.now(), onupdate=func.now())

    def __init__(self, customerId, driverId, pickupLocation, dropoffLocation, orderStatus, paymentAmount, vehicleType, dimensions, weightValue, deliveryTime):
        self.customerId = customerId
        self.driverId = driverId
        self.pickupLocation = pickupLocation
        self.dropoffLocation = dropoffLocation
        self.orderStatus = orderStatus
        self.paymentAmount = paymentAmount
        self.vehicleType = vehicleType
        self.dimensions = dimensions
        self.weightValue = weightValue
        self.deliveryTime = deliveryTime

def get_env_variable(var_name, default_value=None):
    """Get the environment variable or return a default value."""
    return os.getenv(var_name, default_value)

engine = create_engine(
    f"postgresql://{get_env_variable('POSTGRES_USER')}:{get_env_variable('POSTGRES_PASSWORD')}@{get_env_variable('POSTGRES_HOST')}:{get_env_variable('POSTGRES_PORT', '5432')}/{get_env_variable('POSTGRES_DBNAME')}",
    echo=True
)

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()

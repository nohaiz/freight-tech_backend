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
    shipper = "shipper"
    driver = "driver"
    admin = "admin"

class Role(Base):

    __tablename__ = 'Roles'

    roleId = Column(Integer, primary_key=True, autoincrement=True, index=True)
    role = Column(Enum(UserRoleEnum), unique=True, nullable=False)

    user_roles = relationship('UserRole', back_populates='role')

    def to_dict(self):
        return {
            "roleId": self.roleId,
            "role": self.role.value
        }

class User(Base):
    __tablename__ = 'Users'

    userId = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    verifiedUser = Column(Boolean,nullable=False)
    roles = relationship('UserRole', back_populates='user')

    def to_dict(self):
        roles = [user_role.role.role.value for user_role in self.roles]
        return {
            "userId": self.userId,
            "username": self.username,
            "email": self.email,
            "verifiedUser": self.verifiedUser,
            "roles": roles
        }

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
    on_route = "on_route"

class VehicleTypeEnum(enum.Enum):
    car = "car"
    truck = "truck"
    van = "van"

class Order(Base):

    __tablename__ = "Orders"

    orderId = Column(Integer, primary_key=True, autoincrement=True)
    customerId = Column(Integer, ForeignKey('Users.userId'), nullable=False)
    driverId = Column(Integer, ForeignKey('Users.userId'), nullable=True)
    pickupLocation = Column(String, nullable=False)
    dropoffLocation = Column(String, nullable=False)
    orderStatus = Column(Enum(OrderStatusEnum), nullable=False) 
    paymentAmount = Column(Float, nullable=False)
    vehicleType = Column(Enum(VehicleTypeEnum), nullable=False)
    dimensions = Column(Text, nullable=False)
    weightValue = Column(Float, nullable=False)
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

    def to_dict(self):
        return {"orderId": self.orderId,"customerId": self.customerId,"driverId": self.driverId,"pickupLocation": self.pickupLocation,"dropoffLocation": self.dropoffLocation,"orderStatus": self.orderStatus.value,  "paymentAmount": self.paymentAmount,"vehicleType": self.vehicleType.value,"weightValue": self.weightValue,"deliveryTime": self.deliveryTime.isoformat(),"createdAt": self.createdAt.isoformat(),"updatedAt": self.updatedAt.isoformat()
        }
    
def get_env_variable(var_name, default_value=None):
    """Get the environment variable or return a default value."""
    return os.getenv(var_name, default_value)

engine = create_engine(
    f"postgresql://{get_env_variable('POSTGRES_USER')}:{get_env_variable('POSTGRES_PASSWORD')}@{get_env_variable('POSTGRES_HOST')}:{get_env_variable('POSTGRES_PORT', '5432')}/{get_env_variable('POSTGRES_DBNAME')}",
    echo=True
)

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

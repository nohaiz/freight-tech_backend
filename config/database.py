import os
import enum
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, Enum, Float, Text, Date,DateTime, func
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

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

def get_env_variable(var_name, default_value=None):
    """Get the environment variable or return a default value."""
    return os.getenv(var_name, default_value)

engine = create_engine(
    f"postgresql://{get_env_variable('POSTGRES_USER')}:{get_env_variable('POSTGRES_PASSWORD')}@{get_env_variable('POSTGRES_HOST')}:{get_env_variable('POSTGRES_PORT', '5432')}/{get_env_variable('POSTGRES_DBNAME')}",
    echo=True
)

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

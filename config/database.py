import os
import enum
from datetime import date
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, Enum, Float, Text, Date, TIMESTAMP, DateTime, func
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
    # customerId = Column(Integer, ForeignKey('User.Id'), nullable=False)
    # driverId = Column(Integer, ForeignKey('User.Id'), nullable=False)
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

    def __init__(self, pickupLocation, dropoffLocation, orderStatus, paymentAmount, vehicleType, dimensions, weightValue, deliveryTime):
        # self.customerId = customerId
        # self.driverId = driverId
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

# Test

sample_order = Order(
    # customerId=1,
    # driverId=2,
    pickupLocation="123 Elm Street, Springfield",
    dropoffLocation="456 Oak Avenue, Springfield",
    orderStatus=OrderStatusEnum.pending,
    paymentAmount=99.99,
    vehicleType=VehicleTypeEnum.truck,
    dimensions="10x10x10",
    weightValue="200 lbs",
    deliveryTime=date(2024, 12, 25)
)

session.add(sample_order)
session.commit()

print("Sample order added successfully.")

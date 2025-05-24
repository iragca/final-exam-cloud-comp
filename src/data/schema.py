from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class CustInfo(Base):
    __tablename__ = "cust_info"

    cst_id = Column(Integer, primary_key=True)
    cst_key = Column(String, unique=True)
    cst_firstname = Column(String)
    cst_lastname = Column(String)
    cst_marital_status = Column(String)
    cst_gndr = Column(String)
    cst_create_date = Column(Date)

    orders = relationship("SalesDetails", back_populates="customer")
    legacy_records = relationship("CustAz12", back_populates="cust")


class PrdInfo(Base):
    __tablename__ = "prd_info"

    prd_id = Column(Integer, primary_key=True)
    prd_key = Column(String, unique=True)
    prd_nm = Column(String)
    prd_cost = Column(Integer)
    prd_line = Column(String)
    prd_start_dt = Column(Date)
    prd_end_dt = Column(Date)
    category_id = Column(String, ForeignKey("px_cat_g1v2.id"))

    orders = relationship("SalesDetails", back_populates="product")
    category = relationship("PxCatG1v2", back_populates="products")


class PxCatG1v2(Base):
    __tablename__ = "px_cat_g1v2"

    id = Column(String, primary_key=True)
    cat = Column(String)
    subcat = Column(String)
    maintenance = Column(String)

    products = relationship("PrdInfo", back_populates="category")


class SalesDetails(Base):
    __tablename__ = "sales_details"

    sls_ord_num = Column(String, primary_key=True)
    sls_prd_key = Column(String, ForeignKey("prd_info.prd_key"))
    sls_cust_id = Column(Integer, ForeignKey("cust_info.cst_id"))
    sls_order_dt = Column(Date)
    sls_ship_dt = Column(Date)
    sls_due_dt = Column(Date)
    sls_sales = Column(Integer)
    sls_quantity = Column(Integer)
    sls_price = Column(Integer)

    customer = relationship("CustInfo", back_populates="orders")
    product = relationship("PrdInfo", back_populates="orders")


class CustAz12(Base):
    __tablename__ = "cust_az12"

    cid = Column(String, ForeignKey("cust_info.cst_key"), primary_key=True)
    birthdate = Column(Date)

    cust = relationship("CustInfo", back_populates="legacy_records")
    locations = relationship("LocA101", back_populates="customer_aux")


class LocA101(Base):
    __tablename__ = "loc_a101"

    cid = Column(String, ForeignKey("cust_info.cst_key"), primary_key=True)
    country = Column(String)

    customer_aux = relationship("CustAz12", back_populates="locations")

import streamlit as st
from query import *
import mysql.connector

# Fetch data
def view_all_data():
    try:
        conn = mysql.connector.connect(
            host=st.secrets["DB_HOST"],
            port=st.secrets["DB_PORT"],
            user=st.secrets["DB_USER"],
            passwd=st.secrets["DB_PASSWORD"],
            db=st.secrets["DB_NAME"]
        )
        c = conn.cursor()
        query = '''
        SELECT
            fi.SalesOrderNumber,
            dp.EnglishProductName AS NamaProduk,
            dpc.EnglishProductCategoryName AS KategoriProduk,
            dt1.FullDateAlternateKey AS TglOrder,
            dt2.FullDateAlternateKey AS TglSampai,
            dt3.FullDateAlternateKey AS TglPengiriman,
            CONCAT(IFNULL(dc.FirstName, ''), ' ', IFNULL(dc.LastName, '')) AS NamaCustomer,
            fi.CustomerKey as IDCustomer,
            dcurr.CurrencyName AS MataUang,
            dst.SalesTerritoryRegion AS Wilayah,
            fi.OrderQuantity as JmlhItem,
            fi.UnitPrice as BiayaPerItem,
            fi.ExtendedAmount as BiayaYangDipesan,
            fi.ProductStandardCost as BiayaStandardProduk,
            fi.TotalProductCost as TotalHargaProduk,
            fi.SalesAmount as TotalPenjualan,
            fi.TaxAmt AS JmlPajak,
            fi.Freight as BiayaPengiriman
        FROM
            factinternetsales fi
        JOIN
            dimproduct dp ON fi.ProductKey = dp.ProductKey
        JOIN 
            dimproductsubcategory dps ON dp.ProductSubcategoryKey = dps.ProductSubcategoryKey
        JOIN 
            dimproductcategory dpc ON dps.ProductCategoryKey = dpc.ProductCategoryKey
        JOIN
            dimtime dt1 ON fi.OrderDateKey = dt1.TimeKey
        JOIN
            dimtime dt2 ON fi.DueDateKey = dt2.TimeKey
        JOIN
            dimtime dt3 ON fi.ShipDateKey = dt3.TimeKey
        JOIN
            dimcustomer dc ON fi.CustomerKey = dc.CustomerKey
        JOIN
            dimcurrency dcurr ON fi.CurrencyKey = dcurr.CurrencyKey
        JOIN
            dimsalesterritory dst ON fi.SalesTerritoryKey = dst.SalesTerritoryKey
        '''
        c.execute(query)
        data = c.fetchall()
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        data = []
    finally:
        if 'c' in locals() and c:
            c.close()
        if 'conn' in locals() and conn:
            conn.close()
    return data

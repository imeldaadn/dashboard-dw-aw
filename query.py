import streamlit as st
import pandas as pd
import plotly.express as px
from query import *
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
import mysql.connector

# Fetch data
def view_all_data():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            port="3306",
            user="root",
            passwd="",
            db="dump-dw_aw-202403050806"
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
        if c:
            c.close()
        if conn:
            conn.close()
    return data
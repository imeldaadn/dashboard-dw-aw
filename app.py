import streamlit as st
import pandas as pd
import plotly.express as px
from query import *
from numerize.numerize import numerize

# Konfigurasi halaman
st.set_page_config(
    page_title="Data Visualization Dashboard",
    page_icon="🎢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dashboard
st.header('Hi, Welcome to the :blue[**Data Visualization Dashboard!**]')
st.markdown('We are here to showcase your data :orange[in] a cool :orange[and] engaging way :sunglasses:')
st.subheader("Data Warehouse Adventureworks")

# Ambil Data
result = view_all_data()
df = pd.DataFrame(result, columns=["SalesOrderNumber","NamaProduk","KategoriProduk","TglOrder","TglSampai","TglPengiriman","NamaCustomer","IDCustomer","MataUang","Wilayah","JmlhItem","BiayaPerItem","BiayaYangDipesan","BiayaStandardPenjualan","TotalHargaProduk","TotalPenjualan","JmlPajak","BiayaPengiriman"])

# Sidebar
st.sidebar.image("src/logoupnbaru.png", caption="Imelda Audina - 21082010003 - Sistem Informasi - Fakultas Ilmu Komputer")
st.sidebar.title('🛒 Data Visualization Dashboard')

# Filter
st.sidebar.header("Filter: ")
region = st.sidebar.multiselect(
    "Pilih Wilayah", 
    options = df["Wilayah"].unique(),
    default = df["Wilayah"].unique()
)

# Input tanggal awal dan akhir
start_date = st.sidebar.date_input("Tanggal Mulai", df["TglOrder"].min())
end_date = st.sidebar.date_input("Tanggal Akhir", df["TglOrder"].max())

# Konversi kolom tanggal ke format datetime
df["TglOrder"] = pd.to_datetime(df["TglOrder"])

# Filter DataFrame
df_selection = df[
    (df["Wilayah"].isin(region)) &
    (df["TglOrder"] >= pd.to_datetime(start_date)) &
    (df["TglOrder"] <= pd.to_datetime(end_date))
]

# Fungsi Home untuk menampilkan data
def Home():
    with st.expander("Table Data"):
        showData = st.multiselect('Filter Kolom: ', df_selection.columns, default=df_selection.columns.tolist())
        st.write(df_selection[showData])

Home()

######################################################################################################################
# Fungsi untuk menampilkan grafik bar chart - comparisson
container1 = st.container(border=True)
def graphs1():
    # Bar Chart
    total_sales_by_region = df_selection.groupby("Wilayah")[["TotalPenjualan"]].sum().sort_values(by="TotalPenjualan")

    fig_bar = px.bar(
       total_sales_by_region,
       x=total_sales_by_region.index,
       y="TotalPenjualan",
       orientation="v",
       title="<b> Bar Chart: Total Penjualan by Wilayah - Comparisson</b>",
    )
    fig_bar.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="black"),
        yaxis=dict(showgrid=True, gridcolor='#cecdcd'),
        paper_bgcolor='rgba(0, 0, 0, 0)',
        xaxis=dict(showgrid=True, gridcolor='#cecdcd'),
    )
    st.plotly_chart(fig_bar)

# Fungsi untuk analisis data
def analysis1():
    with st.expander("Analysis", expanded=False):
        total_sales_by_region = df_selection.groupby("Wilayah")[["TotalPenjualan"]].sum().sort_values(by="TotalPenjualan")
        total_sales_by_region["TotalPenjualan"] = pd.to_numeric(total_sales_by_region["TotalPenjualan"], errors="coerce")
        
        max_region = total_sales_by_region["TotalPenjualan"].idxmax()
        min_region = total_sales_by_region["TotalPenjualan"].idxmin()
        total_sales = total_sales_by_region["TotalPenjualan"].sum()
        
        st.markdown('**Total Penjualan**')
        st.write(f"Total penjualan dari {start_date} hingga {end_date} adalah {numerize(total_sales)}.")
        st.markdown('')

        st.markdown('**Total Penjualan Berdasarkan Wilayah**')
        st.write(f"Wilayah dengan penjualan tertinggi adalah **{max_region}** dengan total penjualan {numerize(total_sales_by_region.loc[max_region, 'TotalPenjualan'])}.")
        st.write(f"Wilayah dengan penjualan terendah adalah **{min_region}** dengan total penjualan {numerize(total_sales_by_region.loc[min_region, 'TotalPenjualan'])}.")

######################################################################################################################
# Fungsi untuk menampilkan grafik scatter plot - relationship
container2 = st.container(border=True)
def graphs2():
    # Scatter Plot
    x_axis = "TotalPenjualan"
    y_axis = "JmlPajak"
    
    fig_scatter = px.scatter(
        df_selection,
        x=x_axis,
        y=y_axis,
        color="Wilayah",
        title=f"<b>Scatter Plot: {x_axis} vs {y_axis} - Relationship</b>",
        labels={x_axis: x_axis, y_axis: y_axis}
    )
    fig_scatter.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="black"),
        yaxis=dict(showgrid=True, gridcolor='#cecdcd'),
        paper_bgcolor='rgba(0, 0, 0, 0)',
        xaxis=dict(showgrid=True, gridcolor='#cecdcd'),
    )
    st.plotly_chart(fig_scatter)

# Fungsi untuk analisis data
def analysis2():
    with st.expander("Analysis", expanded=False):
        # Scatter Plot
        st.markdown('**Scatter Plot Analysis**')
        x_axis = "TotalPenjualan"
        y_axis = "JmlPajak"
        
        correlation = df_selection[x_axis].corr(df_selection[y_axis])
        st.write(f"Korelasi antara {x_axis} dan {y_axis} adalah {correlation:.2f}.")
        if correlation > 0:
            st.write(f"Ini menunjukkan korelasi positif, artinya ketika {x_axis} meningkat, {y_axis} cenderung meningkat.")
        elif correlation < 0:
            st.write(f"Ini menunjukkan korelasi negatif, artinya ketika {x_axis} meningkat, {y_axis} cenderung menurun.")
        else:
            st.write(f"Tidak ada korelasi antara {x_axis} dan {y_axis}.")

######################################################################################################################
# Fungsi untuk meanmpilkan grafik pie chart - composition
container3 = st.container(border=True)
def graphs3():
    # Pie Chart
    total_sales_by_category = df_selection.groupby("KategoriProduk")[["TotalPenjualan"]].sum().sort_values(by="TotalPenjualan")

    fig_pie = px.pie(
        total_sales_by_category,
        values="TotalPenjualan",
        names=total_sales_by_category.index,
        title="<b>Total Penjualan by Kategori Produk - Composition</b>",
        hole=0.3
    )
    fig_pie.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="black"),
        paper_bgcolor='rgba(0, 0, 0, 0)',
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_pie)

# Fungsi untuk analisis data
def analysis3():
    with st.expander("Analysis", expanded=False):
        st.markdown('**Donut Chart Analysis**')
        st.write("Grafik ini menampilkan total penjualan yang dibagi berdasarkan kategori produk. Berikut adalah beberapa analisis mendalam dari grafik donut:")
            
        total_sales = df_selection["TotalPenjualan"].sum()
        total_sales_by_category = df_selection.groupby("KategoriProduk")[["TotalPenjualan"]].sum().sort_values(by="TotalPenjualan")
        
        for index, row in total_sales_by_category.iterrows():
            percentage = (row["TotalPenjualan"] / total_sales) * 100
            st.write(f"- **{index}**: {percentage:.2f}% dari total penjualan.")
        
######################################################################################################################
# Fungsi untuk menampilkan grafik box plot - distribution
container4 = st.container(border=True)
def graphs4():
    # Box Plot
    fig_box = px.box(
        df_selection,
        x="KategoriProduk",
        y="TotalPenjualan",
        title="<b>Box Plot: Distribusi Total Penjualan berdasarkan Kategori Produk - Distribution</b>",
        labels={"KategoriProduk": "Kategori Produk", "TotalPenjualan": "Total Penjualan"}
    )
    fig_box.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="black"),
        yaxis=dict(showgrid=True, gridcolor='#cecdcd'),
        paper_bgcolor='rgba(0, 0, 0, 0)',
        xaxis=dict(showgrid=True, gridcolor='#cecdcd'),
    )
    st.plotly_chart(fig_box)

# Fungsi untuk analisis data
def analysis4():
    with st.expander("Analysis", expanded=False):
        st.markdown('**Box Plot Analysis**')
        st.write("Box plot menunjukkan distribusi total penjualan untuk setiap kategori produk:")
        
        # Menemukan kategori dengan median penjualan tertinggi
        median_sales = df_selection.groupby("KategoriProduk")["TotalPenjualan"].median().sort_values(ascending=False)
        highest_median_category = median_sales.idxmax()
        highest_median_value = median_sales.max()
        
        # Menemukan kategori dengan rentang penjualan terbesar
        range_sales = df_selection.groupby("KategoriProduk")["TotalPenjualan"].apply(lambda x: x.max() - x.min()).sort_values(ascending=False)
        largest_range_category = range_sales.idxmax()
        largest_range_value = range_sales.max()
        
        st.write(f"Kategori produk dengan median penjualan tertinggi adalah **{highest_median_category}** dengan nilai median {highest_median_value}. Kategori ini adalah produk yang secara konsisten memiliki performa penjualan yang baik.")
        st.write(f"Kategori produk dengan rentang penjualan terbesar adalah **{largest_range_category}** dengan rentang {largest_range_value}. Kategori dengan rentang penjualan terbesar menunjukkan variasi atau fluktuasi penjualan yang besar untuk memahami seberapa beragam penjualan dalam kategori tersebut.")

with container1:
    graphs1()
    analysis1()

with container2:
    graphs2()
    analysis2()

with container3:
    graphs3()
    analysis3()

with container4:
    graphs4()
    analysis4()

import pandas as pd
import mysql.connector as sql
import streamlit as st 
import plotly.express as px
import os 
import json
from streamlit_option_menu import option_menu
from PIL import Image


# Set the Git executable path
os.environ['GIT_PYTHON_GIT_EXECUTABLE'] = r'C:\Program Files\Git\bin\git.exe'

import git
from git import Repo, GitCommandError
import shutil


repo_url = 'https://github.com/PhonePe/pulse'
clone_dir = r'C:\Users\Vinayagamoorthi M\Desktop\my_streamlit_project\phonepe_pulse_repo2'

try:
    if os.path.exists(clone_dir):
        shutil.rmtree(clone_dir)  # Try removing if exists
    Repo.clone_from(repo_url, clone_dir)
    print('Repository cloned successfully.')
except Exception as e:
    print(f"An error occurred: {e}")


# Setting up page configuration
icon = Image.open("ICN.png")
st.set_page_config(page_title= "Phonepe Pulse Data Visualization | By Vinayagamoorthi",
                   page_icon= icon,
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   menu_items={'About': """# This dashboard app is created by *Vinayagamoorthi*!
                                        Data has been cloned from Phonepe Pulse Github Repo"""})

st.sidebar.header(":wave: :violet[**Hello! Welcome to the dashboard**]")    

# Dataframe of aggregated Transactions

path1 = r"C:\Users\Vinayagamoorthi M\Desktop\my_streamlit_project\phonepe_pulse_repo2\data\aggregated\transaction\country\india\state"
agg_trans_list = os.listdir(path1)
columns1 = {'State': [], 'Year': [], 'Quarter': [], 'Transaction_type': [], 'Transaction_count': [], 'Transaction_amount': []}

for state in agg_trans_list:
    cur_state = os.path.join(path1, state)
    if not os.path.isdir(cur_state):
        print(f"Skipping non-directory {cur_state}")
        continue
    agg_year_list = os.listdir(cur_state)
    
    for year in agg_year_list:
        cur_year = os.path.join(cur_state, year)
        if not os.path.isdir(cur_year):
            print(f"Skipping non-directory {cur_year}")
            continue
        agg_file_list = os.listdir(cur_year)
        
        for file in agg_file_list:
            cur_file = os.path.join(cur_year, file)
            if not os.path.isfile(cur_file):
                print(f"Skipping non-file {cur_file}")
                continue
            with open(cur_file, 'r') as data:
                A = json.load(data)
            
            for i in A['data']['transactionData']:
                name = i['name']
                count = i['paymentInstruments'][0]['count']
                amount = i['paymentInstruments'][0]['amount']
                columns1['Transaction_type'].append(name)
                columns1['Transaction_count'].append(count)
                columns1['Transaction_amount'].append(amount)
                columns1['State'].append(state)
                columns1['Year'].append(year)
                columns1['Quarter'].append(int(file.strip('.json')))
                
df_agg_trans = pd.DataFrame(columns1)

print(df_agg_trans.shape)

# Dataframe of aggregated user

path2 = r"C:\Users\Vinayagamoorthi M\Desktop\my_streamlit_project\phonepe_pulse_repo2\data\aggregated\user\country\india\state"

agg_user_list = os.listdir(path2)

columns2= {'State': [], 'Year': [], 'Quarter': [], 'Brands': [], 'Count': [], 'Percentage': []}

for state in agg_user_list:
    cur_state = os.path.join(path2,state)
    if not os.path.isdir(cur_state):
        print(f"Skipping non-directory {cur_state}")
        continue
    agg_user_list = os.listdir(cur_state)

    for year in agg_year_list:
        cur_year = os.path.join(cur_state, year)
        if not os.path.isdir(cur_year):
            print(f"Skipping non-directory {cur_year}")
            continue
        agg_file_list = os.listdir(cur_year)
        
        for file in agg_file_list:
            cur_file = os.path.join(cur_year, file)
            if not os.path.isfile(cur_file):
                print(f"Skipping non-file {cur_file}")
                continue
            with open(cur_file, 'r') as data:
                B = json.load(data)

            try:
                for i in B["data"]["usersByDevice"]:
                    brand_name = i["brand"]
                    counts = i["count"]
                    percents = i["percentage"]
                    columns2["Brands"].append(brand_name)
                    columns2["Count"].append(counts)
                    columns2["Percentage"].append(percents)
                    columns2["State"].append(state)
                    columns2["Year"].append(year)
                    columns2["Quarter"].append(int(file.strip('.json')))
            except:
                pass
df_agg_user = pd.DataFrame(columns2)

print(df_agg_user)

# Dataframe of map transactions

path3 = r"C:\Users\Vinayagamoorthi M\Desktop\my_streamlit_project\phonepe_pulse_repo2\data\map\transaction\hover\country\india\state"

map_trans_list = os.listdir(path3)

columns3 = {'State': [], 'Year': [], 'Quarter': [], 'District': [], 'Count': [], 'Amount': []}

for state in map_trans_list:
    cur_state = os.path.join(path3,state)
    if not os.path.isdir(cur_state):
        print(f"Skipping non-directory {cur_state}")
        continue
    map_year_list = os.listdir(cur_state)

    for year in map_year_list:
        cur_year = os.path.join(cur_state, year)
        if not os.path.isdir(cur_year):
            print(f"Skipping non-directory {cur_year}")
            continue
        map_file_list = os.listdir(cur_year)
        
        for file in map_file_list:
            cur_file = os.path.join(cur_year, file)
            if not os.path.isfile(cur_file):
                print(f"Skipping non-file {cur_file}")
                continue
            with open(cur_file, 'r') as data:
                C = json.load(data)

                for i in C["data"]["hoverDataList"]:
                    district = i["name"]
                    count = i["metric"][0]["count"]
                    amount = i["metric"][0]["amount"]
                    columns3["District"].append(district)
                    columns3["Count"].append(count)
                    columns3["Amount"].append(amount)
                    columns3['State'].append(state)
                    columns3['Year'].append(year)
                    columns3['Quarter'].append(int(file.strip('.json')))
                
df_map_trans = pd.DataFrame(columns3)

print (df_map_trans)

# Dataframe of map user

path4 = r"C:\Users\Vinayagamoorthi M\Desktop\my_streamlit_project\phonepe_pulse_repo2\data\map\user\hover\country\india\state"

map_user_list = os.listdir(path4)

columns4 = {"State": [], "Year": [], "Quarter": [], "District": [], "RegisteredUser": [], "AppOpens": []}

for state in map_user_list:
    cur_state = os.path.join(path4,state)
    if not os.path.isdir(cur_state):
        print(f"Skipping non-directory {cur_state}")
        continue
    map_year_list = os.listdir(cur_state)

    for year in map_year_list:
        cur_year = os.path.join(cur_state, year)
        if not os.path.isdir(cur_year):
            print(f"Skipping non-directory {cur_year}")
            continue
        map_file_list = os.listdir(cur_year)
        
        for file in map_file_list:
            cur_file = os.path.join(cur_year, file)
            if not os.path.isfile(cur_file):
                print(f"Skipping non-file {cur_file}")
                continue
            with open(cur_file, 'r') as data:
                D = json.load(data)

            for i in D["data"]["hoverData"].items():
                district = i[0]
                registereduser = i[1]["registeredUsers"]
                appOpens = i[1]['appOpens']
                columns4["District"].append(district)
                columns4["RegisteredUser"].append(registereduser)
                columns4["AppOpens"].append(appOpens)
                columns4['State'].append(state)
                columns4['Year'].append(year)
                columns4['Quarter'].append(int(file.strip('.json')))
                
df_map_user = pd.DataFrame(columns4)                

print (df_map_user)

# Dataframe of top transactions

path5 = r"C:\Users\Vinayagamoorthi M\Desktop\my_streamlit_project\phonepe_pulse_repo2\data\top\transaction\country\india\state"

top_trans_list = os.listdir(path5)

columns5 = {'State': [], 'Year': [], 'Quarter': [], 'Pincode': [], 'Transaction_count': [], 'Transaction_amount': []}

for state in top_trans_list:
    cur_state = os.path.join(path5,state)
    if not os.path.isdir(cur_state):
        print(f"Skipping non-directory {cur_state}")
        continue
    top_year_list = os.listdir(cur_state)

    for year in top_year_list:
        cur_year = os.path.join(cur_state, year)
        if not os.path.isdir(cur_year):
            print(f"Skipping non-directory {cur_year}")
            continue
        top_file_list = os.listdir(cur_year)
        
        for file in top_file_list:
            cur_file = os.path.join(cur_year, file)
            if not os.path.isfile(cur_file):
                print(f"Skipping non-file {cur_file}")
                continue
            with open(cur_file, 'r') as data:
                E = json.load(data)

            for i in E['data']['pincodes']:
                name = i['entityName']
                count = i['metric']['count']
                amount = i['metric']['amount']
                columns5['Pincode'].append(name)
                columns5['Transaction_count'].append(count)
                columns5['Transaction_amount'].append(amount)
                columns5['State'].append(state)
                columns5['Year'].append(year)
                columns5['Quarter'].append(int(file.strip('.json')))
df_top_trans = pd.DataFrame(columns5)               

print(df_top_trans)


# Dataframe of top users

path6 = r"C:\Users\Vinayagamoorthi M\Desktop\my_streamlit_project\phonepe_pulse_repo2\data\top\user\country\india\state"

top_user_list = os.listdir(path6)

columns6 = {'State': [], 'Year': [], 'Quarter': [], 'Pincode': [], 'RegisteredUsers': []}

for state in top_user_list:
    cur_state = os.path.join(path6,state)
    if not os.path.isdir(cur_state):
        print(f"Skipping non-directory {cur_state}")
        continue
    top_year_list = os.listdir(cur_state)

    for year in top_year_list:
        cur_year = os.path.join(cur_state, year)
        if not os.path.isdir(cur_year):
            print(f"Skipping non-directory {cur_year}")
            continue
        top_file_list = os.listdir(cur_year)
        
        for file in top_file_list:
            cur_file = os.path.join(cur_year, file)
            if not os.path.isfile(cur_file):
                print(f"Skipping non-file {cur_file}")
                continue
            with open(cur_file, 'r') as data:
                F = json.load(data)

                for i in F['data']['pincodes']:
                    name = i['name']
                    registeredUsers = i['registeredUsers']
                    columns6['Pincode'].append(name)
                    columns6['RegisteredUsers'].append(registeredUsers)
                    columns6['State'].append(state)
                    columns6['Year'].append(year)
                    columns6['Quarter'].append(int(file.strip('.json')))
df_top_user = pd.DataFrame(columns6) 

print(df_top_user)

df_agg_trans.isnull().sum()
df_agg_user.isnull().sum()
df_map_trans.isnull().sum()
df_map_user.isnull().sum()
df_top_trans.isnull().sum()
df_top_user.isnull().sum()

# Remove rows with NaN Pincode values
df_top_trans = df_top_trans.dropna(subset=['Pincode'])


# Converting Dataframes to CSV files

df_agg_trans.to_csv('agg_trans.csv',index=False)
df_agg_user.to_csv('agg_user.csv',index=False)
df_map_trans.to_csv('map_trans.csv',index=False)
df_map_user.to_csv('map_user.csv',index=False)
df_top_trans.to_csv('top_trans.csv',index=False)
df_top_user.to_csv('top_user.csv',index=False)

# Creating connection with MySQL
mydb = sql.connect(
        user='root',
        password='Admin',
        host='localhost',
        database= 'phonepe_pulse'
    )
mycursor = mydb.cursor(buffered=True)  

# mycursor.execute("CREATE DATABASE IF NOT EXISTS phonepe_pulse")

# Create tables
    # Creating agg_trans table
mycursor.execute("""
        CREATE TABLE IF NOT EXISTS agg_trans (
            State VARCHAR(255),
            Year INT,
            Quarter INT,
            Transaction_type VARCHAR(255),
            Transaction_count INT,
            Transaction_amount double,
            PRIMARY KEY(State,Year,Quarter,Transaction_type)                 
        )
    """)

# Insert rows into the agg_trans table

for i, row in df_agg_trans.iterrows():
    sql = """
        INSERT INTO agg_trans (State, Year, Quarter, Transaction_type, Transaction_count, Transaction_amount)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            Transaction_count = VALUES(Transaction_count),
            Transaction_amount = VALUES(Transaction_amount)
    """
    mycursor.execute(sql, tuple(row))

# Commit all changes at once
mydb.commit()

# Creating agg_user table

mycursor.execute("""
        CREATE TABLE IF NOT EXISTS agg_user (
            State VARCHAR(255),
            Year INT,
            Quarter INT,
            Brands varchar(255),
            Count int,
            Percentage double,
            PRIMARY KEY (State, Year, Quarter, Brands)
        )
    """)
# Insert rows into the df_agg_user table
for i, row in df_agg_user.iterrows():
    sql = """
        INSERT INTO agg_user (State, Year, Quarter, Brands, Count, Percentage)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            Count = VALUES(Count),
            Percentage = VALUES(Percentage)
    """
    mycursor.execute(sql, tuple(row))

# Commit all changes at once
mydb.commit()

# Creating map_trans table

mycursor.execute("""
        CREATE TABLE IF NOT EXISTS map_trans (
            State VARCHAR(255),
            Year INT,
            Quarter INT,
            District varchar(255),
            Count int,
            Amount double,
            PRIMARY KEY (State, Year, Quarter, District)
        )
    """)
# Insert rows into the map_trans table
for i, row in df_map_trans.iterrows():
    sql = """
        INSERT INTO map_trans (State, Year, Quarter, District, Count, Amount)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            Count = VALUES(Count),
            Amount = VALUES(Amount)
    """
    mycursor.execute(sql, tuple(row))

# Commit all changes at once
mydb.commit()

    
# Creating map_user table

mycursor.execute("""
        CREATE TABLE IF NOT EXISTS map_user (
            State VARCHAR(255),
            Year INT,
            Quarter INT,
            District varchar(255),
            Registered_user int,
            App_opens int,
            PRIMARY KEY (State, Year, Quarter, District)      
        )
    """)
# Insert rows into the df_map_user table
for i, row in df_map_user.iterrows():
    sql = """
        INSERT INTO map_user (State, Year, Quarter, District, Registered_user, App_opens)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            Registered_user = VALUES(Registered_user),
            App_opens = VALUES(App_opens)
    """
    mycursor.execute(sql, tuple(row))

# Commit all changes at once
mydb.commit()


# Creating top_trans table

mycursor.execute("""
        CREATE TABLE IF NOT EXISTS top_trans (
            State VARCHAR(255),
            Year INT,
            Quarter INT,
            Pincode INT,
            Transaction_count int,
            Transaction_amount double,
            PRIMARY KEY (State, Year, Quarter, Pincode)
        )
    """)
# Insert rows into the top_trans table
for i, row in df_top_trans.iterrows():
    sql = """
        INSERT INTO top_trans (State, Year, Quarter, Pincode, Transaction_count, Transaction_amount)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            Transaction_count = VALUES(Transaction_count),
            Transaction_amount = VALUES(Transaction_amount)
    """
    mycursor.execute(sql, tuple(row))

# Commit all changes at once
mydb.commit()
   

# Creating top_user table

mycursor.execute("""
        CREATE TABLE IF NOT EXISTS top_user (
            State VARCHAR(255),
            Year INT,
            Quarter INT,
            Pincode INT,
            Registered_users int,
            PRIMARY KEY (State, Year, Quarter, Pincode)
        )
    """)
# Insert rows into the top_user table
for i, row in df_top_user.iterrows():
    sql = """
        INSERT INTO top_user (State, Year, Quarter, Pincode, Registered_users)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            Registered_users = VALUES(Registered_users)
    """
    mycursor.execute(sql, tuple(row))

# Commit all changes at once
mydb.commit()
  

# List of tables

mycursor.execute("show tables")
mycursor.fetchall()

# Creating option menu in the side bar
with st.sidebar:
    selected = option_menu("Menu", ["Home","Top Charts","Explore Data","About"], 
                icons=["house","graph-up-arrow","bar-chart-line", "exclamation-circle"],
                menu_icon= "menu-button-wide",
                default_index=0,
                styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#6F36AD"},
                        "nav-link-selected": {"background-color": "#6F36AD"}})

# MENU 1 - HOME
if selected == "Home":
    st.image("img.png")
    st.markdown("# :violet[Data Visualization and Exploration]")
    st.markdown("## :violet[A User-Friendly Tool Using Streamlit and Plotly]")
    col1,col2 = st.columns([3,2],gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("### :violet[Domain :] Fintech")
        st.markdown("### :violet[Technologies used :] Github Cloning, Python, Pandas, MySQL, mysql-connector-python, Streamlit, and Plotly.")
        st.markdown("### :violet[Overview :] In this streamlit web app you can visualize the phonepe pulse data and gain lot of insights on transactions, number of users, top 10 state, district, pincode and which brand has most number of users and so on. Bar charts, Pie charts and Geo map visualization are used to get some insights.")
    with col2:
        st.image("home.png") 

# MENU 2 - TOP CHARTS
if selected == "Top Charts":
    st.markdown("## :violet[Top Charts]")
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    colum1,colum2= st.columns([1,1.5],gap="large")
    with colum1:
        Year = st.slider("**Year**", min_value=2018, max_value=2024)
        Quarter = st.slider("Quarter", min_value=1, max_value=4)
    
    with colum2:
        st.info(
                """
                #### From this menu we can get insights like :
                - Overall ranking on a particular Year and Quarter.
                - Top 10 State, District, Pincode based on Total number of transaction and Total amount spent on phonepe.
                - Top 10 State, District, Pincode based on Total phonepe users and their app opening frequency.
                - Top 10 mobile brands and its percentage based on the how many people use phonepe.
                """,icon="🔍"
                )  

# Top Charts - TRANSACTIONS    
    if Type == "Transactions":
        col1,col2,col3 = st.columns([1,1,1],gap="small")
        
        with col1:
            st.markdown("### :violet[State]")
            mycursor.execute(f"select state, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from agg_trans where year = {Year} and quarter = {Quarter} group by state order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Transactions_Count','Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                             names='State',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
        with col2:
            st.markdown("### :violet[District]")
            mycursor.execute(f"select district , sum(Count) as Total_Count, sum(Amount) as Total from map_trans where year = {Year} and quarter = {Quarter} group by district order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Transactions_Count','Total_Amount'])

            fig = px.pie(df, values='Total_Amount',
                             names='District',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
        with col3:
            st.markdown("### :violet[Pincode]")
            mycursor.execute(f"select pincode, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from top_trans where year = {Year} and quarter = {Quarter} group by pincode order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Transactions_Count','Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                             names='Pincode',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

# Top Charts - USERS          
    if Type == "Users":
        col1,col2,col3,col4 = st.columns([1,1,1,1],gap="small")
        
        with col1:
            st.markdown("### :violet[Brands]")
            if Year == 2024 and Quarter in [2,3,4]:
                st.markdown("#### Sorry No Data to Display for 2024 Qtr 2,3,4")
            else:
                mycursor.execute(f"select brands, sum(count) as Total_Count, avg(percentage)*100 as Avg_Percentage from agg_user where year = {Year} and quarter = {Quarter} group by brands order by Total_Count desc limit 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['Brand', 'Total_Users','Avg_Percentage'])
                fig = px.bar(df,
                             title='Top 10',
                             x="Total_Users",
                             y="Brand",
                             orientation='h',
                             color='Avg_Percentage',
                             color_continuous_scale=px.colors.sequential.Agsunset)
                st.plotly_chart(fig,use_container_width=True)   
    
        with col2:
            st.markdown("### :violet[District]")
            mycursor.execute(f"select district, sum(Registered_User) as Total_Users, sum(app_opens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by district order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Total_Users','Total_Appopens'])
            df.Total_Users = df.Total_Users.astype(float)
            fig = px.bar(df,
                         title='Top 10',
                         x="Total_Users",
                         y="District",
                         orientation='h',
                         color='Total_Users',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)
              
        with col3:
            st.markdown("### :violet[Pincode]")
            mycursor.execute(f"select Pincode, sum(Registered_Users) as Total_Users from top_user where year = {Year} and quarter = {Quarter} group by Pincode order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Total_Users'])
            fig = px.pie(df,
                         values='Total_Users',
                         names='Pincode',
                         title='Top 10',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Total_Users'])
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
        with col4:
            st.markdown("### :violet[State]")
            mycursor.execute(f"select state, sum(Registered_user) as Total_Users, sum(App_opens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by state order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
            fig = px.pie(df, values='Total_Users',
                             names='State',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Total_Appopens'],
                             labels={'Total_Appopens':'Total_Appopens'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

# MENU 3 - EXPLORE DATA
if selected == "Explore Data":
    Year = st.sidebar.slider("**Year**", min_value=2018, max_value=2024)
    Quarter = st.sidebar.slider("Quarter", min_value=1, max_value=4)
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    col1,col2 = st.columns(2)             

# EXPLORE DATA - TRANSACTIONS
    if Type == "Transactions":
        
        # Overall State Data - TRANSACTIONS AMOUNT - INDIA MAP 
        with col1:
            st.markdown("## :violet[Overall State Data - Transactions Amount]")
            mycursor.execute(f"select state, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year} and quarter = {Quarter} group by state order by state")
            df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
            df2 = pd.read_csv(r'C:\Users\Vinayagamoorthi M\Desktop\my_streamlit_project\Statenames.csv')
            df1.State = df2

            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                      featureidkey='properties.ST_NM',
                      locations='State',
                      color='Total_amount',
                      color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)
            
        # Overall State Data - TRANSACTIONS COUNT - INDIA MAP
        with col2:
            
            st.markdown("## :violet[Overall State Data - Transactions Count]")
            mycursor.execute(f"select state, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year} and quarter = {Quarter} group by state order by state")
            df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
            df2 = pd.read_csv(r'C:\Users\Vinayagamoorthi M\Desktop\my_streamlit_project\Statenames.csv')
            df1['Total_Transactions'] = df1['Total_Transactions'].astype(pd.Int64Dtype())
            df1.State = df2

            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                      featureidkey='properties.ST_NM',
                      locations='State',
                      color='Total_Transactions',
                      color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)

# BAR CHART - TOP PAYMENT TYPE
        st.markdown("## :violet[Top Payment Type]")
        mycursor.execute(f"select Transaction_type, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from agg_trans where year= {Year} and quarter = {Quarter} group by transaction_type order by Transaction_type")
        df = pd.DataFrame(mycursor.fetchall(), columns=['Transaction_type', 'Total_Transactions','Total_amount'])

        fig = px.bar(df,
                     title='Transaction Types vs Total_Transactions',
                     x="Transaction_type",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=False)         

# BAR CHART TRANSACTIONS - DISTRICT WISE DATA            
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("## :violet[Select any State to explore more]")
        selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
         
        mycursor.execute(f"select State, District,year,quarter, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year} and quarter = {Quarter} and State = '{selected_state}' group by State, District,year,quarter order by state,district")
        
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['State','District','Year','Quarter',
                                                         'Total_Transactions','Total_amount'])
        fig = px.bar(df1,
                     title=selected_state,
                     x="District",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)

# EXPLORE DATA - USERS      
    if Type == "Users":
        
        # Overall State Data - TOTAL APPOPENS - INDIA MAP
        st.markdown("## :violet[Overall State Data - User App opening frequency]")
        mycursor.execute(f"select state, sum(Registered_user) as Total_Users, sum(App_opens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by state order by state")
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
        df2 = pd.read_csv(r'C:\Users\Vinayagamoorthi M\Desktop\my_streamlit_project\Statenames.csv')
        
        df1.Total_Appopens = df1.Total_Appopens.astype(float)
        df1.State = df2
        
        fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                  featureidkey='properties.ST_NM',
                  locations='State',
                  color='Total_Appopens',
                  color_continuous_scale='sunset')

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig,use_container_width=True)                                                              

# BAR CHART TOTAL UERS - DISTRICT WISE DATA 
        st.markdown("## :violet[Select any State to explore more]")
        selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
        
        mycursor.execute(f"select State,year,quarter,District,sum(Registered_user) as Total_Users, sum(App_opens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} and state = '{selected_state}' group by State, District,year,quarter order by state,district")
        
        df = pd.DataFrame(mycursor.fetchall(), columns=['State','year', 'quarter', 'District', 'Total_Users','Total_Appopens'])
        df.Total_Users = df.Total_Users.astype(int)
        
        fig = px.bar(df,
                     title=selected_state,
                     x="District",
                     y="Total_Users",
                     orientation='v',
                     color='Total_Users',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)

# MENU 4 - ABOUT
if selected == "About":
    col1,col2 = st.columns([3,3],gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("### :violet[About PhonePe Pulse:] ")
        st.write("##### BENGALURU, India, On Sept. 3, 2021 PhonePe, India's leading fintech platform, announced the launch of PhonePe Pulse, India's first interactive website with data, insights and trends on digital payments in the country. The PhonePe Pulse website showcases more than 2000+ Crore transactions by consumers on an interactive map of India. With  over 45% market share, PhonePe's data is representative of the country's digital payment habits.")
        
        st.write("##### The insights on the website and in the report have been drawn from two key sources - the entirety of PhonePe's transaction data combined with merchant and customer interviews. The report is available as a free download on the PhonePe Pulse website and GitHub.")
        
        st.markdown("### :violet[About PhonePe:] ")
        st.write("##### PhonePe is India's leading fintech platform with over 300 million registered users. Using PhonePe, users can send and receive money, recharge mobile, DTH, pay at stores, make utility payments, buy gold and make investments. PhonePe forayed into financial services in 2017 with the launch of Gold providing users with a safe and convenient option to buy 24-karat gold securely on its platform. PhonePe has since launched several Mutual Funds and Insurance products like tax-saving funds, liquid funds, international travel insurance and Corona Care, a dedicated insurance product for the COVID-19 pandemic among others. PhonePe also launched its Switch platform in 2018, and today its customers can place orders on over 600 apps directly from within the PhonePe mobile app. PhonePe is accepted at 20+ million merchant outlets across Bharat")
        
        st.write("**:violet[My Project GitHub link]** ⬇️")
        st.write("https://github.com/Vinaymca91/phonepepluse")
        st.write("**:violet[Image and content source]** ⬇️")
        st.write("https://www.prnewswire.com/in/news-releases/phonepe-launches-the-pulse-of-digital-payments-india-s-first-interactive-geospatial-website-888262738.html")
        
    with col2:
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.image("Pulseimg.jpg")                  
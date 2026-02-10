
# PANDAS Installation
- python3 -m pip install pandas mysql-connector-python SQLAlchemy
- python3 -m pip install "pandas[test]"
- python3 -m pip install "pandas[performance]"
- python3 -m pip install "pandas[plot, output-formatting]"
- python3 -m pip install "pandas[computation]"
- python3 -m pip install "pandas[excel]"
- python3 -m pip install "pandas[html]"
- python3 -m pip install "pandas[postgresql, mysql, sql-other]"

# PANDAS test
- python3
        
        -   import pandas as pd
        -   pd.test()

# CSV file read with Pandas
- import pandas as pd
- df = pd.read_csv('data.csv')
- print(df.to_string()) 

# JSON file read with Pandas
- import pandas as pd
- df = pd.read_json('data.json')
- print(df.to_string())

# Pandas dataframe cells management
- import pandas as pd
- df = pd.read_csv('data.csv')
- new_df = df.dropna()                                          # remove empty cells
- new_df = df.dropna(inplace = True)                            # remove cells with NULL values
- df.fillna(130, inplace = True)                                # Replace NULL values with default number ( 130 )
- df.fillna({"Calories": 130}, inplace=True)                    # Replace NULL values with default number only for column 'Calories'
- x = df['Calories'].mean()
- x = df['Calories'].median()
- x = df['Calories'].mode()
- df_fillna({'Calories': x}, implace=True)                      # Calculate the MEAN, MEDIAN or MODE, and replace any empty values with it
- df['Date'] = pd.to_datetime(df['Date'], format='mixed')       # date format for 'Date' column data 
- df.dropna(subset=['Date'], inplace = True)                    # Remove rows with a NULL value in the "Date" column
- df.loc[7, 'Duration'] = 45                                    # Set "Duration" = 45 in row 7
- loop example

        # max limit value of 120 set
        for x in df.index:
                if df.loc[x, "Duration"] > 120:
                df.loc[x, "Duration"] = 120

        # Delete rows where "Duration" is higher than 120 
        for x in df.index:
                if df.loc[x, "Duration"] > 120:
                df.drop(x, inplace = True)

- df.drop_duplicates(inplace = True)                            # Remove all duplicates

- print(new_df.to_string())

# Data Plot visualization
- import pandas as pd
- import matplotlib.pyplot as plt
- df = pd.read_csv('data.csv')
- df.plot()
- df["Duration"].plot(kind = 'hist')
- plt.show()

# DB management ( mysql example )
- nano db_manager.py

        import pandas as pd
        import mysql.connector
        from sqlalchemy import create_engine  #   consigliato per Pandas

        db_config = {
                "host": "localhost",
                "user": "root",
                "password": "",
                "database": "utils",
        }

        query = "SELECT * FROM users ORDER BY id DESC;"

        #   Connessione con SQLAlchemy
        #   --------------------------
        engine = create_engine(
        f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}"
        )
        try:
                df = pd.read_sql(query, engine)
                print(df.head())        # Prime 5 righe del DataFrame
                print(df.tail())        # Ultime 5
                print(df.info())        # Info
        except Exception as e:
                print(f"Errore durante la lettura del database: {e}")

        #   Connessione con mysql.connector
        #   -------------------------------
        # conn = mysql.connector.connect(**db_config)
        # df = pd.read_sql(query, conn)
        # conn.close()


from .config import connection
from SQL_Scripts.SQL_queries import invalid_DOB
import pandas as pd
import pytest
import os
import re

try:
    # connection to CSV and sql
    @pytest.fixture(scope="module")
    def df_csv():
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(base_dir, 'Data', 'sample_data_validation.csv')
        return pd.read_csv(file_path)


    @pytest.fixture(scope="module")
    def df_SQL():
        query = "SELECT * FROM SampleDataValidation"
        return pd.read_sql(query, connection())


    #Null check
    def test_null_check_name(df_csv,df_SQL):
        null_csv=df_csv["Name"].isnull().sum()
        null_SQl=df_SQL["Name"].isnull().sum()
        if  null_SQl!=0 or null_csv!=0:
            print("null check failed null check")
            print("----------------------------------------------------------------------")
        else:
            print("null check Passed null check")
            print("----------------------------------------------------------------------")
        assert null_csv==0 and null_SQl==0,"null check failed for column Name"


    def test_null_check_Country(df_csv,df_SQL):
        null_csv=df_csv["Country"].isnull().sum()
        null_SQl=df_SQL["Country"].isnull().sum()
        if  null_SQl!=0 or null_csv!=0:
            print("null check failed for country columnn")
            print("----------------------------------------------------------------------")
        else:
            print("null check Passed for country columnn")
            print("----------------------------------------------------------------------")
        assert null_csv == 0 and null_SQl == 0, "null check failed for column Country"

    #duplicate Check
    def test_duplicate_check(df_csv,df_SQL):
        null_csv=df_csv[["Name","PhoneNumber"]].duplicated(keep=False).sum()
        null_SQl=df_SQL[["Name","PhoneNumber"]].duplicated(keep=False).sum()
        if  null_SQl!=0 and null_csv!=0:
            print("failed duplicate check")
            print("----------------------------------------------------------------------")
        else:
            print("Passed dupliacte check")
            print("----------------------------------------------------------------------")
        assert null_csv == 0 and null_SQl == 0, "Duplicate check failed for column Name,PhoneNumber"


    def test_date_format(df_csv, df_SQL):
        # Convert to datetime
        df_csv["DateOfBirth"] = pd.to_datetime(df_csv["DateOfBirth"], errors='coerce')
        df_SQL["DateOfBirth"] = pd.to_datetime(df_SQL["DateOfBirth"], errors='coerce')

        # Format dates as strings
        check_csv = df_csv["DateOfBirth"].dropna().dt.strftime("%Y-%m-%d").reset_index(drop=True)
        check_sql = df_SQL["DateOfBirth"].dropna().dt.strftime("%Y-%m-%d").reset_index(drop=True)

        # Check if both have data
        if not check_csv.empty and not check_sql.empty:
            mismatch_found = False

            # Assuming both dataframes are aligned row-by-row
            for i in range(min(len(check_csv), len(check_sql))):
                if check_csv.iloc[i] != check_sql.iloc[i]:
                    print(f"Mismatch at row {i + 1}: CSV = {check_csv.iloc[i]}, SQL = {check_sql.iloc[i]}")
                    print("----------------------------------------------------------------------")
                    mismatch_found = True

            if not mismatch_found:
                print("Date format check passed. All rows match.")
                print("----------------------------------------------------------------------")
            else:
                print("Date format check completed with mismatches.")
                print("----------------------------------------------------------------------")
        else:
            print("No valid dates found in one or both datasets.")
            print("----------------------------------------------------------------------")

        assert len(check_csv) == len(df_csv["DateOfBirth"]), (
            f"Some dates are dropped due to not in correct format: CSV has {len(check_csv)}, SQL has {len(df_csv["DateOfBirth"])}"
        )
        assert len(check_csv) == len(check_sql), (
            f"Date mismatch in number of valid rows: CSV has {len(check_csv)}, SQL has {len(check_sql)}"
        )
        assert check_csv.equals(check_sql), (
            f"Date format mismatch found.\nCSV Dates:\n{check_csv}\n\nSQL Dates:\n{check_sql}"
        )


    def test_valid_number(df_csv, df_SQL):
        # Compile regex pattern for 10-digit phone numbers (Indian format with optional +91)
        pattern = re.compile(r'^(\+91)?[6-9]\d{9}$')

        df_number = df_csv["PhoneNumber"].astype(str)
        flag=0

        for i, phone in enumerate(df_number):
            if pattern.match(phone):
                continue
            else:
                print(f"Row {i + 1}: Phone number '{phone}' is NOT valid")
                print("----------------------------------------------------------------------")
                flag=1
        assert flag==0,"Phone number validation failed for column PhoneNumber"

    def test_age():
        Query=invalid_DOB()
        df_age=pd.read_sql(Query,connection())
        #print(df_age)
        assert df_age.empty,"Some incorrect ages are present in data"

    def test_frame_check(df_csv, df_SQL):
        df_csv['DateOfBirth'] = df_csv['DateOfBirth'].astype(str)
        df_SQL['DateOfBirth'] = df_SQL['DateOfBirth'].astype(str)

        pd.testing.assert_frame_equal(
    df_csv.reset_index(drop=True),
    df_SQL.reset_index(drop=True),
    check_dtype=False
)



    '''
    test_null_check_name(df_CSV,df_SQL)
    test_null_check_Country(df_CSV,df_SQL)
    test_duplicate_check(df_CSV,df_SQL)
    date_format(df_CSV,df_SQL)
    valid_number(df_CSV,df_SQL)
    '''

except:
    print("Error occured Please check your functions")
    print("----------------------------------------------------------------------")

finally:
    print("----------------------------------------------------------------------")
    print("Test_run completed")
    print("----------------------------------------------------------------------")


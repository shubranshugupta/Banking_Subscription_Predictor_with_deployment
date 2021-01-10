import os

import numpy as np
import pandas as pd

from Utill import util1
from bs4 import BeautifulSoup

global df_org, df_modify, __model, file_name
file_path1 = "Data/File to save"
file_path2 = "Data/File to send"
file_path3 = "Data/Html file"
default_val_for_nan = {"age": 40, "job": "admin.", "marital": "married", "education": "university.degree",
                       "default": "no", "contact": "cellular", "month": "may", "day_of_week": "thu",
                       "duration": 999, "campaign": 2.57, "pdays": 962.47, "previous": 0.173, "poutcome": "nonexistent",
                       "emp.var.rate": 0.0818, "cons.price.idx": 93.575, "cons.conf.idx": -40.502}

util1.load_file()


def get_dummy():
    global df_modify
    dummy_col_lst = (
        "job_blue-collar", "job_entrepreneur", "job_housemaid", "job_management", "job_retired", "job_self-employed",
        "job_services",
        "job_student", "job_technician", "job_unemployed", "job_unknown", "marital_married", "marital_single",
        "marital_unknown", "default_unknown",
        "default_yes", "contact_telephone", "month_aug", "month_dec", "month_jul", "month_jun", "month_mar",
        "month_may",
        "month_nov", "month_oct",
        "month_sep", "day_of_week_mon", "day_of_week_thu", "day_of_week_tue", "day_of_week_wed")
    drop_lst = ("job_admin.", "marital_divorced", "default_no", "contact_cellular", "month_apr", "day_of_week_fri")
    dummy_df = pd.get_dummies(df_modify.loc[:, ["job", "marital", "default", "contact", "month", "day_of_week"]])
    for i in dummy_col_lst:
        if i not in list(dummy_df.columns):
            dummy_df[i] = np.zeros(len(dummy_df.index))
        continue
    for i in drop_lst:
        if i in list(dummy_df.columns):
            dummy_df.drop(i, inplace=True, axis=1)
        continue
    return dummy_df


def get_mapped():
    global df_modify
    edu = util1.edu_dict
    pout = util1.pout_dict
    df_modify["education_new"] = pd.Series(df_modify["education"]).map(edu)
    df_modify["poutcome_new"] = pd.Series(df_modify["poutcome"]).map(pout)


def get_file(file_name_server):
    global df_org, df_modify, file_name
    idx_arr = np.array(['age', 'job', 'marital', 'education', 'default', 'contact', 'month',
                        'day_of_week', 'duration', 'campaign', 'pdays', 'previous', 'poutcome',
                        'emp.var.rate', 'cons.price.idx', 'cons.conf.idx'])

    file_name = file_name_server
    try:
        df_org = pd.read_csv(os.path.join(file_path2, file_name), sep='[,:;|]', engine="python")
    except UnicodeDecodeError:
        df_org = pd.read_excel(os.path.join(file_path2, file_name))
    if np.array_equal(np.array(df_org.columns), idx_arr):
        return None
    return "Please Write Correct Columns"


def df_transform():
    global df_modify, df_org, default_val_for_nan

    if df_org.isnull().sum().sum() > 0:
        for k, v in default_val_for_nan.items():
            df_org[k].fillna(value=v, inplace=True, axis=1)

    df_modify = df_org.copy()

    drop_col = ['job', 'marital', 'education', 'default', 'contact', 'month', 'day_of_week', 'poutcome']
    reorder_col = ["age", "duration", "campaign", "pdays", "previous", "emp.var.rate", "cons.price.idx",
                   "cons.conf.idx", "job_blue-collar", "job_entrepreneur",
                   "job_housemaid", "job_management", "job_retired", "job_self-employed", "job_services", "job_student",
                   "job_technician", "job_unemployed",
                   "job_unknown", "marital_married", "marital_single", "marital_unknown", "default_unknown",
                   "default_yes", "contact_telephone", "month_aug",
                   "month_dec", "month_jul", "month_jun", "month_mar", "month_may", "month_nov", "month_oct",
                   "month_sep", "day_of_week_mon", "day_of_week_thu",
                   "day_of_week_tue", "day_of_week_wed", "education_new", "poutcome_new"]
    dummy_df = get_dummy()
    get_mapped()
    df_modify = df_modify.join(dummy_df)
    df_modify.drop(drop_col, axis=1, inplace=True)
    df_modify = df_modify.reindex(columns=reorder_col)


def predict_file():
    global __model, df_org, df_modify
    __model = util1.get_model()
    pred_dict = {0: "Not Subscribed", 1: "Subscribed"}
    pred = __model.predict(df_modify)
    df_org["Prediction"] = pd.Series(pred).map(pred_dict)
    df_modify["y"] = pred


def save_file():
    global file_name, df_modify, df_org
    if not file_name.endswith(".csv"):
        os.remove(os.path.join(file_path2, file_name))
        file_name = file_name.replace(".xlsx", ".csv")
    df_modify.to_csv(os.path.join(file_path1, file_name), index=False)
    df_org.to_csv(os.path.join(file_path2, file_name), index=False)
    df_org.to_html(os.path.join(file_path3, file_name.replace(".csv", ".html")), index=False, border=4, justify="center")
    return file_name


def return_table():
    with open(os.path.join(file_path3, file_name.replace(".csv", ".html")), 'r') as f:
        content = f.read()
        soup = BeautifulSoup(content, 'lxml')
    return str(soup.table)


def return_filename():
    return file_name


def delete_file():
    dir_to_delete = [file_path2, file_path3]
    for path1 in dir_to_delete:
        for path2 in os.listdir(path1):
            full_path = os.path.join(path1, path2)
            if os.path.isfile(full_path):
                os.remove(full_path)
import pickle
import json
import numpy as np
import pandas as pd
import os

'''
This module is contain all function that is use to do data 
transformation and prediction of data pass by form  
'''

global job_arr
__model_cat = None
__data_for_page = None

marital_arr = np.array(["married", "single", "unknown"])
default_arr = np.array(["unknown", "yes"])
comm_arr = np.array(["telephone"])
month_arr = np.array(["aug", "dec", "jul", "jun", "mar", "may", "nov", "oct", "sep"])
day_arr = np.array(["mon", "thu", "tue", "wed"])
edu_dict = {"unknown": -1, "illiterate": 0, "high.school": 1, "university.degree": 2, "professional.course": 3,
            "basic.4y": 4, "basic.6y": 5, "basic.9y": 6}
pout_dict = {"failure": 0, "nonexistent": 1, "success": 2}


def load_file():
    """
    This function use
    1. load catboost model
    2. load option.json file for option in select tag
    3. make Data folder to save data given user
    """

    path1 = "Imp_File/options.json"
    path2_cat = "ML_Model/Catboost.pkl"
    global __data_for_page, __model_cat, job_arr, marital_arr
    global month_arr, day_arr

    with open(path1, "r") as f:
        __data_for_page = json.load(f)
        job_arr = np.array(__data_for_page["job"][1:])

    if __model_cat is None:
        with open(path2_cat, "rb") as f:
            __model_cat = pickle.load(f)

    if not os.path.isdir("Data"):
        os.mkdir("Data")
    if not os.path.isdir("Data/File to save"):
        os.mkdir("Data/File to save")
        with open("Imp_File/data_by_form.txt", "r") as f1, open("Data/File to save/data_by_form.csv", "a") as f2:
            for line in f1:
                f2.write(line)
    if not os.path.isdir("Data/File to send"):
        os.mkdir("Data/File to send")
    if not os.path.isdir("Data/Html file"):
        os.mkdir("Data/Html file")


def get_data_for_page():
    """
    This function return option.json file
    """

    return __data_for_page


def __to_lower(arr):
    """
    It is use to lower the string var in list
    :param arr: List
    """

    for i, j in enumerate(arr):
        try:
            arr[i] = j.lower()
        except (AttributeError, RuntimeError):
            arr[i] = j


def __arr_of_dummy_var():
    """
    This function used to return list of column that are transform
    :return: List
    """

    return [job_arr, marital_arr, default_arr, comm_arr, month_arr, day_arr, edu_dict, pout_dict]


def dummy_str_var(arr_from_client):
    """
    This function perform dummy, ordinal feature transformation of
    array that return by user from client side
    :param arr_from_client: List of all response from client side
    :return: final list that use to send to model for prediction
    """

    final_lst = []
    final_lst.extend(arr_from_client[:8])
    __to_lower(arr_from_client)
    arr_for_dummy = __arr_of_dummy_var()
    for i, j in enumerate(arr_from_client[8:]):
        if type(arr_for_dummy[i]) != dict:
            final_lst.extend((arr_for_dummy[i] == j).astype(np.int8))
        else:
            final_lst.append(arr_for_dummy[i][j])

    return final_lst


def predict_val(arr):
    """
    This function is use to predict client subscription
    :param arr: final arr send by dummy_str_var
    :return: predicted value
    """
    pred = __model_cat.predict([arr])
    arr.append(pred[0])
    df1 = pd.read_csv("Data/File to save/data_by_form.csv")
    df1.loc[len(df1.index)] = arr
    duplicate = df1[df1.duplicated(keep='first')]
    df1.drop(duplicate.index, inplace=True)
    df1.to_csv(r"Data/File to save/data_by_form.csv", index=False)
    return str(pred[0])


# def get_model():
#     """
#     This function return model
#     :return:
#     """
#     return __model_cat

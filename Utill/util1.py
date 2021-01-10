import pickle
import json
import numpy as np
import pandas as pd

global job_arr
__model = None
__data_for_page = None

marital_arr = np.array(["married", "single", "unknown"])
default_arr = np.array(["unknown", "yes"])
comm_arr = np.array(["telephone"])
month_arr = np.array(["aug", "dec", "jul", "jun", "mar", "may", "nov", "oct", "sep"])
day_arr = np.array(["mon", "thu", "tue", "wed"])
edu_dict = {"unknown":-1, "illiterate":0, "high.school":1, "university.degree":2, "professional.course":3,
       "basic.4y":4, "basic.6y":5, "basic.9y":6}
pout_dict = {"failure":0, "nonexistent":1, "success":2}


def load_file():
    path1 = "Json File/options.json"
    path2 = "ML model/model.pkl"
    global __data_for_page, __model, job_arr, marital_arr
    global month_arr, day_arr

    with open(path1, "r") as f:
        __data_for_page = json.load(f)
        job_arr = np.array(__data_for_page["job"][1:])

    if __model is None:
        with open(path2, "rb") as f:
            __model = pickle.load(f)


def get_data_for_page():
    return __data_for_page


def __to_lower(arr):
    for i, j in enumerate(arr):
        try:
            arr[i] = j.lower()
        except (AttributeError, RuntimeError):
            arr[i] = j


def __arr_of_dummy_var():
    return [job_arr, marital_arr, default_arr, comm_arr, month_arr, day_arr, edu_dict, pout_dict]


def dummy_str_var(arr_from_client):
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
    pred = __model.predict([arr])[0]
    arr.append(pred)
    df1 = pd.read_csv("Data/File to save/data_by_form.csv")
    df1.loc[len(df1.index)] = arr
    duplicate = df1[df1.duplicated(keep='first')]
    df1.drop(duplicate.index, inplace=True)
    df1.to_csv("Data/File to save/data_by_form.csv", index=False)
    return str(pred)


def get_model():
    return __model


# if __name__ == "__main__":
#     load_file()
#     print(get_data_for_page())
#     print(__model)
#     arr = dummy_str_var([0, 0, 0, 0, 0, 0, 0, 0, "Self-employed", "Single", "No", "Cellular", "Jun", "Mon", "Illiterate", "Failure"])
#     print(type(predict_val(arr)))
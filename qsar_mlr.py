# Source Code
# Quantitative Structure Activity Relationship
# by Backward Elimination-Least Square Method
# QSAR BELS
# Created by Isman Kurniawan (IKN)
# 1 February 2020


#!/usr/bin/env python
# coding: utf-8

# In[572]:


import pandas as pd
import numpy as np
import sys
import statsmodels.api as sm
import pickle
from scipy.stats import f
#from sklearn.metrics import mean_squared_error, r2_score

# In[573]:

def qsar_web(path,calc,model):
    print("====================================================")
    print("Quantitative Structure Activity Relationship (QSAR)")
    print("Program")
    print("Created by: Isman Kurniawan (IKN)")
    print("====================================================")


    print("Data set (csv file without extension)")
    # path = input(":")
    print("\n")
    print("Calculation type")
    print("1. Model development")
    print("2. Prediction")
    # calc_type = input("(Fill by 1 or 2):")
    calc_type = calc
    calc_type = int(calc_type)
    print(calc_type)
    if calc_type == 1:
        print("\n")
        print("Number of stored model")
        # n_model = input(":")
        n_model = model
        n_model = int(n_model)
    elif calc_type == 2:
        print("\n")
        print("Model name")
        model_name = input(":")

    print("Loading the data set ...")
    data_set = pd.read_csv("{}.csv".format(path))
    data_set = data_set.iloc[:,1:]
    print("OK ...")

    if (calc_type == 1):

        file = open("output.txt","w")
        X = data_set.iloc[:,:-1]
        Y = data_set.iloc[:,-1]
        desc_list = data_set.iloc[:,:-1].columns.values.tolist()


        # In[579]:


        const = {"constant": [1]*X.shape[0]}
        const_df = pd.DataFrame(const)


        # In[580]:


        sel_desc_list = []; coeff_list = []; model_list = []
        param = pd.DataFrame(columns=['r2', 'F_ratio', 'ssr'])


        # In[581]:


        print("Performing backward elimination ...")
        kk = 1
        while len(desc_list) >= 1:
            X_sel = X.loc[:,desc_list]
            X_sel = pd.concat([const_df, X_sel], axis=1)
            model_OLS = sm.OLS(Y, X_sel).fit()
            model_list.append(model_OLS)
            ###
            sel_desc = desc_list[:]
            r2 = model_OLS.rsquared
            ###
            f_val = model_OLS.fvalue
            dfn = X_sel.shape[1] - 1
            dfd = X_sel.shape[0] - X_sel.shape[1]
            if dfd > dfn:
                tmp = dfd
                dfd = dfn
                dfn = tmp
            f_tab = f.ppf(0.05, dfn, dfd)
            f_ratio = f_val / f_tab
            ###
            ssr = model_OLS.ssr
            #q2 = q2_loo(model_OLS, X_sel.values, Y)
            coeff = model_OLS.params.values
            sel_desc_list.append(sel_desc)
            coeff_list.append(coeff)
            param = param.append({'r2': r2, 'F_ratio': f_ratio, 'ssr': ssr}, ignore_index=True)
            ###
            p_val = model_OLS.pvalues
            p_val_df = pd.DataFrame(p_val)
            p_val_df = p_val_df.iloc[1:,:]
            p_val_df.sort_values(0, ascending=False, inplace=True)
            p_val_df.reset_index(inplace=True)
            del_desc = p_val_df.iloc[0,0]
            desc_list.remove(del_desc)
            kk += 1
        print("OK ...")

        # In[582]:


        param.sort_values("r2", ascending=False, inplace=True)
        param.reset_index(inplace=True)
        best_param = param.iloc[:5,:]


        # In[583]:


        print("Writing the output ...")
        for i in range(n_model):
            idx = best_param.loc[i,"index"]
            desc_ = sel_desc_list[idx]
            model_ = model_list[idx]
            coeff_ = coeff_list[idx]
            file.write("================================== \n")
            file.write("Model {} \n".format(i+1))
            file.write("Equation: \n")
            file.write("f(x) = {} + ".format(coeff_[0]))
            for j in range(len(desc_)):
                if j == (len(desc_)-1):
                    file.write("{} {}\n".format(coeff_[-1], desc_[-1]))
                else:
                    file.write("{} {} + ".format(coeff_[j+1], desc_[j]))
            file.write("\n")
            file.write("Validation parameter:\n")
            file.write("r2 = {:.5f}\n".format(best_param.loc[i,"r2"]))
            file.write("F_ratio = {:.5f}\n".format(best_param.loc[i,"F_ratio"]))
            file.write("ssr = {:.5f}\n".format(best_param.loc[i,"ssr"]))
            file.write("================================== \n")
            file.write("\n")
            file.write("\n")
            pickle.dump([desc_, model_], open("./model_{}.p".format(i+1), "wb"))

        print("OK ...")
        # In[584]:


        idx = best_param.loc[0,"index"]
        best_model = model_list[idx]
        best_desc = sel_desc_list[idx]
        pickle.dump(best_model, open("./best_model.p", "wb"))
        pickle.dump(best_desc, open("./best_desc.p", "wb"))


        # In[585]:


        file.close()

        print("Program normally terminated ...")

    elif (calc_type == 2):

        print("Predicting activity ...")
        [desc, model] = pickle.load(open("./{}.p".format(model_name), "rb"))
        X_sel = data_set.loc[:,desc]
        const = {"constant": [1]*X_sel.shape[0]}
        const_df = pd.DataFrame(const)
        X_sel = pd.concat([const_df, X_sel], axis=1)
        pred = model.predict(X_sel)
        pred_dict = {"prediction": pred}
        pred_df = pd.DataFrame(pred_dict)
        print("OK ...")

        print("Storing the results ...")
        tmp = data_set.iloc[:,-1]
        result = pd.concat([tmp,pred_df], axis=1)
        result.to_csv("{}_pred.csv".format(model_name), index=None)
        print("Program normally terminated ...")

    else:
        print("The calculation type is not available")

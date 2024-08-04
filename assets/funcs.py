import re
def recognize(s):

    res = s.split(":")

    if res[0] == "CYN":
        return float(res[1])
    if res[0] == "RUB":
        return float(res[1])
    if res[0] == "BYN":
        return float(res[1])
    else:
        return 0


def calculator(cny, cl_type, usd_cny):

    usdt = cny / usd_cny

    if (usdt > 300):


        if (cl_type == 1):
            return usdt + (usdt * 0.05) + 15
        if(cl_type == 2):
            return usdt + (usdt * 0.05) + 5
        if (cl_type == 3):
            return usdt + (usdt * 0.05) + 2
        if (cl_type == 4):
            return usdt + (usdt * 0.05) + 10
        if (cl_type == 5):
            return usdt + (usdt * 0.05)   

    else:
        if (cl_type == 1):
            return usdt + 30

        if (cl_type == 2):
            return usdt + 20

        if (cl_type == 3):
            return usdt + 12
        
        if (cl_type == 4):
            return usdt + 25
        
        if (cl_type == 5):
            return usdt + 15
        
        


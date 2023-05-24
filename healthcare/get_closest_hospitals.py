#!/usr/bin/env python

import pandas as pd
import argparse
import json
import os
import re

def get_parser():
    """Parses arguments and returns them"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--zip_code", required=True, help="zip code of the city")
    parser.add_argument("--max_distance", required=False, help="Maximum distance of the hospital")
    return parser

def get_sorted_dict_from_df(o, max_value=None):
    o_dict = {}
    for col in o.columns:
        val = float(o[col][0])
        if max_value and val > float(max_value.strip()):
            continue
        else:
            o_dict[col] = float(o[col][0])

    o_list = sorted(o_dict.items(), key=lambda x:x[1])
    sortdict = dict(o_list)
    return sortdict


def main():
    args = get_parser().parse_args()
    zip_code = args.zip_code

    df = pd.read_csv("la_hospitals_distance_data1.csv")
    data = df[df.zip_code == int(zip_code)]

    #print(data)
    o = data.iloc[: , 4:]
    o.dropna(axis=1, how='any', inplace=True)
        
    # o = get_sorted_dict_from_df(o)

    '''
    o = get_sorted_dict_from_df(o, args.max_distance)
    print(json.dumps(o, indent=2))
    '''

    t = o.T
    t.reset_index(inplace=True)
    t.columns = ["hospital_Name", "distance"]
    #t.columns = ["distance"]
    print(t)
    print(type(t))
    print(t.describe())
   
    p = t.sort_values(by=['distance'])
    print(p)
    q = p[p.distance <= float(args.max_distance)]
    q.reset_index(inplace=True)
    print(q)

if __name__ == "__main__":
    main()

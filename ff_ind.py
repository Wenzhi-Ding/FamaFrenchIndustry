import os
from collections import defaultdict

import pandas as pd

RAW_VER = "202202"


def query(sic):
    for ind in range_dct:
        for lo, hi in range_dct[ind]:
            if lo <= sic <= hi:
                return ind
    return CLS_VER  # Default: Other industry.


if __name__ == "__main__":
    for CLS_VER in [5, 10, 12, 17, 30, 38, 48, 49]:
        with open('raw' + os.sep + RAW_VER + os.sep + f'Siccodes{CLS_VER}.txt', 'r+', encoding='utf-8') as f:
            t = f.readlines()

        range_dct = defaultdict(list)
        name_dct = defaultdict(str)
        desc_dct = defaultdict(str)
        for l in t:
            if len(l) == 1: continue
            if l[:2] != '  ':
                # print(l)
                ind = int(l[:2].strip())
                name_dct[ind] = l[3:10].strip()
                desc_dct[ind] = l[10:].strip()
            else:
                range_dct[ind].append([int(x) for x in l[10:19].split('-')])

        df = pd.DataFrame({'sic': range(100, 10000)})
        df[f'ff_{CLS_VER}ind'] = df['sic'].apply(query)
        df[f'ff_{CLS_VER}ind_name'] = df[f'ff_{CLS_VER}ind'].apply(lambda x: name_dct[x])
        df[f'ff_{CLS_VER}ind_desc'] = df[f'ff_{CLS_VER}ind'].apply(lambda x: desc_dct[x])
        df.to_csv(f'ff_{CLS_VER}ind.csv', index=False)
import pandas as pd

def inte(fname):
    for g in [2, 3, 4]:
        df = pd.read_csv(fname+'_{}_{}.csv'.format(str(2), str(1)))
        DF = pd.DataFrame(columns=df.columns)
        cnt = 0
        for k in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            df = pd.read_csv(fname+'_{}_{}.csv'.format(str(g), str(k)))
            row = round(df.mean(axis = 0), 4)
            DF.loc[cnt] = row
            cnt += 1
        DF.to_csv(fname+'_{}.csv'.format(str(g)), index=False)

inte('DOR')
inte('COM')
inte('ALG')
        # DOR = pd.read_csv('DOR_{}_{}.csv'.format(str(g), str(k)))
        # COM = pd.read_csv('COM_{}_{}.csv'.format(str(g), str(k)))
        # ALG = pd.read_csv('ALG_{}_{}.csv'.format(str(g), str(k)))


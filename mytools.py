
import pandas as pd


def 有序变量描述统计函数(表名,变量名):
    result =表名[变量名].value_counts(sort=False)
    描述统计表 = pd.DataFrame(result)
    描述统计表['比例'] = 描述统计表['count'] / 描述统计表['count'].sum()
    描述统计表['累计比例'] =描述统计表['比例'].cumsum()
    return 描述统计表


# 导入各种包
import pandas as pd
from pyreadstat import pyreadstat
import matplotlib.pyplot as plt
from scipy import stats
from tabulate import tabulate
from scipy.stats import somersd
import plotly.express as px

# 绘图设置
plt.rcParams["font.sans-serif"] = ["SimHei"]  # 设置字体


def 使用标准差判断数值变量异常值(数据表, 数值变量):
    mean = 数据表[数值变量].mean()
    std = 数据表[数值变量].std()
    condition1 = (数据表[数值变量] < mean - 3 * std) | (数据表[数值变量] > mean + 3 * std)
    # 识别异常值
    outliers1 = 数据表[condition1]
    print('使用标准差判断的异常值为：', outliers1)


def 计算单变量均值的置信区间(数据表路径及文件名, 变量名, 置信水平=0.95):
    """ 计算指定数据表中数值变量的均值及在指定置信水平下的置信区间 """

    # 打开数据文件
    file_path = 数据表路径及文件名
    df = pd.read_csv(file_path)
    # 计算均值和标准误差
    mean = df[变量名].mean()
    std_error = stats.sem(df[变量名])
    # 设定置信水平
    confidence_level = 置信水平
    # 设定自由度
    自由度 = len(df[变量名]) - 1
    # 计算置信区间
    confidence_interval = stats.t.interval(
        confidence_level, 自由度, loc=mean, scale=std_error)
    # 输出结果
    print(F"变量{变量名}均值：{mean: .2f}")
    print(F"均值在置信水平{confidence_level}下的置信区间为：", confidence_interval)
    return mean, confidence_interval


def 绘制单个类别变量柱状图(数据表, 变量: str):
    """ 绘制单个类别变量柱状 """
    x = 数据表[变量].value_counts().index
    y = 数据表[变量].value_counts(normalize=True).values * 100
    # 创建图
    fig, ax = plt.subplots()
    # 绘制柱状图
    rects1 = ax.bar(x, y)
    # 设置x轴变量名称
    ax.set_xlabel(变量)
    # 设置y轴最大值
    ax.set_ylim(ymax=100)
    # 在柱上方显示对应的值
    ax.bar_label(rects1, fmt="%.1f", padding=3)
    # 显示图形
    plt.show()


def 读取SPSS数据(文件所在位置及名称):
    """ 读取SPSS文件，保留标签内容和有序变量顺序 """
    result, metadata = pyreadstat.read_sav(
        文件所在位置及名称, apply_value_formats=True, formats_as_ordered_category=True)
    return result, metadata


def 有序变量描述统计函数(表名, 变量名):
    """ 对有序类别变量进行描述统计 """
    result = 表名[变量名].value_counts(sort=False)
    描述统计表 = pd.DataFrame(result)
    描述统计表['比例'] = 描述统计表['count'] / 描述统计表['count'].sum()
    描述统计表['累计比例'] = 描述统计表['比例'].cumsum()
    return 描述统计表


def 数值变量描述统计1(数据表, 变量名):
    result = 数据表[变量名].describe()
    中位数 = result['median']
    平均值 = result['mean']
    标准差 = result['std']
    return 中位数, 平均值, 标准差


def 数值变量描述统计(数据表, 变量名):
    """ 对数值变量进行描述统计 """
    result = 数据表[变量名].describe()
    return result


def goodmanKruska_tau_y(df, x: str, y: str) -> float:
    """ 计算两个定序变量相关系数tau_y """
    """ 取得条件次数表 """
    cft = pd.crosstab(df[y], df[x], margins=True)
    """ 取得全部个案数目 """
    n = cft.at['All', 'All']
    """ 初始化变量 """
    E_1 = E_2 = tau_y = 0

    """ 计算E_1 """
    for i in range(cft.shape[0] - 1):
        F_y = cft['All'][i]
        E_1 += ((n - F_y) * F_y) / n
    """ 计算E_2 """
    for j in range(cft.shape[1] - 1):
        for k in range(cft.shape[0] - 1):
            F_x = cft.iloc[cft.shape[0] - 1, j]
            f = cft.iloc[k, j]
            E_2 += ((F_x - f) * f) / F_x
    """ 计算tauy """
    tau_y = (E_1 - E_2) / E_1

    return tau_y


def 相关系数强弱判断(相关系数值):
    """ 相关系数强弱的判断 """
    if 相关系数值 >= 0.8:
        return '极强相关'
    elif 相关系数值 >= 0.6:
        return '强相关'
    elif 相关系数值 >= 0.4:
        return '中等程度相关'
    elif 相关系数值 >= 0.2:
        return '弱相关'
    else:
        return '极弱相关或无相关'


def 制作交叉表(数据表, 自变量, 因变量):
    return pd.crosstab(数据表[自变量], 数据表[因变量], normalize='columns', margins=True)


def 读取SPSS数据文件(文件位置及名称, 是否保留标签值=True):
    数据表, metadata = pyreadstat.read_sav(
        文件位置及名称, apply_value_formats=是否保留标签值, formats_as_ordered_category=True)
    return 数据表


def p值判断(p: float, α=0.05):
    """ p值判断 """
    if p <= α:
        return '拒绝虚无假设'
    else:
        return '接受虚无假设'


def 相关系数判断(系数: int):
    """
    判断相关系数的强弱

    """
    if 系数 >= 0.8:
        return '极强相关'
    elif 系数 >= 0.6:
        return '强相关'
    elif 系数 >= 0.4:
        return '中等强度相关'
    elif 系数 >= 0.2:
        return '弱相关'
    else:
        return '极弱相关或无相关'


def goodmanKruska_tau_y(df, x: str, y: str) -> float:
    """
    计算两个定类变量的goodmanKruska_tau_y相关系数

    df：包含定类变量的数据框
    x：数据框中作为自变量的定类变量名称
    y: 数据框中作为因变量的定类变量名称

    函数返回tau_y相关系数
    """

    cft = pd.crosstab(df[y], df[x], margins=True)
    """ 取得全部个案数目 """
    n = cft.at['All', 'All']
    """ 初始化变量 """
    E_1 = E_2 = tau_y = 0

    """ 计算E_1 """
    for i in range(cft.shape[0] - 1):
        F_y = cft['All'][i]
        E_1 += ((n - F_y) * F_y) / n
    """ 计算E_2 """
    for j in range(cft.shape[1] - 1):
        for k in range(cft.shape[0] - 1):
            F_x = cft.iloc[cft.shape[0] - 1, j]
            f = cft.iloc[k, j]
            E_2 += ((F_x - f) * f) / F_x
    """ 计算tauy """
    tau_y = (E_1 - E_2) / E_1

    return tau_y


def 绘制柱状图(表名):
    x = 表名.index
    y = 表名['count'].values
    fig, ax2 = plt.subplots()
    ax2.bar(x, y)
    plt.show()


def 两个无序类别变量的统计分析(数据表, 自变量, 因变量):
    """ 对两个无序类别变量进行描述统计和推论统计，并给出辅助结论 """
    # 计算相关系数
    tau_y = goodmanKruska_tau_y(数据表, 自变量, 因变量)
    # 制作交互分类表
    交互表 = pd.crosstab(数据表[F"{自变量}"], 数据表[F"{因变量}"])
    # 进行卡方检验
    chi2, p, dof, ex = stats.chi2_contingency(交互表)

    print(F"tau_y系数:{tau_y: 0.4f}", 相关系数判断(tau_y))
    print(tabulate(交互表))
    print(F"卡方值：{chi2: .2f}, p值：{p: .4f},自由度:{dof}。")
    print(p值判断(p))


def 两个有序类别变量的统计分析(数据表, 自变量, 因变量):
    """ 对两个有序类别变量进行描述统计和推论统计，并给出辅助结论 """
    x = 数据表[F"{自变量}"].cat.codes
    y = 数据表[F"{因变量}"].cat.codes
    result = somersd(x, y)
    # 制作交互分类表
    交互表 = pd.crosstab(数据表[F"{自变量}"], 数据表[F"{因变量}"])
    d_y = result.statistic
    p = result.pvalue

    print(F"Somers dy系数:{d_y: 0.4f}", 相关系数判断(d_y))
    print(tabulate(交互表))
    print(F"p值：{p: .4f}")
    print(p值判断(p))


def 两个数值变量的统计分析(数据表, 自变量, 因变量):
    """ 对两个数值变量进行统计分析，并给出辅助结论 """

    x = 数据表[自变量]
    y = 数据表[因变量]
    r, p = stats.pearsonr(x, y)

    fig = px.scatter(数据表, x, y, trendline='ols')
    fig.show()

    print(FR"决定系数r平方：{r*r :0.4f}")
    print(决定系数强弱判断(r*r))
    print(F"p值：{p: .4f}")
    print(p值判断(p))


def 决定系数强弱判断(决定系数: float):
    """ 
    <0.25       <0.06	    微弱相关或不相关
    0.25≤≤0.5	0.06≤≤0.25	低度相关
    0.5≤≤0.75	0.25≤≤0.56	中度相关
    >0.75	    >0.56	     高度相关 
    """
    if 决定系数 > 0.56:
        return "高度相关"
    elif 决定系数 > 0.25:
        return "中度相关"
    elif 决定系数 > 0.26:
        return "低度相关"
    else:
        return "微弱相关或不相关"


def 相关比率强弱判断(相关比率: float):
    """ 
    小于 0.01	微弱相关或不相关
    [0.01-0.06]	低度相关
    [0.06-0.14]	中度相关
    [0.14-0.99]	高度相关
    1	        完全相关
    """
    if 相关比率 > 0.14:
        return "高度相关"
    elif 相关比率 > 0.06:
        return "中度相关"
    elif 相关比率 > 0.01:
        return "低度相关"
    else:
        return "微弱相关或不相关"


def 类别变量与数值变量统计分析(数据表, 类别变量, 数值变量):
    """ 对数值变量的不同类别进行对比，并给出辅助结论 """
    from statsmodels.formula.api import ols

    fig = px.box(数据表, x=类别变量, y=数值变量)
    fig.show()

    model = ols(F'{数值变量} ~ {类别变量}', 数据表).fit()

    print(F"相关比率：{model.rsquared}")

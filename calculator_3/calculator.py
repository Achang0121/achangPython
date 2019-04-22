#!/usr/bin/env python3

import sys
import csv

class Params(object):
    # 获取参数
    def __init__(self):
        self.params = sys.argv[1:]

    def get_params(self):
        # 解析参数
        try:
            params_dict = {}
            params = self.params
            for flag in ('-c', '-d', '-o'):
                index = params.index(flag)
                catalog = params[index+1]
                params_dict[flag] = catalog
        except:
            print('参数输入有错误！')
        return params_dict


class Configs(object):
    # 获取社保信息
    def __init__(self, catalog):
        self.catalog = catalog

    def get_configs(self):
        configs_dict = {}
        with open(self.catalog, 'r') as f:
            datas = f.readlines()
        for data in datas:
            key = data.strip().split('=')[0].strip()
            value = float(data.strip().split('=')[1].strip())
            configs_dict[key] = value
        return configs_dict


class User(object):
    # 获取员工工资
    def __init__(self, catalog):
        self.catalog = catalog

    def get_user_data(self):
        with open(self.catalog, 'r') as f:
            user_dict = dict(csv.reader(f))
            for value in user_dict.values():
                value = value
            return user_dict 


class AfterTaxIncome(object):

    def __init__(self, user_id, user_income):
        self.user_id = user_id    # 员工工号
        self.user_income = int(user_income)  # 员工税前工资

    # 计算每位员工的税后工资
    def calc(self, **shebao_dict):
        jishu_l = shebao_dict['JiShuL']
        jishu_h = shebao_dict['JiShuH']
        base_tax_money = 5000   # 个税齐征点
        tax = 0                 # 个税
        shebao_rate = 0         # 社保费率
        shebao_money = 0        # 社保金额
        aftertax_money = 0      # 税后工资
        del shebao_dict['JiShuL']
        del shebao_dict['JiShuH']
        for value in shebao_dict.values():
            shebao_rate += value
        if self.user_income < jishu_l:
            shebao_money = jishu_l * shebao_rate
        elif self.user_income > jishu_h:
            shebao_money = jishu_h * shebao_rate
        else:
            shebao_money = self.user_income * shebao_rate
        flag = self.user_income - shebao_money - base_tax_money # 应纳税所得额
        if flag > 0 and flag <= 3000:
            tax = flag * 0.03
        elif flag > 3000 and flag <= 12000:
            tax = flag * 0.1 - 210
        elif flag > 12000 and flag <= 25000:
            tax = flag * 0.2 -1410
        elif flag > 25000 and flag <= 35000:
            tax = flag * 0.25 - 2660
        elif flag > 35000 and flag <= 55000:
            tax = flag * 0.3 - 4410
        elif flag > 55000 and flag <= 80000:
            tax = flag * 0.35 - 7160
        elif flag > 80000:
            tax = flag * 0.4 - 15160
        else:
            tax = 0
        aftertax_money = self.user_income - shebao_money - tax
        usr_message = []
        usr_message.append(self.user_id)
        usr_message.append(self.user_income)
        usr_message.append('%.2f'%shebao_money)
        usr_message.append('%.2f'%tax)
        usr_message.append('%.2f'%aftertax_money)
        return usr_message

    def save_to_csv(self, catalog_save, *usr_message):
        try:
            with open(catalog_save, 'a') as f:
                writer = csv.writer(f)
                writer.writerow(usr_message)
        except:
            print('请检查写入的目录是否有问题！')


def main():
    params_dict = Params().get_params()  # 获取参数字典
    shebao_dict = Configs(params_dict['-c']).get_configs() # 获取社保具体数据
    user_dict = User(params_dict['-d']).get_user_data()
    for user_id, user_income in user_dict.items():
        usr = AfterTaxIncome(user_id, int(user_income))
        usr_message = usr.calc(**shebao_dict)
        usr.save_to_csv(params_dict['-o'], *usr_message)



if __name__ == '__main__':
    main()

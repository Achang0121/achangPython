#!/usr/bin/env python3
import sys
import csv
import queue
from collections import namedtuple
from multiprocessing import Process, Queue
import getopt
import configparser
from datetime import datetime


IncomeTaxQuickLookupItem = namedtuple(
    'IncomeTaxQuickLookupItem', 
    ['start_point', 'tax_rate', 'quick_subtractor']
)

# 起征点
INCOME_TAX_START_POINT = 5000

# 税率表
INCOME_TAX_QUICK_LOOKUP_TABLE = [
    IncomeTaxQuickLookupItem(80000, 0.45, 15160),
    IncomeTaxQuickLookupItem(55000, 0.35, 7160),
    IncomeTaxQuickLookupItem(35000, 0.30, 4410),
    IncomeTaxQuickLookupItem(25000, 0.25, 2260),
    IncomeTaxQuickLookupItem(12000, 0.20, 1410),
    IncomeTaxQuickLookupItem(1500, 0.10, 210),
    IncomeTaxQuickLookupItem(0, 0.03, 0)
]

class Args(object):
    # 命令行参数处理类
    def __init__(self):
        self.args = self._get_args_dict()
    
    def _get_args_dict(self):
        # 使用getopt处理命令行参数
        try:
            args_dict = dict(getopt.getopt(sys.argv[1:], 'C:c:d:o:')[0])
            return args_dict
        except (getopt.GetoptError):
            print("参数错误")
            exit()
    
    def _value_after_option(self, option):
        value = self.args.get(option)

        return value

    @property
    def city(self):
        # 城市5险1金
        return self._value_after_option('-C')

    @property
    def config_path(self):
        # 配置文件的路径
        return self._value_after_option('-c')
    
    @property
    def user_data_path(self):
        # 用户数据的路径
        return self._value_after_option('-d')

    @property
    def exporter_path(self):
        # 计算结果输出的路径
        return self._value_after_option('-o')


# 创建全局参数类对象
args = Args()


class Config(object):
    # 配置文件处理类
    
    def __init__(self):
        # 读取配置文件
        self.config = self._read_config()

    def _read_config(self):
        """
        内部函数，读取配置文件数据
        """
        config = configparser.ConfigParser()
        config.read(args.config_path)
        if args.city and args.city.upper() in config.sections():
            return config[args.city.upper()]
        else:
            return config['DEFAULT']

    def _get_config(self, key):
        """
        内部函数，获取配置项的值
        """
        try:
            return float(self.config[key])
        except KeyError:
            print('配置信息错误')
            exit()

    @property
    def social_insurance_baseline_low(self):
        """
        获取社保基数下限
        """
        return self._get_config('JiShuL')
    
    @property
    def social_insurance_baseline_high(self):
        """
        获取社保基数上限
        """
        return self._get_config('JiShuH')

    @property
    def social_insurance_total_rate(self):
        """
        获取社保总费率
        """
        return sum([
            self._get_config('YangLao'),
            self._get_config('YiLiao'),
            self._get_config('ShiYe'),
            self._get_config('GongShang'),
            self._get_config('ShengYu'),
            self._get_config('GongJiJin')
        ])


# 创建全局Config对象
config = Config()


class UserData(Process):
    # 用户数据处理进程
    def __init__(self, userdata_queue):
        super().__init__()
        # 用户数据队列
        self.userdata_queue = userdata_queue

    def _read_users_data(self):
        """
        内部函数，读取用户数据
        """
        userdata = []
        with open(args.user_data_path) as f:
            for line in f.readlines():
                employee_id, income_string = line.strip().split(',')
                try:
                    income = int(income_string)
                except ValueError:
                    print('Params Error')
                    exit()
                userdata.append((employee_id, income))
        return userdata

    def run(self):
        """
        进程入口方法
        """
        # 从用户数据文件依次读取每条用户信息并写入到队列
        for item in self._read_users_data():
            self.userdata_queue.put(item)


class IncomeTaxCalculator(Process):
    # 税后工资计算进程
    def __init__(self, userdata_queue, export_queue):
        super().__init__()
        self.userdata_queue = userdata_queue
        self.export_queue = export_queue

    @staticmethod
    def calc_social_insurance_money(income):
        """
        计算应纳税额
        """
        if income < config.social_insurance_baseline_low:
            return config.social_insurance_baseline_low * \
                config.social_insurance_total_rate
        elif income > config.social_insurance_baseline_high:
            return config.social_insurance_baseline_high * \
                config.social_insurance_total_rate
        else:
            return income * config.social_insurance_total_rate

    @classmethod
    def calc_income_tax_and_remain(cls, income):
        """
        计算税后工资
        """
        # 计算社保金额
        social_insurance_money = cls.calc_social_insurance_money(income)

        # 计算应纳税额
        real_income = income - social_insurance_money
        taxable_part = real_income - INCOME_TAX_START_POINT

        # 从高到低判断落入的税率区间，如果找到则用该区间的参数计算并返回结果
        for item in INCOME_TAX_QUICK_LOOKUP_TABLE:
            if taxable_part > item.start_point:
                tax = taxable_part * item.tax_rate - item.quick_subtractor
                t = '{:.2f}'.format(tax)
                m = '{:.2f}'.format(real_income - tax)
                return t, m
        # 如果没有落入所有的区间
        return '0.00', '{:.2f}'.format(real_income)

    def calculate(self, employee_id, income):
        """
        计算单个用户的税后工资
        """
        # 计算社保金额
        social_insurance_money = '{:.2f}'.format(self.calc_social_insurance_money(income))

        # 计算税后工资
        tax, remain = self.calc_income_tax_and_remain(income)

        return [employee_id, income, social_insurance_money, tax, remain, datetime.now().strftime('%Y-%m-%d %H:%M:%S')]

    def run(self):
        """
        进程入口方法
        """
        # 从用户队列读取数据，计算税后工资，然后写入到导出数据处理队列
        while True:
            # 获取下一个用户
            try:
                # 设置timeout=1 如果超出1秒没有需要处理的数据，则退出进程
                employee_id, income = self.userdata_queue.get(timeout=1)
            except queue.Empty:
                return

            # 计算税后工资
            result = self.calculate(employee_id, income)

            # 将结果写入export_queue
            self.export_queue.put(result)


class IncomeTaxExporter(Process):
    """
    税后工资导出进程
    """
    def __init__(self, export_queue):
        super().__init__()
        self.export_queue = export_queue

        self.f = open(args.exporter_path, 'w', newline='')
        self.writer = csv.writer(self.f)
    
    def run(self):
        """
        进程入口方法
        """
        while True:
            # 获取下一个导出数据
            try:
                # 超时1秒，则视为无数据处理，退出进程
                item = self.export_queue.get(timeout=1)
            except queue.Empty:
                self.f.close()
                return

            # 写入数据到文件
            self.writer.writerow(item)


if __name__ == '__main__':
    # 创建进程间通信队列
    userdata_queue = Queue()
    export_queue = Queue()

    # 用户数据进程
    userdata = UserData(userdata_queue)
    # 税后工资计算进程
    calculator = IncomeTaxCalculator(userdata_queue, export_queue)
    # 税后工资导出进程
    exporter = IncomeTaxExporter(export_queue)

    # 启动进程
    userdata.start()
    calculator.start()
    exporter.start()

    # 等待所有进程结束
    userdata.join()
    calculator.join()
    exporter.join()

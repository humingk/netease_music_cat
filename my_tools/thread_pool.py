# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import time
from threading import Thread, currentThread
from queue import Queue
from my_tools.logger_tool import loggler_tool

logger = loggler_tool()

# 线程停止标志
stop_task = object()


class thread_pool:
    """
    线程池类(弃用，改用future的ThreadPoolExecutor)
    关键错误：出现死锁，待解决

    """

    def __init__(self, thread_max=10):
        """
        线程池初始化

        :param thread_max: 线程最大数
        """
        self.thread_max = thread_max
        # 工作队列
        self.work_queue = Queue()
        # 任务取消标志
        self.cancel = False
        # 任务中断标志
        self.interrupt = False
        # 已实例化线程列表
        self.instance_list = []
        # 空闲线程列表
        self.free_list = []

    def add(self, func, args, callback=None):
        """
        工作队列添加任务

        :param func: 任务函数
        :param args: 任务函数参数
        :param callback: 回调函数，返回：(任务函数执行状态，任务函数返回值)
        :return 若线程池中止，返回True
        """
        # 任务取消
        if self.cancel:
            return
        # 创建新线程 (没有空余线程并且没到最大值)
        if len(self.free_list) == 0 and len(self.instance_list) < self.thread_max:
            self.create_thread()
        # 任务放入工作队列
        self.work_queue.put((func, args, callback))

    def create_thread(self):
        """
        创建一个线程

        """
        Thread(target=self.call).start()

    def call(self):
        """
        循环获取任务函数并执行

        """
        # 当前线程名称
        current_thread_name = currentThread().getName()
        # 加入已实例化列表
        self.instance_list.append(current_thread_name)
        # 从工作队列获取任务
        task = self.work_queue.get()

        """
        循环执行工作队列中的任务，直到遇到 任务中断标志
        """
        while task != stop_task:
            func, args, callback = task
            # 执行任务
            result = func(*args)
            status = True
            # try:
            #     result = func(*args)
            #     status = True
            # except Exception as e:
            #     result = None
            #     status = False
            #     logger.error("Thread pool execute task failed",
            #                  "Thread_name:{},func:{},args:{},error_type:{},error:{}".format(current_thread_name,func, args,type(e),e))
            # 执行回调函数
            if callback is not None:
                try:
                    callback(status, result)
                except Exception as e:
                    logger.error("Thread pool task callback failed",
                                 "Thread_name:{},func:{},args:{},error_type:{},error:{}".format(current_thread_name,
                                                                                                func, args, type(e), e))
            """
            任务完成，此线程加入空闲列表
            
            此处也可使用 with+contextlibs上下文 方法实现
            其中 with部分代码用yeild替代
            """
            self.free_list.append(current_thread_name)
            try:
                # 遇到任务中断标志
                if self.interrupt:
                    # 线程停止
                    task = stop_task
                    logger.info("Thread pool task interrupt then stop", "Thread_name:{}".format(current_thread_name))
                else:
                    # 继续从工作列表获取任务并执行
                    task = self.work_queue.get()
            except Exception as e:
                logger.error("Thread pool task finish then continue failed",
                             "Thread_name:{},func:{},args:{},error_type:{},error:{}".format(current_thread_name, func,
                                                                                            args, type(e), e))
            finally:
                # 循环执行新任务，此线程从空闲列表移除
                self.free_list.remove(current_thread_name)
        else:
            # while 遇到线程停止标志
            self.instance_list.remove(current_thread_name)

    def close(self):
        """
        所有任务执行完，停止所有线程

        """
        # 任务取消标志
        self.cancel = True
        # 已实例化列表个数
        instance_list_length = len(self.instance_list)
        while instance_list_length:
            # 向工作列表添加(已实例化列表个数)个 线程停止标志
            self.work_queue.put(stop_task)
            instance_list_length -= 1

    def interrupt_now(self):
        """
        任务未执行完，提前停止所有线程

        """
        self.interrupt = True
        while self.instance_list:
            # 所有的实例化
            self.work_queue.put(stop_task)


# 测试 -----------------------------------------------------------------

def test(arg):
    """
    执行函数

    :param arg: 执行函数参数
    :return:
    """
    time.sleep(0.1)
    print("task:{} use thread:xx".format(arg + 1))
    print("instance_list:{},free_list:{}".format(len(pool.instance_list), len(pool.free_list)))
    print("test ----------------------------------------------------------------------------------")
    return True, "test callback"


def callback(status, result):
    """
    回调函数

    :param status: 执行函数执行状态
    :param result: 执行函数返回值
    :return:
    """
    print(status)
    print(result)
    print("callback-----------------------")


if __name__ == '__main__':
    pool = thread_pool(100)
    for i in range(1000):
        pool.add(func=test,
                 args=(i,),
                 callback=callback)
    time.sleep(5)
    pool.close()
    print("finish")

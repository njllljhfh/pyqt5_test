import time

def deco01(f):
    def wrapper(*args, **kwargs):
        print("this is deco01")
        start_time = time.time()
        f(*args, **kwargs)
        end_time = time.time()
        execution_time = (end_time - start_time)*1000
        print("time is %d ms" % execution_time)
        print("deco01 end here")
    return wrapper

def deco02(f):
    def wrapper(*args, **kwargs):
        print("this is deco02")
        f(*args, **kwargs)

        print("deco02 end here")
    return wrapper

@deco01
@deco02
def f(a,b):
    print("be on")
    time.sleep(1)
    print("result is %d" %(a+b))

def leave_inference(func):
    """判断当前界面是否是实时监控界面的装饰器"""

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        # logger.debug(f"{args}----{kwargs}")
        try:
            if self.is_leave_real_time_inference_widget():
                ret = WarningMessageBox("确认离开实时监控界面?")
                if not ret.msg_exec():
                    # logger.debug(f"- - - - - 【不切换】 - - - - - -")
                    return
                    # return self.do_nothing(self, *args, **kwargs)
            # logger.debug(f"- - - - - 【执行了么】 - - - - - -")
            return func(self)
        except Exception as e:
            logger.error(f"Error:{e}", exc_info=True)
            WarningMessageBoxOne(str(e))

    return wrapper


self.ui.quick_start_detection_action.triggered.connect(self.quick_start_detection_fun)


def quick_start_detection_fun(self):
    """快速启动检测"""
    try:
        if self.is_leave_real_time_inference_widget():
            ret = WarningMessageBox("确认离开实时监控界面?")
            if not ret.msg_exec():
                return

        if self.ui.stackedWidget.currentWidget() is not self.inference_task_list_widget:
            self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.inference_task_list_widget_index)
            self.inference_task_list_widget.refresh_current_page_signal_handler()
        self.inference_task_list_widget.create_task_btn_clicked_event()
    except Exception as e:
        logger.error(f"Error:{e}", exc_info=True)
        WarningMessageBoxOne(str(e))


def product_statistic_widget_fun(self):
    """产品缺陷率和报废率统计"""
    pass
if __name__ == '__main__':
    f(3,4)

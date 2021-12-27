class Shared(QObject):
    signal_query_begin = pyqtSignal()
    signal_success = pyqtSignal(str)
    signal_error = pyqtSignal(str)
    signal_data_success = pyqtSignal(str)
    signal_data_error = pyqtSignal(str)
    def __init__(self, parent=None):
        super(Shared, self).__init__(parent=parent)
        self.data = []
        self.th = None
    @pyqtSlot(str, str, str)
    def retrive_defect_labels(self, task_id, start_time, end_time):
        self.th = AsynThread(defectTask().retrieve, args=(task_id, start_time, end_time), parent=self)
        self.th.signal_result.connect(self.slot_data_success)
        self.th.signal_result_error.connect(self.slot_data_error)
        self.th.start()
    def slot_data_success(self, data):
        data, records = data
        self.data = records
        self.signal_data_success.emit(json.dumps(data, ensure_ascii=False))
    def slot_data_error(self):
        self.signal_data_error.emit('获取缺陷数据失败')
class DefectTaskStatistics(QWidget):
    def __init__(self, main_window, *args, **kwargs):
        super(DefectTaskStatistics, self).__init__()
        self.main_window = main_window
        styleFile = 'qss/statistics.qss'
        qss = CommonHelper.readQss(styleFile)
        self.setStyleSheet(qss)
        self.vbox = QVBoxLayout(self)
        self.filter_box = QHBoxLayout()
        self.progress_bar = ProgressBarWindow(value_show=False)
        self.shared = Shared(self)
        self.search_input = None
        self.start_time_input = None
        self.end_time_input = None
        self.search_btn = None
        self.download_btn = None
        self.browser = None
        self.channel = None
        self.init_ui()
        self.load_web_page()
        self.init_channel()
    def init_ui(self):
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('请输入任务名称或编码')
        self.search_input.setFixedSize(178, 23)
        self.date_group = DateGroup('缺陷时间:')
        self.start_time_input = self.date_group.start_date
        self.end_time_input = self.date_group.end_date
        self.date_group.comboBox.hide()
        self.search_btn = IconButton(':/icons/search.png')
        self.download_btn = IconButton(':/icons/download.png')
        self.filter_box.addItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.filter_box.addWidget(self.search_input)
        self.filter_box.addWidget(self.date_group)
        self.filter_box.addWidget(self.search_btn)
        self.filter_box.addWidget(self.download_btn)
        self.browser = QWebEngineView()
        self.browser.setContextMenuPolicy(Qt.NoContextMenu)
        self.vbox.addLayout(self.filter_box)
        self.vbox.addWidget(self.browser)
    def init_event(self):
        self.search_input.returnPressed.connect(self.req_statistics_info)
        self.search_btn.clicked.connect(self.req_statistics_info)
        self.download_btn.clicked.connect(self.slot_download)
    def init_channel(self):
        self.channel = QWebChannel()
        self.channel.registerObject("shared", self.shared)
        self.browser.page().setWebChannel(self.channel)
    def load_web_page(self):
        try:
            url = QUrl(QFileInfo('dashboard/compiler/detect-category.html').absoluteFilePath())
            self.browser.load(url)
        except Exception as e:
            WarningMessageBox("")
    def req_statistics_info(self):
        self.shared.signal_query_begin.emit()
        self.key_word = self.search_input.text()
        self.start_time = self.start_time_input.date.toPyDateTime().strftime("%Y-%m-%d %H:%M:%S")
        self.end_time = self.end_time_input.date.toPyDateTime().strftime("%Y-%m-%d %H:%M:%S")
        user_info_dict = self.main_window.user
        user_id = user_info_dict['id']
        role_type = user_info_dict['role_type']
        self.th = AsynThread(defectTask().retrieve_tasks,
                             args=(self.key_word, self.start_time, self.end_time, user_id, role_type),
                             parent=self)
        self.th.signal_result.connect(self.slot_get_statistics_info)
        self.th.signal_result_error.connect(self.slot_get_statistics_info_error)
        self.th.start()
    def slot_get_statistics_info(self, data):
        self.shared.signal_success.emit(json.dumps(data, ensure_ascii=False))
    def slot_get_statistics_info_error(self):
        self.shared.signal_error.emit('请求任务数据失败')
    def slot_download(self):
        if not self.main_window.get_system_func('defect_product_task_download'):
            return InformationMessageBoxOne("暂无权限下载，请联系管理员")
        if len(self.shared.data) == 0:
            return InformationMessageBoxOne("没有数据可供下载，请先查询")
        if self.shared.th.isRunning():
            return InformationMessageBoxOne("正在查询数据，请稍后下载")
        sheets = []
        task_name, data = self.gen_download_data()
        file_name = f"""任务缺陷统计报表_{datetime.now().strftime('%Y%m%d')}.xlsx"""
        file_path = gen_xlsx_path(file_name, "下载任务缺陷统计报表")
        if not file_path:
            return
        self.progress_bar.set_title("正在下载 %s" % file_name)
        self.progress_bar.show()
        formats = {
            "format": {
                'align': 'center',
                'valign': 'vcenter',
                'font_size': '12',
                'border': 1
            },
            "box_format": {
                'align': 'center',
                'valign': 'vcenter',
                'font_size': '12',
                'fg_color': '#b4c6e7',
                'top': 1
            },
            "bg_format": {
                'align': 'center',
                'valign': 'vcenter',
                'font_size': '12',
                'fg_color': '#b4c6e7',
            },
            "bg_format_border": {
                'align': 'center',
                'valign': 'vcenter',
                'font_size': '12',
                'fg_color': '#b4c6e7',
                'border': 1
            }
        }
        options = {
            "height": [(0, 31)]
        }
        title = f"""检测任务统计表_{task_name}_{self.start_time} 至 {self.end_time}"""
        sheet = [
            "检测任务统计报表",
            {
                "A1:G1": {
                    "value": title,
                    "format": "bg_format",
                    "merge": True,
                }
            },
            formats,
            options
        ]
        headers = ['序号', '生产线', '产品型号', '检测点', '缺陷小类', '缺陷位置', '缺陷时间']
        for i in range(len(headers)):
            sheet[1].update({(1, i): {"value": headers[i], "format": "bg_format_border"}})
        data_start_index = 1
        for r, row in enumerate(data):
            for c, cell in enumerate(row):
                sheet[1].update({(r + data_start_index + 1, c): {"value": str(cell), "format": "format"}})
        sheets.append(sheet)
        download_th = AsyncDownload(file_path, sheets, self)  
        download_th.signal_result.connect(self.slot_download_success)
        download_th.signal_result_error.connect(self.slot_download_error)
        download_th.start()
    def slot_download_success(self, data):
        if self.progress_bar:
            self.progress_bar.close()
        InformationMessageBoxOne("下载完成")
    def slot_download_error(self, data):
        if self.progress_bar:
            self.progress_bar.close()
        try:
            raise data.get("error")
        except InvalidWorksheetName as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne(f"工作表包含不允许的字符")
        except FileCreateError as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne(f"下载缺陷位置分布统计报表出错, 该文件处于使用状态")
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("下载缺陷位置分布统计报表出错")
    def gen_download_data(self):
        res = []
        task_name = ''
        try:
            gg_enum = DictInfoCRUD.get_all_gg_enum(True)
            if len(self.shared.data) > 0:
                task_name = self.shared.data[0].D_TASK_NAME
            for index, item in enumerate(self.shared.data):
                create_time = item.CREATE_TIME
                if create_time and isinstance(create_time, datetime):
                    create_time = create_time.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    create_time = ''
                res.append(
                    [
                        item.PRO_LINE_NAME,
                        gg_enum.get(item.GG),
                        DetectSite.value_name(item.DETECT_SITE),
                        item.LAB_CLASS_NAME,
                        self.gen_pos_to_str(item.POSITION), create_time
                    ]
                )
            res.sort(key=lambda x: x[3])
            for index, item in enumerate(res):
                item.insert(0, index + 1)
            return task_name, res
        except Exception as e:
            logger.error(e, exc_info=True)
        return '', []
    @staticmethod
    def gen_pos_to_str(pos):
        try:
            pos = eval(pos)
            tmp = np.array(pos)
            if tmp.ndim > 1:
                tmp_list = []
                for item in pos:
                    tmp_list.append(chr(item[0] + 64) + str(item[1]))
                res = ','.join(tmp_list)
            else:
                res = chr(pos[0] + 64) + str(pos[1])
        except Exception as e:
            print(e)
            res = ''
        return res
class DefectCategoryStatistics(QWidget):
    def __init__(self, main_window, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_window = main_window
        self.cruds = defectCategory()
        self.ui = UI_DefectCategoryStatistics(self)
        self.cb_detect_type = self.ui.filters_pannel.cb_detect_type.comboBox
        self.cb_defect_big_class = self.ui.filters_pannel.cb_defect_big_class.comboBox
        self.start_date = self.ui.filters_pannel.date_group.start_date
        self.end_date = self.ui.filters_pannel.date_group.end_date
        self.cb_date_selections = self.ui.filters_pannel.date_group.comboBox
        self.cb_defect_type = self.ui.filters_pannel.cb_defect_type.comboBox
        self.cb_statistics_dimension = self.ui.filters_pannel.cb_statistics_dimension
        self.btn_search = self.ui.filters_pannel.btn_search
        self.btn_download = self.ui.filters_pannel.btn_download
        self.progress_bar = ProgressBarWindow(value_show=False)  
        self.btn_download.setEnabled(self.main_window.get_system_func("defect_type_statistic_download"))
        self.q_charts = self.ui.q_charts
        self.chart_view = self.ui.chart_view
        self.data_dict = None
        self.data_models = None
        self.DefectCategorySmallStatistics = DefectCategorySmallStatistics()
        self.loading_widget = LoadingWidget(":/icons/loading.gif", parent=self)
        self.echarts_js = None
        self.defect_type = None
        self.dimission_type = None
        self.start_time_for_excel = ""
        self.end_time_for_excel = ""
        self.defect_type_for_excel = ""
        self.req_defect_types()
        self.req_pro_lines_spec()
        self.bind_events()
    def bind_events(self):
        """ 绑定事件 """
        self.cb_detect_type.currentIndexChanged.connect(self.slot_detect_type_changed)
        self.cb_defect_big_class.currentTextChanged.connect(self.slot_defect_type_changed)
        self.btn_search.clicked.connect(self.slot_btn_search_clicked)
        self.btn_download.clicked.connect(self.slot_btn_download_clicked)
        self.ui.statistics_table.signal_defect_class_small_btn_clicked.connect(self.slot_defect_class_small_btn_clicked)
        self.q_charts.signal_chart_frame_resize.connect(self.slot_chart_frame_resize)
    def req_defect_types(self):
        try:
            self.cb_defect_big_class.setDisabled(True)
            self.cb_defect_type.setDisabled(True)
            self.defect_type_th = AsynThread(self.cruds.retrieve_defect_types, parent=self)
            self.defect_type_th.signal_result.connect(self.slot_update_defect_types)
            self.defect_type_th.start()
        except Exception as e:
            logger.error(e, exc_info=True)
    def slot_update_defect_types(self, models):
        try:
            all_defect_types = list(set([model.LAB_CLASS_NAME for model in models]))
            el_defect_types = list(set([model.LAB_CLASS_NAME for model in models if model.CLASS_D_CATEGORY == 1]))
            vi_defect_types = list(set([model.LAB_CLASS_NAME for model in models if model.CLASS_D_CATEGORY == 2]))
            all_defect_types.sort()
            el_defect_types.sort()
            vi_defect_types.sort()
            all_defect_types.insert(0, "全部")
            el_defect_types.insert(0, "全部")
            vi_defect_types.insert(0, "全部")
            self.defect_type = {"全部": all_defect_types, "EL": el_defect_types, "VI": vi_defect_types}
            current_defect_big_type = self.cb_defect_big_class.currentText()
            self.cb_defect_type.addItems(self.defect_type.get(current_defect_big_type))
        except Exception as e:
            logger.error(e)
        finally:
            self.cb_defect_big_class.setDisabled(False)
            self.cb_defect_type.setDisabled(False)
    def init_data(self):
        self.req_statistics_info()
    def slot_detect_type_changed(self, index):
        try:
            if index == 2:
                InformationMessageBoxOne("按【人工复检】统计暂未实现，需对接控制台")
                self.cb_detect_type.setCurrentIndex(0)
        except Exception as e:
            logger.error(e, exc_info=True)
    def slot_defect_type_changed(self, text):
        try:
            self.cb_defect_type.clear()
            self.cb_defect_type.addItems(self.defect_type.get(text))
        except Exception as e:
            logger.error(e, exc_info=True)
    def slot_btn_search_clicked(self):
        try:
            if self.loading_widget.is_loading:
                InformationMessageBoxOne("查询统计完成之后，才可再次查询")
                return
            self.current_pro_line = self.cb_statistics_dimension.pro_lines_combox.currentText()
            self.current_pro_spec = self.cb_statistics_dimension.pro_specs_combox.currentText()
            self.current_detect_site = self.cb_statistics_dimension.detect_sites_combox.currentText()
            self.start_time_for_excel = self.start_date.text()
            self.end_time_for_excel = self.end_date.text()
            self.defect_type_for_excel = self.cb_defect_big_class.currentText()
            self.ui.statistics_table.setRowCount(0)
            self.loading_widget.start()
            self.req_statistics_info()
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("缺陷类型分布统计出错")
    def req_pro_lines_spec(self):
        try:
            self.pro_line_spec_th = AsynThread(self.cruds.retrieve_dimension, parent=self)
            self.pro_line_spec_th.signal_result.connect(self.slot_get_pro_lines_spec)
            self.pro_line_spec_th.signal_result_error.connect(self.slot_get_pro_lines_spec_error)
            self.pro_line_spec_th.start()
        except Exception as e:
            logger.error(str(e), exc_info=True)
    def slot_get_pro_lines_spec(self, data):
        self.ui.filters_pannel.cb_statistics_dimension.set_data(data)
    def slot_get_pro_lines_spec_error(self, data):
        CriticalMessageBoxOne("获取生产线及规格数据失败")
    def req_statistics_info(self):
        try:
            detect_type_index = self.cb_detect_type.currentIndex()
            start_datetime = self.convert_qdate_to_datetime(self.start_date.date)
            end_datetime = self.convert_qdate_to_datetime(self.end_date.date)
            defect_big_class_index = self.cb_defect_big_class.currentIndex()
            defect_type_text = self.cb_defect_type.currentText()
            pro_line_id, pro_spec, detect_site = self.cb_statistics_dimension.data
            user_info_dict = self.main_window.user
            user_id = user_info_dict['id']
            role_type = user_info_dict['role_type']
            if self.pro_line_spec_th.isRunning():
                InformationMessageBoxOne("正在请求生产线、规格数据，请稍后重试")
                return
            self.data_th = AsynThread(
                self.cruds.retrieve,
                args=(
                    start_datetime, end_datetime, detect_type_index, defect_big_class_index,
                    defect_type_text, pro_line_id, pro_spec, detect_site, user_id, role_type
                ),
                parent=self
            )
            self.data_th.signal_result.connect(self.slot_get_statistics_info)
            self.data_th.signal_result_error.connect(self.slot_get_statistics_info_error)
            self.data_th.start()
        except Exception as e:
            logger.error(str(e), exc_info=True)
    def slot_get_statistics_info(self, models):
        try:
            self.data_models = models
            self.ui.statistics_table.update_data(models)
            self.chart_load_data(models)
        except Exception as e:
            logger.error(e, exc_info=True)
        finally:
            self.loading_widget.stop()
    def slot_get_statistics_info_error(self):
        try:
            self.loading_widget.stop()
        except Exception as e:
            logger.error(e, exc_info=True)
        CriticalMessageBoxOne("获取统计数据失败")
    def slot_btn_download_clicked(self):
        if not self.main_window.get_system_func('defect_type_statistic_download'):
            return InformationMessageBoxOne("暂无权限下载，请联系管理员")
        if not self.data_models:
            InformationMessageBoxOne("没有数据可供下载，请先查询")
            return
        if self.loading_widget.is_loading:
            InformationMessageBoxOne("正在查询数据，请稍后下载")
            return
        file_name = f"组件缺陷类型分布统计报表_{datetime.now().strftime('%Y%m%d')}.xlsx"
        file_path = gen_xlsx_path(file_name, "下载缺陷类型分布统计报表")
        if not file_path:
            return
        self.download_excel(file_path)
    def download_excel(self, file_path):
        self.progress_bar.set_title("正在下载 %s" % os.path.basename(file_path))
        self.progress_bar.show()
        sheets = []
        formats = {
            "format": {
                'align': 'center',
                'valign': 'vcenter',
                'font_size': '12',
                'border': 1
            },
            "box_format": {
                'align': 'center',
                'valign': 'vcenter',
                'font_size': '12',
                'fg_color': '#b4c6e7',
                'top': 1
            },
            "bg_format": {
                'align': 'center',
                'valign': 'vcenter',
                'font_size': '12',
                'fg_color': '#b4c6e7',
            },
            "bg_format_border": {
                'align': 'center',
                'valign': 'vcenter',
                'font_size': '12',
                'fg_color': '#b4c6e7',
                'border': 1
            }
        }
        options = {
            "height": [(0, 31)]
        }
        sheet1 = [
            "缺陷大类分布统计报表",
            {
                "A1:L1": {
                    "value": "缺陷类型分布统计报表",
                    "format": "bg_format",
                    "merge": True,
                },
                "A2:E2": {
                    "value": None,
                    "format": "box_format",
                },
                "F2": {
                    "value": '缺陷大类：',
                    "format": "box_format",
                },
                "G2": {
                    "value": self.defect_type_for_excel,
                    "format": "box_format",
                },
                "H2": {
                    "value": '时间范围：',
                    "format": "box_format",
                },
                "I2:L2": {
                    "value": f"{self.start_time_for_excel} 至 {self.end_time_for_excel}",
                    "format": "box_format",
                    "merge": True,
                },
            },
            formats,
            options
        ]
        data_1_col_num = self.ui.statistics_table.columnCount()
        for i in range(data_1_col_num):
            header = self.ui.statistics_table.model().headerData(i, Qt.Horizontal, Qt.DisplayRole)
            sheet1[1].update({(2, i): {"value": header, "format": "bg_format_border"}})
        data_rows_1 = self.ui.statistics_table.data
        data_start_index = 3
        for r, row in enumerate(data_rows_1):
            for c, cell in enumerate(row):
                sheet1[1].update({(r + data_start_index, c): {"value": cell, "format": "format"}})
        sheets.append(sheet1)
        sheet_s = [
            f"缺陷小类分布明细",
            {
                "A1:M1": {
                    "value": "缺陷类型分布（小类）统计报表",
                    "format": "bg_format",
                    "merge": True,
                },
                "A2:E2": {
                    "value": None,
                    "format": "box_format",
                },
                "F2": {
                    "value": '缺陷大类：',
                    "format": "box_format",
                },
                "G2": {
                    "value": self.defect_type_for_excel,
                    "format": "box_format",
                },
                "H2": {
                    "value": '时间范围：',
                    "format": "box_format",
                },
                "I2:M2": {
                    "value": f"{self.start_date.text()} 至 {self.end_date.text()}",
                    "format": "box_format",
                    "merge": True,
                },
                "A3": {
                    "value": '序号',
                    "format": "bg_format_border",
                },
                "B3": {
                    "value": '产品类型',
                    "format": "bg_format_border",
                },
                "C3": {
                    "value": '生产线',
                    "format": "bg_format_border",
                },
                "D3": {
                    "value": '产品型号',
                    "format": "bg_format_border",
                },
                "E3": {
                    "value": '检测点',
                    "format": "bg_format_border",
                },
                "F3": {
                    "value": '缺陷小类',
                    "format": "bg_format_border",
                },
                "G3": {
                    "value": '串焊机',
                    "format": "bg_format_border",
                },
                "H3": {
                    "value": '缺陷数量',
                    "format": "bg_format_border",
                },
                "I3": {
                    "value": '占比',
                    "format": "bg_format_border",
                },
                "J3": {
                    "value": '产品数量',
                    "format": "bg_format_border",
                },
                "K3": {
                    "value": '平均缺陷数量',
                    "format": "bg_format_border",
                },
                "L3": {
                    "value": '当前缺陷平均修复率',
                    "format": "bg_format_border",
                },
                "M3": {
                    "value": '报废率',
                    "format": "bg_format_border",
                }
            },
            formats,
            options
        ]
        data_1_row_num = self.ui.statistics_table.rowCount()
        sub_table_data = []
        for page_index in range(data_1_row_num):
            _, data_s_table = self.get_small_class_table_data(page_index)
            sub_table_data.extend(data_s_table)
        total_ng_count = 0
        for index, item in enumerate(sub_table_data):
            item[0] = index + 1
            total_ng_count += item[7]
        if total_ng_count > 0:
            for item in sub_table_data:
                item[8] = str(round((item[7] / total_ng_count) * 100, 2)) + '%'
        data_start_index = 3
        for r, row in enumerate(sub_table_data):
            for c, cell in enumerate(row):
                sheet_s[1].update({(r + data_start_index, c): {"value": cell, "format": "format"}})
        sheets.append(sheet_s)
        self.download_th = AsyncDownload(file_path, sheets, self)
        self.download_th.signal_result.connect(self.slot_download_success)
        self.download_th.signal_result_error.connect(self.slot_download_error)
        self.download_th.start()
    def slot_download_success(self, data):
        if self.progress_bar:
            self.progress_bar.close()
        InformationMessageBoxOne("下载完成")
    def slot_download_error(self, data):
        if self.progress_bar:
            self.progress_bar.close()
        try:
            raise data.get("error")
        except InvalidWorksheetName as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne(f"工作表包含不允许的字符")
        except FileCreateError as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne(f"下载缺陷类型分布统计报表出错, 该文件处于使用状态")
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("下载缺陷类型分布统计报表出错")
    def get_small_class_table_data(self, row_index):
        headers = []
        obj = self.parent().DefectCategorySmallStatistics.ui.statistics_table
        col_mun = obj.columnCount()
        for i in range(col_mun):
            header = obj.model().headerData(i, Qt.Horizontal, Qt.DisplayRole)
            headers.append(header)
        table = obj.preview_table_data(self.data_models[row_index].small_class_models)
        return headers, table
    def convert_qdate_to_datetime(self, qdate: QDate):
        date_str = datetime.strftime(qdate.toPyDateTime(), '%Y-%m-%d %H:%M:%S')
        return date_str
    def slot_defect_class_small_btn_clicked(self, s_class_models):
        try:
            self.parent().DefectCategorySmallStatistics.load_data(s_class_models)
            self.parent().DefectCategorySmallStatistics.ui.tab.setCurrentIndex(0)  
            self.main_window.init_navigation_bar_fun(
                [{"统计分析 | 组件缺陷类型分布统计": self.parent().DefectCategoryStatistics_index},
                 {"缺陷小类分布详情": self.parent().DefectCategorySmallStatistics_index}])
            self.parent().setCurrentIndex(self.parent().DefectCategorySmallStatistics_index)
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("跳转缺陷小类页面出错")
    def slot_chart_frame_resize(self, size: QSize):
        try:
            fw, fh = size.width(), size.height()
            self.chart_view.setFixedSize(QSize(fw, fh))
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("重置图表尺寸失败")
    def chart_load_data(self, models):
        """ 图表加载数据 """
        data_frame_dict = {"EL": [], "VI": []}
        class_name_list = []
        map_productName_ElViPercent = {}
        map_productNameModel_index = {}
        for index, model in enumerate(models):
            dimission = model.pro_line_name + " " + str(model.pro_spec) + " " + str(
                model.detect_site) + model.product_type
            if dimission not in map_productName_ElViPercent:
                map_productName_ElViPercent[dimission] = [0, 0]
            percent_index = 0 if model.defect_type == 'EL' else 1
            map_productName_ElViPercent[dimission][percent_index] = index
            map_productNameModel_index.update({(dimission, model.defect_type): index})
        for product_name, percents in map_productName_ElViPercent.items():
            el_key = (product_name, 'EL')
            if el_key in map_productNameModel_index:
                el_index = map_productNameModel_index.get(el_key)
                el_percent = float(models[el_index].defects_percent[:-1])
                el_percent = int(el_percent) if el_percent == int(el_percent) else el_percent
                data_frame_dict['EL'].append(el_percent)
            else:
                data_frame_dict['EL'].append(0)
            vi_key = (product_name, 'VI')
            if vi_key in map_productNameModel_index:
                vi_index = map_productNameModel_index.get(vi_key)
                vi_percent = float(models[vi_index].defects_percent[:-1])
                vi_percent = int(vi_percent) if vi_percent == int(vi_percent) else vi_percent
                data_frame_dict['VI'].append(vi_percent)
            else:
                data_frame_dict['VI'].append(0)
            class_name_list.append(product_name)
        self.draw_chart(data_frame_dict, class_name_list)
    def draw_chart(self, data_frame, axisX_labels, axisY_range=[0, 100]):
        set_list = []
        for set_name, set_data_list in data_frame.items():
            set_ = QBarSet(set_name)
            set_.append(set_data_list)
            set_.setLabelColor(QColor(0, 0, 0))
            set_list.append(set_)
        series = QBarSeries()
        for set_ in set_list:
            series.append(set_)
        if series.count():
            width = 1 / series.count()
            max_width = 0.2 * series.count()
            min_width = 0.2 * series.count()
            if width > max_width:
                width = max_width
            if width < min_width:
                width = min_width
            series.setBarWidth(width)  
        series.setLabelsVisible(True)
        series.setLabelsPosition(QAbstractBarSeries.LabelsInsideBase)
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("产品缺陷分布占比图")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        axisX = QBarCategoryAxis()
        axisX.append(axisX_labels)
        chart.addAxis(axisX, Qt.AlignBottom)
        series.attachAxis(axisX)
        axisY = QValueAxis()
        axisY.setRange(*axisY_range)
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)
        if len(data_frame) < 2:
            chart.legend().setVisible(False)
        chart.legend().setAlignment(Qt.AlignBottom)
        self.chart_view.setChart(chart)
    def resizeEvent(self, event: QResizeEvent):
        """ 调整大小事件 """
        super().resizeEvent(event)
        self.loading_widget.resize(self.ui.tab.size())
        self.loading_widget.move(self.ui.tab.pos())
class UI_DefectCategoryStatistics(object):
    def __init__(self, parent):
        styleFile = 'qss/statistics.qss'
        qss = CommonHelper.readQss(styleFile)
        parent.setStyleSheet(qss)
        parent.setWindowTitle("缺陷类型分布统计")
        layout = QVBoxLayout(parent)
        self.filters_pannel = FiltersPannel()
        layout.addWidget(self.filters_pannel)
        self.tab = QTabWidget()
        layout.addWidget(self.tab)  
        self.statistics_table = DefectCategoryTable()
        self.tab.addTab(self.statistics_table, "列表")
        self.q_charts = QChartFrame()
        self.tab.addTab(self.q_charts, "图表")
        self.chart_view = QChartView(parent=self.q_charts)
class DefectCategoryTable(QTableWidget):
    signal_defect_class_small_btn_clicked = pyqtSignal(list)
    def __init__(self, *args):
        super().__init__(*args)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setHighlightSections(False)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)  
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)  
        self.setAlternatingRowColors(True)  
        self.verticalHeader().setHidden(True)  
        headers = ['序号', '产品类型', '生产线', '产品型号', '检测点', '缺陷类型', '检测方式', '缺陷小类', '维修率', '报废率', '缺陷总数量', '分布占比']
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        self.data = []
        self.set_column_width(0, 80)
    def set_column_width(self, index, width):
        """ 指定列宽 """
        self.horizontalHeader().setSectionResizeMode(index, QHeaderView.Custom)
        self.setColumnWidth(index, width)
    def update_data(self, rows_data):
        """ 更新数据 """
        self.setRowCount(len(rows_data))
        self.data = []
        gg_enum = DictInfoCRUD.get_all_gg_enum(True)
        for i, model in enumerate(rows_data):
            row_data = [
                i + 1,  
                model.product_type,  
                model.pro_line_name,
                model.pro_spec,
                model.detect_site,
                model.defect_type,  
                model.detect_type,  
                model.defect_small_class_num,  
                model.repaired_ratio,  
                model.scraped_ratio,  
                model.defects_sum_num,  
                model.defects_percent  
            ]
            self.data.append(row_data)
            for col, data in enumerate(row_data):
                if col == 7:
                    q_btn = QPushButton(str(data))
                    q_btn.setStyleSheet("""
                        border: none;
                        background-color: rgba(0,0,0,0);
                        color: rgb(19, 140, 222)
                    """)
                    q_btn.setCursor(Qt.PointingHandCursor)
                    q_btn.clicked.connect(self.slot_defect_class_small_btn_clicked(model.small_class_models))
                    self.setCellWidget(i, col, q_btn)
                else:
                    q_table_item = QTableWidgetItem()
                    q_table_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    q_table_item.setText(str(data))
                    self.setItem(i, col, q_table_item)
    def slot_defect_class_small_btn_clicked(self, s_class_models):
        """ 点击缺陷小类数量按钮 slot
        :param s_class_models: 缺陷小类 model 数据列表 [DefectStatisticSmallModel, DefectStatisticSmallModel, ...]
        :return:
        """
        try:
            def wrapper():
                self.signal_defect_class_small_btn_clicked.emit(s_class_models)
            return wrapper
        except Exception as e:
            logger.error(e, exc_info=True)
class FiltersPannel(QFrame):
    """ 搜索条件面板 """
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        title = QLabel("缺陷类型分布统计")
        title.hide()
        title.setObjectName("h1")
        layout.addWidget(title)  
        layout.addItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout2 = QGridLayout()
        self.cb_detect_type = ComboBoxGroup("检测方式:", ["AI检测", "人工复检"])
        layout2.addWidget(self.cb_detect_type, 0, 0)
        self.date_group = DateGroup('起止时间:')
        layout2.addWidget(self.date_group, 0, 1, 1, 4)
        self.cb_defect_big_class = ComboBoxGroup("缺陷大类:", ["全部", "VI", "EL"])
        layout2.addWidget(self.cb_defect_big_class, 1, 0)
        self.cb_defect_type = ComboBoxGroup("缺陷类型:", [])
        layout2.addWidget(self.cb_defect_type, 1, 1)
        self.cb_statistics_dimension = DimissionFilter()
        layout2.addWidget(self.cb_statistics_dimension, 1, 2)
        layout.addLayout(layout2)
        self.btn_search = IconButton(':/icons/search.png')
        layout.addWidget(self.btn_search)
        self.btn_download = IconButton(':/icons/download.png')
        layout.addWidget(self.btn_download)
        self.init_state()
    def init_state(self):
        """ 初始化界面布局 """
        self.cb_detect_type.comboBox.setCurrentIndex(0)
        self.date_group.comboBox.setCurrentIndex(0)
        self.cb_defect_big_class.comboBox.setCurrentIndex(0)
        self.cb_defect_type.comboBox.setCurrentIndex(0)
class QChartFrame(QFrame):
    signal_chart_frame_resize = pyqtSignal(QSize)
    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        self.signal_chart_frame_resize.emit(self.size())
class DimissionFilter(QFrame):
    """
    统计维度搜索控件
    """
    def __init__(self, parent=None):
        super(DimissionFilter, self).__init__(parent)
        self.config = []  
        self.hbox = QHBoxLayout(self)
        self.init_ui()
    def init_ui(self):
        title = QLabel("统计维度:")
        self.hbox.addWidget(title)
        self.pro_lines_combox = QComboBox()  
        self.pro_specs_combox = QComboBox()  
        self.detect_sites_combox = QComboBox()  
        self.detect_sites_combox.addItem('全部检测点', '')
        self.detect_sites_combox.addItem('层前EL&VI', '(1)')
        self.detect_sites_combox.addItem('层后EL', '(3)')
        self.hbox.addWidget(self.pro_lines_combox)
        self.hbox.addWidget(self.pro_specs_combox)
        self.hbox.addWidget(self.detect_sites_combox)
    def set_data(self, data):
        """
        设置生产线和规格下拉框
        """
        self.config = data
        self.pro_lines_combox.clear()
        self.pro_specs_combox.clear()
        pro_lines = [{'pro_line_id': '', 'pro_line_name': '全部产线'}]
        pro_lines.extend(data.get('pro_lines'))
        pro_specs = [{'id': '', 'name': '全部规格'}]
        pro_specs.extend(data.get('pro_specs'))
        for item in pro_lines:
            self.pro_lines_combox.addItem(item.get('pro_line_name'), item.get('pro_line_id'))
        for item in pro_specs:
            self.pro_specs_combox.addItem(item.get('name'), item.get('id'))
    @property
    def data(self):
        """
        动态获取当前产线ID、规格、检测点
        """
        pro_line_id = self.pro_lines_combox.currentData()
        pro_spec = self.pro_specs_combox.currentData()
        detect_site = self.detect_sites_combox.currentData()
        return pro_line_id, pro_spec, detect_site
class DefectCategorySmallStatistics(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = UI_DefectCategoryStatistics(self)
        self.q_charts = self.ui.q_charts
        self.chart_view = self.ui.chart_view
        self.pie_view = QWebEngineView()
        self.echarts_js = ''
        self.bind_events()
    def bind_events(self):
        self.q_charts.signal_chart_frame_resize.connect(self.slot_chart_frame_resize)
        self.ui.btn_back.clicked.connect(self.slot_btn_back_clicked)
    def load_data(self, data):
        """ 加载表格数据
        数据格式：
            {
                缺陷小类: [0,1,2,0,0,0,0,0],    
            }
        """
        try:
            self.ui.statistics_table.update_data(data)
            defect_class_percent_list = []  
            repaired_percent_list = []  
            class_name_list = []
            for model in data:
                dc_percent = float(model.defects_percent[:-1])
                dc_percent = int(dc_percent) if dc_percent == int(dc_percent) else round(dc_percent, 2)
                defect_class_percent_list.append(dc_percent)
                class_name_list.append(model.defect_class_name)
                repaired_percent = float(model.average_repaired_ratio[:-1])
                repaired_percent = int(repaired_percent) if repaired_percent == int(repaired_percent) else round(
                    repaired_percent, 2)
                repaired_percent_list.append(repaired_percent)
            zipped = zip(class_name_list, defect_class_percent_list, repaired_percent_list)
            sort_zipped = sorted(list(zipped), key=lambda x: x[1], reverse=True)
            res = zip(*sort_zipped)
            class_name_list, defect_class_percent_list, repaired_percent_list = [list(x) for x in res]
            chart1 = [
                [
                    [
                        defect_class_percent_list,
                        repaired_percent_list
                    ],
                    class_name_list
                ],
                {
                    "max_y": 100,
                    "show_data_handler": {
                        0: lambda x: "0%" if x == 0 else f"{x}%",
                        1: lambda x: "0%" if x == 0 else f"{x}%"
                    },
                    "legends": ["缺陷分布占比", "缺陷平均修复率"]
                }
            ]
            charts = [chart1]
            self.chart_load_data(charts)
            defect_data = []
            repaired_data = []
            labels = []
            for index in range(len(class_name_list)):
                label = class_name_list[index]
                defect_data.append([label, defect_class_percent_list[index]])
                repaired_data.append([label, repaired_percent_list[index]])
                labels.append(label)
            self.load_pie_chart(defect_data, repaired_data, labels)
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("缺陷类型小类页面加载数据出错")
    @staticmethod
    def label_opts(repaired_data, labels):
        params = "let repaired_data = " + str(repaired_data) + ";" + "let labels = " + str(
            labels) + "; let repaired = null;"
        fn = """
            function(params) {
            """ + params + """
                for (let i=0; i < labels.length; i++) {
                    if (labels[i] === params.name) {
                        repaired = repaired_data[i];
                        break;
                    }
                }
                return params.name + '\\n缺陷分布占比：' + params.value + '%' + '\\n平均修复率: ' + repaired[1] + '%';
            }
            """
        return options.LabelOpts(formatter=JsCode(fn))
    def load_pie_chart(self, defect_data, repaired_data, labels):
        """ 加载饼状图 """
        try:
            colors = ['#FF7C7C', '#9188E7', '#60ACFC', '#34D2EB', '#5CC49F', '#A5A5A5', '#FEB64E', '#7BD5F8', '#8A67C5',
                      '#E78A3F', '#20908F', '#E47BA6', '#4477E0', '#89AAEE', '#10B674', '#A0E8CC', '#4C648E', '#A8B0C3',
                      '#F7C225', '#FAE39E']
            pie = Pie()
            pie.add('', defect_data, center=["50%", "55%"], radius=["0%", "50%"])
            pie.set_colors(colors)
            pie.set_global_opts(legend_opts=options.LegendOpts(legend_icon='circle')) \
                .set_series_opts(label_opts=self.label_opts(repaired_data, labels))
            html = pie.render()
            if not self.echarts_js:
                with open("pyecharts/render/templates/echarts.min.js", "r", encoding="utf8") as f:
                    self.echarts_js = f.read()
            html = html.replace(
                '<script type="text/javascript" src="https://assets.pyecharts.org/assets/echarts.min.js"></script>',
                '<script type="text/javascript">\n' + self.echarts_js + '\n</script>'
            )
            html = html.replace(
                'style="width:900px; height:500px;"',
                'style="width:1700px; height:780px; margin:0px auto;"'
            )
            self.ui.q_pie_chart.setHtml(html)
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("绘制饼状图出错")
    def chart_load_data(self, charts):
        """ 图表加载数据
        :param charts: [(chart1_args,chart1_kwargs),(chart2_args,chart2_kwargs)]
        """
        try:
            self.ui.q_charts.clear()
            pro_counts = len(charts[0][0][1])
            for i, chart in enumerate(charts):
                bar = BarGraph()
                bar.set_bar_bgcorlor(QColor(70, 70, 70))
                if i == 0:
                    bar.set_color_map(
                        [
                            [QColor(246, 228, 114), QColor(237, 153, 45)],
                            [QColor(110, 228, 33), QColor(28, 82, 2)],
                            [QColor(255, 110, 40), QColor(165, 1, 38)],
                        ]
                    )
                bar.set_bar_width(0.025 * pro_counts)
                bar.set_bar_margin(0.005 * pro_counts)
                bar.set_data_frame(*chart[0], **chart[1])
                self.ui.q_charts.add_widget(bar)
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("绘制柱状图出错")
    def draw_chart(self, data_frame, axisX_labels, axisY_range=[0, 100]):
        """ 绘制图表
        :param data_frame: 数据表 {"set_name":[1,2,3,4,5,6]}
        :param axisX_labels: x 轴标签
        :param axisY_range: y 轴值范围
        """
        set_list = []
        for set_name, set_data_list in data_frame.items():
            set_ = QBarSet(set_name)
            set_.append(set_data_list)
            set_.setLabelColor(QColor(0, 0, 0))
            set_list.append(set_)
        series = QBarSeries()
        for set_ in set_list:
            series.append(set_)
        if series.count():
            width = 1 / series.count()
            max_width = 0.15
            if width > max_width:
                width = max_width
            series.setBarWidth(width)  
        series.setLabelsVisible(True)
        series.setLabelsPosition(QAbstractBarSeries.LabelsOutsideEnd)
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("缺陷小类占比图")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        axisX = QBarCategoryAxis()
        axisX.append(axisX_labels)
        chart.addAxis(axisX, Qt.AlignBottom)
        series.attachAxis(axisX)
        axisY = QValueAxis()
        axisY.setRange(*axisY_range)
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)
        if len(data_frame) < 2:
            chart.legend().setVisible(False)
        chart.legend().setAlignment(Qt.AlignBottom)
        self.chart_view.setChart(chart)
    def slot_chart_frame_resize(self, size: QSize):
        try:
            fw, fh = size.width(), size.height()
            self.chart_view.setFixedSize(QSize(fw, fh))
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("重置图表尺寸失败")
    def slot_btn_back_clicked(self):
        """ 返回上级 """
        try:
            self.parent().parent().parent().init_navigation_bar_fun(
                [{"统计分析 | 组件缺陷类型分布统计": self.parent().DefectCategoryStatistics_index}])
            self.parent().setCurrentIndex(self.parent().DefectCategoryStatistics_index)
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("返回上级列表失败")
class UI_DefectCategoryStatistics(object):
    def __init__(self, parent):
        styleFile = 'qss/statistics.qss'
        qss = CommonHelper.readQss(styleFile)
        parent.setStyleSheet(qss)
        parent.setWindowTitle("缺陷类型分布统计")
        layout = QVBoxLayout(parent)
        layout_1 = QHBoxLayout()
        title = QLabel("缺陷小类分布详情")
        title.hide()
        title.setObjectName("h1")
        layout_1.addWidget(title)  
        layout_1.addItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addLayout(layout_1)  
        self.tab = QTabWidget()
        layout.addWidget(self.tab)  
        self.statistics_table = DefectCategorySmallTable()
        self.tab.addTab(self.statistics_table, "列表")
        self.q_charts = QChartFrame()
        self.tab.addTab(self.q_charts, "柱状图")
        self.chart_view = QChartView()
        self.q_pie_chart = QWebEngineView()
        self.tab.addTab(self.q_pie_chart, "饼状图")
        layout_3 = QHBoxLayout()
        layout_3.addItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.btn_back = QPushButton("返回上级")
        self.btn_back.setObjectName('back_btn')
        self.btn_back.setCursor(Qt.PointingHandCursor)
        layout_3.addWidget(self.btn_back)
        layout_3.addItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addLayout(layout_3)
class DefectCategorySmallTable(QTableWidget):
    def __init__(self, *args):
        super().__init__(*args)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setHighlightSections(False)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)  
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)  
        self.setAlternatingRowColors(True)  
        self.verticalHeader().setHidden(True)  
        headers = ['序号', '产品类型', '生产线', '产品型号', '检测点', '缺陷小类', '串焊机', '缺陷数量', '占比', '产品数量', '平均缺陷数量', '当前缺陷平均修复率',
                   '报废率']
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        self.data = []
        self.set_column_width(0, 80)
    def set_column_width(self, index, width):
        """ 指定列宽 """
        self.horizontalHeader().setSectionResizeMode(index, QHeaderView.Fixed)
        self.setColumnWidth(index, width)
    def preview_table_data(self, data):
        """ 预览表格数据，用作下载 """
        results = []
        gg_enum = DictInfoCRUD.get_all_gg_enum(True)
        for i, model in enumerate(data):
            results.append([
                i + 1,  
                model.product_type,  
                model.pro_line_name,
                gg_enum.get(model.pro_spec),
                model.detect_site,
                model.defect_class_name,  
                model.welding,  
                model.defects_num,  
                model.defects_percent,  
                model.product_num,  
                model.average_defects,  
                model.average_repaired_ratio,  
                model.scraped_ratio  
            ])
        return results
    def update_data(self, rows_data):
        """ 更新截面数据 """
        self.setRowCount(len(rows_data))
        self.data = []
        gg_enum = DictInfoCRUD.get_all_gg_enum(True)
        for i, model in enumerate(rows_data):
            row_data = [
                i + 1,  
                model.product_type,  
                model.pro_line_name,
                gg_enum.get(model.pro_spec),
                model.detect_site,
                model.defect_class_name,  
                model.welding,  
                model.defects_num,  
                model.defects_percent,  
                model.product_num,  
                model.average_defects,  
                model.average_repaired_ratio,  
                model.scraped_ratio,  
            ]
            self.data.append(row_data)
            for col, data in enumerate(row_data):
                q_table_item = QTableWidgetItem()
                q_table_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.setItem(i, col, q_table_item)
                if col == 6:
                    q_table_item.setToolTip(str(data))
                    q_table_item.setText(str(data)[:15] + "..." if len(str(data)) > 15 else str(data))
                else:
                    q_table_item.setText(str(data))
class QChartFrame(QFrame):
    signal_chart_frame_resize = pyqtSignal(QSize)
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.widgets = []
    def add_widget(self, widget):
        try:
            self.widgets.append(widget)
            self.layout.addWidget(widget)
        except Exception as e:
            logger.error(e, exc_info=True)
    def clear(self):
        """ 清除数据 """
        for widget in self.widgets:
            self.layout.removeWidget(widget)
        self.widgets = []
    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        self.signal_chart_frame_resize.emit(self.size())
class QPieChartFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.widgets = []
        self.pixmap = QPixmap()
    def add_widget(self, widget):
        try:
            self.widgets.append(widget)
            self.layout.addWidget(widget)
        except Exception as e:
            logger.error(e, exc_info=True)
    def clear(self):
        """ 清除数据 """
        for widget in self.widgets:
            self.layout.removeWidget(widget)
        self.widgets = []
    def draw_pixmap(self, pixmap):
        self.pixmap = pixmap
        self.repaint()
    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        try:
            painter.begin(self)
            painter.save()
            print(self.pixmap.size())
            if self.pixmap.size() != QSize(0, 0):
                x_ratio = (self.width() - 80) / self.pixmap.width()  
                y_ratio = (self.height() - 80) / self.pixmap.height()
                scale_ratio = min(x_ratio, y_ratio)
                new_pixmap = self.pixmap.scaled(
                    QSize(self.pixmap.width() * scale_ratio, self.pixmap.height() * scale_ratio))
                painter.translate(self.width() / 2, self.height() / 2)
                painter.drawPixmap(
                    QRect(-new_pixmap.width() / 2, -new_pixmap.height() / 2, new_pixmap.width(), new_pixmap.height()),
                    new_pixmap)
                painter.restore()
        except Exception as e:
            logger.error(e, exc_info=True)
        finally:
            painter.end()
class DefectPosStatistics(QWidget):
    def __init__(self, main_window, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_window = main_window
        self.cruds = defectPos()
        self.ui = UI_DefectPosStatistics(self)
        self.cb_detect_type = self.ui.filters_pannel.cb_detect_type.comboBox  
        self.cb_line = self.ui.filters_pannel.cb_line.comboBox  
        self.start_date = self.ui.filters_pannel.date_group.start_date  
        self.end_date = self.ui.filters_pannel.date_group.end_date  
        self.cb_date_selections = self.ui.filters_pannel.date_group.comboBox  
        self.cb_defect_big_class = self.ui.filters_pannel.cb_defect_big_class.comboBox  
        self.cb_defect_type = self.ui.filters_pannel.cb_defect_type.comboBox  
        self.cb_statistics_dimension = self.ui.filters_pannel.cb_statistics_dimension.comboBox  
        self.cb_product_size = self.ui.filters_pannel.cb_product_size.comboBox  
        self.btn_search = self.ui.filters_pannel.btn_search  
        self.btn_download = self.ui.filters_pannel.btn_download  
        self.progress_bar = ProgressBarWindow(value_show=False)  
        self.btn_download.setEnabled(self.main_window.get_system_func("defect_statistic_download"))
        self.current_statistics_dimension_index = 0  
        self.is_loading = False  
        self.loading_widget = LoadingWidget(":/icons/loading.gif", parent=self)
        self.current_product_spec = None  
        self.data_dict = None  
        self.data_models = None  
        self.defect_big_class_type = None  
        self.defect_type = None  
        self.start_time_for_excel = ""  
        self.end_time_for_excel = ""  
        self.pro_line_for_excel = ""  
        self.defect_type_for_excel = ""  
        self.excel_data = None
        self.req_product_size()  
        self.req_defect_types()  
        self.req_product_line()  
        self.bind_events()
    def bind_events(self):
        """ 绑定事件 """
        self.cb_defect_big_class.currentTextChanged.connect(self.slot_defect_type_changed)
        self.cb_statistics_dimension.currentIndexChanged.connect(self.slot_statistics_dimension_changed)
        self.cb_product_size.currentIndexChanged.connect(self.slot_product_size_changed)
        self.ui.statistics_table.signal_defect_class_small_btn_clicked.connect(self.slot_defect_class_small_btn_clicked)
        self.btn_search.clicked.connect(self.slot_btn_search_clicked)
        self.btn_download.clicked.connect(self.slot_btn_download_clicked)
    def slot_defect_type_changed(self, text):
        """
        缺陷大类切换选项
        :param text: 当前缺陷大类下拉框文本
        :return:
        """
        try:
            self.cb_defect_type.clear()
            self.cb_defect_type.addItems(self.defect_type.get(text))
        except Exception as e:
            logger.error(e, exc_info=True)
    def slot_statistics_dimension_changed(self, index):
        """ 切换统计维度
        需求，如果选中产品型号，必须指定一个产品尺寸，不能是全部（方便绘制图表）
        """
        try:
            if index == 1:  
                if self.cb_product_size.currentIndex() == 0:  
                    if self.cb_product_size.count() == 1:
                        self.cb_statistics_dimension.setCurrentIndex(0)
                        self.cb_product_size.setCurrentIndex(0)
                        InformationMessageBoxOne("由于没有具体产品尺寸，产品型号统计维度不可选")
        except Exception as e:
            logger.error(e, exc_info=True)
    def slot_product_size_changed(self, index):
        """ 切换产品尺寸 """
        try:
            if index == 0:  
                if self.cb_statistics_dimension.currentIndex() == 1:  
                    self.cb_product_size.setCurrentIndex(self.cb_product_size.prev_index)
                    InformationMessageBoxOne("统计维度为产品型号时，只能选择具体的产品尺寸")
            else:
                self.cb_product_size.prev_index = index
        except Exception as e:
            logger.error(e, exc_info=True)
    def req_product_line(self):
        """
        获取生产线列表
        :return:
        """
        try:
            self.line_th = AsynThread(self.cruds.retrieve_product_lines, parent=self)
            self.line_th.signal_result.connect(self.slot_update_product_lines)
            self.line_th.start()
        except Exception as e:
            logger.error(e, exc_info=True)
    def slot_update_product_lines(self, product_lines):
        """
        更新生产性下拉列表槽函数
        :param product_lines: [{'pro_line_id': xxx, 'pro_line_name': xxx}, ...]
        :return:
        """
        try:
            self.cb_line.clear()
            if isinstance(product_lines, list):
                product_lines.insert(0, {'pro_line_id': '', 'pro_line_name': '全部'})
            else:
                return CriticalMessageBoxOne("获取生产线列表失败")
            for item in product_lines:
                self.cb_line.addItem(item.get('pro_line_name'), item.get('pro_line_id'))
        except Exception as e:
            logger.error(e, exc_info=True)
    def req_product_size(self):
        """ 获取产品尺寸
        这里的产品尺寸，其实是数据库中的规格
        :return:
        """
        try:
            self.product_size_th = AsynThread(self.cruds.retrieve_product_spec, args=(2,), parent=self)
            self.product_size_th.signal_result.connect(self.slot_update_product_size)
            self.product_size_th.start()
        except Exception as e:
            logger.error(e, exc_info=True)
    def slot_update_product_size(self, data):
        """ 更新产品尺寸的槽函数
        产品尺寸真实对应数据库的规格字段
        """
        try:
            self.cb_product_size.clear()
            pro_specs = [{'id': '', 'name': '全部规格'}]
            if isinstance(data, list):
                pro_specs.extend(data)
            for item in pro_specs:
                self.cb_product_size.addItem(item.get('name'), item.get('id'))
        except Exception as e:
            logger.error(e, exc_info=True)
    def req_defect_types(self):
        """
        获取缺陷类型
        :return:
        """
        try:
            self.cb_defect_big_class.setDisabled(True)  
            self.cb_defect_type.setDisabled(True)
            self.defect_type_th = AsynThread(self.cruds.retrieve_defect_types, parent=self)
            self.defect_type_th.signal_result.connect(self.slot_update_defect_types)
            self.defect_type_th.start()
        except Exception as e:
            logger.error(e, exc_info=True)
    def slot_update_defect_types(self, models):
        """ 更新缺陷类型的槽函数 """
        try:
            all_defect_types = list(set([model.LAB_CLASS_NAME for model in models]))
            el_defect_types = list(set([model.LAB_CLASS_NAME for model in models if model.CLASS_D_CATEGORY == 1]))
            vi_defect_types = list(set([model.LAB_CLASS_NAME for model in models if model.CLASS_D_CATEGORY == 2]))
            all_defect_types.sort()
            el_defect_types.sort()
            vi_defect_types.sort()
            all_defect_types.insert(0, "全部")
            el_defect_types.insert(0, "全部")
            vi_defect_types.insert(0, "全部")
            self.defect_type = {"全部": all_defect_types, "EL": el_defect_types, "VI": vi_defect_types}  
            current_defect_big_type = self.cb_defect_big_class.currentText()
            self.cb_defect_type.addItems(self.defect_type.get(current_defect_big_type))
            self.ui.q_heatmap.defects_combobox.addItems(self.defect_type.get(current_defect_big_type))
        except Exception as e:
            logger.error(e, exc_info=True)
        finally:
            self.cb_defect_big_class.setDisabled(False)  
            self.cb_defect_type.setDisabled(False)
    def slot_defect_class_small_btn_clicked(self, s_class_models):
        """ 点击缺陷小类数量按钮 slot
        :param s_class_models: 缺陷小类 model 数据列表 [DefectPosStatisticSmallModel, DefectPosStatisticSmallModel, ...]
        """
        try:
            self.parent().DefectPosSmallStatistics.load_data(self.current_statistics_dimension_index, s_class_models)
            self.parent().DefectPosSmallStatistics.ui.tab.setCurrentIndex(0)  
            self.main_window.init_navigation_bar_fun([{"统计分析 | 组件缺陷位置分布统计": self.parent().DefectPosStatistics_index},
                                                      {"缺陷类型分组统计": self.parent().DefectPosSmallStatistics_index}])
            self.parent().setCurrentIndex(self.parent().DefectPosSmallStatistics_index)
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("跳转缺陷位置小类页面出错")
    def slot_btn_search_clicked(self):
        """ 点击搜索按钮 """
        try:
            if self.loading_widget.is_loading:
                InformationMessageBoxOne("查询统计完成之后，才可再次查询")
                return
            self.ui.statistics_table.setRowCount(0)  
            self.loading_widget.start()  
            self.current_statistics_dimension_index = self.cb_statistics_dimension.currentIndex()
            if self.current_statistics_dimension_index == 0:
                self.ui.statistics_table.setHorizontalHeaderItem(1, QTableWidgetItem("产品尺寸"))
            else:
                self.ui.statistics_table.setHorizontalHeaderItem(1, QTableWidgetItem("产品型号"))
            self.start_time_for_excel = self.start_date.text()
            self.end_time_for_excel = self.end_date.text()
            self.defect_type_for_excel = self.cb_defect_big_class.currentText()
            self.pro_line_for_excel = self.cb_line.currentText()
            self.req_statistics_info()  
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("缺陷位置分布统计出错")
    def req_statistics_info(self):
        """ 异步请求统计信息 """
        try:
            detect_type_index = self.cb_detect_type.currentIndex()  
            product_line = self.cb_line.itemData(self.cb_line.currentIndex())  
            start_datetime = self.convert_qdate_to_datetime(self.start_date.date)  
            end_datetime = self.convert_qdate_to_datetime(self.end_date.date)  
            defect_big_class_index = self.cb_defect_big_class.currentIndex()  
            defect_type_text = self.cb_defect_type.currentText()  
            statistics_dimension_index = self.cb_statistics_dimension.currentIndex()  
            product_size = self.cb_product_size.currentData()  
            self.defect_big_class_type = self.cb_defect_big_class.currentText()  
            self.ui.q_heatmap.defects_combobox.clear()  
            defect_type = copy.copy(self.defect_type.get(self.defect_big_class_type))
            del defect_type[0]  
            self.ui.q_heatmap.defects_combobox.addItems(defect_type)
            user_info_dict = self.main_window.user
            user_id = user_info_dict['id']
            role_type = user_info_dict['role_type']
            self.data_th = AsynThread(
                self.cruds.retrieve,
                args=(
                    start_datetime, end_datetime, detect_type_index, product_line, defect_big_class_index,
                    defect_type_text, statistics_dimension_index, product_size, user_id, role_type
                ),
                parent=self
            )
            self.data_th.signal_result.connect(self.slot_get_statistics_info)
            self.data_th.signal_result_error.connect(self.slot_get_statistics_info_error)
            self.data_th.start()
        except Exception as e:
            logger.error(str(e), exc_info=True)
    def slot_get_statistics_info(self, models):
        """
        获取到的统计信息
        """
        try:
            model_list, map_defects_positions, map_size_and_pos_failure, excel_data = models
            self.data_models = model_list
            self.excel_data = excel_data
            self.ui.statistics_table.update_data(model_list)
            self.chart_load_data(map_size_and_pos_failure)
            self.heatmap_load_data(map_defects_positions)
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("查询缺陷位置分布统计数据出错")
        finally:
            self.loading_widget.stop()
    def slot_get_statistics_info_error(self):
        """
        查询数据失败槽函数
        :return:
        """
        try:
            self.loading_widget.stop()
        except Exception as e:
            logger.error(e, exc_info=True)
        CriticalMessageBoxOne("获取缺陷位置数据失败")
    def calc_type(self, items):
        """
        判断列表是否需要被展开，判断依据是列表中的项是否是可迭代对象
        :param items:
        :return:
        """
        for item in items:
            if isinstance(item, Iterable):
                return True
        return False
    def flatten(self, items):
        """
        展开一维列表中包含的多维列表
        :param items:
        :return:
        """
        if not isinstance(items, Iterable):
            yield items
        else:
            if not self.calc_type(items):
                if len(items) > 2 or items == [None, None]:
                    for item in items:
                        yield item
                else:
                    yield tuple(items)
            else:
                for item in items:
                    if isinstance(item, Iterable) and np.array(item).ndim > 1:
                        for sub_item in self.flatten(item):
                            yield tuple(sub_item)
                    elif isinstance(item, Iterable):
                        yield tuple(item)
                    else:
                        yield item
    def slot_btn_download_clicked(self):
        """ 点击下载按钮 """
        try:
            if not self.main_window.get_system_func('defect_statistic_download'):
                return InformationMessageBoxOne("暂无权限下载，请联系管理员")
            if not self.excel_data:  
                InformationMessageBoxOne("没有数据可供下载，请先查询")
                return
            if self.loading_widget.is_loading:
                InformationMessageBoxOne("正在查询数据，请稍后下载")
                return
            file_name = f"组件缺陷位置分布统计报表_{datetime.now().strftime('%Y%m%d')}.xlsx"
            file_path = gen_xlsx_path(file_name, "下载缺陷位置分布统计报表")
            if not file_path:
                return
            self.download_excel(file_path)
        except FileCreateError as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne(f"下载缺陷位置分布统计报表出错, {e}")
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("下载缺陷位置分布统计报表出错")
    def download_excel(self, file_path):
        """
        下载excel数据
        :param file_path: 文件下载路径
        :return:
        """
        self.progress_bar.set_title("正在下载 %s" % os.path.basename(file_path))
        self.progress_bar.show()
        sum_data, detail_data, sub_data = self.excel_data
        self.download_th = AsyncDownloadPackedDetectPos(sum_data, detail_data, sub_data,
                                                        self.cb_detect_type.currentIndex(),
                                                        self.current_statistics_dimension_index,
                                                        [self.start_time_for_excel, self.end_time_for_excel], file_path,
                                                        self)
        self.download_th.signal_result.connect(self.slot_download_success)
        self.download_th.signal_result_error.connect(self.slot_download_error)
        self.download_th.start()
    def slot_download_success(self, data):
        """
        下载成功槽函数
        :param data:
        :return:
        """
        if self.progress_bar:
            self.progress_bar.close()
        InformationMessageBoxOne("下载完成")
    def slot_download_error(self, data):
        """
        下载失败槽函数
        :param data:
        :return:
        """
        if self.progress_bar:
            self.progress_bar.close()
        try:
            raise data.get("error")
        except InvalidWorksheetName as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne(f"工作表包含不允许的字符")
        except FileCreateError as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne(f"下载缺陷位置分布统计报表出错, 该文件处于使用状态")
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("下载缺陷位置分布统计报表出错")
    def get_small_class_table_data(self, row_index):
        """ 获取缺陷小类的数据
        :param row_index: 缺陷大类行索引，用户获取子类数据列表
        :return: headers, table
        """
        headers = []
        obj = self.parent().DefectPosSmallStatistics.ui.statistics_table
        col_mun = obj.columnCount()
        for i in range(col_mun):
            header = obj.model().headerData(i, Qt.Horizontal, Qt.DisplayRole)
            headers.append(header)
        table = obj.preview_table_data(self.data_models[row_index].small_class_models)
        return headers, table
    @staticmethod
    def convert_qdate_to_datetime(qdate: QDate):
        """ 将日期文本转换成
        :param qdate: QDate
        :return:
        """
        date_str = datetime.strftime(qdate.toPyDateTime(), '%Y-%m-%d %H:%M:%S')
        return date_str
    def resizeEvent(self, event: QResizeEvent):
        """ 调整大小事件 """
        super().resizeEvent(event)
        self.loading_widget.resize(self.ui.tab.size())
        self.loading_widget.move(self.ui.tab.pos())
    def chart_load_data(self, map_size_and_pos_failure):
        """ 图表加载数据
        :param map_size_and_pos_failure: 格式如下
        {
            "产品尺寸1": [
                [(1,1),(2,1),(3,2)],    
                "failure_percent",
                [product_id]
            ],
            "产品尺寸2":[
                [],
                "",
                [product_id]
            ]
        }
        {(产品尺寸, 产品型号): {"隐裂":[product_id,product_id],[(1,1),(2,2),(3,3)]}}
        :param positions: 所有的缺陷位置
        :return:
        """
        chart_data = {}
        for product_size, postions_failure_products in map_size_and_pos_failure.items():
            positions, failure_percent = postions_failure_products
            flatten_items = []
            for item in self.flatten(positions):
                flatten_items.append(tuple(item)) if item else flatten_items.append(item)
            pos_set = set(flatten_items)
            postions_data = []  
            for pos in pos_set:
                if pos:  
                    postions_data.append((pos[0] - 1, pos[1] - 1, flatten_items.count(pos)))
            chart_data.update({product_size: [postions_data, failure_percent]})
        self.ui.q_charts.set_charts(chart_data)
    def heatmap_load_data(self, map_defects_positions):
        """ 热力图加载数据
        :param map_defects_positions: 所有缺陷的缺陷位置 
        20200617 需求：需要选择每一个【缺陷类】后，才可以显示对应的缺陷类热力图
        """
        try:
            self.ui.q_heatmap.set_map_defects_and_positions(map_defects_positions)  
            self.ui.q_heatmap.slot_change_filter_index(0)  
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("绘制热力图失败")
class UI_DefectPosStatistics(object):
    def __init__(self, parent):
        styleFile = 'qss/statistics.qss'
        qss = CommonHelper.readQss(styleFile)
        parent.setStyleSheet(qss)
        parent.setWindowTitle("缺陷位置分布统计")
        layout = QVBoxLayout(parent)
        self.filters_pannel = FiltersPannel()
        layout.addWidget(self.filters_pannel)
        self.tab = QTabWidget()
        layout.addWidget(self.tab)  
        self.statistics_table = DefectPosTable()
        self.tab.addTab(self.statistics_table, "列表")
        self.q_charts = QChartFrame()
        self.tab.addTab(self.q_charts, "图表")
        self.q_heatmap = QHeatMap()
        self.tab.addTab(self.q_heatmap, "热力图")
class FiltersPannel(QFrame):
    """ 搜索条件面板 """
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        title = QLabel("缺陷位置分布统计")
        title.hide()
        title.setObjectName("h1")
        layout.addWidget(title)  
        layout.addItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout2 = QGridLayout()
        self.cb_detect_type = ComboBoxGroup("检测方式:", ["AI检测", "人工复检"])
        layout2.addWidget(self.cb_detect_type, 0, 0)
        self.cb_line = ComboBoxGroup("生产线:", ["全部", "L2", "L3"])
        layout2.addWidget(self.cb_line, 0, 1)
        self.date_group = DateGroup('起止时间:')
        layout2.addWidget(self.date_group, 0, 2, 1, 3)
        self.cb_defect_big_class = ComboBoxGroup("缺陷大类:", ["全部", "VI", "EL"])
        layout2.addWidget(self.cb_defect_big_class, 1, 0)
        self.cb_defect_type = ComboBoxGroup("缺陷类型:", [])
        layout2.addWidget(self.cb_defect_type, 1, 1)
        self.cb_statistics_dimension = ComboBoxGroup("统计维度:", ["产品尺寸", '产品型号'])
        layout2.addWidget(self.cb_statistics_dimension, 1, 2)
        self.cb_product_size = ComboBoxGroup("产品尺寸:", ["全部"])
        layout2.addWidget(self.cb_product_size, 1, 4)
        layout.addLayout(layout2)
        self.btn_search = IconButton(':/icons/search.png')
        layout.addWidget(self.btn_search)
        self.btn_download = IconButton(':/icons/download.png')
        layout.addWidget(self.btn_download)
    def init_data(self):
        """ 初始化数据 """
        pass
class DefectPosTable(QTableWidget):
    signal_defect_class_small_btn_clicked = pyqtSignal(list)
    def __init__(self, *args):
        super().__init__(*args)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setHighlightSections(False)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)  
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)  
        self.setAlternatingRowColors(True)  
        self.verticalHeader().setHidden(True)  
        headers = ['序号', '产品尺寸', '缺陷总数', '单产品缺陷平均数', '缺陷类型数量', '最高缺陷位', '总体不良率']
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        self.data = []
        self.set_column_width(0, 80)
    def set_column_width(self, index, width):
        """ 指定列宽 """
        self.horizontalHeader().setSectionResizeMode(index, QHeaderView.Custom)
        self.setColumnWidth(index, width)
    def update_data(self, rows_data):
        """ 更新数据 """
        self.setRowCount(len(rows_data))
        self.data = []
        for i, model in enumerate(rows_data):
            temp_statistics_dimension = model.temp_statistics_dimension
            row_data = [
                i + 1,  
                temp_statistics_dimension,  
                model.defects_sum_num,  
                model.average_defects,  
                model.defect_small_class_num,  
                model.most_defect_pos,  
                model.failure_percent,  
            ]
            self.data.append(row_data)
            for col, data in enumerate(row_data):
                if col == 4:
                    q_btn = QPushButton(str(data))
                    q_btn.setStyleSheet("""
                        border: none;
                        background-color: rgba(0,0,0,0);
                        color: rgb(19, 140, 222)
                    """)
                    q_btn.setCursor(Qt.PointingHandCursor)
                    q_btn.clicked.connect(self.slot_defect_class_small_btn_clicked(model.small_class_models))
                    self.setCellWidget(i, col, q_btn)
                else:
                    q_table_item = QTableWidgetItem()
                    q_table_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    q_table_item.setText(str(data))
                    self.setItem(i, col, q_table_item)
    def slot_defect_class_small_btn_clicked(self, s_class_models):
        """ 点击缺陷小类数量按钮 slot
        :param s_class_models: 缺陷小类 model 数据列表 [DefectStatisticSmallModel, DefectStatisticSmallModel, ...]
        :return:
        """
        try:
            def wrapper():
                self.signal_defect_class_small_btn_clicked.emit(s_class_models)
            return wrapper
        except Exception as e:
            logger.error(e, exc_info=True)
class QChartFrame(QFrame):
    signal_chart_frame_resize = pyqtSignal(QSize)
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout_widget = []
        self.table_class = DefectRateTableChart
    def set_charts(self, charts_data):
        """ 统计界面显示的 chart 图表
        :param charts_data: {产品尺寸:[[(0,0,count),(1,1,count),(2,2,count)], "failure_percent"]}
        """
        self.clear_data()
        for product_size, pos_failure in charts_data.items():
            positions_data, failure_percent = pos_failure
            title = QLabel(f"产品尺寸({product_size})缺陷位统计图表")
            title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.addWidget(title)
            if product_size is None:
                continue
            new_table = self.table_class()
            _row, _col = product_size.split("*")
            new_table.set_product_spec(int(_row), int(_col))
            new_table.load_data(positions_data, failure_percent)
            self.layout.addWidget(new_table)
            self.layout_widget.append(new_table)
            self.layout_widget.append(title)
            self.layout_widget.append(new_table)
    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        self.signal_chart_frame_resize.emit(self.size())
    def clear_data(self):
        """ 清空面板数据 """
        logger.info("清空缺陷位图表数据")
        for item in self.layout_widget:
            self.layout.removeWidget(item)
            item.close()
        self.layout_widget = []
class QHeatMap(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_ui()
        self.map_defects_and_pos = {}
        self.init_heatmap_page()  
        self.shared = Shared()
        self.init_channel()
        self.bind_events()
    def init_ui(self):
        """
        初始化样式
        :return:
        """
        layout = QVBoxLayout(self)
        layout_1 = QHBoxLayout()
        layout.addLayout(layout_1)
        layout_1.addItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum))
        combobox_product_size = ComboBoxGroup("产品尺寸:", [])
        combobox_product_size.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.product_size_combobox = combobox_product_size.comboBox
        layout_1.addWidget(combobox_product_size)
        combobox_group = ComboBoxGroup("缺陷类型:", [])
        combobox_group.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.defects_combobox = combobox_group.comboBox
        layout_1.addWidget(combobox_group)
        layout_1.addItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.heatmap_view = QWebEngineView()
        self.heatmap_view.setContextMenuPolicy(Qt.NoContextMenu)
        layout.addWidget(self.heatmap_view)
    def bind_events(self):
        self.product_size_combobox.currentIndexChanged.connect(self.slot_change_filter_index)
        self.defects_combobox.currentIndexChanged.connect(self.slot_change_filter_index)
    def init_channel(self):
        """
        初始化web页面管道
        :return:
        """
        self.channel = QWebChannel()
        self.channel.registerObject("shared", self.shared)
        self.heatmap_view.page().setWebChannel(self.channel)
    def init_heatmap_page(self):
        try:
            url = QUrl(QFileInfo('dashboard/compiler/heatmap.html').absoluteFilePath())
            self.heatmap_view.load(url)
        except Exception as e:
            logger.error(e)
    def set_map_defects_and_positions(self, map_defects_and_positions):
        """ 设置缺陷位heatmap数据
        :param map_defects_and_positions: 所有缺陷的缺陷位置, {产品尺寸:{"隐裂": [(0,0),(0,1),(2,1)]}}
        :return:
        """
        self.map_defects_and_pos = map_defects_and_positions
        self.product_size_combobox.clear()
        self.product_size_combobox.addItems(list(map_defects_and_positions.keys()))
        self.slot_change_filter_index(0)  
    def get_current_spec(self):
        """ 获取当前选中的产品尺寸 """
        spec = self.product_size_combobox.currentText()
        if spec:
            row_num, col_num = spec.split("*")
        else:
            row_num, col_num = 0, 0
        return int(row_num), int(col_num)
    def slot_change_filter_index(self, index):
        """ 改变当前选中的 product_size 或 defects
        注意：切换的 defect 可能没有对应的缺陷，要置为空
        """
        try:
            current_product_size = self.product_size_combobox.currentText()
            current_defect = self.defects_combobox.currentText()
            if current_product_size:
                current_pos_list = self.map_defects_and_pos.get(current_product_size, {}).get(current_defect, [])
                self.draw_heatmap(current_pos_list)
            else:
                self.draw_heatmap([])
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("切换缺陷类型位置分布热力图失败")
    def draw_heatmap(self, pos_list):
        """ 绘制热力图的方法
        :param pos_list: 缺陷位置列表：[(1,1),(2,3),(1,1),(4,3)] 坐标从 (0,0) 开始(row,col)
        :return:
        """
        rows_num, cols_num = self.get_current_spec()
        cols = [i + 1 for i in range(cols_num)]
        rows = [chr(i + 65) for i in range(rows_num)]
        rows.reverse()
        data = []
        for row in range(rows_num):
            for col in range(cols_num):
                data.append([col, len(rows) - 1 - row, pos_list.count((row, col))])  
        heatmap_data = []
        min_value = 0
        max_value = 0
        for d in data:
            heatmap_data.append([d[0], d[1], d[2] or '-'])  
            if d[2] > max_value:
                max_value = d[2]
            if d[2] < min_value:
                min_value = d[2]
        res = {'x_axis': cols, 'y_axis': rows, 'min_value': min_value, 'max_value': max_value, 'data': heatmap_data}
        self.shared.signal_data_success.emit(json.dumps(res, ensure_ascii=False))
class DefectRateTableChart(QTableWidget):
    """ 不良率表图 """
    def __init__(self, *__args):
        """
        :param __args:
        """
        super().__init__(*__args)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setHighlightSections(False)
        self.verticalHeader().setHidden(True)
        self.spec_row = 0
        self.spec_col = 0
    def set_product_spec(self, row, col):
        """ 设置产品规格，用来重新加载表格尺寸
        :param row: int
        :param col: int
        :return:
        """
        self.spec_row = row
        self.spec_col = col
        col_labels = [""]
        col_labels.extend([str(i + 1) for i in range(col)])
        col_labels.extend(["不良率"])
        self.setColumnCount(len(col_labels))
        self.setHorizontalHeaderLabels(col_labels)
        row_labels = [chr(i + 65) for i in range(row)]
        self.setRowCount(len(row_labels))
        for i, text in enumerate(row_labels):
            item = QTableWidgetItem(text)
            item.setTextAlignment(Qt.AlignCenter)
            self.setItem(i, 0, item)
        self.setSpan(0, len(col_labels) - 1, len(row_labels), 1)
        self.set_column_width(0, 30)
        self.set_column_width(len(col_labels) - 1, 100)  
    def set_column_width(self, index, width):
        """ 指定列宽 """
        self.horizontalHeader().setSectionResizeMode(index, QHeaderView.Custom)
        self.setColumnWidth(index, width)
    def load_data(self, positions_data, failure_percent):
        """ 加载数据
        :param positions_data: index 从 0 开始的数据 (row_index, col_index, data)
        """
        try:
            for pos_data in positions_data:
                row_index, col_index, data = pos_data
                if col_index + 1 > self.spec_col or row_index + 1 > self.spec_row:
                    continue
                if col_index < 0:  
                    continue
                col_index += 1
                item = QTableWidgetItem(str(data))
                item.setTextAlignment(Qt.AlignCenter)
                self.setItem(row_index, col_index, item)
            item = QTableWidgetItem(str(failure_percent))
            item.setTextAlignment(Qt.AlignCenter)
            self.setItem(0, self.columnCount() - 1, item)
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("加载缺陷位置图表数据失败")
class Shared(QObject):
    """
    连接web页面管道类
    """
    signal_data_success = pyqtSignal(str)  
    signal_data_error = pyqtSignal(str)  
    def __init__(self, parent=None):
        super(Shared, self).__init__(parent=parent)
class DefectPosSmallStatistics(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = UI_DefectPosSmallStatistics(self)
        self.bind_events()
    def bind_events(self):
        """ 绑定事件 """
        self.ui.btn_back.clicked.connect(self.slot_btn_back_clicked)
    def load_data(self, current_statistics_dimension_index, models):
        """ 加载表格数据
        :param current_statistics_dimension_index: 当前统计维度索引
        :param models: 模型列表 [DefectPosStatisticSmallModel,DefectPosStatisticSmallModel,...]
        :return:
        """
        try:
            if current_statistics_dimension_index == 0:
                self.ui.statistics_table.setHorizontalHeaderItem(1, QTableWidgetItem("产品尺寸"))
            else:
                self.ui.statistics_table.setHorizontalHeaderItem(1, QTableWidgetItem("产品型号"))
            self.ui.statistics_table.update_data(models)
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("缺陷位置小类页面加载数据出错")
    def slot_btn_back_clicked(self):
        """ 返回上级 """
        try:
            self.parent().parent().parent().init_navigation_bar_fun(
                [{"统计分析 | 组件缺陷位置分布统计": self.parent().DefectPosStatistics_index}])
            self.parent().setCurrentIndex(self.parent().DefectPosStatistics_index)
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("返回上级列表失败")
class UI_DefectPosSmallStatistics(object):
    def __init__(self, parent):
        styleFile = 'qss/statistics.qss'
        qss = CommonHelper.readQss(styleFile)
        parent.setStyleSheet(qss)
        parent.setWindowTitle("缺陷位置分布统计")
        layout = QVBoxLayout(parent)
        layout_1 = QHBoxLayout()
        title = QLabel("缺陷类型分组统计")
        title.hide()
        title.setObjectName("h1")
        layout_1.addWidget(title)  
        layout_1.addItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addLayout(layout_1)
        self.tab = QTabWidget()
        layout.addWidget(self.tab)  
        self.statistics_table = DefectPosSmallTable()
        self.tab.addTab(self.statistics_table, "列表")
        layout_3 = QHBoxLayout()
        layout_3.addItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.btn_back = QPushButton("返回上级")
        self.btn_back.setObjectName('back_btn')
        self.btn_back.setCursor(Qt.PointingHandCursor)
        layout_3.addWidget(self.btn_back)
        layout_3.addItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addLayout(layout_3)
class QChartFrame(QFrame):
    signal_chart_frame_resize = pyqtSignal(QSize)
    def __init__(self, parent=None):
        super().__init__(parent=parent)
    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        self.signal_chart_frame_resize.emit(self.size())
class DefectPosSmallTable(QTableWidget):
    def __init__(self, *args):
        super().__init__(*args)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setHighlightSections(False)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)  
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)  
        self.setAlternatingRowColors(True)  
        self.verticalHeader().setHidden(True)  
        headers = ['序号', '产品尺寸', '缺陷小类', '缺陷数量', '占比', '产品数量', '最高缺陷位', '不良率']
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        self.set_column_width(0, 80)
    def set_column_width(self, index, width):
        """ 指定列宽 """
        self.horizontalHeader().setSectionResizeMode(index, QHeaderView.Custom)
        self.setColumnWidth(index, width)
    def preview_table_data(self, data):
        """ 预览表格数据，用作下载 """
        results = []
        for i, model in enumerate(data):
            results.append([
                i + 1,  
                model.temp_statistics_dimension,  
                model.defect_class_name,  
                model.defects_num,  
                model.defects_percent,  
                model.product_num,  
                model.most_defect_pos,  
                model.failure_percent,  
            ])
        return results
    def update_data(self, rows_data):
        """ 更新截面数据 """
        self.setRowCount(len(rows_data))
        for i, model in enumerate(rows_data):
            row_data = [
                i + 1,  
                model.temp_statistics_dimension,  
                model.defect_class_name,  
                model.defects_num,  
                model.defects_percent,  
                model.product_num,  
                model.most_defect_pos,  
                model.failure_percent,  
            ]
            for col, data in enumerate(row_data):
                q_table_item = QTableWidgetItem()
                q_table_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                q_table_item.setText(str(data))
                self.setItem(i, col, q_table_item)
class ErrorOmissionStatistics(QWidget):
    def __init__(self, main_window, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_window = main_window
        self.ui = UI_ErrorOmissionStatistics(self)
        self.start_date = self.ui.filters_pannel.date_group.start_date  
        self.end_date = self.ui.filters_pannel.date_group.end_date  
        self.cb_statistics_dimension = self.ui.filters_pannel.cb_statistics_dimension.comboBox  
        self.btn_search = self.ui.filters_pannel.btn_search  
        self.btn_download = self.ui.filters_pannel.btn_download  
        self.progress_bar = ProgressBarWindow(value_show=False)  
        self.start_time_for_excel = ""  
        self.end_time_for_excel = ""  
        self.dimension_for_excel = ""  
        self.btn_download.setEnabled(self.main_window.get_system_func("defect_statistic_download"))
        self.current_statistics_dimension_index = 0  
        self.is_loading = False  
        self.loading_widget = LoadingWidget(":/icons/loading.gif", parent=self)
        self.data_rows = []  
        self.xlsx_data = {}
        self.cruds = errorAndOmission()
        self.bind_event()
    def bind_event(self):
        """ 绑定事件 """
        self.btn_search.clicked.connect(self.slot_btn_search_clicked)
        self.btn_download.clicked.connect(self.slot_btn_download_clicked)
    def slot_detect_type_index_changed(self, index):
        """ 修改检测方式 """
        try:
            if index == 2:
                InformationMessageBoxOne("按【人工复检】统计暂未实现，需对接控制台")
                self.cb_detect_type.setCurrentIndex(0)
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("切换检测方式出错")
    def slot_btn_search_clicked(self):
        """ 点击搜索按钮处理函数 """
        try:
            if self.loading_widget.is_loading:
                InformationMessageBoxOne("查询统计完成之后，才可再次查询")
                return
            self.ui.statistics_table.setRowCount(0)  
            self.loading_widget.start()  
            self.ui.statistics_table.setHorizontalHeaderItem(2, QTableWidgetItem(
                self.cb_statistics_dimension.currentText()))
            self.start_time_for_excel = self.start_date.text()
            self.end_time_for_excel = self.end_date.text()
            self.dimension_for_excel = self.cb_statistics_dimension.currentText()
            self.req_statistics_info()  
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("产品误判率和漏检率统计出错")
    def slot_btn_download_clicked(self):
        """ 点击下载按钮处理函数 """
        try:
            if not self.main_window.get_system_func('defect_product_wupan_loujian_download'):
                return InformationMessageBoxOne("暂无权限下载，请联系管理员")
            if not self.data_rows:  
                InformationMessageBoxOne("没有数据可供下载，请先查询")
                return
            if self.loading_widget.is_loading:
                InformationMessageBoxOne("正在查询数据，请稍后下载")
                return
            file_name = f"组件产品误判率和漏检率统计报表_{datetime.now().strftime('%Y%m%d')}.xlsx"
            file_path = gen_xlsx_path(file_name, "组件产品误判率和漏检率统计报表")
            if not file_path:
                return
            self.download_excel(file_path)
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("下载产品误判率和漏检率统计报表出错")
    def download_excel(self, file_path):
        """ 下载 excel 数据 """
        self.progress_bar.set_title("正在下载 %s" % os.path.basename(file_path))
        self.progress_bar.show()
        download_th = AsyncDownloadPackedErrorOmission(file_path, self.xlsx_data, self)
        download_th.signal_result.connect(self.slot_download_success)
        download_th.signal_result_error.connect(self.slot_download_error)
        download_th.start()
    def slot_download_success(self, data):
        """
        下载成功槽函数
        :param data:
        :return:
        """
        if self.progress_bar:
            self.progress_bar.close()
        InformationMessageBoxOne("下载完成")
    def slot_download_error(self, data):
        """
        下载失败槽函数
        :param data:
        :return:
        """
        if self.progress_bar:
            self.progress_bar.close()
        try:
            raise data.get("error")
        except SheetTitleException as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne(f"工作表包含不允许的字符")
        except PermissionError as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne(f"下载产品误判率和漏检率统计报表出错, 该文件处于使用状态")
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("下载产品误判率和漏检率统计报表出错")
    def req_statistics_info(self):
        """ 异步请求统计信息 """
        try:
            start_datetime = self.convert_qdate_to_datetime(self.start_date.date)  
            end_datetime = self.convert_qdate_to_datetime(self.end_date.date)  
            statistics_dimension_index = self.cb_statistics_dimension.currentIndex()  
            user_info_dict = self.main_window.user
            user_id = user_info_dict['id']
            role_type = user_info_dict['role_type']
            self.data_th = AsynThread(
                self.cruds.retrieve,
                args=(start_datetime, end_datetime, statistics_dimension_index, user_id, role_type),
                parent=self
            )
            self.data_th.signal_result.connect(self.slot_get_statistics_info)
            self.data_th.signal_result_error.connect(self.slot_get_statistics_info_error)
            self.data_th.start()
        except Exception as e:
            logger.error(str(e), exc_info=True)
    def slot_get_statistics_info(self, models):
        """ 异步处理统计数据
        :param models:
        """
        try:
            data_rows, charts, xlsx_data = models
            self.data_rows = data_rows
            self.xlsx_data = xlsx_data
            self.ui.statistics_table.update_data(data_rows)
            self.chart_load_data(charts)
        except Exception as e:
            self.data_rows = []  
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("处理查询的统计数据出错")
        finally:
            self.loading_widget.stop()  
    def slot_get_statistics_info_error(self, *args):
        """
        查询数据失败槽函数
        """
        try:
            self.loading_widget.stop()
        except Exception as e:
            logger.error(e, exc_info=True)
        CriticalMessageBoxOne("获取统计数据失败")
    def chart_load_data(self, charts):
        """ 图表加载数据
        :param charts: [(chart1_args,chart1_kwargs),(chart2_args,chart2_kwargs)]
        """
        try:
            self.ui.q_charts.clear()
            pro_counts = len(charts[0][0][1])
            for i, chart in enumerate(charts):
                bar = BarGraph()
                bar.set_bar_width(0.025 * pro_counts)
                bar.set_bar_margin(0.005 * pro_counts)
                bar.set_bar_bgcorlor(QColor(70, 70, 70))
                bar.set_data_frame(*chart[0], **chart[1])
                self.ui.q_charts.add_widget(bar)
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("绘制图表出错")
    def resizeEvent(self, event: QResizeEvent):
        """ 调整大小事件 """
        super().resizeEvent(event)
        self.loading_widget.resize(self.ui.tab.size())
        self.loading_widget.move(self.ui.tab.pos())
    def convert_qdate_to_datetime(self, qdate: QDate):
        """ 将日期文本转换成
        :param qdate: QDate
        """
        date_str = datetime.strftime(qdate.toPyDateTime(), '%Y-%m-%d %H:%M:%S')
        return date_str
class UI_ErrorOmissionStatistics(object):
    def __init__(self, parent):
        styleFile = 'qss/statistics.qss'
        qss = CommonHelper.readQss(styleFile)
        parent.setStyleSheet(qss)
        parent.setWindowTitle("产品误判率和漏检率统计")
        layout = QVBoxLayout(parent)
        self.filters_pannel = FiltersPannel()
        layout.addWidget(self.filters_pannel)
        self.tab = QTabWidget()
        layout.addWidget(self.tab)  
        self.statistics_table = DefectList()
        self.tab.addTab(self.statistics_table, "列表")
        self.q_charts = QChartFrame()
        self.tab.addTab(self.q_charts, "图表")
class FiltersPannel(QFrame):
    """ 搜索条件面板 """
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        title = QLabel("产品误判率和漏检率统计")
        title.hide()
        title.setObjectName("h1")
        layout.addWidget(title)  
        layout.addItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout2 = QGridLayout()
        self.date_group = DateGroup('起止时间:')
        layout2.addWidget(self.date_group, 0, 1, 1, 3)
        self.cb_statistics_dimension = ComboBoxGroup("统计维度:", ['生产线', '检测任务'])
        layout2.addWidget(self.cb_statistics_dimension, 0, 0)
        layout.addLayout(layout2)
        self.btn_search = IconButton(':/icons/search.png')
        layout.addWidget(self.btn_search)
        self.btn_download = IconButton(':/icons/download.png')
        layout.addWidget(self.btn_download)
class QChartFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.widgets = []
    def add_widget(self, widget):
        try:
            self.widgets.append(widget)
            self.layout.addWidget(widget)
        except Exception as e:
            logger.error(e, exc_info=True)
    def clear(self):
        """ 清除数据 """
        for widget in self.widgets:
            self.layout.removeWidget(widget)
        self.widgets = []
class DefectList(QTableWidget):
    def __init__(self, *args):
        super().__init__(*args)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setHighlightSections(False)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)  
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)  
        self.setAlternatingRowColors(True)  
        self.verticalHeader().setHidden(True)  
        headers = ['序号', '产品类型', '生产线', '检测点', '产品数量', 'AI合格数量', 'AI缺陷数量', '复检缺陷数量', '人工合格数', '差异数量',
                   '误判数量', '误判率', '漏检数量', '漏检率', '准确率']
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        self.data = []
        self.set_column_width(0, 80)
    def set_column_width(self, index, width):
        """ 指定列宽 """
        self.horizontalHeader().setSectionResizeMode(index, QHeaderView.Custom)
        self.setColumnWidth(index, width)
    def update_data(self, rows_data):
        """ 更新数据 """
        self.setRowCount(len(rows_data))
        self.data = []
        for i, row_data in enumerate(rows_data):
            row_data.insert(0, i + 1)
            row_data = row_data[:-1]
            self.data.append(row_data)
            for col, data in enumerate(row_data):
                q_table_item = QTableWidgetItem()
                q_table_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                q_table_item.setText(str(data))
                self.setItem(i, col, q_table_item)
class UI_ProductStatistic(object):
    """产品统计UI"""
    def __init__(self, parent):
        layout = QVBoxLayout(parent)
        self.h_layout_1 = QHBoxLayout()
        self.h_layout_1.setContentsMargins(0, 0, 0, 0)
        self.product_statistic_label = QLabel()
        self.product_statistic_label.setObjectName("product_statistic_label")
        self.product_statistic_label.setText("缺陷率和报废率统计")
        self.product_statistic_label.hide()
        self.h_layout_1.addWidget(self.product_statistic_label)
        self.spacer_1 = QSpacerItem(30, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.h_layout_1.addItem(self.spacer_1)
        self.statistic_condition = StatisticCondition(parent=parent)
        self.statistic_condition.setObjectName("statistic_condition")
        self.h_layout_1.addWidget(self.statistic_condition)
        self.spacer_2 = QSpacerItem(30, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.h_layout_1.addItem(self.spacer_2)
        self.statistic_btn = IconButton(':/icons/search.png')
        self.h_layout_1.addWidget(self.statistic_btn)
        self.download_btn = IconButton(':/icons/download.png')
        self.h_layout_1.addWidget(self.download_btn)
        layout.addLayout(self.h_layout_1)
        self.product_statistic_tab = ProductStatisticTab(parent=parent)  
        self.product_statistic_tab.setObjectName("product_statistic_tab")
        layout.addWidget(self.product_statistic_tab)
"""====================================="""
"""            产品统计-总控件             """
"""====================================="""
class ProductStatistic(QWidget):
    """产品统计-总控件"""
    def __init__(self, main_window, *args, parent=None, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.ui = UI_ProductStatistic(self)
        self.show()  
        self.setWindowIcon(QIcon(':/icons/title.png'))
        style_file = 'qss/statistics.qss'
        self.qss_style = CommonHelper.readQss(style_file)  
        self.main_window = main_window
        self.product_statistic_thread = ProductStatisticThread()  
        self.loading_widget = LoadingWidget(":/icons/loading.gif", parent=self)
        if self.main_window.get_system_func("defect_baofei_statistic_download") is False:
            self.ui.download_btn.setEnabled(False)
        self.setStyleSheet(self.qss_style)  
        self.progress_bar = ProgressBarWindow(value_show=False)  
        self.start_time_for_excel = ""  
        self.end_time_for_excel = ""  
        self.ui.statistic_btn.clicked.connect(self.statistic_btn_clicked_handler)
        self.ui.download_btn.clicked.connect(self.download_btn_clicked_handler)
        self.ui.statistic_condition.statistic_dimension.statistic_dimension_changed_signal.connect(
            self.ui.product_statistic_tab.product_table.set_h_header
        )
        self.product_statistic_thread.err_msg_signal.connect(self.thread_err_msg_signal_handler)  
        self.product_statistic_thread.statistic_result_signal.connect(self.update_statistic_data_handler)  
    def statistic_btn_clicked_handler(self):
        """统计按钮-点击事件"""
        try:
            if self.loading_widget.is_loading:
                InformationMessageBoxOne("查询统计完成之后，才可再次查询")
                return
            self.loading_widget.start()
            q_date_start = self.ui.statistic_condition.date_span.start_date.date.toPyDateTime()
            q_date_end = self.ui.statistic_condition.date_span.end_date.date.toPyDateTime()
            date_start = q_date_start.strftime('%Y-%m-%d %H:%M:%S')
            date_end = q_date_end.strftime('%Y-%m-%d %H:%M:%S')
            self.current_dimission = self.ui.statistic_condition.statistic_dimension.combo_box.currentText()
            self.ui.product_statistic_tab.product_table.setHorizontalHeaderItem(2, QTableWidgetItem(
                self.current_dimission))
            self.start_time_for_excel = self.ui.statistic_condition.date_span.start_date.date.toString(
                Qt.ISODate).replace('T', ' ')
            self.end_time_for_excel = self.ui.statistic_condition.date_span.end_date.date.toString(Qt.ISODate).replace(
                'T', ' ')
            user_info_dict = self.main_window.user
            user_id = user_info_dict['id']
            role_type = user_info_dict['role_type']
            if not self.product_statistic_thread.isRunning():
                self.product_statistic_thread.init_data(
                    statistic_dimension=self.ui.statistic_condition.statistic_dimension.combo_box.currentIndex(),
                    inference_mode=self.ui.statistic_condition.inference_mode.combo_box.currentIndex(),
                    start_date=date_start,
                    end_date=date_end,
                    user_id=user_id,
                    role_type=role_type
                )
                self.product_statistic_thread.start()
        except Exception as e:
            logger.error(f"Error:{e}", exc_info=True)
            WarningMessageBoxOne(str(e))
    @pyqtSlot(dict)
    def update_statistic_data_handler(self, data_dict):
        """更新产品统计列表&图表"""
        try:
            if data_dict:
                self.ui.product_statistic_tab.product_table.insert_rows(list(data_dict.values()), refresh_all=True)
                data, categories = self.ui.product_statistic_tab.product_table.organize_chart_data()
                value_range = [0, 100]
                self.ui.product_statistic_tab.product_chart.clear_data()
                self.ui.product_statistic_tab.product_chart.set_data(data, categories, value_range)
            else:
                self.ui.product_statistic_tab.product_table.insert_rows(list(), refresh_all=True)
                self.ui.product_statistic_tab.product_chart.clear_data()
                self.ui.product_statistic_tab.product_chart.set_default_bar_set()
        except Exception as e:
            logger.error(f"Error:{e}", exc_info=True)
            WarningMessageBoxOne(str(e))
        finally:
            self.loading_widget.stop()
    def download_btn_clicked_handler(self):
        """下载按钮-点击事件"""
        try:
            if not self.main_window.get_system_func('defect_baofei_statistic_download'):
                return InformationMessageBoxOne("暂无权限下载，请联系管理员")
            if self.loading_widget.is_loading:
                InformationMessageBoxOne("正在查询数据，请稍后下载")
                return
            if self.ui.product_statistic_tab.product_table.rowCount() > 0:
                file_name = f"产品缺陷率和报废率统计表_{datetime.now().strftime('%Y%m%d')}.xlsx"
                file_path = gen_xlsx_path(file_name, "产品缺陷率和报废率统计表")
                if not file_path:
                    return
                self.download_excel(file_path)
            else:
                InformationMessageBoxOne(f"没有数据可以下载")
        except FileCreateError as e:
            msg = f"当前下载路径无法写入数据，请尝试下载到其他目录"
            logger.error(f"{e}:{msg}", exc_info=True)
            WarningMessageBoxOne(msg)
        except Exception as e:
            logger.error(f"Error:{e}", exc_info=True)
            WarningMessageBoxOne(str(e))
    def download_excel(self, file_path):
        """ 下载 excel 数据 """
        self.progress_bar.set_title("正在下载 %s" % os.path.basename(file_path))
        self.progress_bar.show()
        sheets = []
        formats = {
            "format": {
                'align': 'center',  
                'valign': 'vcenter',  
                'font_size': '12',  
                'border': 1  
            },
            "box_format": {
                'align': 'center',  
                'valign': 'vcenter',  
                'font_size': '12',  
                'fg_color': '
                'top': 1  
            },
            "bg_format": {
                'align': 'center',  
                'valign': 'vcenter',  
                'font_size': '12',  
                'fg_color': '
            },
            "bg_format_border": {
                'align': 'center',  
                'valign': 'vcenter',  
                'font_size': '12',  
                'fg_color': '
                'border': 1  
            }
        }
        options = {
            "height": [(0, 31)]
        }
        sheet1 = [
            "缺陷率和报废率统计报表",
            {
                "A1:K1": {
                    "value": "缺陷率和报废率统计报表",
                    "format": "bg_format",
                    "merge": True,
                },
                "A2:G2": {
                    "value": None,
                    "format": "box_format",
                },
                "H2": {
                    "value": '时间范围：',
                    "format": "box_format",
                },
                "I2:K2": {
                    "value": f"{self.start_time_for_excel} 至 {self.end_time_for_excel}",
                    "format": "box_format",
                    "merge": True,
                },
            },
            formats,
            options
        ]
        data_1_col_num = self.ui.product_statistic_tab.product_table.columnCount()
        for i in range(data_1_col_num):
            header = self.ui.product_statistic_tab.product_table.model().headerData(i, Qt.Horizontal, Qt.DisplayRole)
            sheet1[1].update({(2, i): {"value": header, "format": "bg_format_border"}})
        data_rows_1 = self.ui.product_statistic_tab.product_table.get_all_rows_data()
        data_start_index = 3
        for r, row in enumerate(data_rows_1):
            for c, cell in enumerate(row):
                sheet1[1].update({(r + data_start_index, c): {"value": cell, "format": "format"}})
        sheets.append(sheet1)
        download_th = AsyncDownload(file_path, sheets, self)
        download_th.signal_result.connect(self.slot_download_success)
        download_th.signal_result_error.connect(self.slot_download_error)
        download_th.start()
    def slot_download_success(self, data):
        """
        下载成功槽函数
        :param data:
        :return:
        """
        if self.progress_bar:
            self.progress_bar.close()
        InformationMessageBoxOne("下载完成")
    def slot_download_error(self, data):
        """
        下载失败槽函数
        :param data:
        :return:
        """
        if self.progress_bar:
            self.progress_bar.close()
        try:
            raise data.get("error")
        except InvalidWorksheetName as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne(f"工作表包含不允许的字符")
        except FileCreateError as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne(f"下载产品误判率和漏检率统计数据出错, 该文件处于使用状态")
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("下载产品误判率和漏检率统计数据出错")
    @pyqtSlot(str)
    def thread_err_msg_signal_handler(self, msg):
        """线程中的错误信息-处理"""
        self.loading_widget.stop()
        WarningMessageBoxOne(msg)
    def resizeEvent(self, event: QResizeEvent):
        """ 调整大小事件 """
        super().resizeEvent(event)
        self.loading_widget.resize(self.ui.product_statistic_tab.size())
        self.loading_widget.move(self.ui.product_statistic_tab.pos())
"""====================================="""
"""            产品统计-子控件             """
"""====================================="""
class StatisticCondition(QWidget):
    """统计条件控件"""
    def __init__(self, *args, parent=None, **kwargs):
        super().__init__(parent, *args, **kwargs)
        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.date_span = DateGroup("起止时间:")
        layout.addWidget(self.date_span, 0, 0, 1, 3)
        self.inference_mode = InferenceMode(self)
        layout.addWidget(self.inference_mode, 1, 0, Qt.AlignLeft)
        self.statistic_dimension = StatisticDimension(self)
        layout.addWidget(self.statistic_dimension, 1, 1, 1, 2, Qt.AlignLeft)
    def init_data(self):
        """初始化数据"""
        pass
class InferenceMode(QWidget):
    """检测方式控件"""
    def __init__(self, parent, *args):
        super().__init__(parent, *args)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self._combo_box_old_index = ProductStatisticDimension.pro_name.value
        self.label = QLabel()
        self.label.setText("检测方式:")
        layout.addWidget(self.label)
        self.combo_box = QComboBox(parent=parent)
        layout.addWidget(self.combo_box)
        self.init_data()
    def init_data(self):
        """初始化数据"""
        for inference_mode in ProductInferenceMode:
            self.combo_box.addItem("")
            self.combo_box.setItemText(inference_mode.value,
                                       ProductInferenceMode.value_name(inference_mode.value))
        self.combo_box.setCurrentIndex(ProductInferenceMode.ai.value)
    def combo_box_currentIndexChanged_handler(self, index):
        """index改变"""
        if index == ProductInferenceMode.manual.value:
            self.combo_box.setCurrentIndex(self._combo_box_old_index)
            InformationMessageBoxOne(f'按【{ProductInferenceMode.value_name(index)}】统计暂未实现，需对接控制台')
        else:
            self._combo_box_old_index = index
class StatisticDimension(QWidget):
    """统计维度控件"""
    statistic_dimension_changed_signal = pyqtSignal(str)
    def __init__(self, parent, *args):
        super().__init__(parent, *args)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self._combo_box_old_index = ProductStatisticDimension.pro_name.value
        self.label = QLabel()
        self.label.setText("统计维度:")
        layout.addWidget(self.label)
        self.combo_box = QComboBox(parent=self)
        self.combo_box.addItems(['生产线', '产品型号', '检测点'])
        layout.addWidget(self.combo_box)
        self.combo_box.currentIndexChanged.connect(self.combo_box_currentIndexChanged_handler)
        self.init_data()
    def init_data(self):
        """初始化数据"""
        pass
    def combo_box_currentIndexChanged_handler(self, index):
        """index改变"""
        pass
class ProductStatisticTab(QTabWidget):
    """产品统计tab"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.table_tab = QWidget()  
        layout_table_tab = QVBoxLayout(self.table_tab)
        layout_table_tab.setContentsMargins(0, 0, 0, 0)
        layout_table_tab.setSpacing(0)
        self.product_table = ProductStatisticTable(parent=parent)
        self.product_table.setObjectName("product_table")
        layout_table_tab.addWidget(self.product_table)
        self.addTab(self.table_tab, "列表")
        self.chart_tab = QWidget()  
        layout_chart_tab = QVBoxLayout(self.chart_tab)
        layout_chart_tab.setContentsMargins(0, 0, 0, 0)
        layout_chart_tab.setSpacing(0)
        self.product_chart = ProductStatisticChart(parent=parent, default_bar_ls=["缺陷率", "报废率"])
        self.product_chart.setObjectName("product_chart")
        layout_chart_tab.addWidget(self.product_chart)
        self.addTab(self.chart_tab, "图表")
class ProductStatisticTable(QTableWidget):
    """产品统计列表"""
    def __init__(self, *args, parent=None):
        super().__init__(parent, *args)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  
        self.horizontalHeader().setHighlightSections(False)
        self.verticalHeader().setHidden(True)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setAlternatingRowColors(True)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  
        self.h_head_dict = {
            "pro_name": ["序号", "产品类型", "产品型号", "检测方式", "产品数量", "合格数量",
                         "维修数量", "维修率", "报废数量", "报废率", "成品率"],
            "production_line": ["序号", "生产线", "产品型号", "检测方式", "产品数量", "合格数量",
                                "维修数量", "维修率", "报废数量", "报废率", "成品率"],
        }
        self.set_h_header("pro_name")
    def set_h_header(self, h_head_key: str):
        """设置水平表头"""
        h_head = self.h_head_dict.get(h_head_key, None)
        if h_head:
            self.setMinimumSize(1000, 500)
            self.setColumnCount(len(h_head))
            self.setObjectName("task_table_widget")
            self.setHorizontalHeaderLabels(h_head)
    def insert_one_row(self, data: dict, row: int):
        """
        在指定行插入一条新产品
        :param data: 数据
        :param row: 要插入的行号
        :return:
        """
        try:
            serial_number = self.rowCount() + 1
            self.insertRow(row)
            """各列数据"""
            Item = QTableWidgetItem(str(serial_number))
            Item.setTextAlignment(Qt.AlignVCenter | Qt.AlignCenter)
            self.setItem(row, 0, Item)
            text = f'{ProType.value_name(data["pro_type"])}'
            Item = QTableWidgetItem(text)
            Item.setTextAlignment(Qt.AlignVCenter | Qt.AlignCenter)
            self.setItem(row, 1, Item)
            text = str(data["pro_statistic_dimension"])
            Item = QTableWidgetItem(text)
            Item.setTextAlignment(Qt.AlignVCenter | Qt.AlignCenter)
            self.setItem(row, 2, Item)
            text = str(ProductInferenceMode.value_name(data["inference_mode"]))
            Item = QTableWidgetItem(text)
            Item.setTextAlignment(Qt.AlignVCenter | Qt.AlignCenter)
            self.setItem(row, 3, Item)
            text = str(data["pro_count"])
            Item = QTableWidgetItem(text)
            Item.setTextAlignment(Qt.AlignVCenter | Qt.AlignCenter)
            self.setItem(row, 4, Item)
            text = str(data["qualification_count"])
            Item = QTableWidgetItem(text)
            Item.setTextAlignment(Qt.AlignVCenter | Qt.AlignCenter)
            self.setItem(row, 5, Item)
            text = str(data["maintenance_count"])
            Item = QTableWidgetItem(text)
            Item.setTextAlignment(Qt.AlignVCenter | Qt.AlignCenter)
            self.setItem(row, 6, Item)
            text = str(data["maintenance_ratio"])
            Item = QTableWidgetItem(text)
            Item.setTextAlignment(Qt.AlignVCenter | Qt.AlignCenter)
            Item.setToolTip(text)
            self.setItem(row, 7, Item)
            text = str(data["scrap_count"])
            Item = QTableWidgetItem(text)
            Item.setTextAlignment(Qt.AlignVCenter | Qt.AlignCenter)
            self.setItem(row, 8, Item)
            text = str(data["scrap_ratio"])
            Item = QTableWidgetItem(text)
            Item.setTextAlignment(Qt.AlignVCenter | Qt.AlignCenter)
            self.setItem(row, 9, Item)
            text = str(data["finished_ratio"])
            Item = QTableWidgetItem(text)
            Item.setTextAlignment(Qt.AlignVCenter | Qt.AlignCenter)
            self.setItem(row, 10, Item)
            self._set_column_width()
        except Exception as e:
            logger.error(f"Error:{e}", exc_info=True)
            WarningMessageBoxOne(str(e))
    def insert_rows(self, rows_data, refresh_all=True):
        """
        添加行
        :param rows_data:
        :param refresh_all: 刷新全部数据,rows_data传全部要显示的数据
        :return:
        """
        try:
            if refresh_all:
                self.clearContents()
                self.setRowCount(0)
            existed_rows = self.rowCount()  
            rows_data.sort(key=lambda x: x.get('pro_statistic_dimension'))
            for i, data in enumerate(rows_data):
                row = existed_rows + i
                self.insert_one_row(data, row)
            self._set_column_width()
        except Exception as e:
            logger.error(f"Error:{e}", exc_info=True)
            WarningMessageBoxOne(str(e))
    def _set_column_width(self):
        """设置列宽度"""
        if self.rowCount() > 0:
            self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)  
    def organize_chart_data(self):
        """组织统计分析图表数据"""
        statistic_data = {
            "缺陷率": list(),
            "报废率": list(),
        }
        categories = list()
        for row in range(self.rowCount()):
            category_item = self.item(row, 2)
            categories.append(category_item.text())
            maintenance_ratio_item = self.item(row, 7)
            statistic_data["缺陷率"].append(float(maintenance_ratio_item.text()[:-1]))
            scrap_ratio_item = self.item(row, 9)
            statistic_data["报废率"].append(float(scrap_ratio_item.text()[:-1]))
        return statistic_data, categories
    def get_h_header_ls(self) -> list:
        """获取水平表头列表"""
        try:
            return [self.horizontalHeaderItem(column).text() for column in range(self.columnCount())]
        except Exception as e:
            logger.error(f"Error:{e}", exc_info=True)
            WarningMessageBoxOne(str(e))
    def get_all_rows_data(self) -> [[], ...]:
        try:
            rows_data = list()
            for row in range(self.rowCount()):
                one_row_data = list()
                for column in range(self.columnCount()):
                    one_row_data.append(f'{self.item(row, column).text()}')
                rows_data.append(one_row_data)
            return rows_data
        except Exception as e:
            logger.error(f"Error:{e}", exc_info=True)
            WarningMessageBoxOne(str(e))
class ProductStatisticChart(QChartView):
    """产品统计图表"""
    def __init__(self, parent=None, default_bar_ls: [str, ...] = None):
        """
        :param parent:
        :param default_bar_ls: 默认的bar
        """
        super().__init__(parent)
        self.series = QBarSeries()
        self.series.setLabelsPosition(QAbstractBarSeries.LabelsCenter)  
        self.series.setLabelsVisible(True)  
        self.series.setLabelsPosition(QAbstractBarSeries.LabelsInsideBase)
        self.chart = QChart()
        self.chart.addSeries(self.series)
        self.chart.setTitle("产品缺陷率和报废率分布（%）")
        self.chart.setAnimationOptions(QChart.SeriesAnimations)  
        self.axis_x = QBarCategoryAxis()
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.series.attachAxis(self.axis_x)
        self.axis_y = QValueAxis()
        self.axis_y.setLabelFormat("%.2f")
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)
        self.series.attachAxis(self.axis_y)
        self.set_axis_y([0, 100])
        self.default_bar_ls = default_bar_ls
        if self.default_bar_ls:
            self.set_default_bar_set()
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)
        self.setChart(self.chart)
        self.setRenderHint(QPainter.Antialiasing)
    def set_data(self, bar_set_date: dict, categories: list, value_range: list):
        """设置图表数据"""
        self.set_axis_x(categories)
        self.set_name_and_value_of_bars(bar_set_date)
        self.set_axis_y(value_range)
    def clear_data(self):
        """清空数据"""
        self.series.clear()
        self.axis_x.setGridLineVisible(False)
        self.axis_x.clear()
        self.chart.removeAxis(self.axis_x)
        self.axis_x = QBarCategoryAxis()
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.series.attachAxis(self.axis_x)
    def set_axis_x(self, categories: list):
        """
        设置x轴（统计维度）
        :param categories: 不同x值的列表
        :return:
        """
        if categories:
            self.axis_x.append(categories)
    def set_axis_y(self, value_range: list):
        """
        设置y轴范围
        :param value_range: y轴范围
        :return:
        """
        if value_range:
            self.axis_y.setRange(*value_range)
    def set_default_bar_set(self):
        """界面初始化或数据为空时:设置默认的bar"""
        for name in self.default_bar_ls:
            q_bar_set = QBarSet("")
            q_bar_set.setLabel(name)
            q_bar_set.init_color = q_bar_set.color()
            self.series.append(q_bar_set)
    def set_name_and_value_of_bars(self, bar_set_date: dict):
        """
        设置要统计的字段名（如：'报废率'，'缺陷率', ...）,及其对应的数据
        :param bar_set_date:
            举例：
                {
                    "报废率": [10, 20, 30], 
                    "缺陷率": [40, 50, 60], 
                }
        :return:
        """
        try:
            if bar_set_date:
                for name, date in bar_set_date.items():
                    q_bar_set = QBarSet("")
                    q_bar_set.setLabelColor(QColor(0, 0, 0))
                    q_bar_set.setLabel(name)
                    q_bar_set.append(date)
                    q_bar_set.init_color = q_bar_set.color()
                    self.series.append(q_bar_set)
                if self.series.count():
                    width = 1 / self.series.count()
                    max_width = 0.1 * self.series.count()
                    min_width = 0.1 * self.series.count()
                    if width > max_width:
                        width = max_width
                    if width < min_width:
                        width = min_width
                    self.series.setBarWidth(width)
        except Exception as e:
            logger.error(f"Error:{e}", exc_info=True)
            WarningMessageBoxOne(str(e))
    def q_bar_set_hovered_handler(self, q_bar_set: QBarSet, status: bool, index: int):
        """鼠标移到QBarSet上-事件处理"""
        if status:
            color_1 = QColor()
            color_1.setRgb(255, 0, 0, 255)
            q_bar_set.setColor(color_1)
        else:
            q_bar_set.setColor(q_bar_set.init_color)
class PathSelectionDialog(QFileDialog):
    """文件夹路径选择"""
    def __init__(self, *args, parent=None):
        super().__init__(parent, *args)
"""================ 异步请求-线程  ================"""
class ProductStatisticThread(QThread):
    """异步查询产品数据并计算统计数据-线程"""
    err_msg_signal = pyqtSignal(str)  
    statistic_result_signal = pyqtSignal(dict)  
    def __init__(self, *args):
        super().__init__(*args)
        self.statistic_dimension = None
        self.inference_mode = None
        self.start_date = None
        self.end_date = None
    def init_data(self, statistic_dimension: int, inference_mode: int, start_date: datetime, end_date: datetime,
                  user_id, role_type):
        """初始化数据"""
        self.statistic_dimension = statistic_dimension
        self.inference_mode = inference_mode
        self.start_date = start_date
        self.end_date = end_date
        self.user_id = user_id
        self.role_type = role_type
    def run(self):
        try:
            data_dict: dict = defectAndScrap().retrieve(
                self.statistic_dimension,
                self.inference_mode,
                self.start_date,
                self.end_date,
                self.user_id,
                self.role_type
            )
            self.statistic_result_signal.emit(data_dict)
        except Exception as e:
            logger.error(f'Error={e}', exc_info=True)
            self.err_msg_signal.emit(str(e))
class Shared(QObject):
    """
    连接web页面管道类
    """
    signal_query_begin = pyqtSignal()  
    signal_success = pyqtSignal(str)  
    signal_error = pyqtSignal(str)  
    signal_data_success = pyqtSignal(str)  
    signal_data_error = pyqtSignal(str)  
    def __init__(self, parent=None):
        super(Shared, self).__init__(parent=parent)
        self.data = []  
        self.th = None
    @pyqtSlot(str, str, str)
    def retrive_defect_labels(self, task_id, start_time, end_time):
        """
        异步获取缺陷数据
        :param task_id: 任务ID
        :param start_time: 开始时间字符串 Y-m-d H:M:S
        :param end_time:  结束时间字符串 Y-m-d H:M:S
        :return:
        """
        self.th = AsynThread(defectTask().retrieve, args=(task_id, start_time, end_time), parent=self)
        self.th.signal_result.connect(self.slot_data_success)
        self.th.signal_result_error.connect(self.slot_data_error)
        self.th.start()
    def slot_data_success(self, data):
        """
        获取数据成功槽函数
        :param data:
        :return:
        """
        data, records = data
        self.data = records
        self.signal_data_success.emit(json.dumps(data, ensure_ascii=False))
    def slot_data_error(self):
        """
        获取数据失败槽函数
        :return:
        """
        self.signal_data_error.emit('获取缺陷数据失败')
class DefectTaskStatistics(QWidget):
    def __init__(self, main_window, *args, **kwargs):
        super(DefectTaskStatistics, self).__init__()
        self.main_window = main_window
        styleFile = 'qss/statistics.qss'
        qss = CommonHelper.readQss(styleFile)
        self.setStyleSheet(qss)
        self.vbox = QVBoxLayout(self)
        self.filter_box = QHBoxLayout()
        self.progress_bar = ProgressBarWindow(value_show=False)  
        self.shared = Shared(self)
        self.search_input = None  
        self.start_time_input = None  
        self.end_time_input = None  
        self.search_btn = None  
        self.download_btn = None  
        self.browser = None  
        self.channel = None  
        self.init_ui()  
        self.init_event()  
        self.load_web_page()  
        self.init_channel()  
    def init_ui(self):
        """
        初始化样式
        :return:
        """
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('请输入任务名称或编码')
        self.search_input.setFixedSize(178, 23)
        self.date_group = DateGroup('缺陷时间:')
        self.start_time_input = self.date_group.start_date
        self.end_time_input = self.date_group.end_date
        self.date_group.comboBox.hide()
        self.search_btn = IconButton(':/icons/search.png')
        self.download_btn = IconButton(':/icons/download.png')
        self.filter_box.addItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.filter_box.addWidget(self.search_input)
        self.filter_box.addWidget(self.date_group)
        self.filter_box.addWidget(self.search_btn)
        self.filter_box.addWidget(self.download_btn)
        self.browser = QWebEngineView()
        self.browser.setContextMenuPolicy(Qt.NoContextMenu)
        self.vbox.addLayout(self.filter_box)
        self.vbox.addWidget(self.browser)
    def init_event(self):
        """
        初始化信号事件连接
        :return:
        """
        self.search_input.returnPressed.connect(self.req_statistics_info)  
        self.search_btn.clicked.connect(self.req_statistics_info)  
        self.download_btn.clicked.connect(self.slot_download)  
    def init_channel(self):
        """
        初始化web页面管道
        :return:
        """
        self.channel = QWebChannel()
        self.channel.registerObject("shared", self.shared)
        self.browser.page().setWebChannel(self.channel)
    def load_web_page(self):
        try:
            url = QUrl(QFileInfo('dashboard/compiler/detect-category.html').absoluteFilePath())
            self.browser.load(url)
        except Exception as e:
            WarningMessageBox("加载任务缺陷页面失败")
    def req_statistics_info(self):
        """
        搜索按钮槽函数
        :return:
        """
        self.shared.signal_query_begin.emit()
        self.key_word = self.search_input.text()
        self.start_time = self.start_time_input.date.toPyDateTime().strftime("%Y-%m-%d %H:%M:%S")
        self.end_time = self.end_time_input.date.toPyDateTime().strftime("%Y-%m-%d %H:%M:%S")
        user_info_dict = self.main_window.user
        user_id = user_info_dict['id']
        role_type = user_info_dict['role_type']
        self.th = AsynThread(defectTask().retrieve_tasks,
                             args=(self.key_word, self.start_time, self.end_time, user_id, role_type),
                             parent=self)
        self.th.signal_result.connect(self.slot_get_statistics_info)
        self.th.signal_result_error.connect(self.slot_get_statistics_info_error)
        self.th.start()
    def slot_get_statistics_info(self, data):
        """
        获取任务列表并向web管道中存入json字符串
        :param data:
        :return:
        """
        self.shared.signal_success.emit(json.dumps(data, ensure_ascii=False))
    def slot_get_statistics_info_error(self):
        """
        获取任务列表失败
        :return:
        """
        self.shared.signal_error.emit('请求任务数据失败')
    def slot_download(self):
        """
        下载excel
        :return:
        """
        if not self.main_window.get_system_func('defect_product_task_download'):
            return InformationMessageBoxOne("暂无权限下载，请联系管理员")
        if len(self.shared.data) == 0:
            return InformationMessageBoxOne("没有数据可供下载，请先查询")
        if self.shared.th.isRunning():
            return InformationMessageBoxOne("正在查询数据，请稍后下载")
        sheets = []
        task_name, data = self.gen_download_data()
        file_name = f"""任务缺陷统计报表_{datetime.now().strftime('%Y%m%d')}.xlsx"""
        file_path = gen_xlsx_path(file_name, "下载任务缺陷统计报表")
        if not file_path:
            return
        self.progress_bar.set_title("正在下载 %s" % file_name)  
        self.progress_bar.show()
        formats = {
            "format": {
                'align': 'center',  
                'valign': 'vcenter',  
                'font_size': '12',  
                'border': 1  
            },
            "box_format": {
                'align': 'center',  
                'valign': 'vcenter',  
                'font_size': '12',  
                'fg_color': '
                'top': 1  
            },
            "bg_format": {
                'align': 'center',  
                'valign': 'vcenter',  
                'font_size': '12',  
                'fg_color': '
            },
            "bg_format_border": {
                'align': 'center',  
                'valign': 'vcenter',  
                'font_size': '12',  
                'fg_color': '
                'border': 1  
            }
        }
        options = {
            "height": [(0, 31)]
        }
        title = f"""检测任务统计表_{task_name}_{self.start_time} 至 {self.end_time}"""
        sheet = [
            "检测任务统计报表",
            {
                "A1:G1": {
                    "value": title,
                    "format": "bg_format",
                    "merge": True,
                }
            },
            formats,
            options
        ]
        headers = ['序号', '生产线', '产品型号', '检测点', '缺陷小类', '缺陷位置', '缺陷时间']
        for i in range(len(headers)):
            sheet[1].update({(1, i): {"value": headers[i], "format": "bg_format_border"}})
        data_start_index = 1
        for r, row in enumerate(data):
            for c, cell in enumerate(row):
                sheet[1].update({(r + data_start_index + 1, c): {"value": str(cell), "format": "format"}})
        sheets.append(sheet)
        download_th = AsyncDownload(file_path, sheets, self)  
        download_th.signal_result.connect(self.slot_download_success)
        download_th.signal_result_error.connect(self.slot_download_error)
        download_th.start()
    def slot_download_success(self, data):
        """
        下载成功槽函数
        :param data:
        :return:
        """
        if self.progress_bar:
            self.progress_bar.close()
        InformationMessageBoxOne("下载完成")
    def slot_download_error(self, data):
        """
        下载失败槽函数
        :param data:
        :return:
        """
        if self.progress_bar:
            self.progress_bar.close()
        try:
            raise data.get("error")
        except InvalidWorksheetName as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne(f"工作表包含不允许的字符")
        except FileCreateError as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne(f"下载缺陷位置分布统计报表出错, 该文件处于使用状态")
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("下载缺陷位置分布统计报表出错")
    def gen_download_data(self):
        """
        组装下载的数据
        :return: 任务名，数据
        """
        res = []
        task_name = self.shared.data[1]
        try:
            gg_enum = DictInfoCRUD.get_all_gg_enum(True)  
            for index, item in enumerate(self.shared.data[0]):
                if item.IS_AUTO == 0:
                    lab_class_name = item.MANUAL_LAB_CLASS
                else:
                    lab_class_name = item.DL_LAB_CLASS
                if not lab_class_name:
                    continue
                try:
                    create_time = item.CREATE_TIME.strftime('%Y-%m-%d %H:%M:%S')
                except:
                    create_time = ""
                labels = lab_class_name.split(";")
                for label in labels:
                    tmp = label.split('|')
                    if len(tmp) != 3:
                        continue
                    label_name = tmp[1]
                    position = tmp[2]
                    res.append(
                        [
                            item.PRO_LINE_NAME,
                            gg_enum.get(item.GG),
                            DetectSite.value_name(item.DETECT_SITE),
                            label_name,
                            self.gen_pos_to_str(position), create_time
                        ]
                    )
            res.sort(key=lambda x: x[3])
            for index, item in enumerate(res):
                item.insert(0, index + 1)
            return task_name, res
        except Exception as e:
            logger.error(e, exc_info=True)
        return '', []
    @staticmethod
    def gen_pos_to_str(pos):
        """
        将缺陷位置列表转换为字符串
        :param pos:
        :return:
        """
        try:
            pos = eval(pos)
            tmp = np.array(pos)
            if tmp.ndim > 1:  
                tmp_list = []
                for item in pos:
                    tmp_list.append(chr(item[0] + 64) + str(item[1]))
                res = ','.join(tmp_list)
            else:
                res = chr(pos[0] + 64) + str(pos[1])
        except Exception as e:
            print(e)
            res = ''
        return res
class DefectCategoryStatistics(QWidget):
    def __init__(self, main_window, *args, **kwargs):
        """
        :param main_window: 主窗口对象，里面有要用的鉴权的功能
        """
        super().__init__(*args, **kwargs)
        self.main_window = main_window
        self.cruds = defectCategory()
        self.ui = UI_DefectCategoryStatistics(self)
        self.cb_detect_type = self.ui.filters_pannel.cb_detect_type.comboBox
        self.cb_defect_big_class = self.ui.filters_pannel.cb_defect_big_class.comboBox
        self.start_date = self.ui.filters_pannel.date_group.start_date
        self.end_date = self.ui.filters_pannel.date_group.end_date
        self.cb_date_selections = self.ui.filters_pannel.date_group.comboBox
        self.cb_defect_type = self.ui.filters_pannel.cb_defect_type.comboBox
        self.cb_statistics_dimension = self.ui.filters_pannel.cb_statistics_dimension
        self.btn_search = self.ui.filters_pannel.btn_search
        self.btn_download = self.ui.filters_pannel.btn_download
        self.progress_bar = ProgressBarWindow(value_show=False)  
        self.btn_download.setEnabled(self.main_window.get_system_func("defect_type_statistic_download"))
        self.q_charts = self.ui.q_charts
        self.chart_view = self.ui.chart_view
        self.data_dict = None  
        self.data_models = None  
        self.DefectCategorySmallStatistics = DefectCategorySmallStatistics()
        self.loading_widget = LoadingWidget(":/icons/loading.gif", parent=self)
        self.echarts_js = None
        self.defect_big_class_type = None  
        self.defect_type = None  
        self.dimission_type = None
        self.start_time_for_excel = ""  
        self.end_time_for_excel = ""  
        self.defect_type_for_excel = ""  
        self.req_defect_types()  
        self.req_pro_lines_spec()
        self.bind_events()
    def bind_events(self):
        """ 绑定事件 """
        self.cb_defect_big_class.currentTextChanged.connect(self.slot_defect_type_changed)
        self.btn_search.clicked.connect(self.slot_btn_search_clicked)
        self.btn_download.clicked.connect(self.slot_btn_download_clicked)
        self.ui.statistics_table.signal_defect_class_small_btn_clicked.connect(self.slot_defect_class_small_btn_clicked)
        self.q_charts.signal_chart_frame_resize.connect(self.slot_chart_frame_resize)
    def req_defect_types(self):
        """ 获取产品缺陷类型 """
        try:
            self.cb_defect_big_class.setDisabled(True)  
            self.cb_defect_type.setDisabled(True)
            self.defect_type_th = AsynThread(self.cruds.retrieve_defect_types, parent=self)
            self.defect_type_th.signal_result.connect(self.slot_update_defect_types)
            self.defect_type_th.start()
        except Exception as e:
            logger.error(e, exc_info=True)
    def slot_update_defect_types(self, models):
        """ 更新缺陷类型的槽函数 """
        try:
            all_defect_types = list(set([model.LAB_CLASS_NAME for model in models]))
            el_defect_types = list(set([model.LAB_CLASS_NAME for model in models if model.CLASS_D_CATEGORY == 1]))
            vi_defect_types = list(set([model.LAB_CLASS_NAME for model in models if model.CLASS_D_CATEGORY == 2]))
            all_defect_types.sort()
            el_defect_types.sort()
            vi_defect_types.sort()
            all_defect_types.insert(0, "全部")
            el_defect_types.insert(0, "全部")
            vi_defect_types.insert(0, "全部")
            self.defect_type = {"全部": all_defect_types, "EL": el_defect_types, "VI": vi_defect_types}  
            current_defect_big_type = self.cb_defect_big_class.currentText()
            self.cb_defect_type.addItems(self.defect_type.get(current_defect_big_type))
        except Exception as e:
            logger.error(e)
        finally:
            self.cb_defect_big_class.setDisabled(False)  
            self.cb_defect_type.setDisabled(False)
    def init_data(self):
        """ 初始化数据 """
        self.req_statistics_info()  
    def slot_defect_type_changed(self, text):
        """
        缺陷大类切换选项
        :param text: 当前缺陷大类下拉框文本
        :return:
        """
        try:
            self.cb_defect_type.clear()
            self.cb_defect_type.addItems(self.defect_type.get(text))
        except Exception as e:
            logger.error(e, exc_info=True)
    def slot_btn_search_clicked(self):
        """ 点击搜索按钮 """
        try:
            if self.loading_widget.is_loading:
                InformationMessageBoxOne("查询统计完成之后，才可再次查询")
                return
            self.current_pro_line = self.cb_statistics_dimension.pro_lines_combox.currentText()  
            self.current_pro_spec = self.cb_statistics_dimension.pro_specs_combox.currentText()  
            self.welding = self.cb_statistics_dimension.welding_combox.currentText()  
            self.start_time_for_excel = self.start_date.text()  
            self.end_time_for_excel = self.end_date.text()  
            self.defect_type_for_excel = self.cb_defect_big_class.currentText()  
            self.ui.statistics_table.setRowCount(0)  
            self.loading_widget.start()  
            self.req_statistics_info()  
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("缺陷类型分布统计出错")
    def req_pro_lines_spec(self):
        """
        异步获取生产线及规格信息
        """
        try:
            self.pro_line_spec_th = AsynThread(self.cruds.retrieve_dimension, parent=self)
            self.pro_line_spec_th.signal_result.connect(self.slot_get_pro_lines_spec)
            self.pro_line_spec_th.signal_result_error.connect(self.slot_get_pro_lines_spec_error)
            self.pro_line_spec_th.start()
        except Exception as e:
            logger.error(str(e), exc_info=True)
    def slot_get_pro_lines_spec(self, data):
        """
        设置统计维度中的生产线和产品规格下拉框
        :param data:
        :return:
        """
        self.ui.filters_pannel.cb_statistics_dimension.set_data(data)
    def slot_get_pro_lines_spec_error(self, data):
        """
        获取产线及规格数据失败
        """
        CriticalMessageBoxOne("获取生产线及规格数据失败")
    def req_statistics_info(self):
        """ 异步请求统计信息 """
        try:
            detect_type_index = self.cb_detect_type.currentIndex()  
            start_datetime = self.convert_qdate_to_datetime(self.start_date.date)  
            end_datetime = self.convert_qdate_to_datetime(self.end_date.date)  
            defect_big_class_index = self.cb_defect_big_class.currentIndex()  
            defect_type_text = self.cb_defect_type.currentText()  
            pro_line_id, pro_spec, welding_id = self.cb_statistics_dimension.data
            user_info_dict = self.main_window.user
            user_id = user_info_dict['id']
            role_type = user_info_dict['role_type']
            if self.pro_line_spec_th.isRunning():
                InformationMessageBoxOne("正在请求生产线、规格数据，请稍后重试")
                return
            self.data_th = AsynThread(
                self.cruds.retrieve,
                args=(
                    start_datetime, end_datetime, detect_type_index, defect_big_class_index,
                    defect_type_text, pro_line_id, pro_spec, welding_id, user_id, role_type
                ),
                parent=self
            )
            self.data_th.signal_result.connect(self.slot_get_statistics_info)
            self.data_th.signal_result_error.connect(self.slot_get_statistics_info_error)
            self.data_th.start()
        except Exception as e:
            logger.error(str(e), exc_info=True)
    def slot_get_statistics_info(self, models):
        """
        组装缺陷类型分布统计表格需要的数据格式
        :param models:
        :return:
        """
        try:
            self.data_models = models
            self.ui.statistics_table.update_data(models)
            self.chart_load_data(models)
            self.req_pro_lines_spec()  
        except Exception as e:
            logger.error(e, exc_info=True)
        finally:
            self.loading_widget.stop()
    def slot_get_statistics_info_error(self):
        """
        查询数据失败槽函数
        :return:
        """
        try:
            self.loading_widget.stop()
        except Exception as e:
            logger.error(e, exc_info=True)
        CriticalMessageBoxOne("获取统计数据失败")
    def slot_btn_download_clicked(self):
        """ 点击下载按钮 """
        if not self.main_window.get_system_func('defect_type_statistic_download'):
            return InformationMessageBoxOne("暂无权限下载，请联系管理员")
        if not self.data_models:  
            InformationMessageBoxOne("没有数据可供下载，请先查询")
            return
        if self.loading_widget.is_loading:
            InformationMessageBoxOne("正在查询数据，请稍后下载")
            return
        file_name = f"串件缺陷类型分布统计报表_{datetime.now().strftime('%Y%m%d')}.xlsx"
        file_path = gen_xlsx_path(file_name, "下载串件缺陷类型分布统计报表")
        if not file_path:
            return
        self.download_excel(file_path)
    def download_excel(self, file_path):
        """ 下载 excel 数据 """
        self.progress_bar.set_title("正在下载 %s" % os.path.basename(file_path))
        self.progress_bar.show()
        sheets = []
        formats = {
            "format": {
                'align': 'center',  
                'valign': 'vcenter',  
                'font_size': '12',  
                'border': 1  
            },
            "box_format": {
                'align': 'center',  
                'valign': 'vcenter',  
                'font_size': '12',  
                'fg_color': '
                'top': 1  
            },
            "bg_format": {
                'align': 'center',  
                'valign': 'vcenter',  
                'font_size': '12',  
                'fg_color': '
            },
            "bg_format_border": {
                'align': 'center',  
                'valign': 'vcenter',  
                'font_size': '12',  
                'fg_color': '
                'border': 1  
            }
        }
        options = {
            "height": [(0, 31)]
        }
        sheet1 = [
            "缺陷大类分布统计报表",
            {
                "A1:L1": {
                    "value": "缺陷类型分布统计报表",
                    "format": "bg_format",
                    "merge": True,
                },
                "A2:E2": {
                    "value": None,
                    "format": "box_format",
                },
                "F2": {
                    "value": '缺陷大类：',
                    "format": "box_format",
                },
                "G2": {
                    "value": self.defect_type_for_excel,
                    "format": "box_format",
                },
                "H2": {
                    "value": '时间范围：',
                    "format": "box_format",
                },
                "I2:L2": {
                    "value": f"{self.start_time_for_excel} 至 {self.end_time_for_excel}",
                    "format": "box_format",
                    "merge": True,
                }
            },
            formats,
            options
        ]
        data_1_col_num = self.ui.statistics_table.columnCount()
        for i in range(data_1_col_num):
            header = self.ui.statistics_table.model().headerData(i, Qt.Horizontal, Qt.DisplayRole)
            sheet1[1].update({(2, i): {"value": header, "format": "bg_format_border"}})
        data_rows_1 = self.ui.statistics_table.data
        data_start_index = 3
        for r, row in enumerate(data_rows_1):
            for c, cell in enumerate(row):
                sheet1[1].update({(r + data_start_index, c): {"value": cell, "format": "format"}})
        sheets.append(sheet1)
        sheet_s = [
            f"缺陷类型分布（小类）统计报表明细",
            {
                "A1:M1": {
                    "value": "缺陷类型分布（小类）统计报表",
                    "format": "bg_format",
                    "merge": True,
                },
                "A2:E2": {
                    "value": None,
                    "format": "box_format",
                },
                "F2": {
                    "value": '缺陷大类：',
                    "format": "box_format",
                },
                "G2": {
                    "value": self.defect_type_for_excel,
                    "format": "box_format",
                },
                "H2": {
                    "value": '时间范围：',
                    "format": "box_format",
                },
                "I2:M2": {
                    "value": f"{self.start_date.text()} 至 {self.end_date.text()}",
                    "format": "box_format",
                    "merge": True,
                },
                "A3": {
                    "value": '序号',
                    "format": "bg_format_border",
                },
                "B3": {
                    "value": '产品类型',
                    "format": "bg_format_border",
                },
                "C3": {
                    "value": '生产线',
                    "format": "bg_format_border",
                },
                "D3": {
                    "value": '产品型号',
                    "format": "bg_format_border",
                },
                "E3": {
                    "value": '检测点',
                    "format": "bg_format_border",
                },
                "F3": {
                    "value": '缺陷小类',
                    "format": "bg_format_border",
                },
                "G3": {
                    "value": '串焊机',
                    "format": "bg_format_border",
                },
                "H3": {
                    "value": '缺陷数量',
                    "format": "bg_format_border",
                },
                "I3": {
                    "value": '占比',
                    "format": "bg_format_border",
                },
                "J3": {
                    "value": '产品数量',
                    "format": "bg_format_border",
                },
                "K3": {
                    "value": '平均缺陷数量',
                    "format": "bg_format_border",
                },
                "L3": {
                    "value": '当前缺陷平均修复率',
                    "format": "bg_format_border",
                },
                "M3": {
                    "value": '报废率',
                    "format": "bg_format_border",
                }
            },
            formats,
            options
        ]
        data_1_row_num = self.ui.statistics_table.rowCount()  
        sub_table_data = []
        for page_index in range(data_1_row_num):  
            _, data_s_table = self.get_small_class_table_data(page_index)
            sub_table_data.extend(data_s_table)
        total_ng_count = 0
        for index, item in enumerate(sub_table_data):
            item[0] = index + 1
            total_ng_count += item[7]
        if total_ng_count > 0:
            for item in sub_table_data:
                item[8] = str(round((item[7] / total_ng_count) * 100, 2)) + '%'
        data_start_index = 3
        for r, row in enumerate(sub_table_data):
            for c, cell in enumerate(row):
                sheet_s[1].update({(r + data_start_index, c): {"value": cell, "format": "format"}})
        sheets.append(sheet_s)
        self.download_th = AsyncDownload(file_path, sheets, self)
        self.download_th.signal_result.connect(self.slot_download_success)
        self.download_th.signal_result_error.connect(self.slot_download_error)
        self.download_th.start()
    def slot_download_success(self, data):
        """
        下载成功槽函数
        :param data:
        :return:
        """
        if self.progress_bar:
            self.progress_bar.close()
        InformationMessageBoxOne("下载完成")
    def slot_download_error(self, data):
        """
        下载失败槽函数
        :param data:
        :return:
        """
        if self.progress_bar:
            self.progress_bar.close()
        try:
            raise data.get("error")
        except InvalidWorksheetName as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne(f"工作表包含不允许的字符")
        except FileCreateError as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne(f"下载缺陷类型分布统计报表出错, 该文件处于使用状态")
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("下载缺陷类型分布统计报表出错")
    def get_small_class_table_data(self, row_index):
        """ 获取缺陷小类的数据
        :param row_index: 缺陷大类行索引，用户获取子类数据列表
        :return: headers, table
        """
        headers = []
        obj = self.parent().DefectCategorySmallStatistics.ui.statistics_table
        col_mun = obj.columnCount()
        for i in range(col_mun):
            header = obj.model().headerData(i, Qt.Horizontal, Qt.DisplayRole)
            headers.append(header)
        table = obj.preview_table_data(self.data_models[row_index].small_class_models)
        return headers, table
    def convert_qdate_to_datetime(self, qdate: QDate):
        """ 将日期文本转换成
        :param qdate: QDate
        :return:
        """
        date_str = datetime.strftime(qdate.toPyDateTime(), '%Y-%m-%d %H:%M:%S')
        return date_str
    def slot_defect_class_small_btn_clicked(self, s_class_models):
        """ 点击缺陷小类数量按钮 slot
        :param s_class_models: 缺陷小类 model 数据列表 [DefectStatisticSmallModel, DefectStatisticSmallModel, ...]
        """
        try:
            self.parent().unpackedDefectCategorySmallStatistics.load_data(s_class_models)
            self.parent().unpackedDefectCategorySmallStatistics.ui.tab.setCurrentIndex(0)  
            self.main_window.init_navigation_bar_fun(
                [{"统计分析 | 串件缺陷类型分布统计": self.parent().unpacked_DefectCategoryStatistics_index},
                 {"缺陷小类分布详情": self.parent().unpackedDefectCategorySmallStatistics_index}])
            self.parent().setCurrentIndex(self.parent().unpackedDefectCategorySmallStatistics_index)
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("跳转缺陷小类页面出错")
    def slot_chart_frame_resize(self, size: QSize):
        try:
            fw, fh = size.width(), size.height()
            self.chart_view.setFixedSize(QSize(fw, fh))
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("重置图表尺寸失败")
    def chart_load_data(self, models):
        """ 图表加载数据 """
        data_frame_dict = {"EL": [], "VI": []}
        class_name_list = []
        map_productName_ElViPercent = {}
        map_productNameModel_index = {}
        for index, model in enumerate(models):
            dimission = model.pro_line_name + " " + str(model.pro_spec) + " " + str(
                model.detect_site) + " " + model.product_type
            if dimission not in map_productName_ElViPercent:
                map_productName_ElViPercent[dimission] = [0, 0]
            percent_index = 0 if model.defect_type == 'EL' else 1
            map_productName_ElViPercent[dimission][percent_index] = index
            map_productNameModel_index.update({(dimission, model.defect_type): index})
        for product_name, percents in map_productName_ElViPercent.items():
            el_key = (product_name, 'EL')
            if el_key in map_productNameModel_index:
                el_index = map_productNameModel_index.get(el_key)
                el_percent = float(models[el_index].defects_percent[:-1])
                el_percent = int(el_percent) if el_percent == int(el_percent) else el_percent
                data_frame_dict['EL'].append(el_percent)
            else:
                data_frame_dict['EL'].append(0)
            vi_key = (product_name, 'VI')
            if vi_key in map_productNameModel_index:
                vi_index = map_productNameModel_index.get(vi_key)
                vi_percent = float(models[vi_index].defects_percent[:-1])
                vi_percent = int(vi_percent) if vi_percent == int(vi_percent) else vi_percent
                data_frame_dict['VI'].append(vi_percent)
            else:
                data_frame_dict['VI'].append(0)
            class_name_list.append(product_name)
        self.draw_chart(data_frame_dict, class_name_list)
    def draw_chart(self, data_frame, axisX_labels, axisY_range=[0, 100]):
        """ 绘制图表
        :param data_frame: 数据表 {"set_name":[1,2,3,4,5,6]}
        :param axisX_labels: x 轴标签
        :param axisY_range: y 轴值范围
        """
        set_list = []
        for set_name, set_data_list in data_frame.items():
            set_ = QBarSet(set_name)
            set_.append(set_data_list)
            set_.setLabelColor(QColor(0, 0, 0))
            set_list.append(set_)
        series = QBarSeries()
        for set_ in set_list:
            series.append(set_)
        if series.count():
            width = 1 / series.count()
            max_width = 0.2 * series.count()
            min_width = 0.2 * series.count()
            if width > max_width:
                width = max_width
            if width < min_width:
                width = min_width
            series.setBarWidth(width)  
        series.setLabelsVisible(True)
        series.setLabelsPosition(QAbstractBarSeries.LabelsInsideBase)
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("产品缺陷分布占比图")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        axisX = QBarCategoryAxis()
        axisX.append(axisX_labels)
        chart.addAxis(axisX, Qt.AlignBottom)
        series.attachAxis(axisX)
        axisY = QValueAxis()
        axisY.setRange(*axisY_range)
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)
        if len(data_frame) < 2:
            chart.legend().setVisible(False)
        chart.legend().setAlignment(Qt.AlignBottom)
        self.chart_view.setChart(chart)
    def resizeEvent(self, event: QResizeEvent):
        """ 调整大小事件 """
        super().resizeEvent(event)
        self.loading_widget.resize(self.ui.tab.size())
        self.loading_widget.move(self.ui.tab.pos())
class UI_DefectCategoryStatistics(object):
    def __init__(self, parent):
        styleFile = 'qss/statistics.qss'
        qss = CommonHelper.readQss(styleFile)
        parent.setStyleSheet(qss)
        parent.setWindowTitle("缺陷类型分布统计")
        layout = QVBoxLayout(parent)
        self.filters_pannel = FiltersPannel()
        layout.addWidget(self.filters_pannel)
        self.tab = QTabWidget()
        layout.addWidget(self.tab)  
        self.statistics_table = DefectCategoryTable()
        self.tab.addTab(self.statistics_table, "列表")
        self.q_charts = QChartFrame()
        self.tab.addTab(self.q_charts, "图表")
        self.chart_view = QChartView(parent=self.q_charts)
class DefectCategoryTable(QTableWidget):
    signal_defect_class_small_btn_clicked = pyqtSignal(list)
    def __init__(self, *args):
        super().__init__(*args)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setHighlightSections(False)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)  
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)  
        self.setAlternatingRowColors(True)  
        self.verticalHeader().setHidden(True)  
        headers = ['序号', '产品类型', '生产线', '产品型号', '串焊机', '缺陷类型', '检测方式', '缺陷小类', '维修率', '报废率', '缺陷总数量', '分布占比']
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        self.data = []
        self.set_column_width(0, 80)
    def set_column_width(self, index, width):
        """ 指定列宽 """
        self.horizontalHeader().setSectionResizeMode(index, QHeaderView.Custom)
        self.setColumnWidth(index, width)
    def update_data(self, rows_data):
        """ 更新数据 """
        self.setRowCount(len(rows_data))
        self.data = []
        gg_enum = DictInfoCRUD.get_all_gg_enum(True)
        for i, model in enumerate(rows_data):
            row_data = [
                i + 1,  
                model.product_type,  
                model.pro_line_name,
                model.pro_spec,
                model.detect_site,
                model.defect_type,  
                model.detect_type,  
                model.defect_small_class_num,  
                model.repaired_ratio,  
                model.scraped_ratio,  
                model.defects_sum_num,  
                model.defects_percent  
            ]
            self.data.append(row_data)
            for col, data in enumerate(row_data):
                if col == 7:
                    q_btn = QPushButton(str(data))
                    q_btn.setStyleSheet("""
                        border: none;
                        background-color: rgba(0,0,0,0);
                        color: rgb(19, 140, 222)
                    """)
                    q_btn.setCursor(Qt.PointingHandCursor)
                    q_btn.clicked.connect(self.slot_defect_class_small_btn_clicked(model.small_class_models))
                    self.setCellWidget(i, col, q_btn)
                else:
                    q_table_item = QTableWidgetItem()
                    q_table_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    q_table_item.setText(str(data))
                    self.setItem(i, col, q_table_item)
    def slot_defect_class_small_btn_clicked(self, s_class_models):
        """ 点击缺陷小类数量按钮 slot
        :param s_class_models: 缺陷小类 model 数据列表 [DefectStatisticSmallModel, DefectStatisticSmallModel, ...]
        :return:
        """
        try:
            def wrapper():
                self.signal_defect_class_small_btn_clicked.emit(s_class_models)
            return wrapper
        except Exception as e:
            logger.error(e, exc_info=True)
class FiltersPannel(QFrame):
    """ 搜索条件面板 """
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        title = QLabel("缺陷类型分布统计")
        title.hide()
        title.setObjectName("h1")
        layout.addWidget(title)  
        layout.addItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout2 = QGridLayout()
        self.cb_detect_type = ComboBoxGroup("检测方式:", ["AI检测", "人工复检"])
        layout2.addWidget(self.cb_detect_type, 0, 0)
        self.date_group = DateGroup('起止时间:')
        layout2.addWidget(self.date_group, 0, 1, 1, 4)
        self.cb_defect_big_class = ComboBoxGroup("缺陷大类:", ["全部", "VI", "EL"])
        layout2.addWidget(self.cb_defect_big_class, 1, 0)
        self.cb_defect_type = ComboBoxGroup("缺陷类型:", [])
        layout2.addWidget(self.cb_defect_type, 1, 1)
        self.cb_statistics_dimension = DimissionFilter()
        layout2.addWidget(self.cb_statistics_dimension, 1, 2)
        layout.addLayout(layout2)
        self.btn_search = IconButton(':/icons/search.png')
        layout.addWidget(self.btn_search)
        self.btn_download = IconButton(':/icons/download.png')
        layout.addWidget(self.btn_download)
        self.init_state()
    def init_state(self):
        """ 初始化界面布局 """
        self.cb_detect_type.comboBox.setCurrentIndex(0)
        self.date_group.comboBox.setCurrentIndex(0)
        self.cb_defect_big_class.comboBox.setCurrentIndex(0)
        self.cb_defect_type.comboBox.setCurrentIndex(0)
        self.cb_statistics_dimension.comboBox.setCurrentIndex(1)
class QChartFrame(QFrame):
    signal_chart_frame_resize = pyqtSignal(QSize)
    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        self.signal_chart_frame_resize.emit(self.size())
class DimissionFilter(QFrame):
    """
    统计维度搜索控件
    """
    def __init__(self, parent=None):
        super(DimissionFilter, self).__init__(parent)
        self.config = []  
        self.pro_line_id = ''  
        self.detect_site = ''  
        self.spec = ''  
        self.pro_lines = ''  
        self.pro_specs = ''  
        self.detect_sites = ''  
        self.hbox = QHBoxLayout(self)
        self.init_ui()
    def init_ui(self):
        title = QLabel("统计维度:")
        self.hbox.addWidget(title)
        self.comboBox = QComboBox()
        self.pro_lines_combox = QComboBox()  
        self.pro_specs_combox = QComboBox()  
        self.welding_combox = QComboBox()  
        self.welding_combox.addItem('全部串焊机', '')
        self.pro_lines_combox.currentTextChanged.connect(self.slot_pro_lines_changed)
        self.pro_lines_combox.activated[str].connect(self.slot_pro_lines_actived)
        self.pro_specs_combox.activated[str].connect(self.slot_pro_specs_actived)
        self.hbox.addWidget(self.pro_lines_combox)
        self.hbox.addWidget(self.welding_combox)
        self.hbox.addWidget(self.pro_specs_combox)
    def set_data(self, data):
        """
        设置生产线和规格下拉框
        """
        self.config = data
        current_pro_line = self.pro_lines_combox.currentText()
        current_welding_name = self.welding_combox.currentText()
        current_spec = self.pro_specs_combox.currentText()
        self.pro_lines_combox.clear()
        self.pro_specs_combox.clear()
        pro_lines = [{'pro_line_id': '', 'pro_line_name': '全部产线', 'welding': []}]
        pro_lines.extend(data.get('pro_lines'))
        pro_specs = [{'id': '', 'name': '全部规格'}]
        pro_specs.extend(data.get('pro_specs'))
        for item in pro_lines:
            self.pro_lines_combox.addItem(item.get('pro_line_name'), item.get('pro_line_id'))
        for item in pro_specs:
            self.pro_specs_combox.addItem(item.get('name'), item.get('id'))
        self.pro_lines_combox.setCurrentText(current_pro_line)
        self.welding_combox.setCurrentText(current_welding_name)
        self.pro_specs_combox.setCurrentText(current_spec)
    def slot_pro_lines_actived(self, pro_lines):
        """
        生产线下拉框手动选择时设置当前产线名称并且清空当前规格名称，根据产线名称动态更新规格下拉框
        """
        self.pro_lines = pro_lines
        self.pro_specs = ''
        self.slot_pro_lines_changed()
    def slot_pro_specs_actived(self, pro_specs):
        """
        规格下拉框手动选择后更新当前规格名称
        """
        self.pro_specs = pro_specs
    def slot_pro_lines_changed(self, ):
        """
        产线下拉框变化时动态更新规格
        """
        self.welding_combox.clear()
        pro_line = self.pro_lines_combox.currentData()
        weldings = [{'welding_id': '', 'welding_name': '全部串焊机'}]
        if not pro_line:
            if isinstance(self.config, dict):
                for item in self.config.get('pro_lines'):
                    weldings.extend(item.get('welding', []))
        else:
            if isinstance(self.config, dict):
                for item in self.config.get('pro_lines', []):
                    if item.get('pro_line_id') == pro_line:
                        weldings.extend(item.get('welding', []))
        for item in weldings:
            self.welding_combox.addItem(item.get('welding_name'), item.get('welding_id'))
    @property
    def data(self):
        """
        动态获取当前产线ID、规格、检测点
        """
        pro_line_id = self.pro_lines_combox.currentData()
        pro_spec = self.pro_specs_combox.currentData()
        welding_id = self.welding_combox.currentData()
        return pro_line_id, pro_spec, welding_id
class DefectCategorySmallStatistics(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = UI_DefectCategoryStatistics(self)
        self.q_charts = self.ui.q_charts
        self.chart_view = self.ui.chart_view
        self.pie_view = QWebEngineView()
        self.echarts_js = ''
        self.bind_events()
    def bind_events(self):
        self.q_charts.signal_chart_frame_resize.connect(self.slot_chart_frame_resize)
        self.ui.btn_back.clicked.connect(self.slot_btn_back_clicked)
    def load_data(self, data):
        """ 加载表格数据
        数据格式：
            {
                缺陷小类: [0,1,2,0,0,0,0,0],    
            }
        """
        try:
            self.ui.statistics_table.update_data(data)
            defect_class_percent_list = []  
            repaired_percent_list = []  
            class_name_list = []
            for model in data:
                dc_percent = float(model.defects_percent[:-1])
                dc_percent = int(dc_percent) if dc_percent == int(dc_percent) else round(dc_percent, 2)
                defect_class_percent_list.append(dc_percent)
                defect_class_name = model.defect_class_name
                defect_class_name = defect_class_name.split(',') if defect_class_name else ['']
                defect_class_name = list(set(defect_class_name))
                class_name_list.append(defect_class_name[0])
                repaired_percent = float(model.average_repaired_ratio[:-1])
                repaired_percent = int(repaired_percent) if repaired_percent == int(repaired_percent) else round(
                    repaired_percent, 2)
                repaired_percent_list.append(repaired_percent)
            zipped = zip(class_name_list, defect_class_percent_list, repaired_percent_list)
            sort_zipped = sorted(list(zipped), key=lambda x: x[1], reverse=True)
            res = zip(*sort_zipped)
            class_name_list, defect_class_percent_list, repaired_percent_list = [list(x) for x in res]
            chart1 = [
                [
                    [
                        defect_class_percent_list,
                        repaired_percent_list
                    ],
                    class_name_list
                ],
                {
                    "max_y": 100,
                    "show_data_handler": {
                        0: lambda x: "0%" if x == 0 else f"{x}%",
                        1: lambda x: "0%" if x == 0 else f"{x}%"
                    },
                    "legends": ["缺陷分布占比", "缺陷平均修复率"]
                }
            ]
            charts = [chart1]
            self.chart_load_data(charts)
            defect_data = []
            repaired_data = []
            labels = []
            for index in range(len(class_name_list)):
                label = class_name_list[index]
                defect_data.append([label, defect_class_percent_list[index]])
                repaired_data.append([label, repaired_percent_list[index]])
                labels.append(label)
            self.load_pie_chart(defect_data, repaired_data, labels)
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("缺陷类型小类页面加载数据出错")
    @staticmethod
    def label_opts(repaired_data, labels):
        params = "let repaired_data = " + str(repaired_data) + ";" + "let labels = " + str(
            labels) + "; let repaired = null;"
        fn = """
            function(params) {
            """ + params + """
                for (let i=0; i < labels.length; i++) {
                    if (labels[i] === params.name) {
                        repaired = repaired_data[i];
                        break;
                    }
                }
                return params.name + '\\n缺陷分布占比：' + params.value + '%' + '\\n平均修复率: ' + repaired[1] + '%';
            }
            """
        return options.LabelOpts(formatter=JsCode(fn))
    def load_pie_chart(self, defect_data, repaired_data, labels):
        """ 加载饼状图 """
        try:
            colors = ['#FF7C7C', '#9188E7', '#60ACFC', '#34D2EB', '#5CC49F', '#A5A5A5', '#FEB64E', '#7BD5F8', '#8A67C5',
                      '#E78A3F', '#20908F', '#E47BA6', '#4477E0', '#89AAEE', '#10B674', '#A0E8CC', '#4C648E', '#A8B0C3',
                      '#F7C225', '#FAE39E']
            pie = Pie()
            pie.add('', defect_data, center=["50%", "55%"], radius=["0%", "50%"])
            pie.set_colors(colors)
            pie.set_global_opts(legend_opts=options.LegendOpts(legend_icon='circle')) \
                .set_series_opts(label_opts=self.label_opts(repaired_data, labels))
            html = pie.render()
            if not self.echarts_js:
                with open("pyecharts/render/templates/echarts.min.js", "r", encoding="utf8") as f:
                    self.echarts_js = f.read()
            html = html.replace(
                '<script type="text/javascript" src="https://assets.pyecharts.org/assets/echarts.min.js"></script>',
                '<script type="text/javascript">\n' + self.echarts_js + '\n</script>'
            )
            html = html.replace(
                'style="width:900px; height:500px;"',
                'style="width:1700px; height:780px; margin:0px auto;"'
            )
            self.ui.q_pie_chart.setHtml(html)
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("绘制饼状图出错")
    def chart_load_data(self, charts):
        """ 图表加载数据
        :param charts: [(chart1_args,chart1_kwargs),(chart2_args,chart2_kwargs)]
        """
        try:
            self.ui.q_charts.clear()
            pro_counts = len(charts[0][0][1])
            for i, chart in enumerate(charts):
                bar = BarGraph()
                bar.set_bar_bgcorlor(QColor(70, 70, 70))
                if i == 0:
                    bar.set_color_map(
                        [
                            [QColor(246, 228, 114), QColor(237, 153, 45)],
                            [QColor(110, 228, 33), QColor(28, 82, 2)],
                            [QColor(255, 110, 40), QColor(165, 1, 38)],
                        ]
                    )
                bar.set_bar_width(0.025 * pro_counts)
                bar.set_bar_margin(0.005 * pro_counts)
                bar.set_data_frame(*chart[0], **chart[1])
                self.ui.q_charts.add_widget(bar)
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("绘制柱状图出错")
    def draw_chart(self, data_frame, axisX_labels, axisY_range=[0, 100]):
        """ 绘制图表
        :param data_frame: 数据表 {"set_name":[1,2,3,4,5,6]}
        :param axisX_labels: x 轴标签
        :param axisY_range: y 轴值范围
        """
        set_list = []
        for set_name, set_data_list in data_frame.items():
            set_ = QBarSet(set_name)
            set_.append(set_data_list)
            set_.setLabelColor(QColor(0, 0, 0))
            set_list.append(set_)
        series = QBarSeries()
        for set_ in set_list:
            series.append(set_)
        if series.count():
            width = 1 / series.count()
            max_width = 0.15
            if width > max_width:
                width = max_width
            series.setBarWidth(width)  
        series.setLabelsVisible(True)
        series.setLabelsPosition(QAbstractBarSeries.LabelsOutsideEnd)
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("缺陷小类占比图")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        axisX = QBarCategoryAxis()
        axisX.append(axisX_labels)
        chart.addAxis(axisX, Qt.AlignBottom)
        series.attachAxis(axisX)
        axisY = QValueAxis()
        axisY.setRange(*axisY_range)
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)
        if len(data_frame) < 2:
            chart.legend().setVisible(False)
        chart.legend().setAlignment(Qt.AlignBottom)
        self.chart_view.setChart(chart)
    def slot_chart_frame_resize(self, size: QSize):
        try:
            fw, fh = size.width(), size.height()
            self.chart_view.setFixedSize(QSize(fw, fh))
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("重置图表尺寸失败")
    def slot_btn_back_clicked(self):
        """ 返回上级 """
        try:
            self.parent().parent().parent().init_navigation_bar_fun(
                [{"统计分析 | 串件缺陷类型分布统计": self.parent().unpacked_DefectCategoryStatistics_index}])
            self.parent().setCurrentIndex(self.parent().unpacked_DefectCategoryStatistics_index)
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("返回上级列表失败")
class UI_DefectCategoryStatistics(object):
    def __init__(self, parent):
        styleFile = 'qss/statistics.qss'
        qss = CommonHelper.readQss(styleFile)
        parent.setStyleSheet(qss)
        parent.setWindowTitle("缺陷类型分布统计")
        layout = QVBoxLayout(parent)
        layout_1 = QHBoxLayout()
        title = QLabel("缺陷小类分布详情")
        title.hide()
        title.setObjectName("h1")
        layout_1.addWidget(title)  
        layout_1.addItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addLayout(layout_1)  
        self.tab = QTabWidget()
        layout.addWidget(self.tab)  
        self.statistics_table = DefectCategorySmallTable()
        self.tab.addTab(self.statistics_table, "列表")
        self.q_charts = QChartFrame()
        self.tab.addTab(self.q_charts, "柱状图")
        self.chart_view = QChartView()
        self.q_pie_chart = QWebEngineView()
        self.tab.addTab(self.q_pie_chart, "饼状图")
        layout_3 = QHBoxLayout()
        layout_3.addItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.btn_back = QPushButton("返回上级")
        self.btn_back.setObjectName('back_btn')
        self.btn_back.setCursor(Qt.PointingHandCursor)
        layout_3.addWidget(self.btn_back)
        layout_3.addItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addLayout(layout_3)
class DefectCategorySmallTable(QTableWidget):
    def __init__(self, *args):
        super().__init__(*args)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setHighlightSections(False)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)  
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)  
        self.setAlternatingRowColors(True)  
        self.verticalHeader().setHidden(True)  
        headers = ['序号', '产品类型', '生产线', '产品型号', '检测点', '缺陷小类', '串焊机', '缺陷数量', '占比', '产品数量', '平均缺陷数量', '当前缺陷平均修复率',
                   '报废率']
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        self.data = []
        self.set_column_width(0, 80)
    def set_column_width(self, index, width):
        """ 指定列宽 """
        self.horizontalHeader().setSectionResizeMode(index, QHeaderView.Fixed)
        self.setColumnWidth(index, width)
    def preview_table_data(self, data):
        """ 预览表格数据，用作下载 """
        results = []
        gg_enum = DictInfoCRUD.get_all_gg_enum(True)
        for i, model in enumerate(data):
            results.append([
                i + 1,  
                model.product_type,  
                model.pro_line_name,
                gg_enum.get(model.pro_spec),
                model.detect_site,
                model.defect_class_name,  
                model.welding,  
                model.defects_num,  
                model.defects_percent,  
                model.product_num,  
                model.average_defects,  
                model.average_repaired_ratio,  
                model.scraped_ratio  
            ])
        return results
    def update_data(self, rows_data):
        """ 更新截面数据 """
        self.setRowCount(len(rows_data))
        self.data = []
        gg_enum = DictInfoCRUD.get_all_gg_enum(True)
        for i, model in enumerate(rows_data):
            defect_class_name = model.defect_class_name
            defect_class_name = defect_class_name.split(',') if defect_class_name else ['']
            defect_class_name = list(set(defect_class_name))
            row_data = [
                i + 1,  
                model.product_type,  
                model.pro_line_name,
                gg_enum.get(model.pro_spec),
                model.detect_site,
                defect_class_name[0],  
                model.welding,  
                model.defects_num,  
                model.defects_percent,  
                model.product_num,  
                model.average_defects,  
                model.average_repaired_ratio,  
                model.scraped_ratio,  
            ]
            self.data.append(row_data)
            for col, data in enumerate(row_data):
                q_table_item = QTableWidgetItem()
                q_table_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.setItem(i, col, q_table_item)
                if col == 6:
                    q_table_item.setToolTip(str(data))
                    q_table_item.setText(str(data)[:15] + "..." if len(str(data)) > 15 else str(data))
                else:
                    q_table_item.setText(str(data))
class QChartFrame(QFrame):
    signal_chart_frame_resize = pyqtSignal(QSize)
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.widgets = []
    def add_widget(self, widget):
        try:
            self.widgets.append(widget)
            self.layout.addWidget(widget)
        except Exception as e:
            logger.error(e, exc_info=True)
    def clear(self):
        """ 清除数据 """
        for widget in self.widgets:
            self.layout.removeWidget(widget)
        self.widgets = []
    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        self.signal_chart_frame_resize.emit(self.size())
class QPieChartFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.widgets = []
        self.pixmap = QPixmap()
    def add_widget(self, widget):
        try:
            self.widgets.append(widget)
            self.layout.addWidget(widget)
        except Exception as e:
            logger.error(e, exc_info=True)
    def clear(self):
        """ 清除数据 """
        for widget in self.widgets:
            self.layout.removeWidget(widget)
        self.widgets = []
    def draw_pixmap(self, pixmap):
        self.pixmap = pixmap
        self.repaint()
    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        try:
            painter.begin(self)
            painter.save()
            print(self.pixmap.size())
            if self.pixmap.size() != QSize(0, 0):
                x_ratio = (self.width() - 80) / self.pixmap.width()  
                y_ratio = (self.height() - 80) / self.pixmap.height()
                scale_ratio = min(x_ratio, y_ratio)
                new_pixmap = self.pixmap.scaled(
                    QSize(self.pixmap.width() * scale_ratio, self.pixmap.height() * scale_ratio))
                painter.translate(self.width() / 2, self.height() / 2)
                painter.drawPixmap(
                    QRect(-new_pixmap.width() / 2, -new_pixmap.height() / 2, new_pixmap.width(), new_pixmap.height()),
                    new_pixmap)
                painter.restore()
        except Exception as e:
            logger.error(e, exc_info=True)
        finally:
            painter.end()
class DefectPosStatistics(QWidget):
    def __init__(self, main_window, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_window = main_window
        self.cruds = defectPos()
        self.ui = UI_DefectPosStatistics(self)
        self.cb_detect_type = self.ui.filters_pannel.cb_detect_type.comboBox  
        self.cb_line = self.ui.filters_pannel.cb_line.comboBox  
        self.cb_weld = self.ui.filters_pannel.cb_weld.comboBox  
        self.start_date = self.ui.filters_pannel.date_group.start_date  
        self.end_date = self.ui.filters_pannel.date_group.end_date  
        self.cb_date_selections = self.ui.filters_pannel.date_group.comboBox  
        self.cb_defect_big_class = self.ui.filters_pannel.cb_defect_big_class.comboBox  
        self.cb_defect_type = self.ui.filters_pannel.cb_defect_type.comboBox  
        self.cb_statistics_dimension = self.ui.filters_pannel.cb_statistics_dimension.comboBox  
        self.cb_product_size = self.ui.filters_pannel.cb_product_size.comboBox  
        self.btn_search = self.ui.filters_pannel.btn_search  
        self.btn_download = self.ui.filters_pannel.btn_download  
        self.progress_bar = ProgressBarWindow(value_show=False)  
        self.btn_download.setEnabled(self.main_window.get_system_func("defect_statistic_download"))
        self.current_statistics_dimension_index = 0  
        self.is_loading = False  
        self.loading_widget = LoadingWidget(":/icons/loading.gif", parent=self)
        self.current_product_spec = None  
        self.data_dict = None  
        self.data_models = None  
        self.defect_big_class_type = None  
        self.defect_type = None  
        self.pro_lines_config = None  
        self.start_time_for_excel = ""  
        self.end_time_for_excel = ""  
        self.pro_line_for_excel = ""  
        self.defect_type_for_excel = ""  
        self.excel_data = None
        self.req_product_size()  
        self.req_defect_types()  
        self.req_product_line()  
        self.bind_events()
    def bind_events(self):
        """ 绑定事件 """
        self.cb_line.currentIndexChanged.connect(self.slot_line_changed)
        self.cb_defect_big_class.currentTextChanged.connect(self.slot_defect_type_changed)
        self.cb_statistics_dimension.currentIndexChanged.connect(self.slot_statistics_dimension_changed)
        self.cb_product_size.currentIndexChanged.connect(self.slot_product_size_changed)
        self.ui.statistics_table.signal_defect_class_small_btn_clicked.connect(self.slot_defect_class_small_btn_clicked)
        self.btn_search.clicked.connect(self.slot_btn_search_clicked)
        self.btn_download.clicked.connect(self.slot_btn_download_clicked)
    def slot_line_changed(self, index):
        """
        生产线下拉框改变事件
        :param index:
        :return:
        """
        try:
            self.cb_weld.clear()
            pro_line_id = self.cb_line.currentData()
            welding = [{'welding_id': '', 'welding_name': '全部'}]
            if not pro_line_id:  
                if isinstance(self.pro_lines_config, list):
                    for item in self.pro_lines_config:
                        welding.extend(item.get('welding', []))
            else:
                for item in self.pro_lines_config:
                    if item.get('pro_line_id') == pro_line_id:
                        welding.extend(item.get('welding', []))
                        break
            for item in welding:
                self.cb_weld.addItem(item.get('welding_name'), item.get('welding_id'))
        except Exception as e:
            logger.error(e, exc_info=True)
    def slot_defect_type_changed(self, text):
        """
        缺陷大类切换选项
        :param text: 当前缺陷大类下拉框文本
        :return:
        """
        try:
            self.cb_defect_type.clear()
            self.cb_defect_type.addItems(self.defect_type.get(text))
        except Exception as e:
            logger.error(e, exc_info=True)
    def slot_statistics_dimension_changed(self, index):
        """ 切换统计维度
        需求，如果选中产品型号，必须指定一个产品尺寸，不能是全部（方便绘制图表）
        """
        try:
            if index == 1:  
                if self.cb_product_size.currentIndex() == 0:  
                    if self.cb_product_size.count() == 1:
                        self.cb_statistics_dimension.setCurrentIndex(0)
                        self.cb_product_size.setCurrentIndex(0)
                        InformationMessageBoxOne("由于没有具体产品尺寸，产品型号统计维度不可选")
        except Exception as e:
            logger.error(e, exc_info=True)
    def slot_product_size_changed(self, index):
        """ 切换产品尺寸 """
        try:
            if index == 0:  
                if self.cb_statistics_dimension.currentIndex() == 1:  
                    self.cb_product_size.setCurrentIndex(self.cb_product_size.prev_index)
                    InformationMessageBoxOne("统计维度为产品型号时，只能选择具体的产品尺寸")
            else:
                self.cb_product_size.prev_index = index
        except Exception as e:
            logger.error(e, exc_info=True)
    def req_product_line(self):
        """
        获取生产线列表
        :return:
        """
        try:
            self.line_th = AsynThread(self.cruds.retrieve_product_lines, parent=self)
            self.line_th.signal_result.connect(self.slot_update_product_lines)
            self.line_th.start()
        except Exception as e:
            logger.error(e, exc_info=True)
    def slot_update_product_lines(self, product_lines):
        """
        更新生产性下拉列表槽函数
        :param product_lines: [{'pro_line_id': xxx, 'pro_line_name': xxx}, ...]
        :return:
        """
        try:
            self.cb_line.clear()
            if isinstance(product_lines, list):
                product_lines.insert(0, {'pro_line_id': '', 'pro_line_name': '全部'})
            else:
                return CriticalMessageBoxOne("获取生产线列表失败")
            self.pro_lines_config = product_lines
            for item in product_lines:
                self.cb_line.addItem(item.get('pro_line_name'), item.get('pro_line_id'))
        except Exception as e:
            logger.error(e, exc_info=True)
    def req_product_size(self):
        """ 获取产品尺寸
        这里的产品尺寸，其实是数据库中的规格
        :return:
        """
        try:
            self.product_size_th = AsynThread(self.cruds.retrieve_product_spec, args=(1,), parent=self)
            self.product_size_th.signal_result.connect(self.slot_update_product_size)
            self.product_size_th.start()
        except Exception as e:
            logger.error(e, exc_info=True)
    def slot_update_product_size(self, data):
        """ 更新产品尺寸的槽函数
        产品尺寸真实对应数据库的规格字段
        """
        try:
            self.cb_product_size.clear()
            if not isinstance(data, list):
                data = [{'id': '', 'name': '全部'}]
            else:
                data.insert(0, {'id': '', 'name': '全部'})
            for item in data:
                self.cb_product_size.addItem(item.get('name'), item.get('id'))
        except Exception as e:
            logger.error(e, exc_info=True)
    def req_defect_types(self):
        """
        获取缺陷类型
        :return:
        """
        try:
            self.cb_defect_big_class.setDisabled(True)  
            self.cb_defect_type.setDisabled(True)
            self.defect_type_th = AsynThread(self.cruds.retrieve_defect_types, parent=self)
            self.defect_type_th.signal_result.connect(self.slot_update_defect_types)
            self.defect_type_th.start()
        except Exception as e:
            logger.error(e, exc_info=True)
    def slot_update_defect_types(self, models):
        """ 更新缺陷类型的槽函数 """
        try:
            all_defect_types = list(set([model.LAB_CLASS_NAME for model in models]))
            el_defect_types = list(set([model.LAB_CLASS_NAME for model in models if model.CLASS_D_CATEGORY == 1]))
            vi_defect_types = list(set([model.LAB_CLASS_NAME for model in models if model.CLASS_D_CATEGORY == 2]))
            all_defect_types.sort()
            el_defect_types.sort()
            vi_defect_types.sort()
            all_defect_types.insert(0, "全部")
            el_defect_types.insert(0, "全部")
            vi_defect_types.insert(0, "全部")
            self.defect_type = {"全部": all_defect_types, "EL": el_defect_types, "VI": vi_defect_types}  
            current_defect_big_type = self.cb_defect_big_class.currentText()
            self.cb_defect_type.addItems(self.defect_type.get(current_defect_big_type))
            self.ui.q_heatmap.defects_combobox.addItems(self.defect_type.get(current_defect_big_type))
        except Exception as e:
            logger.error(e, exc_info=True)
        finally:
            self.cb_defect_big_class.setDisabled(False)  
            self.cb_defect_type.setDisabled(False)
    def slot_defect_class_small_btn_clicked(self, s_class_models):
        """ 点击缺陷小类数量按钮 slot
        :param s_class_models: 缺陷小类 model 数据列表 [DefectPosStatisticSmallModel, DefectPosStatisticSmallModel, ...]
        """
        try:
            self.parent().unpackedDefectPosSmallStatistics.load_data(self.current_statistics_dimension_index,
                                                                     s_class_models)
            self.parent().DefectPosSmallStatistics.ui.tab.setCurrentIndex(0)  
            self.main_window.init_navigation_bar_fun(
                [{"统计分析 | 串件缺陷位置分布统计": self.parent().unpacked_DefectPosStatistics_index},
                 {"缺陷类型分组统计": self.parent().unpacked_DefectPosSmallStatistics_index}])
            self.parent().setCurrentIndex(self.parent().unpacked_DefectPosSmallStatistics_index)
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("跳转缺陷位置小类页面出错")
    def slot_btn_search_clicked(self):
        """ 点击搜索按钮 """
        try:
            if self.loading_widget.is_loading:
                InformationMessageBoxOne("查询统计完成之后，才可再次查询")
                return
            self.ui.statistics_table.setRowCount(0)  
            self.loading_widget.start()  
            self.current_statistics_dimension_index = self.cb_statistics_dimension.currentIndex()
            if self.current_statistics_dimension_index == 0:
                self.ui.statistics_table.setHorizontalHeaderItem(1, QTableWidgetItem("产品尺寸"))
            else:
                self.ui.statistics_table.setHorizontalHeaderItem(1, QTableWidgetItem("产品型号"))
            self.start_time_for_excel = self.start_date.text()
            self.end_time_for_excel = self.end_date.text()
            self.defect_type_for_excel = self.cb_defect_big_class.currentText()
            self.pro_line_for_excel = self.cb_line.currentText()
            self.req_statistics_info()  
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("缺陷位置分布统计出错")
    def req_statistics_info(self):
        """ 异步请求统计信息 """
        try:
            detect_type_index = self.cb_detect_type.currentIndex()  
            product_line = self.cb_line.currentData()  
            weld = self.cb_weld.currentData()  
            start_datetime = self.convert_qdate_to_datetime(self.start_date.date)  
            end_datetime = self.convert_qdate_to_datetime(self.end_date.date)  
            defect_big_class_index = self.cb_defect_big_class.currentIndex()  
            defect_type_text = self.cb_defect_type.currentText()  
            statistics_dimension_index = self.cb_statistics_dimension.currentIndex()  
            product_size = self.cb_product_size.currentData()  
            self.defect_big_class_type = self.cb_defect_big_class.currentText()  
            self.ui.q_heatmap.defects_combobox.clear()  
            defect_type = copy.copy(self.defect_type.get(self.defect_big_class_type))
            del defect_type[0]  
            self.ui.q_heatmap.defects_combobox.addItems(defect_type)
            user_info_dict = self.main_window.user
            user_id = user_info_dict['id']
            role_type = user_info_dict['role_type']
            self.data_th = AsynThread(
                self.cruds.retrieve,
                args=(
                    start_datetime, end_datetime, detect_type_index, product_line, weld, defect_big_class_index,
                    defect_type_text, statistics_dimension_index, product_size, user_id, role_type
                ),
                parent=self
            )
            self.data_th.signal_result.connect(self.slot_get_statistics_info)
            self.data_th.signal_result_error.connect(self.slot_get_statistics_info_error)
            self.data_th.start()
        except Exception as e:
            logger.error(str(e), exc_info=True)
    def slot_get_statistics_info(self, models):
        """
        获取到的统计信息
        """
        try:
            model_list, map_defects_positions, map_size_and_pos_failure, excel_data = models
            self.data_models = model_list
            self.excel_data = excel_data
            self.ui.statistics_table.update_data(model_list)
            self.chart_load_data(map_size_and_pos_failure)
            self.heatmap_load_data(map_defects_positions)
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("查询缺陷位置分布统计数据出错")
        finally:
            self.loading_widget.stop()
    def slot_get_statistics_info_error(self):
        """
        查询数据失败槽函数
        :return:
        """
        try:
            self.loading_widget.stop()
        except Exception as e:
            logger.error(e, exc_info=True)
        CriticalMessageBoxOne("获取缺陷位置数据失败")
    def calc_type(self, items):
        """
        判断列表是否需要被展开，判断依据是列表中的项是否是可迭代对象
        :param items:
        :return:
        """
        for item in items:
            if isinstance(item, Iterable):
                return True
        return False
    def flatten(self, items):
        """
        展开一维列表中包含的多维列表
        :param items:
        :return:
        """
        if not isinstance(items, Iterable):
            yield items
        else:
            if not self.calc_type(items):
                if len(items) > 2 or items == [None, None]:
                    for item in items:
                        yield item
                else:
                    yield tuple(items)
            else:
                for item in items:
                    if isinstance(item, Iterable) and np.array(item).ndim > 1:
                        for sub_item in self.flatten(item):
                            yield tuple(sub_item)
                    elif isinstance(item, Iterable):
                        yield tuple(item)
                    else:
                        yield item
    def slot_btn_download_clicked(self):
        """ 点击下载按钮 """
        try:
            if not self.main_window.get_system_func('defect_statistic_download'):
                return InformationMessageBoxOne("暂无权限下载，请联系管理员")
            if not self.excel_data:  
                InformationMessageBoxOne("没有数据可供下载，请先查询")
                return
            if self.loading_widget.is_loading:
                InformationMessageBoxOne("正在查询数据，请稍后下载")
                return
            file_name = f"串件缺陷位置分布统计报表_{datetime.now().strftime('%Y%m%d')}.xlsx"
            file_path = gen_xlsx_path(file_name, "下载串件缺陷位置分布统计报表")
            if not file_path:
                return
            self.download_excel(file_path)
        except FileCreateError as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne(f"下载缺陷位置分布统计报表出错, {e}")
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("下载缺陷位置分布统计报表出错")
    def download_excel(self, file_path):
        """
        下载excel数据
        :param file_path: 文件下载路径
        :param data: 数据
        :return:
        """
        self.progress_bar.set_title("正在下载 %s" % os.path.basename(file_path))
        self.progress_bar.show()
        sum_data, detail_data, sub_data = self.excel_data
        self.download_th = AsyncDownloadPackedDetectPos(sum_data, detail_data, sub_data,
                                                        self.cb_detect_type.currentIndex(),
                                                        self.current_statistics_dimension_index,
                                                        [self.start_time_for_excel, self.end_time_for_excel], file_path,
                                                        self)
        self.download_th.signal_result.connect(self.slot_download_success)
        self.download_th.signal_result_error.connect(self.slot_download_error)
        self.download_th.start()
    def slot_download_success(self, data):
        """
        下载成功槽函数
        :param data:
        :return:
        """
        if self.progress_bar:
            self.progress_bar.close()
        InformationMessageBoxOne("下载完成")
    def slot_download_error(self, data):
        """
        下载失败槽函数
        :param data:
        :return:
        """
        if self.progress_bar:
            self.progress_bar.close()
        try:
            raise data.get("error")
        except InvalidWorksheetName as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne(f"工作表包含不允许的字符")
        except FileCreateError as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne(f"下载缺陷位置分布统计报表出错, 该文件处于使用状态")
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("下载缺陷位置分布统计报表出错")
    def get_small_class_table_data(self, row_index):
        """ 获取缺陷小类的数据
        :param row_index: 缺陷大类行索引，用户获取子类数据列表
        :return: headers, table
        """
        headers = []
        obj = self.parent().DefectPosSmallStatistics.ui.statistics_table
        col_mun = obj.columnCount()
        for i in range(col_mun):
            header = obj.model().headerData(i, Qt.Horizontal, Qt.DisplayRole)
            headers.append(header)
        table = obj.preview_table_data(self.data_models[row_index].small_class_models)
        return headers, table
    @staticmethod
    def convert_qdate_to_datetime(qdate: QDate):
        """ 将日期文本转换成
        :param qdate: QDate
        :return:
        """
        date_str = datetime.strftime(qdate.toPyDateTime(), '%Y-%m-%d %H:%M:%S')
        return date_str
    def resizeEvent(self, event: QResizeEvent):
        """ 调整大小事件 """
        super().resizeEvent(event)
        self.loading_widget.resize(self.ui.tab.size())
        self.loading_widget.move(self.ui.tab.pos())
    def chart_load_data(self, map_size_and_pos_failure):
        """ 图表加载数据
        :param map_size_and_pos_failure: 格式如下
        {
            "产品尺寸1": [
                [(1,1),(2,1),(3,2)],    
                "failure_percent",
                [product_id]
            ],
            "产品尺寸2":[
                [],
                "",
                [product_id]
            ]
        }
        {(产品尺寸, 产品型号): {"隐裂":[product_id,product_id],[(1,1),(2,2),(3,3)]}}
        :param positions: 所有的缺陷位置
        :return:
        """
        chart_data = {}
        for product_size, postions_failure_products in map_size_and_pos_failure.items():
            positions, failure_percent = postions_failure_products
            flatten_items = []
            for item in self.flatten(positions):
                flatten_items.append(tuple(item)) if item else flatten_items.append(item)
            pos_set = set(flatten_items)
            postions_data = []  
            for pos in pos_set:
                if pos:  
                    postions_data.append((pos[0] - 1, pos[1] - 1, flatten_items.count(pos)))
            chart_data.update({product_size: [postions_data, failure_percent]})
        self.ui.q_charts.set_charts(chart_data)
    def heatmap_load_data(self, map_defects_positions):
        """ 热力图加载数据
        :param map_defects_positions: 所有缺陷的缺陷位置 
        20200617 需求：需要选择每一个【缺陷类】后，才可以显示对应的缺陷类热力图
        """
        try:
            self.ui.q_heatmap.set_map_defects_and_positions(map_defects_positions)  
            self.ui.q_heatmap.slot_change_filter_index(0)  
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("绘制热力图失败")
class UI_DefectPosStatistics(object):
    def __init__(self, parent):
        styleFile = 'qss/statistics.qss'
        qss = CommonHelper.readQss(styleFile)
        parent.setStyleSheet(qss)
        parent.setWindowTitle("缺陷位置分布统计")
        layout = QVBoxLayout(parent)
        self.filters_pannel = FiltersPannel()
        layout.addWidget(self.filters_pannel)
        self.tab = QTabWidget()
        layout.addWidget(self.tab)  
        self.statistics_table = DefectPosTable()
        self.tab.addTab(self.statistics_table, "列表")
        self.q_charts = QChartFrame()
        self.tab.addTab(self.q_charts, "图表")
        self.q_heatmap = QHeatMap()
        self.tab.addTab(self.q_heatmap, "热力图")
class FiltersPannel(QFrame):
    """ 搜索条件面板 """
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        title = QLabel("缺陷位置分布统计")
        title.hide()
        title.setObjectName("h1")
        layout.addWidget(title)  
        layout.addItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout2 = QGridLayout()
        self.cb_detect_type = ComboBoxGroup("检测方式:", ["AI检测", "人工复检"])
        layout2.addWidget(self.cb_detect_type, 0, 0)
        self.cb_line = ComboBoxGroup("生产线:", ["全部", "L2", "L3"])
        layout2.addWidget(self.cb_line, 0, 1)
        self.cb_weld = ComboBoxGroup("串焊机:", ["全部", "1号", "2号", "3号", "4号", "5号", "6号"])  
        layout2.addWidget(self.cb_weld, 0, 2)
        self.date_group = DateGroup('起止时间:')
        layout2.addWidget(self.date_group, 0, 3, 1, 3)
        self.cb_defect_big_class = ComboBoxGroup("缺陷大类:", ["全部", "VI", "EL"])
        layout2.addWidget(self.cb_defect_big_class, 1, 0)
        self.cb_defect_type = ComboBoxGroup("缺陷类型:", [])
        layout2.addWidget(self.cb_defect_type, 1, 1)
        self.cb_statistics_dimension = ComboBoxGroup("统计维度:", ["产品尺寸", '产品型号'])
        layout2.addWidget(self.cb_statistics_dimension, 1, 2)
        self.cb_product_size = ComboBoxGroup("产品尺寸:", ["全部"])
        layout2.addWidget(self.cb_product_size, 1, 3)
        layout.addLayout(layout2)
        self.btn_search = IconButton(':/icons/search.png')
        layout.addWidget(self.btn_search)
        self.btn_download = IconButton(':/icons/download.png')
        layout.addWidget(self.btn_download)
    def init_data(self):
        """ 初始化数据 """
        pass
class DefectPosTable(QTableWidget):
    signal_defect_class_small_btn_clicked = pyqtSignal(list)
    def __init__(self, *args):
        super().__init__(*args)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setHighlightSections(False)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)  
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)  
        self.setAlternatingRowColors(True)  
        self.verticalHeader().setHidden(True)  
        headers = ['序号', '产品尺寸', '缺陷总数', '单产品缺陷平均数', '缺陷类型数量', '最高缺陷位', '总体不良率']
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        self.data = []
        self.set_column_width(0, 80)
    def set_column_width(self, index, width):
        """ 指定列宽 """
        self.horizontalHeader().setSectionResizeMode(index, QHeaderView.Custom)
        self.setColumnWidth(index, width)
    def update_data(self, rows_data):
        """ 更新数据 """
        self.setRowCount(len(rows_data))
        self.data = []
        for i, model in enumerate(rows_data):
            temp_statistics_dimension = model.temp_statistics_dimension
            row_data = [
                i + 1,  
                temp_statistics_dimension,  
                model.defects_sum_num,  
                model.average_defects,  
                model.defect_small_class_num,  
                model.most_defect_pos,  
                model.failure_percent,  
            ]
            self.data.append(row_data)
            for col, data in enumerate(row_data):
                if col == 4:
                    q_btn = QPushButton(str(data))
                    q_btn.setStyleSheet("""
                        border: none;
                        background-color: rgba(0,0,0,0);
                        color: rgb(19, 140, 222)
                    """)
                    q_btn.setCursor(Qt.PointingHandCursor)
                    q_btn.clicked.connect(self.slot_defect_class_small_btn_clicked(model.small_class_models))
                    self.setCellWidget(i, col, q_btn)
                else:
                    q_table_item = QTableWidgetItem()
                    q_table_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    q_table_item.setText(str(data))
                    self.setItem(i, col, q_table_item)
    def slot_defect_class_small_btn_clicked(self, s_class_models):
        """ 点击缺陷小类数量按钮 slot
        :param s_class_models: 缺陷小类 model 数据列表 [DefectStatisticSmallModel, DefectStatisticSmallModel, ...]
        :return:
        """
        try:
            def wrapper():
                self.signal_defect_class_small_btn_clicked.emit(s_class_models)
            return wrapper
        except Exception as e:
            logger.error(e, exc_info=True)
class QChartFrame(QFrame):
    signal_chart_frame_resize = pyqtSignal(QSize)
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout_widget = []
        self.table_class = DefectRateTableChart
    def set_charts(self, charts_data):
        """ 统计界面显示的 chart 图表
        :param charts_data: {产品尺寸:[[(0,0,count),(1,1,count),(2,2,count)], "failure_percent"]}
        """
        self.clear_data()
        for product_size, pos_failure in charts_data.items():
            positions_data, failure_percent = pos_failure
            title = QLabel(f"产品尺寸({product_size})缺陷位统计图表")
            title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout.addWidget(title)
            if product_size is None:
                continue
            new_table = self.table_class()
            _row, _col = product_size.split("*")
            new_table.set_product_spec(int(_row), int(_col))
            new_table.load_data(positions_data, failure_percent)
            self.layout.addWidget(new_table)
            self.layout_widget.append(new_table)
            self.layout_widget.append(title)
            self.layout_widget.append(new_table)
    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        self.signal_chart_frame_resize.emit(self.size())
    def clear_data(self):
        """ 清空面板数据 """
        logger.info("清空缺陷位图表数据")
        for item in self.layout_widget:
            self.layout.removeWidget(item)
            item.close()
        self.layout_widget = []
class QHeatMap(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_ui()
        self.map_defects_and_pos = {}
        self.init_heatmap_page()  
        self.shared = Shared()
        self.init_channel()
        self.bind_events()
        self.map_defects_and_pos = {}
        self.echarts_js = ""  
        self.bind_events()
    def init_ui(self):
        """
        初始化样式
        :return:
        """
        layout = QVBoxLayout(self)
        layout_1 = QHBoxLayout()
        layout.addLayout(layout_1)
        layout_1.addItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum))
        combobox_product_size = ComboBoxGroup("产品尺寸:", [])
        combobox_product_size.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.product_size_combobox = combobox_product_size.comboBox
        layout_1.addWidget(combobox_product_size)
        combobox_group = ComboBoxGroup("缺陷类型:", [])
        combobox_group.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.defects_combobox = combobox_group.comboBox
        layout_1.addWidget(combobox_group)
        layout_1.addItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.heatmap_view = QWebEngineView()
        self.heatmap_view.setContextMenuPolicy(Qt.NoContextMenu)
        layout.addWidget(self.heatmap_view)
    def bind_events(self):
        self.product_size_combobox.currentIndexChanged.connect(self.slot_change_filter_index)
        self.defects_combobox.currentIndexChanged.connect(self.slot_change_filter_index)
    def init_channel(self):
        """
        初始化web页面管道
        :return:
        """
        self.channel = QWebChannel()
        self.channel.registerObject("shared", self.shared)
        self.heatmap_view.page().setWebChannel(self.channel)
    def init_heatmap_page(self):
        try:
            url = QUrl(QFileInfo('dashboard/compiler/heatmap.html').absoluteFilePath())
            self.heatmap_view.load(url)
        except Exception as e:
            logger.error(e)
    def set_map_defects_and_positions(self, map_defects_and_positions):
        """ 设置缺陷位heatmap数据
        :param map_defects_and_positions: 所有缺陷的缺陷位置, {产品尺寸:{"隐裂": [(0,0),(0,1),(2,1)]}}
        :return:
        """
        self.map_defects_and_pos = map_defects_and_positions
        self.product_size_combobox.clear()
        self.product_size_combobox.addItems(list(map_defects_and_positions.keys()))
        self.slot_change_filter_index(0)  
    def get_current_spec(self):
        """ 获取当前选中的产品尺寸 """
        spec = self.product_size_combobox.currentText()
        if spec:
            row_num, col_num = spec.split("*")
        else:
            row_num, col_num = 0, 0
        return int(row_num), int(col_num)
    def slot_change_filter_index(self, index):
        """ 改变当前选中的 product_size 或 defects
        注意：切换的 defect 可能没有对应的缺陷，要置为空
        """
        try:
            current_product_size = self.product_size_combobox.currentText()
            current_defect = self.defects_combobox.currentText()
            if current_product_size:
                current_pos_list = self.map_defects_and_pos.get(current_product_size, {}).get(current_defect, [])
                self.draw_heatmap(current_pos_list)
            else:
                self.draw_heatmap([])
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("切换缺陷类型位置分布热力图失败")
    def draw_heatmap(self, pos_list):
        """ 绘制热力图的方法
        :param pos_list: 缺陷位置列表：[(1,1),(2,3),(1,1),(4,3)] 坐标从 (0,0) 开始(row,col)
        :return:
        """
        rows_num, cols_num = self.get_current_spec()
        cols = [i + 1 for i in range(cols_num)]
        rows = [chr(i + 65) for i in range(rows_num)]
        rows.reverse()
        data = []
        for row in range(rows_num):
            for col in range(cols_num):
                data.append([col, len(rows) - 1 - row, pos_list.count((row, col))])  
        heatmap_data = []
        min_value = 0
        max_value = 0
        for d in data:
            heatmap_data.append([d[0], d[1], d[2] or '-'])  
            if d[2] > max_value:
                max_value = d[2]
            if d[2] < min_value:
                min_value = d[2]
        res = {'x_axis': cols, 'y_axis': rows, 'min_value': min_value, 'max_value': max_value, 'data': heatmap_data}
        self.shared.signal_data_success.emit(json.dumps(res, ensure_ascii=False))
class DefectRateTableChart(QTableWidget):
    """ 不良率表图 """
    def __init__(self, *__args):
        """
        :param __args:
        """
        super().__init__(*__args)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setHighlightSections(False)
        self.verticalHeader().setHidden(True)
        self.spec_row = 0
        self.spec_col = 0
    def set_product_spec(self, row, col):
        """ 设置产品规格，用来重新加载表格尺寸
        :param row: int
        :param col: int
        :return:
        """
        self.spec_row = row
        self.spec_col = col
        col_labels = [""]
        col_labels.extend([str(i + 1) for i in range(col)])
        col_labels.extend(["不良率"])
        self.setColumnCount(len(col_labels))
        self.setHorizontalHeaderLabels(col_labels)
        row_labels = [chr(i + 65) for i in range(row)]
        self.setRowCount(len(row_labels))
        for i, text in enumerate(row_labels):
            item = QTableWidgetItem(text)
            item.setTextAlignment(Qt.AlignCenter)
            self.setItem(i, 0, item)
        self.setSpan(0, len(col_labels) - 1, len(row_labels), 1)
        self.set_column_width(0, 30)
        self.set_column_width(len(col_labels) - 1, 100)  
    def set_column_width(self, index, width):
        """ 指定列宽 """
        self.horizontalHeader().setSectionResizeMode(index, QHeaderView.Custom)
        self.setColumnWidth(index, width)
    def load_data(self, positions_data, failure_percent):
        """ 加载数据
        :param positions_data: index 从 0 开始的数据 (row_index, col_index, data)
        """
        try:
            for pos_data in positions_data:
                row_index, col_index, data = pos_data
                if col_index + 1 > self.spec_col or row_index + 1 > self.spec_row:
                    continue
                if col_index < 0:  
                    continue
                col_index += 1
                item = QTableWidgetItem(str(data))
                item.setTextAlignment(Qt.AlignCenter)
                self.setItem(row_index, col_index, item)
            item = QTableWidgetItem(str(failure_percent))
            item.setTextAlignment(Qt.AlignCenter)
            self.setItem(0, self.columnCount() - 1, item)
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("加载缺陷位置图表数据失败")
class Shared(QObject):
    """
    连接web页面管道类
    """
    signal_data_success = pyqtSignal(str)  
    signal_data_error = pyqtSignal(str)  
    def __init__(self, parent=None):
        super(Shared, self).__init__(parent=parent)
class DefectPosSmallStatistics(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = UI_DefectPosSmallStatistics(self)
        self.bind_events()
    def bind_events(self):
        """ 绑定事件 """
        self.ui.btn_back.clicked.connect(self.slot_btn_back_clicked)
    def load_data(self, current_statistics_dimension_index, models):
        """ 加载表格数据
        :param current_statistics_dimension_index: 当前统计维度索引
        :param models: 模型列表 [DefectPosStatisticSmallModel,DefectPosStatisticSmallModel,...]
        :return:
        """
        try:
            if current_statistics_dimension_index == 0:
                self.ui.statistics_table.setHorizontalHeaderItem(1, QTableWidgetItem("产品尺寸"))
            else:
                self.ui.statistics_table.setHorizontalHeaderItem(1, QTableWidgetItem("产品型号"))
            self.ui.statistics_table.update_data(models)
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("缺陷位置小类页面加载数据出错")
    def slot_btn_back_clicked(self):
        """ 返回上级 """
        try:
            self.parent().parent().parent().init_navigation_bar_fun(
                [{"统计分析 | 串件缺陷位置分布统计": self.parent().unpacked_DefectPosStatistics_index}])
            self.parent().setCurrentIndex(self.parent().unpacked_DefectPosStatistics_index)
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("返回上级列表失败")
class UI_DefectPosSmallStatistics(object):
    def __init__(self, parent):
        styleFile = 'qss/statistics.qss'
        qss = CommonHelper.readQss(styleFile)
        parent.setStyleSheet(qss)
        parent.setWindowTitle("缺陷位置分布统计")
        layout = QVBoxLayout(parent)
        layout_1 = QHBoxLayout()
        title = QLabel("缺陷类型分组统计")
        title.hide()
        title.setObjectName("h1")
        layout_1.addWidget(title)  
        layout_1.addItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addLayout(layout_1)
        self.tab = QTabWidget()
        layout.addWidget(self.tab)  
        self.statistics_table = DefectPosSmallTable()
        self.tab.addTab(self.statistics_table, "列表")
        layout_3 = QHBoxLayout()
        layout_3.addItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.btn_back = QPushButton("返回上级")
        self.btn_back.setObjectName('back_btn')
        self.btn_back.setCursor(Qt.PointingHandCursor)
        layout_3.addWidget(self.btn_back)
        layout_3.addItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addLayout(layout_3)
class QChartFrame(QFrame):
    signal_chart_frame_resize = pyqtSignal(QSize)
    def __init__(self, parent=None):
        super().__init__(parent=parent)
    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        self.signal_chart_frame_resize.emit(self.size())
class DefectPosSmallTable(QTableWidget):
    def __init__(self, *args):
        super().__init__(*args)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setHighlightSections(False)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)  
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)  
        self.setAlternatingRowColors(True)  
        self.verticalHeader().setHidden(True)  
        headers = ['序号', '产品尺寸', '缺陷小类', '缺陷数量', '占比', '产品数量', '最高缺陷位', '不良率']
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        self.set_column_width(0, 80)
    def set_column_width(self, index, width):
        """ 指定列宽 """
        self.horizontalHeader().setSectionResizeMode(index, QHeaderView.Custom)
        self.setColumnWidth(index, width)
    def preview_table_data(self, data):
        """ 预览表格数据，用作下载 """
        results = []
        for i, model in enumerate(data):
            results.append([
                i + 1,  
                model.temp_statistics_dimension,  
                model.defect_class_name,  
                model.defects_num,  
                model.defects_percent,  
                model.product_num,  
                model.most_defect_pos,  
                model.failure_percent,  
            ])
        return results
    def update_data(self, rows_data):
        """ 更新截面数据 """
        self.setRowCount(len(rows_data))
        for i, model in enumerate(rows_data):
            row_data = [
                i + 1,  
                model.temp_statistics_dimension,  
                model.defect_class_name,  
                model.defects_num,  
                model.defects_percent,  
                model.product_num,  
                model.most_defect_pos,  
                model.failure_percent,  
            ]
            for col, data in enumerate(row_data):
                q_table_item = QTableWidgetItem()
                q_table_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                q_table_item.setText(str(data))
                self.setItem(i, col, q_table_item)
class ErrorOmissionStatistics(QWidget):
    def __init__(self, main_window, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_window = main_window
        self.ui = UI_ErrorOmissionStatistics(self)
        self.start_date = self.ui.filters_pannel.date_group.start_date  
        self.end_date = self.ui.filters_pannel.date_group.end_date  
        self.cb_statistics_dimension = self.ui.filters_pannel.cb_statistics_dimension.comboBox  
        self.btn_search = self.ui.filters_pannel.btn_search  
        self.btn_download = self.ui.filters_pannel.btn_download  
        self.progress_bar = ProgressBarWindow(value_show=False)  
        self.start_time_for_excel = ""  
        self.end_time_for_excel = ""  
        self.dimension_for_excel = ""  
        self.btn_download.setEnabled(self.main_window.get_system_func("defect_statistic_download"))
        self.current_statistics_dimension_index = 0  
        self.is_loading = False  
        self.loading_widget = LoadingWidget(":/icons/loading.gif", parent=self)
        self.data_rows = []  
        self.xlsx_data = {}
        self.cruds = errorAndOmission()
        self.bind_event()
    def bind_event(self):
        """ 绑定事件 """
        self.btn_search.clicked.connect(self.slot_btn_search_clicked)
        self.btn_download.clicked.connect(self.slot_btn_download_clicked)
    def slot_detect_type_index_changed(self, index):
        """ 修改检测方式 """
        try:
            if index == 2:
                InformationMessageBoxOne("按【人工复检】统计暂未实现，需对接控制台")
                self.cb_detect_type.setCurrentIndex(0)
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("切换检测方式出错")
    def slot_btn_search_clicked(self):
        """ 点击搜索按钮处理函数 """
        try:
            if self.loading_widget.is_loading:
                InformationMessageBoxOne("查询统计完成之后，才可再次查询")
                return
            self.ui.statistics_table.setRowCount(0)  
            self.loading_widget.start()  
            self.ui.statistics_table.setHorizontalHeaderItem(2, QTableWidgetItem(
                self.cb_statistics_dimension.currentText()))
            self.start_time_for_excel = self.start_date.text()
            self.end_time_for_excel = self.end_date.text()
            self.dimension_for_excel = self.cb_statistics_dimension.currentText()
            self.req_statistics_info()  
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("产品误判率和漏检率统计出错")
    def slot_btn_download_clicked(self):
        """ 点击下载按钮处理函数 """
        try:
            if not self.main_window.get_system_func('defect_product_wupan_loujian_download'):
                return InformationMessageBoxOne("暂无权限下载，请联系管理员")
            if not self.data_rows:  
                InformationMessageBoxOne("没有数据可供下载，请先查询")
                return
            if self.loading_widget.is_loading:
                InformationMessageBoxOne("正在查询数据，请稍后下载")
                return
            file_name = f"串件产品误判率和漏检率统计报表_{datetime.now().strftime('%Y%m%d')}.xlsx"
            file_path = gen_xlsx_path(file_name, "串件产品误判率和漏检率统计报表")
            if not file_path:
                return
            self.download_excel(file_path)
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("下载产品误判率和漏检率统计报表出错")
    def download_excel(self, file_path):
        """ 下载 excel 数据 """
        self.progress_bar.set_title("正在下载 %s" % os.path.basename(file_path))
        self.progress_bar.show()
        download_th = AsyncDownloadUnpackedErrorOmission(file_path, self.xlsx_data, self)
        download_th.signal_result.connect(self.slot_download_success)
        download_th.signal_result_error.connect(self.slot_download_error)
        download_th.start()
    def slot_download_success(self, data):
        """
        下载成功槽函数
        :param data:
        :return:
        """
        if self.progress_bar:
            self.progress_bar.close()
        InformationMessageBoxOne("下载完成")
    def slot_download_error(self, data):
        """
        下载失败槽函数
        :param data:
        :return:
        """
        if self.progress_bar:
            self.progress_bar.close()
        try:
            raise data.get("error")
        except SheetTitleException as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne(f"工作表包含不允许的字符")
        except PermissionError as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne(f"下载产品误判率和漏检率统计报表出错, 该文件处于使用状态")
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("下载产品误判率和漏检率统计报表出错")
    def req_statistics_info(self):
        """ 异步请求统计信息 """
        try:
            start_datetime = self.convert_qdate_to_datetime(self.start_date.date)  
            end_datetime = self.convert_qdate_to_datetime(self.end_date.date)  
            statistics_dimension_index = self.cb_statistics_dimension.currentIndex()  
            user_info_dict = self.main_window.user
            user_id = user_info_dict['id']
            role_type = user_info_dict['role_type']
            self.data_th = AsynThread(
                self.cruds.retrieve,
                args=(start_datetime, end_datetime, statistics_dimension_index, user_id, role_type),
                parent=self
            )
            self.data_th.signal_result.connect(self.slot_get_statistics_info)
            self.data_th.signal_result_error.connect(self.slot_get_statistics_info_error)
            self.data_th.start()
        except Exception as e:
            logger.error(str(e), exc_info=True)
    def slot_get_statistics_info(self, models):
        """ 异步处理统计数据
        :param models:
        """
        try:
            data_rows, charts, xlsx_data = models
            self.data_rows = data_rows
            self.xlsx_data = xlsx_data
            self.ui.statistics_table.update_data(data_rows)
            self.chart_load_data(charts)
        except Exception as e:
            self.data_rows = []  
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("处理查询的统计数据出错")
        finally:
            self.loading_widget.stop()  
    def slot_get_statistics_info_error(self, *args):
        """
        查询数据失败槽函数
        """
        try:
            self.loading_widget.stop()
        except Exception as e:
            logger.error(e, exc_info=True)
        CriticalMessageBoxOne("获取统计数据失败")
    def chart_load_data(self, charts):
        """ 图表加载数据
        :param charts: [(chart1_args,chart1_kwargs),(chart2_args,chart2_kwargs)]
        """
        try:
            self.ui.q_charts.clear()
            pro_counts = len(charts[0][0][1])
            for i, chart in enumerate(charts):
                bar = BarGraph()
                bar.set_bar_width(0.025 * pro_counts)
                bar.set_bar_margin(0.005 * pro_counts)
                bar.set_bar_bgcorlor(QColor(70, 70, 70))
                bar.set_data_frame(*chart[0], **chart[1])
                self.ui.q_charts.add_widget(bar)
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("绘制图表出错")
    def resizeEvent(self, event: QResizeEvent):
        """ 调整大小事件 """
        super().resizeEvent(event)
        self.loading_widget.resize(self.ui.tab.size())
        self.loading_widget.move(self.ui.tab.pos())
    def convert_qdate_to_datetime(self, qdate: QDate):
        """ 将日期文本转换成
        :param qdate: QDate
        """
        date_str = datetime.strftime(qdate.toPyDateTime(), '%Y-%m-%d %H:%M:%S')
        return date_str
class UI_ErrorOmissionStatistics(object):
    def __init__(self, parent):
        styleFile = 'qss/statistics.qss'
        qss = CommonHelper.readQss(styleFile)
        parent.setStyleSheet(qss)
        parent.setWindowTitle("产品误判率和漏检率统计")
        layout = QVBoxLayout(parent)
        self.filters_pannel = FiltersPannel()
        layout.addWidget(self.filters_pannel)
        self.tab = QTabWidget()
        layout.addWidget(self.tab)  
        self.statistics_table = DefectList()
        self.tab.addTab(self.statistics_table, "列表")
        self.q_charts = QChartFrame()
        self.tab.addTab(self.q_charts, "图表")
class FiltersPannel(QFrame):
    """ 搜索条件面板 """
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        title = QLabel("产品误判率和漏检率统计")
        title.hide()
        title.setObjectName("h1")
        layout.addWidget(title)  
        layout.addItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout2 = QGridLayout()
        self.date_group = DateGroup('起止时间:')
        layout2.addWidget(self.date_group, 0, 1, 1, 3)
        self.cb_statistics_dimension = ComboBoxGroup("统计维度:", ['生产线', '检测任务'])
        layout2.addWidget(self.cb_statistics_dimension, 0, 0)
        layout.addLayout(layout2)
        self.btn_search = IconButton(':/icons/search.png')
        layout.addWidget(self.btn_search)
        self.btn_download = IconButton(':/icons/download.png')
        layout.addWidget(self.btn_download)
class QChartFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.widgets = []
    def add_widget(self, widget):
        try:
            self.widgets.append(widget)
            self.layout.addWidget(widget)
        except Exception as e:
            logger.error(e, exc_info=True)
    def clear(self):
        """ 清除数据 """
        for widget in self.widgets:
            self.layout.removeWidget(widget)
        self.widgets = []
class DefectList(QTableWidget):
    def __init__(self, *args):
        super().__init__(*args)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setHighlightSections(False)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)  
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)  
        self.setAlternatingRowColors(True)  
        self.verticalHeader().setHidden(True)  
        headers = ['序号', '产品类型', '生产线', '串焊机', '产品数量', 'AI合格数量', 'AI缺陷数量', '复检缺陷数量',
                   '人工合格数', '差异数量', '误判数量', '误判率', '漏检数量', '漏检率', '准确率']
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        self.data = []
        self.set_column_width(0, 80)
    def set_column_width(self, index, width):
        """ 指定列宽 """
        self.horizontalHeader().setSectionResizeMode(index, QHeaderView.Custom)
        self.setColumnWidth(index, width)
    def update_data(self, rows_data):
        """ 更新数据 """
        self.setRowCount(len(rows_data))
        self.data = []
        for i, row_data in enumerate(rows_data):
            row_data.insert(0, i + 1)
            self.data.append(row_data)
            for col, data in enumerate(row_data):
                q_table_item = QTableWidgetItem()
                q_table_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                q_table_item.setText(str(data))
                self.setItem(i, col, q_table_item)
class AsynThread(QThread):
    """ 异步线程 """
    signal_result = pyqtSignal(object, dict)
    signal_result_error = pyqtSignal(object, dict)
    def __init__(self, callback, args=(), kwargs={}, delivery={}, parent=None):
        super().__init__(parent=parent)
        self.callback = callback
        self.args = args
        self.kwargs = kwargs
        self.delivery = delivery
    def run(self):
        try:
            result = self.callback(*self.args, **self.kwargs)
            self.signal_result.emit(result, self.delivery)
        except Exception as e:
            logger.error(f"异步线程捕获异常: {e}", exc_info=True)
            self.signal_result_error.emit(e, self.delivery)
class AsyncDownload(QThread):
    """
    异步下载表格数据
    """
    signal_result = pyqtSignal(object)
    signal_result_error = pyqtSignal(object)
    def __init__(self, file_path, sheets, parent=None):
        super(AsyncDownload, self).__init__(parent=parent)
        self.file_path = file_path
        self.sheets = sheets
    def run(self):
        try:
            XlsxWtiter().save_excel(self.sheets, self.file_path)
        except Exception as e:
            self.signal_result_error.emit({"error": e})
        else:
            self.signal_result.emit({"file_path": self.file_path})
class AsyncDownloadPackedDetectPos(QThread):
    """
    异步下载缺陷位置表格数据
    """
    signal_result = pyqtSignal(object)
    signal_result_error = pyqtSignal(object)
    def __init__(self, sum_data, detail_data, sub_data, detect_type, dimension, time_range, file_path, parent=None):
        """
        :param sum_data: 主表数据
        :param detail_data: 详情表数据
        :param sub_data: 子表数据
        :param detect_type: 检测类型
        :param time_range: 时间范围
        :param parent:
        """
        super(AsyncDownloadPackedDetectPos, self).__init__(parent=parent)
        self.sum_data = sum_data
        self.detail_data = detail_data
        self.sub_data = sub_data
        self.detect_type = detect_type
        self.time_range = time_range
        self.file_path = file_path
        self.dimension = dimension
    def run(self) -> None:
        try:
            DefectPosExcel(self.sum_data, self.detail_data, self.sub_data, self.detect_type, self.dimension,
                           self.time_range).save(self.file_path)
        except Exception as e:
            self.signal_result_error.emit({"error": e})
        else:
            self.signal_result.emit({"file_path": self.file_path})
class AsyncDownloadPackedErrorOmission(QThread):
    """
    异步下载表格数据
    """
    signal_result = pyqtSignal(object)
    signal_result_error = pyqtSignal(object)
    def __init__(self, file_path, data, parent=None):
        super(AsyncDownloadPackedErrorOmission, self).__init__(parent=parent)
        self.file_path = file_path
        self.data = data
    def run(self):
        try:
            packedErrorOmissionExcel(self.data).save(self.file_path)
        except Exception as e:
            self.signal_result_error.emit({"error": e})
        else:
            self.signal_result.emit({"file_path": self.file_path})
class AsyncDownloadUnpackedErrorOmission(QThread):
    """
    异步下载表格数据
    """
    signal_result = pyqtSignal(object)
    signal_result_error = pyqtSignal(object)
    def __init__(self, file_path, data, parent=None):
        super(AsyncDownloadUnpackedErrorOmission, self).__init__(parent=parent)
        self.file_path = file_path
        self.data = data
    def run(self):
        try:
            unpackedErrorOmissionExcel(self.data).save(self.file_path)
        except Exception as e:
            self.signal_result_error.emit({"error": e})
        else:
            self.signal_result.emit({"file_path": self.file_path})
class ComboBoxGroup(QFrame):
    def __init__(self, label, options=[], default=0, *args, **kwargs):
        """
        :param label:  显示的标签
        :param options: 下拉框显示的值列表
        :param default: 默认选中索引
        :param args: 默认参数
        :param kwargs: 默认参数
        """
        super().__init__(*args, **kwargs)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(label)
        layout.addWidget(self.label)
        self.comboBox = QComboBox()
        self.comboBox.setView(QListView(self.comboBox))
        self.comboBox.addItems(options)
        self.comboBox.setCurrentIndex(default)
        layout.addWidget(self.comboBox)
class DateGroup(QFrame):
    def __init__(self, label, options=None, default=0, *args, **kwargs):
        """
        :param label:  显示的标签
        :param options: 下拉框显示的值列表
        :param default: 默认选中索引
        :param args: 默认参数
        :param kwargs: 默认参数
        """
        super().__init__(*args, **kwargs)
        qss = CommonHelper.readQss('qss/date_group.qss')
        self.setStyleSheet(qss)
        if options is None:
            options = ['今日', '本周', '本月', '本季度', '本年度']
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(label)
        layout.addWidget(self.label)
        self.start_date = DateLineEdit()
        layout.addWidget(self.start_date)
        layout.addWidget(QLabel('至'))
        self.end_date = DateLineEdit()
        layout.addWidget(self.end_date)
        self.comboBox = QComboBox()
        self.comboBox.setView(QListView(self.comboBox))
        self.comboBox.addItems(options)
        self.comboBox.setCurrentIndex(-1)
        layout.addWidget(self.comboBox)
        self.calendar = QCalendarWidget()
        self.calendar.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup)
        self.__default_combobox_index__ = default
        self.__init_minimumDate__ = self.calendar.minimumDate()
        self.__current_minimumDate__ = self.__init_minimumDate__
        self.__current_lineEdit__ = 0  
        self.bind_event()
        self.init_data()
    def bind_event(self):
        self.comboBox.currentIndexChanged.connect(self.slot_date_range_changed)
        self.comboBox.activated.connect(self.slot_date_range_changed)
        self.start_date.dateTimeChanged.connect(self.start_datetime_changed)
        self.end_date.dateTimeChanged.connect(self.end_datetime_changed)
    def init_data(self):
        self.comboBox.setCurrentIndex(self.__default_combobox_index__)
    def start_datetime_changed(self, qtime):
        self.end_date.setMinimumDateTime(qtime)
    def end_datetime_changed(self, qtime):
        self.start_date.setMaximumDateTime(qtime)
    def show_calendar(self, tx, ty):
        if not self.calendar.isVisible():
            self.calendar.setGeometry(tx, ty, 300, 300)
            self.calendar.show()
            self.calendar.setFocus()  
    def slot_start_date_lineEdit_clicked(self, tx, ty):
        try:
            self.calendar.setMinimumDate(self.__init_minimumDate__)
            self.calendar.setSelectedDate(self.start_date.date)
            self.show_calendar(tx, ty)
            self.__current_lineEdit__ = 0
        except Exception as e:
            logger.error(f"点击开始日期输入框出错, {e}", exc_info=True)
            CriticalMessageBoxOne('点击开始日期输入框出错')
    def slot_end_date_lineEdit_clicked(self, tx, ty):
        try:
            self.calendar.setMinimumDate(self.__current_minimumDate__)
            self.calendar.setSelectedDate(self.end_date.date)
            self.show_calendar(tx, ty)
            self.__current_lineEdit__ = 1
        except Exception as e:
            logger.error(f"点击结束日期输入框出错, {e}", exc_info=True)
            CriticalMessageBoxOne('点击结束日期输入框出错')
    def slot_date_range_changed(self, index):
        """ 下拉列表修改当前日期范围
        """
        try:
            now = datetime.now()
            if index == 0:
                start_date = QDateTime(now.year, now.month, now.day, 0, 0, 0)
                end_date = QDateTime(now.year, now.month, now.day, 23, 59, 59)
            elif index == 1:  
                start = now - timedelta(days=now.weekday())
                end = now + timedelta(days=6 - now.weekday())
                start_date = QDateTime(start.year, start.month, start.day, 0, 0, 0)
                end_date = QDateTime(end.year, end.month, end.day, 23, 59, 59)
            elif index == 2:  
                days = (datetime(now.year, now.month + 1, 1) - datetime(now.year, now.month,
                                                                        1)).days if now.month != 12 else 31
                start_date = QDateTime(now.year, now.month, 1, 0, 0, 0)
                end_date = QDateTime(now.year, now.month, days, 23, 59, 59)
            elif index == 3:  
                last_month = now.month - (now.month - 1) % 3 + 2
                last_days = (datetime(now.year, last_month + 1, 1) - datetime(now.year, last_month,
                                                                              1)).days if last_month != 12 else 31
                start_date = QDateTime(now.year, now.month - (now.month - 1) % 3, 1, 0, 0, 0)
                end_date = QDateTime(now.year, last_month, last_days, 23, 59, 59)
            elif index == 4:  
                start_date = QDateTime(now.year, 1, 1, 0, 0, 0)
                end_date = QDateTime(now.year, 12, 31, 23, 59, 59)
            self.start_date.date = start_date
            self.end_date.date = end_date
            self.__current_minimumDate__ = start_date
        except Exception as e:
            logger.error(f"切换日期范围失败, {e}", exc_info=True)
            CriticalMessageBoxOne('切换日期范围失败')
    def slot_select_date(self, date: QDate = None, datetime_date=None):
        try:
            if self.__current_lineEdit__ == 0:
                self.start_date.date = date
                self.__current_minimumDate__ = date
                if (self.end_date.date is None) or (self.start_date.date > self.end_date.date):
                    self.end_date.date = date
            else:
                self.end_date.date = date
        except Exception as e:
            logger.error(f"点击日历中日期出错, {e}", exc_info=True)
            CriticalMessageBoxOne('点击日历中日期出错')
    def slot_doubleclicked_select_date(self, date: QDate = None, datetime_date=None):
        self.slot_select_date(date, datetime_date)
        self.calendar.close()
class DateLineEdit(QDateTimeEdit):
    def __init__(self, *args, **kwargs):
        super(DateLineEdit, self).__init__()
        self.setCalendarPopup(True)
        self.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.calendarWidget().setVerticalHeaderFormat(QCalendarWidget.ISOWeekNumbers)
    @property
    def date(self):
        return self.dateTime()
    @date.setter
    def date(self, value):
        self.setDateTime(value)
class DateLineEdit1(QLineEdit):  
    signal_date_lineEdit_clicked = pyqtSignal(int, int)
    def __init__(self, *args):
        super().__init__(*args)
        self.setCursor(Qt.PointingHandCursor)
        self.__date__ = None
    def mousePressEvent(self, event: QMouseEvent):
        super().mousePressEvent(event)
        gx, gy = event.globalX(), event.globalY()
        tx = gx - event.x()
        ty = gy - event.y() + self.height()
        self.signal_date_lineEdit_clicked.emit(tx, ty)
    @property
    def date(self):
        return self.__date__
    @date.setter
    def date(self, date: QDate):
        self.__date__ = date
        date_text = "%d-%d-%d" % (date.year(), date.month(), date.day())
        self.setText(date_text)
class BarGraph(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAttribute(Qt.WA_StyledBackground)
        self.margins = [20, 20, 20, 20]
        self.bar_width = 0.2
        self.bar_margin = 0.05
        self.bar_bgcolor = QColor(37, 63, 81)
        self.x_axis_labels = []
        self.data_frame = []
        self.legends = {}
        self.legends_height = 50
        self.x_axis_label_height_times = 3
        self.x_ticks_color = QColor(255, 255, 255)
        self.max_y = 100
        self.show_data_handler = {}
        self.color_map = [
            [QColor(246, 228, 114), QColor(237, 153, 45)],
            [QColor(255, 110, 40), QColor(165, 1, 38)],
            [QColor(110, 228, 33), QColor(28, 82, 2)]
        ]
    def set_bar_bgcorlor(self, color: QColor):
        self.bar_bgcolor = color
    def set_bar_width(self, width):
        self.bar_width = width
    def set_bar_margin(self, width):
        self.bar_margin = width
    def set_marigns(self, top, right, bottom, left):
        self.margins = [top, right, bottom, left]
    def set_legend(self, index, title):
        self.legends.update({
            index: title
        })
    def set_color_map(self, color_map):
        self.color_map = color_map
    def set_data_frame(self, data_frame, x_labels, max_y=100, show_data_handler=None, legends=None):
        self.data_frame = data_frame
        self.x_axis_labels = x_labels
        self.max_y = max_y
        if show_data_handler:
            self.show_data_handler = show_data_handler
        if legends:
            self.legends = legends
    def paintEvent(self, event: QPaintEvent):
        try:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing, True)
            font_size = painter.fontInfo().pixelSize()
            x_labels_height = font_size * self.x_axis_label_height_times
            pen = QPen(Qt.NoPen)
            painter.setPen(pen)
            brush = QBrush(self.bar_bgcolor, Qt.SolidPattern)
            painter.setBrush(brush)
            painter.begin(self)
            painter.save()
            painter.translate(self.margins[3], self.margins[0])
            if self.data_frame and all(self.data_frame):
                width, height = self.width(), self.height()
                tw = width - self.margins[1] - self.margins[3]
                th = height - self.margins[0] - self.margins[2]
                per_scale_w = tw / len(self.x_axis_labels)
                max_bar_h = th - self.legends_height - x_labels_height
                bar_num = len(self.legends)
                max_bar_width = 1 / (bar_num + 2)
                if self.bar_width > max_bar_width:
                    self.bar_width = max_bar_width
                bar_w = self.bar_width * per_scale_w
                for i, x_label in enumerate(self.x_axis_labels):
                    bar_start_x = (1 - self.bar_width * bar_num - self.bar_margin * (
                            bar_num - 1)) * per_scale_w / 2
                    for j in range(bar_num):
                        pen.setColor(self.x_ticks_color)
                        pen.setStyle(Qt.NoPen)
                        painter.setPen(pen)
                        brush.setStyle(Qt.SolidPattern)
                        brush.setColor(self.bar_bgcolor)
                        painter.setBrush(brush)
                        bar_x = bar_start_x + (self.bar_width + self.bar_margin) * per_scale_w * j  
                        painter.drawRect(QRectF(bar_x + per_scale_w * i, self.legends_height, bar_w, max_bar_h))
                        bar_h = (self.data_frame[j][i] / self.max_y) * max_bar_h
                        offset_h = max_bar_h - bar_h
                        lg_color = QLinearGradient(0, self.legends_height + offset_h, 0,
                                                   self.legends_height + max_bar_h)
                        lg_color.setColorAt(0.0, self.color_map[j][1])
                        lg_color.setColorAt(1.0, self.color_map[j][0])
                        painter.setBrush(QBrush(lg_color))
                        painter.drawRect(QRectF(bar_x + per_scale_w * i, self.legends_height + offset_h, bar_w, bar_h))
                        x_label = str(self.x_axis_labels[i])
                        pen.setColor(self.x_ticks_color)
                        pen.setStyle(Qt.SolidLine)
                        painter.setPen(pen)
                        brush.setStyle(Qt.NoBrush)
                        painter.setBrush(brush)
                        x_label = QFontMetrics(self.font()).elidedText(x_label, Qt.ElideRight, per_scale_w - 5)
                        painter.drawText(QRectF(per_scale_w * i, self.legends_height + max_bar_h, per_scale_w - 5,
                                                font_size * self.x_axis_label_height_times), Qt.AlignCenter, x_label)
                        bar_x_center = bar_x + bar_w / 2
                        bar_data_label_x = bar_x_center - per_scale_w / 2 + per_scale_w * i
                        bar_data_label_y = self.legends_height + offset_h - font_size * self.x_axis_label_height_times
                        bar_data_label_h = font_size * self.x_axis_label_height_times
                        bar_data_label_w = per_scale_w
                        bar_data_label = self.show_data_handler.get(j)(
                            self.data_frame[j][i]) if self.show_data_handler.get(j) else str(self.data_frame[j][i])
                        painter.drawText(QRectF(bar_data_label_x, bar_data_label_y, bar_data_label_w, bar_data_label_h),
                                         Qt.AlignCenter, bar_data_label)
                legend_widths = [0]
                for k, legend in enumerate(self.legends):
                    legend_width = self.caculate_text_width(font_size, str(legend))
                    legend_width += 4 * font_size
                    legend_widths.append(legend_width)
                sum_legends_width = sum(legend_widths)
                now_legend_x = tw - sum_legends_width
                for k, legend in enumerate(self.legends):
                    now_legend_x += legend_widths[k]
                    pen.setStyle(Qt.NoPen)
                    painter.setPen(pen)
                    lg_color = QLinearGradient(0, 0, 0, font_size)
                    lg_color.setColorAt(0.0, self.color_map[k][1])
                    lg_color.setColorAt(1.0, self.color_map[k][0])
                    painter.setBrush(QBrush(lg_color))
                    painter.drawEllipse(QRectF(now_legend_x + 3 * font_size, 0, font_size, font_size))
                    pen.setStyle(Qt.SolidLine)
                    pen.setColor(self.color_map[k][0])
                    painter.setPen(pen)
                    brush.setStyle(Qt.NoBrush)
                    painter.setBrush(brush)
                    painter.drawText(now_legend_x, 0, legend_widths[k + 1], self.legends_height, Qt.AlignRight,
                                     str(legend))
            painter.restore()
            painter.end()
        except Exception as e:
            logging.error(e, exc_info=True)
    def caculate_text_width(self, font_size, text):
        """ 计算文本开宽度
        :param font_size:font_size = painter.fontInfo().pixelSize()
        """
        text_len = font_size  
        for s in text:
            if ord(s) < 128:
                text_len += font_size * 1 / 2
            else:
                text_len += font_size * 1
        return text_len
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = QWidget()
    layout = QVBoxLayout(win)
    bar = BarGraph()
    bar.set_bar_width(0.16)
    bar.set_data_frame(
        [
            [1, 2, 3, 4, 5, 6, 7],
            [11, 22, 33, 44, 55, 66, 77],
            [11, 22, 33, 44, 55, 66, 77]
        ],
        [1, 2, 3, 4, 5, 6, 7],
        max_y=100,
        show_data_handler={
            0: lambda x: f"{x}%"
        },
        legends=["这是什么我也不知道", "你说你不知道，其实我也不知道", "这是什么"]
    )
    layout.addWidget(bar)
    win.show()
    sys.exit(app.exec_())
class IconButton(QPushButton):
    def __init__(self, icon, *args):
        """
        :param icon: QIcon 的路径参数
        """
        super(IconButton, self).__init__(*args)
        self.setIcon(QIcon(icon))
        self.setCursor(Qt.PointingHandCursor)
    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        self.resize(QSize(self.height(), self.height()))
class ImgViewer(QDialog):
    def __init__(self):
        super().__init__()
        self.container = None  
        self.loading_container = None  
        self.hbox = None  
        self.loading = None  
        self.data = None  
        self.progress_bar = None  
        self.file_path = None  
        self.th = None  
        self.initUI()
    def initUI(self):
        """
        初始化界面
        :return:
        """
        self.setWindowIcon(QIcon(':/icons/title.png'))
        self.setStyleSheet("""background: white;""")  
        self.setWindowFlags(Qt.WindowCloseButtonHint)  
        self.vbox = QVBoxLayout(self)
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.loading_container = QLabel(self)
        self.loading_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.loading_container.setAlignment(Qt.AlignCenter)
        self.vbox.addWidget(self.loading_container)
        self.setLayout(self.vbox)
        self.resize(1300, 800)
        self.progress_bar = ProgressBarWindow(value_show=True)
    def loading_page(self):
        """
        loading图标
        :return:
        """
        self.loading = QMovie(r"./icons/loading.gif")
        self.loading_container.setMovie(self.loading)
        self.loading.start()
    def remove_loading_page(self):
        """
        移除loading页面
        :return:
        """
        self.loading.stop()
        self.loading_container.setMovie(None)
        self.vbox.removeWidget(self.loading_container)
    def open_img(self, file_path, data):
        """
        打开图片
        :return:
        """
        self.data = data
        file_name = os.path.basename(file_path)
        self.setWindowTitle("正在打开 %s" % file_name)
        self.loading_page()
        self.th = AsynThread(file_path, "./icons/bad_file.png", "./icons/file_not_found.png", 1300, self)
        self.th.signal_result.connect(self.render_img)
        self.th.signal_result_error.connect(self.render_img_error)
        self.th.start()
    def render_img_error(self):
        """
        渲染图片失败
        :return:
        """
        pass
    def render_img(self, data):
        """
        渲染图片
        :param data:
        :return:
        """
        try:
            container = data.get("container")
            ratio = data.get("ratio")
            img_ok = data.get("img_ok")
            self.file_path = data.get("file_path")
            win_title = data.get("win_title")
            if not img_ok:
                container.setScaledContents(False)  
            else:
                container.setScaledContents(True)  
            self.resize(1300, int(1300 / ratio) + 60)
            self.setWindowTitle(win_title)  
            self.vbox.addWidget(container)
            self.remove_loading_page()
            self.render_detail(img_ok)
        except Exception as e:
            print(e)
    def render_detail(self, img_ok):
        """
        渲染详情列表
        :param img_ok:
        :param file_path:
        :return:
        """
        try:
            self.hbox = QHBoxLayout()
            self.spacer = QSpacerItem(30, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)  
            self.hbox.addItem(self.spacer)
            self.task_name_label = QLabel()
            self.task_name_label.setText("任务名称：%s" % self.data[1])
            self.hbox.addWidget(self.task_name_label)
            self.spacer1 = QSpacerItem(30, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)  
            self.hbox.addItem(self.spacer1)
            self.img_name_label = QLabel()
            self.img_name_label.setText("图像名称：%s" % self.data[3])
            self.hbox.addWidget(self.img_name_label)
            self.spacer2 = QSpacerItem(30, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)  
            self.hbox.addItem(self.spacer2)
            self.create_time_label = QLabel()
            self.create_time_label.setText("创建时间：%s" % self.data[6])
            self.hbox.addWidget(self.create_time_label)
            self.spacer3 = QSpacerItem(30, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)  
            self.hbox.addItem(self.spacer3)
            self.download_btn = QPushButton()
            self.download_btn.setStyleSheet("""background: #1997fd; color: white; border: none; border-radius: 5px;""")
            self.download_btn.setText("下载图片")
            self.download_btn.setFixedSize(80, 30)
            if not img_ok:
                self.download_btn.setEnabled(False)
                self.download_btn.setStyleSheet("""background: grey; color: white; border: none; border-radius: 5px;""")
            else:
                self.download_btn.setEnabled(True)
                self.download_btn.clicked.connect(self.download)
                self.download_btn.setCursor(Qt.PointingHandCursor)
            self.hbox.addWidget(self.download_btn)
            self.spacer4 = QSpacerItem(30, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)  
            self.hbox.addItem(self.spacer4)
            self.vbox.addLayout(self.hbox)
        except Exception as e:
            print(e)
    def download(self):
        """
        下载图片
        :return:
        """
        try:
            if not self.file_path:
                CriticalMessageBoxOne("图片路径不存在")
            if not os.path.exists(self.file_path):
                CriticalMessageBoxOne("文件不存在")
            file_name = os.path.basename(self.file_path)
            dst_path = QFileDialog().getSaveFileName(caption=file_name, directory="/" + file_name)[0]
            if not dst_path:
                return
            self.progress_bar.show()
            self.progress_bar.set_title("正在下载 %s" % file_name)
            down_load_th = DownloadThread(self.file_path, dst_path, self)
            down_load_th.signal_result.connect(self.down_load_success)
            down_load_th.signal_processing.connect(self.down_load_processing)
            down_load_th.signal_error.connect(self.down_load_error)
            down_load_th.start()
        except Exception as e:
            print(e)
    def down_load_success(self, data):
        """
        下载成功槽函数
        :param data:
        :return:
        """
        self.progress_bar.close()
        InformationMessageBoxOne("下载成功")
    @staticmethod
    def down_load_error(self):
        """
        下载失败槽函数
        :return:
        """
        self.progress_bar.close()
        CriticalMessageBoxOne("下载失败")
    def down_load_processing(self, percent):
        """
        下载进度槽函数
        :param percent:
        :return:
        """
        self.progress_bar.set_value(percent)
    def stop_load_success(self, evt):
        evt.accept()
    def stop_load_error(self, evt):
        evt.accept()
    def closeEvent(self, evt):
        """
        关闭页面事件
        :param evt:
        :return:
        """
        try:
            if not self.th.isFinished():
                msg = InformationMessageBox("图片正在加载中，是否立即结束？")
                if msg.msg_exec() == QDialog.Rejected:
                    evt.ignore()
                    return
                stop_th = AsyncStopLoading(self.th, self)
                stop_th.signal_success.connect(lambda: self.stop_load_success(evt))
                stop_th.signal_error.connect(lambda: self.stop_load_error(evt))
                stop_th.start()
            else:
                evt.accept()
        except Exception as e:
            print(e)
            evt.accept()
class DownloadThread(QThread):
    """
    下载图片异步线程
    """
    signal_result = pyqtSignal(dict)  
    signal_processing = pyqtSignal(int)  
    signal_error = pyqtSignal()  
    def __init__(self, file_path, dst_path, parent=None):
        """
        :param file_path: 原始图片路径
        :param dst_path: 保存图片路径
        :param parent: 父类
        """
        super(DownloadThread, self).__init__(parent=parent)
        self.file_path = file_path
        self.dst_path = dst_path
    def run(self):
        """
        拷贝文件，并发送进度
        :return:
        """
        try:
            file_size = os.path.getsize(self.file_path)  
            coped_size = 0
            with open(self.file_path, 'rb') as ofp, open(self.dst_path, 'wb') as nfp:
                while True:
                    content = ofp.read(1024 * 8)
                    if not content:
                        break
                    nfp.write(content)
                    coped_size += len(content)  
                    percent = int(coped_size / file_size * 100)  
                    self.signal_processing.emit(percent)
        except:
            self.signal_error.emit()
        else:
            self.signal_result.emit({"file_path": self.file_path, "dst_path": self.dst_path})
class AsynThread(QThread):
    """ 异步线程 """
    signal_result = pyqtSignal(dict)
    signal_result_error = pyqtSignal()
    def __init__(self, file_path, error_file_path, not_found_file_path, img_max_width, parent=None):
        super().__init__(parent=parent)
        self.container = QLabel()
        self.file_path = file_path  
        self.error_file_path = error_file_path  
        self.not_found_file_path = not_found_file_path  
        self.img_max_width = img_max_width  
    def resize(self):
        """
        对图片进行压缩
        :return:
        """
        try:
            file_name = os.path.basename(self.file_path)
            dir_name = os.path.dirname(self.file_path)
            defect_img = os.path.join(dir_name, 'defect_' + file_name)  
            if os.path.exists(defect_img):
                img = cv2.imread(defect_img, cv2.IMREAD_UNCHANGED)  
                if img is None:
                    img = cv2.imread(self.file_path, cv2.IMREAD_UNCHANGED)  
            else:
                img = cv2.imread(self.file_path, cv2.IMREAD_UNCHANGED)  
            if img is None:
                return None
            orign_width, orign_height = img.shape[1], img.shape[0]  
            if orign_width < self.img_max_width:  
                scale_percent = 1
            else:
                scale_percent = self.img_max_width / orign_width
            width, height = int(orign_width * scale_percent), int(orign_height * scale_percent)  
            resized = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)  
            cvimg = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)  
            cvimg = QImage(cvimg.data, width, height, QImage.Format_RGB888)  
            return cvimg
        except Exception as e:
            return None
    def run(self):
        """
        异步加载图片
        :return:
        """
        try:
            ratio = 1.625
            file_name = os.path.basename(self.file_path)
            if not os.path.exists(self.file_path):  
                pixmap = QPixmap(self.not_found_file_path)
                img_ok = False
                file_name = "%s 图片不存在" % file_name
            else:
                resized_img = self.resize()  
                if not resized_img:  
                    img_ok = False
                    pixmap = QPixmap(self.error_file_path)  
                    file_name = "%s 图片已损坏" % file_name
                else:
                    pixmap = QPixmap.fromImage(resized_img)
                    img_ok = True
                    ratio = pixmap.width() / pixmap.height()
            self.container.setPixmap(pixmap)
            self.container.setMaximumSize(self.img_max_width, int(self.img_max_width / ratio))
            self.container.setAlignment(Qt.AlignCenter)
            self.signal_result.emit({"container": self.container, "ratio": ratio, "img_ok": img_ok,
                                     "file_path": self.file_path, "win_title": file_name})
        except Exception as e:
            self.signal_result_error.emit()
class AsyncStopLoading(QThread):
    """
    异步关闭加载图像的线程
    """
    signal_success = pyqtSignal()
    signal_error = pyqtSignal()
    def __init__(self, th, parent):
        super(AsyncStopLoading, self).__init__(parent=parent)
        self.th = th
    def run(self):
        try:
            self.th.quit()
            self.th.wait()
            self.signal_success.emit()
        except Exception as e:
            self.signal_error.emit()
class LoadingWidget(QWidget):
    """ 等待加载的界面 """
    def __init__(self, icon, parent=None):
        """
        :param icon: icon 路径
        """
        super().__init__(parent=parent)
        self.icon_waiting = QMovie(icon)
        self.label = QLabel(self)
        self.setStyleSheet("background-color: rgba(0,0,0,0)")
        self.label.resize(80, 80)
        self.label.setAlignment(Qt.AlignCenter | Qt.AlignHCenter)
        self.label.setMovie(self.icon_waiting)
        self.close()  
        self.is_loading = False  
    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        label_w = self.label.width()
        label_h = self.label.height()
        w, h = self.width(), self.height()
        self.label.move((w - label_w) / 2, (h - label_h) / 2)
    def paintEvent(self, event: QPaintEvent):
        painter = QPainter()
        painter.begin(self)
        try:
            pen = QPen()
            pen.setColor(QColor(0, 0, 0, 0))
            brush = QBrush()
            brush.setColor(QColor(0, 0, 255, 0))
            brush.setStyle(Qt.SolidPattern)
            painter.setPen(pen)
            painter.setBrush(brush)
            painter.drawRect(QRectF(0, 0, self.width(), self.height()))
        except Exception as e:
            logger.error(e, exc_info=True)
        finally:
            painter.end()
    def start(self):
        self.is_loading = True
        self.icon_waiting.start()
        self.show()
    def stop(self):
        self.is_loading = False
        self.icon_waiting.stop()
        self.close()
class ProgressBar(QProgressBar):
    def __init__(self, *args, **kwargs):
        super(ProgressBar, self).__init__(*args, **kwargs)
        self.setValue(0)
    def set_value(self, value):
        self.setValue(value)
class ProgressBarWindow(QWidget):
    def __init__(self, value_show=True, *args, **kwargs):
        super(ProgressBarWindow, self).__init__(*args, **kwargs)
        self.resize(450, 50)
        layout = QVBoxLayout(self)
        self.setWindowIcon(QIcon(':/icons/title.png'))
        self.setWindowFlags(Qt.WindowCloseButtonHint)  
        self.setStyleSheet(StyleSheet)
        if value_show:
            self.progress_bar = ProgressBar(self, minimum=0, maximum=100, textVisible=True,
                                            objectName="radiusProgressBar")
        else:
            self.progress_bar = ProgressBar(self, minimum=0, maximum=0, textVisible=False,
                                            objectName="radiusProgressBar")
        layout.addWidget(self.progress_bar)
    def set_title(self, title):
        """
        设置窗口标题
        :param title:
        :return:
        """
        self.setWindowTitle(title)
    def set_value(self, value):
        """
        设置进度条值
        :param value:
        :return:
        """
        self.progress_bar.set_value(value)
def gen_xlsx_path(file_name, caption="", directory=''):
    file_dialog = QFileDialog()
    file_path = file_dialog.getSaveFileName(directory=os.path.join(directory, file_name), filter="Excel 工作簿(*.xlsx)",
                                            caption=caption)[0]
    return file_path
class XlsxWtiter(object):
    def __init__(self):
        self.workbook = xlsxwriter.Workbook  
    def save_excel(self, sheets, path):
        if not path:
            return
        workbook = self.workbook(path)
        try:
            for sheet in sheets:  
                sheet_title, sheet_data, sheet_formats, sheet_options = sheet
                worksheet = workbook.add_worksheet(sheet_title)
                formats = {}
                for f_name, f_style in sheet_formats.items():
                    formats.update({f_name: workbook.add_format(f_style)})
                cols_width = {}
                for pos, cell in sheet_data.items():
                    if type(pos) == tuple:
                        pos = self.convert_range(*pos)
                    else:
                        pos = self.convert_range(pos)
                    if len(pos) == 4:  
                        if cell.get("merge"):  
                            worksheet.merge_range(*pos, cell["value"], formats[cell["format"]])
                        else:
                            for r in range(pos[0], pos[2] + 1):  
                                for c in range(pos[1], pos[3] + 1):
                                    worksheet.write(r, c, cell["value"], formats[cell["format"]])
                                    width = self.len_byte(str(cell["value"])) + 2  
                                    existed_width = cols_width.get(c, 10.27)
                                    if width > existed_width:  
                                        cols_width.update({c: width})  
                                    else:
                                        cols_width.update({c: existed_width})  
                    else:  
                        worksheet.write(*pos, cell["value"], formats[cell["format"]])
                        width = self.len_byte(str(cell["value"])) + 2  
                        existed_width = cols_width.get(pos[1], 10.27)
                        if width > existed_width:  
                            cols_width.update({pos[1]: width})  
                        else:
                            cols_width.update({pos[1]: existed_width})  
                for col, width in cols_width.items():
                    worksheet.set_column(col, col, width)  
                for row_height in sheet_options.get("height", []):
                    worksheet.set_row(*row_height)  
        except Exception:
            raise
        finally:
            workbook.close()
    @staticmethod
    def convert_range(*args):
        try:
            if len(args):
                int(args[0])
        except ValueError:
            if ':' in args[0]:
                cell_1, cell_2 = args[0].split(':')
                row_1, col_1 = xl_cell_to_rowcol(cell_1)
                row_2, col_2 = xl_cell_to_rowcol(cell_2)
            else:
                row_1, col_1 = xl_cell_to_rowcol(args[0])
                row_2, col_2 = row_1, col_1
            new_args = [row_1, col_1, row_2, col_2]
            new_args.extend(args[1:])
            args = new_args
        return args
    def __auto_scale_width__(self, worksheet, dataTable):
        """ 自动适应宽度
        把每个单元格的值长度都计算并记录下来，取每列最长的,
        那数据格式得定好，每个单元格都必须有值，如果有的 cell 没有值填充 None
        :param worksheet: worksheet 对象
        :param dataTable: worksheet 所有表格的数据
        """
        cols_width = {}
        for r, row in enumerate(dataTable):
            for c, cell in enumerate(row):
                if c == len(cols_width):
                    cols_width.append(10.27)  
                if cell is not None:  
                    width = self.len_byte(str(cell)) + 2
                    if width > 10.27 and width > cols_width[c]:  
                        cols_width[c] = width  
                        worksheet.set_column(c, c, width)  
    @staticmethod
    def len_byte(value):
        """ 计算字符串字节长度 """
        length = len(value)
        utf8_length = len(value.encode('utf-8'))
        length = (utf8_length - length) / 2 + length
        return int(length)
class TaskPerformanceStatistics(QWidget):
    def __init__(self, main_window, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_window = main_window
        self.ui = UI_TaskPerformanceStatistics(self)
        self.start_date = self.ui.filters_pannel.date_group.start_date  
        self.end_date = self.ui.filters_pannel.date_group.end_date  
        self.cb_statistics_dimension = self.ui.filters_pannel.cb_statistics_dimension.comboBox  
        self.btn_search = self.ui.filters_pannel.btn_search  
        self.btn_download = self.ui.filters_pannel.btn_download  
        self.progress_bar = ProgressBarWindow(value_show=False)  
        self.start_time_for_excel = ""  
        self.end_time_for_excel = ""  
        self.dimension_for_excel = ""  
        self.btn_download.setEnabled(self.main_window.get_system_func("defect_statistic_download"))
        self.bind_event()
        self.current_statistics_dimension_index = 0  
        self.is_loading = False  
        self.loading_widget = LoadingWidget(":/icons/loading.gif", parent=self)
        self.data_models = None  
    def bind_event(self):
        """ 绑定事件 """
        self.btn_search.clicked.connect(self.slot_btn_search_clicked)
        self.btn_download.clicked.connect(self.slot_btn_download_clicked)
        self.ui.statistics_table.signal_failure_number_btn_clicked.connect(self.slot_defect_class_small_btn_clicked)
    def slot_btn_search_clicked(self):
        """ 点击搜索按钮处理函数 """
        try:
            if self.loading_widget.is_loading:
                InformationMessageBoxOne("查询统计完成之后，才可再次查询")
                return
            self.ui.statistics_table.setRowCount(0)  
            self.loading_widget.start()  
            self.current_statistics_dimension_index = self.cb_statistics_dimension.currentIndex()  
            current_dimission = self.cb_statistics_dimension.currentText()
            self.ui.statistics_table.setHorizontalHeaderItem(2, QTableWidgetItem(current_dimission))
            self.start_time_for_excel = self.start_date.text()
            self.end_time_for_excel = self.end_date.text()
            self.dimension_for_excel = self.cb_statistics_dimension.currentText()
            self.req_statistics_info()  
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("智能检测任务执行情况统计出错")
    def slot_btn_download_clicked(self):
        """ 点击下载按钮处理函数 """
        if not self.main_window.get_system_func('defect_product_zhinen_download'):
            return InformationMessageBoxOne("暂无权限下载，请联系管理员")
        if not self.data_models:  
            InformationMessageBoxOne("没有数据可供下载，请先查询")
            return
        if self.loading_widget.is_loading:
            InformationMessageBoxOne("正在查询数据，请稍后下载")
            return
        file_name = f"智能检测任务执行情况统计报表_{datetime.now().strftime('%Y%m%d')}.xlsx"
        file_path = gen_xlsx_path(file_name, "下载智能检测任务执行情况统计报表")
        if not file_path:
            return
        try:
            self.download_excel(file_path)
        except FileCreateError as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne(f"下载智能检测任务执行情况统计数据出错, {e}")
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("下载智能检测任务执行情况统计数据出错")
    def download_excel(self, file_path):
        """ 下载 excel 数据 """
        self.progress_bar.set_title("正在下载 %s" % os.path.basename(file_path))
        self.progress_bar.show()
        sheets = []
        formats = {
            "format": {
                'align': 'center',  
                'valign': 'vcenter',  
                'font_size': '12',  
                'border': 1  
            },
            "box_format": {
                'align': 'center',  
                'valign': 'vcenter',  
                'font_size': '12',  
                'fg_color': '
                'top': 1  
            },
            "bg_format": {
                'align': 'center',  
                'valign': 'vcenter',  
                'font_size': '12',  
                'fg_color': '
            },
            "bg_format_border": {
                'align': 'center',  
                'valign': 'vcenter',  
                'font_size': '12',  
                'fg_color': '
                'border': 1  
            }
        }
        options = {
            "height": [(0, 31)]
        }
        sheet1 = [
            "智能检测任务执行情况统计",
            {
                "A1:M1": {
                    "value": "智能检测任务执行情况统计",
                    "format": "bg_format",
                    "merge": True,
                },
                "A2:G2": {
                    "value": None,
                    "format": "box_format",
                },
                "H2": {
                    "value": '统计维度：',
                    "format": "box_format",
                },
                "I2": {
                    "value": self.dimension_for_excel,
                    "format": "box_format",
                },
                "J2": {
                    "value": '时间范围：',
                    "format": "box_format",
                },
                "K2:M2": {
                    "value": f"{self.start_time_for_excel} 至 {self.end_time_for_excel}",
                    "format": "box_format",
                    "merge": True,
                },
            },
            formats,
            options
        ]
        data_1_col_num = self.ui.statistics_table.columnCount()
        for i in range(data_1_col_num):
            header = self.ui.statistics_table.model().headerData(i, Qt.Horizontal, Qt.DisplayRole)
            sheet1[1].update({(2, i): {"value": header, "format": "bg_format_border"}})
            data_rows_1 = self.ui.statistics_table.data
            data_start_index = 3
            for r, row in enumerate(data_rows_1):
                for c, cell in enumerate(row):
                    sheet1[1].update({(r + data_start_index, c): {"value": cell, "format": "format"}})
        sheets.append(sheet1)
        download_th = AsyncDownload(file_path, sheets, self)
        download_th.signal_result.connect(self.slot_download_success)
        download_th.signal_result_error.connect(self.slot_download_error)
        download_th.start()
    def slot_download_success(self, *args):
        """
        下载成功槽函数
        :param args:
        :return:
        """
        if self.progress_bar:
            self.progress_bar.close()
        InformationMessageBoxOne("下载完成")
    def slot_download_error(self, data):
        """
        下载失败槽函数
        :param data:
        :return:
        """
        if self.progress_bar:
            self.progress_bar.close()
        try:
            raise data.get("error")
        except InvalidWorksheetName as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne(f"工作表包含不允许的字符")
        except FileCreateError as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne(f"下载智能检测任务执行情况统计报表出错, 该文件处于使用状态")
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("下载智能检测任务执行情况统计报表出错")
    def req_statistics_info(self):
        """ 异步请求统计信息 """
        try:
            start_datetime = self.convert_qdate_to_datetime(self.start_date.date)  
            end_datetime = self.convert_qdate_to_datetime(self.end_date.date)  
            statistics_dimension_index = self.cb_statistics_dimension.currentIndex()  
            user_info_dict = self.main_window.user
            user_id = user_info_dict['id']
            role_type = user_info_dict['role_type']
            self.data_th = AsynThread(
                smartDefect().retrieve,
                args=(start_datetime, end_datetime, statistics_dimension_index, user_id, role_type),
                parent=self)
            self.data_th.signal_result.connect(self.slot_get_statistics_info)
            self.data_th.signal_result_error.connect(self.slot_get_statistics_info_error)
            self.data_th.start()
        except Exception as e:
            logger.error(str(e), exc_info=True)
    def slot_defect_class_small_btn_clicked(self, models):
        """ 点击缺陷小类数量按钮 slot
        :param models: 缺陷小类 model 数据列表 [DefectPosStatisticSmallModel, DefectPosStatisticSmallModel, ...]
        """
        try:
            self.parent().TaskPerformanceSmallStatistics.load_data(models)
            self.parent().TaskPerformanceSmallStatistics.ui.tab.setCurrentIndex(0)  
            self.main_window.init_navigation_bar_fun(
                [{"统计分析 | 智能检测任务执行情况统计": self.parent().TaskPerformanceStatistics_index},
                 {"检测失败情况统计": self.parent().TaskPerformanceSmallStatistics_index}])
            self.parent().setCurrentIndex(self.parent().TaskPerformanceSmallStatistics_index)
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("检测失败情况统计页面出错")
    def slot_get_statistics_info(self, models):
        """ 异步处理统计数据
        :param models:
        """
        try:
            data, charts = models
            self.data_models = data
            self.ui.statistics_table.update_data(data)
            self.chart_load_data(charts)
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("处理查询的统计数据出错")
        finally:
            self.loading_widget.stop()  
    def slot_get_statistics_info_error(self):
        """
        查询数据失败槽函数
        :return:
        """
        try:
            self.loading_widget.stop()
        except Exception as e:
            logger.error(e, exc_info=True)
        CriticalMessageBoxOne("获取数据失败")
    def chart_load_data(self, charts):
        """ 图表加载数据
        :param charts: [(chart1_args,chart1_kwargs),(chart2_args,chart2_kwargs)]
        """
        try:
            pro_counts = len(charts[0][0][1])
            self.ui.q_charts.clear()
            for i, chart in enumerate(charts):
                bar = BarGraph()
                bar.set_bar_bgcorlor(QColor(70, 70, 70))
                bar.set_bar_width(0.025 * pro_counts)  
                bar.set_bar_margin(0.005 * pro_counts)  
                bar.set_data_frame(*chart[0], **chart[1])
                self.ui.q_charts.add_widget(bar)
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("绘制图表出错")
    def resizeEvent(self, event: QResizeEvent):
        """ 调整大小事件 """
        super().resizeEvent(event)
        self.loading_widget.resize(self.ui.tab.size())
        self.loading_widget.move(self.ui.tab.pos())
    @staticmethod
    def convert_qdate_to_datetime(qdate: QDate):
        """ 将日期文本转换成
        :param qdate: QDate
        """
        date_str = datetime.strftime(qdate.toPyDateTime(), '%Y-%m-%d %H:%M:%S')
        return date_str
class UI_TaskPerformanceStatistics(object):
    def __init__(self, parent):
        styleFile = 'qss/statistics.qss'
        qss = CommonHelper.readQss(styleFile)
        parent.setStyleSheet(qss)
        parent.setWindowTitle("智能检测任务执行情况统计")
        layout = QVBoxLayout(parent)
        self.filters_pannel = FiltersPannel()
        layout.addWidget(self.filters_pannel)
        self.tab = QTabWidget()
        layout.addWidget(self.tab)  
        self.statistics_table = DefectList()
        self.tab.addTab(self.statistics_table, "列表")
        self.q_charts = QChartFrame()
        self.tab.addTab(self.q_charts, "图表")
class FiltersPannel(QFrame):
    """ 搜索条件面板 """
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        title = QLabel("智能检测任务执行情况统计")
        title.hide()
        title.setObjectName("h1")
        layout.addWidget(title)  
        layout.addItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout2 = QGridLayout()
        self.date_group = DateGroup('起止时间:')
        layout2.addWidget(self.date_group, 0, 1, 1, 3)
        self.cb_statistics_dimension = ComboBoxGroup("统计维度:", ["生产线", '产品型号', '检测点'])
        layout2.addWidget(self.cb_statistics_dimension, 0, 0)
        layout.addLayout(layout2)
        self.btn_search = IconButton(':/icons/search.png')
        layout.addWidget(self.btn_search)
        self.btn_download = IconButton(':/icons/download.png')
        layout.addWidget(self.btn_download)
class QChartFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.widgets = []
    def add_widget(self, widget):
        try:
            self.widgets.append(widget)
            self.layout.addWidget(widget)
        except Exception as e:
            logger.error(e, exc_info=True)
    def clear(self):
        """ 清除数据 """
        for widget in self.widgets:
            self.layout.removeWidget(widget)
        self.widgets = []
class DefectList(QTableWidget):
    signal_failure_number_btn_clicked = pyqtSignal(list)
    def __init__(self, *args):
        super().__init__(*args)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setHighlightSections(False)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)  
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)  
        self.setAlternatingRowColors(True)  
        self.verticalHeader().setHidden(True)  
        headers = ['序号', '产品类型', '生产线', '产品分类', '任务数量', '检测方式', '故障次数', '故障率', '平均检测时间(s)',
                   '检测时间最高(s)', '检测时间最低(s)', '检测失败次数', '检测失败率']
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        self.data = []
        self.set_column_width(0, 80)
    def set_column_width(self, index, width):
        """ 指定列宽 """
        self.horizontalHeader().setSectionResizeMode(index, QHeaderView.Custom)
        self.setColumnWidth(index, width)
    def update_data(self, rows_data):
        """ 更新数据 """
        self.setRowCount(len(rows_data))
        self.data = []
        for i, model in enumerate(rows_data):
            row_data = [
                i + 1,  
                model.product_type,  
                model.temp_statistics_dimension,  
                model.obj_type,
                model.task_num,  
                model.detect_type,  
                model.failure_num,  
                model.failure_percent,  
                model.average_detect_time,  
                model.max_detect_time,  
                model.min_detect_time,  
                model.detect_failure_times,  
                model.detect_failure_percent,  
            ]
            self.data.append(row_data)
            btn_qss = """border: none; background-color: rgba(0,0,0,0); color: rgb(19, 140, 222);"""
            for col, data in enumerate(row_data):
                if col == 6:
                    q_btn = QPushButton(str(data))
                    q_btn.setStyleSheet(btn_qss)
                    q_btn.setCursor(Qt.PointingHandCursor)
                    self.setCellWidget(i, col, q_btn)
                elif col == 11:
                    q_btn = QPushButton(str(data))
                    q_btn.setStyleSheet(btn_qss)
                    q_btn.setCursor(Qt.PointingHandCursor)
                    q_btn.clicked.connect(self.slot_failure_number_btn_clicked(model.failure_models))
                    self.setCellWidget(i, col, q_btn)
                else:
                    q_table_item = QTableWidgetItem()
                    q_table_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    q_table_item.setText(str(data))
                    self.setItem(i, col, q_table_item)
    def slot_failure_number_btn_clicked(self, s_class_models):
        """ 点击故障次数按钮 slot
        :param s_class_models: 缺陷小类 model 数据列表 [DefectStatisticSmallModel, DefectStatisticSmallModel, ...]
        :return:
        """
        try:
            def wrapper():
                self.signal_failure_number_btn_clicked.emit(s_class_models)
            return wrapper
        except Exception as e:
            logger.error(e, exc_info=True)
class FailureSmallStatistics(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = UI_FailureSmallStatistics(self)
        self.bind_events()
    def bind_events(self):
        """ 绑定事件 """
        self.ui.btn_back.clicked.connect(self.slot_btn_back_clicked)
    def load_data(self, models):
        """ 加载表格数据
        :param models: 模型列表
        :return:
        """
        try:
            self.ui.statistics_table.update_data(models)
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("检测失败次数加载数据出错")
    def slot_btn_back_clicked(self):
        """ 返回上级 """
        try:
            self.parent().parent().parent().init_navigation_bar_fun(
                [{"统计分析 | 智能检测任务执行情况统计": self.parent().TaskPerformanceStatistics_index}])
            self.parent().setCurrentIndex(self.parent().TaskPerformanceStatistics_index)
        except Exception as e:
            logger.error(e, exc_info=True)
            CriticalMessageBoxOne("返回上级列表失败")
class UI_FailureSmallStatistics(object):
    def __init__(self, parent):
        styleFile = 'qss/statistics.qss'
        qss = CommonHelper.readQss(styleFile)
        parent.setStyleSheet(qss)
        parent.setWindowTitle("缺陷位置分布统计")
        layout = QVBoxLayout(parent)
        layout_1 = QHBoxLayout()
        title = QLabel("缺陷类型分组统计")
        title.hide()
        title.setObjectName("h1")
        layout_1.addWidget(title)  
        layout_1.addItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addLayout(layout_1)
        self.tab = QTabWidget()
        layout.addWidget(self.tab)  
        self.statistics_table = FailureSmallTable()
        self.tab.addTab(self.statistics_table, "列表")
        layout_3 = QHBoxLayout()
        layout_3.addItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.btn_back = QPushButton("返回上级")
        self.btn_back.setObjectName('back_btn')
        self.btn_back.setCursor(Qt.PointingHandCursor)
        layout_3.addWidget(self.btn_back)
        layout_3.addItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addLayout(layout_3)
class FailureSmallTable(QTableWidget):
    def __init__(self, *args):
        super().__init__(*args)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setHighlightSections(False)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)  
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)  
        self.setAlternatingRowColors(True)  
        self.verticalHeader().setHidden(True)  
        headers = ['序号', '任务名称', '产品名称', '图像名称', '检测开始时间', '检测结束时间', '创建时间', '操作']
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        self.set_column_width(0, 80)
        self.img_viewer = ImgViewer()
    def set_column_width(self, index, width):
        """ 指定列宽 """
        self.horizontalHeader().setSectionResizeMode(index, QHeaderView.Custom)
        self.setColumnWidth(index, width)
    def update_data(self, rows_data):
        """ 更新截面数据 """
        self.setRowCount(len(rows_data))
        for i, model in enumerate(rows_data):
            row_data = [
                i + 1,  
                model.get("task_name"),
                model.get("product_name"),
                model.get("img_name"),
                model.get("start_time"),
                model.get("end_time"),
                model.get("create_time"),
                model.get("img_path"),
            ]
            for col, data in enumerate(row_data):
                if col == 0:
                    self.horizontalHeader().setSectionResizeMode(col, QHeaderView.Fixed)
                    self.setColumnWidth(col, 40)
                if col == 7:
                    check_btn = QPushButton('查看')
                    check_btn.setStyleSheet("""background: #1997fd; color: white; border-radius: 4px;""")
                    check_btn.setCursor(QCursor(Qt.PointingHandCursor))
                    check_btn.setFixedSize(60, 24)
                    check_btn.clicked.connect(self.check_btn(row_data))
                    self.horizontalHeader().setSectionResizeMode(col, QHeaderView.Fixed)
                    self.setColumnWidth(col, 100)
                    self.setCellWidget(i, col, check_btn)
                else:
                    q_table_item = QTableWidgetItem()
                    q_table_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    q_table_item.setText(str(data))
                    self.setItem(i, col, q_table_item)
    def check_btn(self, data):
        """
        查看按钮
        :param data: 此数据行的数据
        :return:
        """
        def wrapper():
            try:
                local_dir = CONSTANT.get('local_dir')
                real_path = os.path.join(local_dir, data[7])
                img_viewer = ImgViewer()
                img_viewer.open_img(real_path, data)
                if img_viewer.exec_() in [QDialog.Accepted, QDialog.Rejected]:
                    del img_viewer
            except Exception as e:
                logger.error(e, exc_info=True)
                CriticalMessageBoxOne("打开 %s 图片失败" % data[3])
        return wrapper
    def download_btn(self, img_path):
        def wrapper():
            CriticalMessageBoxOne(img_path)
        return wrapper
class FailureStatisticSmallModel(object):
    def __init__(self):
        self.task_name = ""  
        self.product_name = ""  
        self.img_name = ""  
        self.img_path = ""  
        self.start_time = ""  
        self.end_time = 0  
        self.create_time = ""  

# -*- coding:utf-8 -*-
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QVBoxLayout, QFrame, QApplication
from pyecharts import options as opts
from pyecharts.charts import Pie
from pyecharts.faker import Faker

# c = (
#     Pie()
#         .add("", [list(z) for z in zip(Faker.choose(), Faker.values())])
#         .set_colors(["blue", "green", "yellow", "red", "pink", "orange", "purple"])
#         .set_global_opts(title_opts=opts.TitleOpts(title="Pie-设置颜色"))
#         .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
#         .render("pie_set_color.html")
# )
html = Pie() \
    .add("", [list(z) for z in zip(Faker.choose(), Faker.values())]) \
    .set_colors(["blue", "green", "yellow", "red", "pink", "orange", "purple"]) \
    .set_global_opts(title_opts=opts.TitleOpts(title="Pie-设置颜色")) \
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}")) \
    .render_embed()

# print("html = {}".format(html))
print("type(html) = {}".format(type(html)))


class QPie(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        layout = QVBoxLayout(self)
        self.pie_view = QWebEngineView()
        self.pie_view.setContextMenuPolicy(Qt.NoContextMenu)
        layout.addWidget(self.pie_view)
        self.pie_view.setHtml(html)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = QPie()
    ex.show()
    sys.exit(app.exec_())

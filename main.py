import sys
import pyqtgraph as pg
import pandas as pd
import matplotlib.dates as mdates
from datetime import timedelta, datetime
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, \
    QWidget, QMessageBox, QDialog, QVBoxLayout, QGraphicsView, QGraphicsScene, QSpacerItem, QSizePolicy
from PySide6.QtGui import QPixmap, QMovie
from PySide6.QtCore import Qt, QTimer
from finances import get_difference
from functions import get_id, get_data_for_graph, read_table


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Portfolio against S&P500 by @vikiase")
        self.setWindowState(Qt.WindowMaximized)
        self.welcome_screen = self.create_welcome_screen()
        self.input_screen = self.create_input_screen()
        self.action_screen = self.create_action_screen()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        self.layout.addWidget(self.welcome_screen)

    def create_welcome_screen(self):
        welcome_widget = QWidget()
        layout = QVBoxLayout()

        logo_layout = QHBoxLayout()
        logo_label = QLabel(self)
        pixmap = QPixmap("logo.jpg")
        pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(logo_label)
        logo_layout.setAlignment(Qt.AlignCenter)
        layout.addLayout(logo_layout)
        spacer_top = QSpacerItem(20, 50, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer_top)

        welcome_label = QLabel("Your Portfolio vs the S&P500 - Let's Get Started!")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("font-size: 36px;")
        layout.addWidget(welcome_label)

        start_button = QPushButton("Run Program")
        start_button.setStyleSheet("font-size: 24px; padding: 10px;")
        start_button.clicked.connect(self.show_input_screen)
        layout.addWidget(start_button)

        spacer_bottom = QSpacerItem(20, 50, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer_bottom)

        footer_label = QLabel("Made by @vikiase")
        footer_label.setAlignment(Qt.AlignCenter)
        footer_label.setStyleSheet("font-size: 12px; color: gray;")
        layout.addWidget(footer_label)

        version_label = QLabel("V1.0")
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setStyleSheet("font-size: 12px; color: gray;")
        layout.addWidget(version_label)

        layout.setContentsMargins(20, 20, 20, 20)
        layout.setAlignment(Qt.AlignCenter)
        welcome_widget.setLayout(layout)

        return welcome_widget

    def create_input_screen(self):
        input_widget = QWidget()
        layout = QVBoxLayout()

        input_label = QLabel("Google Sheets link:")
        input_label.setAlignment(Qt.AlignCenter)
        input_label.setStyleSheet("font-size: 24px;")
        layout.addWidget(input_label)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Your Google Sheets link...")
        self.input_field.setStyleSheet("font-size: 18px; padding: 10px;")
        layout.addWidget(self.input_field)

        save_button = QPushButton("Save")
        save_button.setStyleSheet("font-size: 18px; padding: 10px;")
        save_button.clicked.connect(self.save_input)
        layout.addWidget(save_button)

        hint_button = QPushButton("?")
        hint_button.setStyleSheet("font-size: 24px; padding: 10px; background-color: lightgrey; border-radius: 50%;")
        hint_button.clicked.connect(self.show_hint)
        layout.addWidget(hint_button)

        layout.setContentsMargins(20, 20, 20, 20)
        layout.setAlignment(Qt.AlignCenter)
        input_widget.setLayout(layout)
        return input_widget

    def create_action_screen(self):
        """Nastavení obrazovky Action."""
        action_widget = QWidget()
        layout = QVBoxLayout()

        generate_button = QPushButton("Generate graph")
        generate_button.setStyleSheet("font-size: 18px; padding: 10px;")
        generate_button.clicked.connect(self.show_result_screen)
        layout.addWidget(generate_button)

        view_portfolio_button = QPushButton("View Portfolio")
        view_portfolio_button.setStyleSheet("font-size: 18px; padding: 10px;")
        view_portfolio_button.clicked.connect(self.view_portfolio)
        layout.addWidget(view_portfolio_button)

        back_button = QPushButton("Back")
        back_button.setStyleSheet("font-size: 18px; padding: 10px;")
        back_button.clicked.connect(self.show_input_screen)
        layout.addWidget(back_button)

        layout.setContentsMargins(20, 20, 20, 20)
        layout.setAlignment(Qt.AlignCenter)
        action_widget.setLayout(layout)
        return action_widget

    def view_portfolio(self):
        self.clear_layout(self.layout)
        table = read_table(self.extracted_id)
        print(table)
        portfolio_widget = QWidget()
        layout = QVBoxLayout()

        portfolio_label = QLabel("Portfolio Details")
        portfolio_label.setAlignment(Qt.AlignCenter)
        portfolio_label.setStyleSheet("font-size: 24px; color: black; padding: 10px;")
        layout.addWidget(portfolio_label)

        # Replace with actual portfolio data rendering
        portfolio_details = QLabel("Here are the details of your portfolio:\n\n"
                                   "Example Data:\n"
                                   " - Stock A: +10%\n"
                                   " - Stock B: -5%\n"
                                   " - Stock C: +15%")
        portfolio_details.setAlignment(Qt.AlignCenter)
        portfolio_details.setStyleSheet("font-size: 16px; color: black; margin: 20px;")
        layout.addWidget(portfolio_details)

        back_button = QPushButton("Back")
        back_button.setStyleSheet("font-size: 18px; padding: 10px; margin-top: 20px;")
        back_button.clicked.connect(self.show_action_screen)
        layout.addWidget(back_button)

        layout.setContentsMargins(20, 20, 20, 20)
        layout.setAlignment(Qt.AlignCenter)
        portfolio_widget.setLayout(layout)

        self.layout.addWidget(portfolio_widget)

    def save_input(self):
        link = self.input_field.text()
        self.extracted_id = get_id(link)
        print(f"Extrahované ID: {self.extracted_id}")
        QMessageBox.information(self, "Success", "Google Sheets link saved!")
        self.clear_layout(self.layout)
        self.layout.addWidget(self.action_screen)

    def create_graph(self, time):
        today = datetime.today()
        if time == '14 days':
            num_days = 14
        elif time == '1 month':
            num_days = 30
        elif time == '6 months':
            num_days = 180
        elif time == '1 year':
            num_days = 365
        else:
            num_days = float('inf')

        if num_days == float('inf'):
            date_before = datetime(1900, 1, 1)
        else:
            date_before = today - timedelta(days=num_days)

        try:
            self.table = read_table(self.extracted_id)
            port_data, snp_data, buy, sell, invest_list, snp_buy, snp_sell = get_data_for_graph(self.extracted_id, date_before)
        except Exception as e:
            port_data, snp_data, buy, sell, invest_list = get_data_for_graph(self.extracted_id, date_before)

        port_df = pd.DataFrame(port_data)
        snp_df = pd.DataFrame(snp_data)

        if port_df.index.name == 'Date':
            port_df.reset_index(inplace=True)
        port_df.columns = ['Date', 'Price']

        if snp_df.index.name == 'Date':
            snp_df.reset_index(inplace=True)
        snp_df.columns = ['Date', 'Price']

        port_df['Date'] = pd.to_datetime(port_df['Date']).dt.tz_localize(None)
        snp_df['Date'] = pd.to_datetime(snp_df['Date']).dt.tz_localize(None)

        all_dates = pd.date_range(start=port_df['Date'].min(), end=port_df['Date'].max(), freq='D')

        port_df = port_df.set_index('Date').reindex(all_dates).rename_axis('Date').reset_index()
        snp_df = snp_df.set_index('Date').reindex(all_dates).rename_axis('Date').reset_index()

        port_df['Price'] = port_df['Price'].fillna(method='ffill')
        snp_df['Price'] = snp_df['Price'].fillna(method='ffill')

        if time == '14 days':
            date_cutoff = pd.to_datetime('today') - timedelta(days=14)
        elif time == '1 month':
            date_cutoff = pd.to_datetime('today') - timedelta(days=30)
        elif time == '6 months':
            date_cutoff = pd.to_datetime('today') - timedelta(days=180)
        elif time == '1 year':
            date_cutoff = pd.to_datetime('today') - timedelta(days=365)
        elif time == 'Full':
            date_cutoff = pd.to_datetime('1900-01-01')
        else:
            raise ValueError("Unknown time range")

        port_df_filtered = port_df[port_df['Date'] >= date_cutoff]
        snp_df_filtered = snp_df[snp_df['Date'] >= date_cutoff]

        port_df_filtered = port_df_filtered.reset_index(drop=True)
        snp_df_filtered = snp_df_filtered.reset_index(drop=True)

        port_df_filtered.loc[:, 'Date_num'] = mdates.date2num(port_df_filtered['Date'])
        snp_df_filtered.loc[:, 'Date_num'] = mdates.date2num(snp_df_filtered['Date'])

        plot_widget = pg.PlotWidget()
        plot_widget.plot(port_df_filtered['Date_num'], port_df_filtered['Price'], pen='blue', name='Portfolio')
        plot_widget.plot( snp_df_filtered['Date_num'], snp_df_filtered['Price'], pen='white', name='S&P 500')

        num_ticks = len(port_df_filtered)
        tick_interval = 1
        if num_ticks > 20:
            tick_interval = max(1, num_ticks // 20)

        ticks = []
        for i in range(0, num_ticks, tick_interval):
            date = port_df_filtered['Date'][i]
            tick_label = date.strftime('%m-%d')
            ticks.append((mdates.date2num(date), tick_label))

        plot_widget.getAxis('bottom').setTicks([ticks])
        plot_widget.getAxis('bottom').setStyle(showValues=True)

        if date_before != datetime(1900, 1, 1):
            port_diff, port_perc, snp_diff, snp_perc = get_difference(port_df_filtered['Price'], snp_df_filtered['Price'], buy, sell, snp_buy, snp_sell)
        else:
            port_diff, port_perc, snp_diff, snp_perc = get_difference(port_df_filtered['Price'], snp_df_filtered['Price'], buy, sell)

        result_layout = QVBoxLayout()

        portfolio_layout = QHBoxLayout()

        portfolio_label = QLabel("Portfolio profit:")
        portfolio_label.setStyleSheet("font-size: 18px; color: #0000FF;")
        portfolio_layout.addWidget(portfolio_label, alignment=Qt.AlignLeft)

        portfolio_dollar_color = 'green' if port_diff > snp_diff else 'black'
        portfolio_percent_color = 'green' if port_perc > snp_perc else 'black'
        if port_perc < 0:
            portfolio_dollar_color = 'red'
            portfolio_percent_color = 'red'

        portfolio_dollar_label = QLabel(f"${port_diff:.2f}")
        portfolio_dollar_label.setStyleSheet(f"font-size: 18px; color: {portfolio_dollar_color};")
        portfolio_layout.addWidget(portfolio_dollar_label, alignment=Qt.AlignHCenter)

        portfolio_percent_label = QLabel(f"{port_perc:.2f}%")
        portfolio_percent_label.setStyleSheet(f"font-size: 18px; color: {portfolio_percent_color};")
        portfolio_layout.addWidget(portfolio_percent_label, alignment=Qt.AlignRight)

        result_layout.addLayout(portfolio_layout)

        sp500_layout = QHBoxLayout()

        sp500_label = QLabel("S&P500 profit (dynamic investing):")
        sp500_label.setStyleSheet("font-size: 18px; color: black;")
        sp500_layout.addWidget(sp500_label, alignment=Qt.AlignLeft)

        sp500_dollar_color = 'green' if snp_diff > port_diff else 'black'
        sp500_percent_color = 'green' if snp_perc > port_perc else 'black'
        if snp_perc < 0:
            sp500_dollar_color = 'red'
            sp500_percent_color = 'red'

        sp500_dollar_label = QLabel(f"${snp_diff:.2f}")
        sp500_dollar_label.setStyleSheet(f"font-size: 18px; color: {sp500_dollar_color};")
        sp500_layout.addWidget(sp500_dollar_label, alignment=Qt.AlignHCenter)

        sp500_percent_label = QLabel(f"{snp_perc:.2f}%")
        sp500_percent_label.setStyleSheet(f"font-size: 18px; color: {sp500_percent_color};")
        sp500_layout.addWidget(sp500_percent_label, alignment=Qt.AlignRight)

        result_layout.addLayout(sp500_layout)

        result_widget = QWidget()
        result_widget.setLayout(result_layout)

        return plot_widget, result_widget, invest_list

    def create_result_screen(self, time='Full'):
        result_widget = QWidget()
        layout = QVBoxLayout()

        portfolio_label = QLabel("Portfolio vs S&P500 Performance")
        portfolio_label.setAlignment(Qt.AlignCenter)
        portfolio_label.setStyleSheet("font-size: 24px; color: black; padding: 10px;")
        layout.addWidget(portfolio_label)

        plot_widget, result_details, investment_data = self.create_graph(time)

        layout.addWidget(plot_widget)
        layout.addWidget(result_details)

        buttons_layout = QHBoxLayout()
        button_titles = ["14 days", "1 month", "6 months", "1 year", "Full"]
        button_values = [14, 30, 180, 365, 0]
        for title in button_titles:
            button = QPushButton(title)
            button.setStyleSheet("font-size: 18px; padding: 10px; margin: 5px;")
            if len(investment_data) < button_values[button_titles.index(title)]:
                button.setStyleSheet("background-color: gray; color: lightgray;")
                button.setDisabled(True)
                buttons_layout.addWidget(button)
                continue
            button.clicked.connect(lambda checked, t=title: self.update_result_screen(t))
            buttons_layout.addWidget(button)
        layout.addLayout(buttons_layout)

        back_button = QPushButton("Back")
        back_button.setStyleSheet("font-size: 18px; padding: 10px; margin-top: 20px;")
        back_button.clicked.connect(self.show_action_screen)
        layout.addWidget(back_button)

        layout.setContentsMargins(20, 20, 20, 20)
        layout.setAlignment(Qt.AlignCenter)
        result_widget.setLayout(layout)
        return result_widget

    def update_result_screen(self, time):
        self.clear_layout(self.layout)
        self.result_screen = self.create_result_screen(time)
        self.layout.addWidget(self.result_screen)
    def show_input_screen(self):
        self.clear_layout(self.layout)
        self.layout.addWidget(self.input_screen)

    def show_action_screen(self):
        self.clear_layout(self.layout)
        self.layout.addWidget(self.action_screen)

    def show_hint(self):
        hint_dialog = QDialog(self)
        hint_dialog.setWindowTitle("Hint")

        hint_layout = QVBoxLayout()

        hint_label = QLabel("This is how your Google Sheets should look like:")
        hint_label.setAlignment(Qt.AlignCenter)
        hint_label.setStyleSheet("font-size: 20px; margin-bottom: 20px;")
        hint_layout.addWidget(hint_label)

        pixmap = QPixmap("table.png")
        pixmap = pixmap.scaled(800, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_view = QGraphicsView()
        scene = QGraphicsScene()
        scene.addPixmap(pixmap)
        image_view.setScene(scene)
        hint_layout.addWidget(image_view)

        close_button = QPushButton("Close")
        close_button.setStyleSheet("font-size: 18px; padding: 10px; margin-top: 20px;")
        close_button.clicked.connect(hint_dialog.accept)
        hint_layout.addWidget(close_button)

        hint_dialog.setLayout(hint_layout)
        hint_dialog.exec_()

    def show_result_screen(self):
        self.clear_layout(self.layout)
        loading_text_label = QLabel("Loading...", self)
        loading_text_label.setStyleSheet("font-size: 20px; font-weight: bold; color: black;")
        loading_text_label.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(loading_text_label, alignment=Qt.AlignCenter)

        self.layout.update()

        QTimer.singleShot(2500, lambda: self.load_results(loading_text_label))
    def load_results(self, loading_text_label):
        self.clear_layout(self.layout)
        loading_text_label.deleteLater()
        self.result_screen = self.create_result_screen()
        self.layout.addWidget(self.result_screen)

    def clear_layout(self, layout):
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

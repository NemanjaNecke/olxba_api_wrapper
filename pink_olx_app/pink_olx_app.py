# Main GUI application (PyQt5)
# pink_olx_app.py

import sys
import statistics
import csv

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QSpinBox,
    QTextEdit,
    QPushButton,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QCheckBox,
    QTabWidget,
    QLabel,
    QFileDialog,
    QListWidget,
    QListWidgetItem,
    QHBoxLayout
)

# Our custom modules
from pink_olx_app import pink_olx_logic as logic
from pink_olx_app import pink_store
from pink_olx_app import pink_data_analysis

class PinkOLXApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pink OLX Search - Modular Edition")
        self.setGeometry(100, 100, 1100, 750)

        # Optionally set up pink style
        self.setStyleSheet("""
            QMainWindow {
                background-color: pink;
            }
            ...
        """)

        # Initialize the local DB (so we can store search results)
        pink_store.init_db()

        # Main layout with tabs
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        self.tabs = QTabWidget()
        self.main_layout.addWidget(self.tabs)

        self.search_tab = QWidget()
        self.results_tab = QWidget()
        self.tabs.addTab(self.search_tab, "Search & Filters")
        self.tabs.addTab(self.results_tab, "Results & Analysis")

        # Build UI elements
        self.build_search_tab()
        self.build_results_tab()

        # Timer for autosuggest
        self.autosuggest_timer = QTimer()
        self.autosuggest_timer.setSingleShot(True)
        self.autosuggest_timer.timeout.connect(self.run_autosuggest)

        # For storing the final results we display
        self.current_listings = []
        self.search_api = None

    def build_search_tab(self):
        """Create all input/filters on the first tab."""
        layout = QVBoxLayout(self.search_tab)

        form_layout = QFormLayout()

        # 1) Query Input
        self.query_input = QLineEdit()
        self.query_input.setPlaceholderText("Type something (e.g. 'Xiaomi tablet')...")
        self.query_input.textChanged.connect(self.on_query_text_changed)
        form_layout.addRow("Search Query:", self.query_input)

        # 2) Autosuggest result list
        #    We'll use a QListWidget to display suggestions
        self.suggestions_list = QListWidget()
        self.suggestions_list.hide()
        # Clicking a suggestion updates the query_input
        self.suggestions_list.itemClicked.connect(self.on_suggestion_clicked)
        layout.addWidget(self.suggestions_list)

        # 3) Login or Token
        self.use_login_checkbox = QCheckBox("Use Login?")
        self.use_login_checkbox.setChecked(False)
        form_layout.addRow(self.use_login_checkbox)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username (optional)")
        form_layout.addRow("Username:", self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Password (optional)")
        form_layout.addRow("Password:", self.password_input)

        self.token_input = QLineEdit()
        self.token_input.setPlaceholderText("Bearer token (optional)")
        form_layout.addRow("Token:", self.token_input)

        # 4) Page + Filters
        self.per_page_input = QSpinBox()
        self.per_page_input.setRange(1, 1000)
        self.per_page_input.setValue(40)
        form_layout.addRow("Results Per Page:", self.per_page_input)

        self.max_pages_input = QSpinBox()
        self.max_pages_input.setRange(1, 50)
        self.max_pages_input.setValue(5)
        form_layout.addRow("Max Pages:", self.max_pages_input)

        self.min_price_input = QLineEdit()
        self.min_price_input.setPlaceholderText("Min Price")
        form_layout.addRow("Min Price:", self.min_price_input)

        self.max_price_input = QLineEdit()
        self.max_price_input.setPlaceholderText("Max Price")
        form_layout.addRow("Max Price:", self.max_price_input)

        self.condition_filter = QComboBox()
        self.condition_filter.addItem("All")
        self.condition_filter.addItem("new")
        self.condition_filter.addItem("used")
        form_layout.addRow("Condition:", self.condition_filter)

        self.sort_combo = QComboBox()
        self.sort_combo.addItem("None")
        self.sort_combo.addItem("Ascending")
        self.sort_combo.addItem("Descending")
        form_layout.addRow("Sort by Price:", self.sort_combo)

        # Search button
        self.search_button = QPushButton("Search OLX")
        self.search_button.clicked.connect(self.perform_search)
        form_layout.addRow(self.search_button)

        layout.addLayout(form_layout)

    def build_results_tab(self):
        """Create the table, stats area, and some data science features."""
        layout = QVBoxLayout(self.results_tab)

        # Table for listings
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(4)
        self.results_table.setHorizontalHeaderLabels(["Title", "Price", "Condition", "Location"])
        self.results_table.setColumnWidth(0, 350)
        layout.addWidget(self.results_table)

        # Stats area
        self.stats_area = QTextEdit()
        self.stats_area.setReadOnly(True)
        layout.addWidget(self.stats_area)

        # A row of buttons for advanced features
        btn_layout = QHBoxLayout()

        self.export_button = QPushButton("Export CSV")
        self.export_button.clicked.connect(self.export_to_csv)
        btn_layout.addWidget(self.export_button)

        self.plot_button = QPushButton("Show Plot")
        self.plot_button.clicked.connect(self.on_show_plot)
        btn_layout.addWidget(self.plot_button)

        layout.addLayout(btn_layout)

    # -- Autosuggest Flow --
    def on_query_text_changed(self, text):
        """Start the timer for autosuggest if text >=2 chars."""
        self.suggestions_list.hide()  # hide suggestions while typing
        if len(text.strip()) < 2:
            return
        self.autosuggest_timer.start(350)

    def run_autosuggest(self):
        """Retrieve suggestions from OLX and display them in the QListWidget."""
        text = self.query_input.text().strip()
        if len(text) < 2:
            return

        if not self.search_api:
            self.search_api = logic.create_search_api(
                self.use_login_checkbox.isChecked(),
                self.username_input.text().strip(),
                self.password_input.text().strip(),
                self.token_input.text().strip(),
            )

        data = logic.autosuggest_olx(self.search_api, text)
        refined = data.get("autocomplete", [])
        categories = data.get("categories", [])

        self.suggestions_list.clear()

        # Add refined queries
        for r in refined:
            item = QListWidgetItem(r)
            self.suggestions_list.addItem(item)

        # Add categories
        for cat in categories:
            item = QListWidgetItem(cat["name"])
            self.suggestions_list.addItem(item)

        if refined or categories:
            self.suggestions_list.show()

    def on_suggestion_clicked(self, item):
        """Put the clicked suggestion text into the query_input."""
        suggestion_text = item.text()
        self.query_input.setText(suggestion_text)
        self.suggestions_list.hide()

    # -- Search Flow --
    def perform_search(self):
        """Perform the OLX search, store results in DB, display them."""
        self.stats_area.clear()
        self.results_table.setRowCount(0)
        query = self.query_input.text().strip()
        if not query:
            self.stats_area.setText("Please enter a search query.")
            self.tabs.setCurrentIndex(1)
            return

        # Create or reuse search_api
        if not self.search_api:
            self.search_api = logic.create_search_api(
                self.use_login_checkbox.isChecked(),
                self.username_input.text().strip(),
                self.password_input.text().strip(),
                self.token_input.text().strip(),
            )

        # Get listings
        listings = logic.search_all_listings(
            self.search_api,
            query,
            self.per_page_input.value(),
            self.max_pages_input.value()
        )

        # Save them for historical tracking
        pink_store.save_listings(listings, query)

        # Filter
        min_p, max_p = self.parse_price_range()
        condition = self.condition_filter.currentText()
        filtered = logic.filter_listings_by_price_condition(listings, min_p, max_p, condition)

        # Sort
        sort_order = self.sort_combo.currentText()
        final_list = logic.sort_listings_by_price(filtered, sort_order)

        # Display
        self.current_listings = final_list[:]  # store locally
        self.display_listings_in_table(final_list)
        self.show_price_stats(final_list)

        # Switch tab
        self.tabs.setCurrentIndex(1)

    def parse_price_range(self):
        """Safely parse min/max price from QLineEdits."""
        try:
            min_p = float(self.min_price_input.text())
        except ValueError:
            min_p = None

        try:
            max_p = float(self.max_price_input.text())
        except ValueError:
            max_p = None

        return (min_p, max_p)

    def display_listings_in_table(self, listings):
        """Fill the QTableWidget with listing data."""
        self.results_table.setRowCount(len(listings))
        for row, item in enumerate(listings):
            # Title
            title = item.get("title", "N/A")
            price = str(item.get("price", "N/A"))
            cond = item.get("state", "N/A")
            loc = (item.get("location") or {}).get("city", "N/A")

            self.results_table.setItem(row, 0, QTableWidgetItem(title))
            self.results_table.setItem(row, 1, QTableWidgetItem(price))
            self.results_table.setItem(row, 2, QTableWidgetItem(cond))
            self.results_table.setItem(row, 3, QTableWidgetItem(loc))
        self.results_table.resizeColumnsToContents()

    def show_price_stats(self, listings):
        """Compute & show min, max, avg price in stats_area."""
        if not listings:
            self.stats_area.setText("No listings found after filtering.")
            return

        prices = []
        for item in listings:
            try:
                p = float(item.get("price", 0) or 0)
                if p > 0:
                    prices.append(p)
            except:
                pass

        if not prices:
            self.stats_area.append("No valid prices among these listings.")
            return

        min_p = min(prices)
        max_p = max(prices)
        avg_p = statistics.mean(prices)

        self.stats_area.append("\n=== Price Stats ===")
        self.stats_area.append(f"Count: {len(prices)}")
        self.stats_area.append(f"Min : {min_p:.2f}")
        self.stats_area.append(f"Max : {max_p:.2f}")
        self.stats_area.append(f"Avg : {avg_p:.2f}")

    # -- CSV Export --
    def export_to_csv(self):
        """Export current_listings to a CSV file."""
        if not self.current_listings:
            self.stats_area.append("No listings to export.")
            return

        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(self, "Save CSV", "", "CSV Files (*.csv)")
        if not file_path:
            return

        try:
            with open(file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Title", "Price", "Condition", "City"])
                for item in self.current_listings:
                    row = [
                        item.get("id", ""),
                        item.get("title", ""),
                        item.get("price", ""),
                        item.get("state", ""),
                        (item.get("location") or {}).get("city", "")
                    ]
                    writer.writerow(row)

            self.stats_area.append(f"Exported to CSV: {file_path}")
        except Exception as e:
            self.stats_area.append(f"Export Error: {e}")

    # -- Show Plot --
    def on_show_plot(self):
        """Use pink_data_analysis to plot the distribution of current_listings' prices."""
        if not self.current_listings:
            self.stats_area.append("No data to plot. Search first!")
            return

        fig = pink_data_analysis.plot_price_distribution(self.current_listings)
        if fig:
            fig.show()  # opens a new matplotlib window
        else:
            self.stats_area.append("Could not create a plot.")


def main():
    """Main entry point."""
    app = QApplication(sys.argv)
    font = QFont("Arial", 10)
    app.setFont(font)

    window = PinkOLXApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

import tkinter as tk
import json
from datetime import datetime
from tkinter import ttk
from bs4 import BeautifulSoup
import requests
import time
import webbrowser
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np  





def plot_graph(canvas, values_list, reference_value):
    """Plot the graph with horizontal and value lines colored based on comparison with reference value.
    
    Parameters:
    - canvas: The canvas widget to draw the plot on.
    - values_list: The data to plot on the graph.
    - reference_value: The value at which the horizontal reference line should be drawn.
    """
    fig = canvas.figure
    fig.clear()
    ax = fig.add_subplot(111)

    # Adjust values to be relative to the reference line
    adjusted_values = [value - reference_value for value in values_list]
    
    # Determine the color of the value line
    last_value = values_list[-1] if values_list else reference_value
    if last_value < reference_value:
        value_line_color = 'r'  # Red if the last value is less than the reference value
        ref_line_color = 'r'    # Red if the last value is less than the reference value
    else:
        value_line_color = 'g'  # Green if the last value is greater than or equal to the reference value
        ref_line_color = 'g'    # Green if the last value is greater than or equal to the reference value
    
    # Plot the graph with adjusted values and no dots
    ax.plot(adjusted_values, linestyle='-', color=value_line_color)  # Line color based on the condition
    
    # Draw horizontal reference line
    ax.axhline(y=0, color=ref_line_color, linestyle='--')  # Reference line color based on the condition

    # Remove spines (borders)
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    # Remove ticks and grid
    ax.xaxis.set_ticks([])
    ax.yaxis.set_ticks([])
    ax.grid(False)
    
    # Calculate range for y-axis
    y_min = min(adjusted_values)
    y_max = max(adjusted_values)
    y_range = max(abs(y_min), abs(y_max))
    
    # Set fixed height for the graph, adjust to center the reference line
    ax.set_ylim(-y_range - 1, y_range + 1)  # Ensure the reference line is centered
    
    # Set a fixed width for the graph
    ax.set_xlim(0, max(7, len(values_list)) - 1)  # X-axis limit based on the number of data points

    # Adjust figure size to ensure fixed height and adjust width based on data
    fig.set_size_inches(4, 0.5)  # Width in inches, height fixed
    canvas.figure.tight_layout(pad=0.5)

    canvas.draw()


# Define constants
now = datetime.now()

# Load the reference data from file
with open('/home/vikram/Desktop/closing_price.txt', 'r') as file:
    loaded_dict = json.load(file)
with open('/home/vikram/Desktop/day_historical.txt', 'r') as file:
    historical_data = json.load(file)


loaded_portfolio_dict = loaded_dict['portfolio']
loaded_index_dict = loaded_dict['index']
loaded_closing_dict = loaded_dict['closing_price']

now = datetime.now()
comparison_time = now.replace(hour=9, minute=15, second=0, microsecond=0)

if now == comparison_time:
    
    dumping_dic = {key: [] for key in historical_data}
    with open('/home/vikram/Desktop/day_historical.txt', 'w') as file:
        json.dump(dumping_dic, file)

    print("Closing Price saved to file.")
        
else:
    print("Current time is not later than 3:15 PM. Dictionary not saved.")


# Define tickers and quantities
ticker = ["NAM-INDIA", "NTPC", "PNB", "IRFC", "HAL", "TATAMOTORS", "TATATECH"]
qunat = [5, 7, 43, 20, 2, 3, 30]

index_ticker = ["BSESN", "NSEI","IXIC", "DJI"]
index_mapper= {"BSESN" : "SENSEX", "NSEI" : "NIFTY 50", "IXIC": "NASDAQ", "DJI" : "Dow Jones"}
reverse_index_mapper = {value: key for key, value in index_mapper.items()}


d = {"NAM-INDIA": 3549.75, "NTPC": 2821.0, "PNB": 4863.3, "IRFC": 3470.0, "HAL": 9576.4, "TATAMOTORS": 3206.1, "TATATECH": 32292.0}
index_dic = {"BSESN": 81183.93, "NSEI": 24852.15, "IXIC": 16690.83, "DJI": 40345.41}

d_price = {"NAM-INDIA": 689.50, "NTPC": 395.0, "PNB": 109.93, "IRFC": 169.98, "HAL": 4703.4, "TATAMOTORS": 1050.65, "TATATECH": 1109.35}
total_Asset = 0
for i, j in zip(ticker, qunat):
    url = f"https://www.google.com/finance/quote/{i}:NSE"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    class1 = "YMlKec fxKbKc"
    val = soup.find(class_=class1).text
    val = float(val[1:].replace(",", ""))
    d[i] = round(val * j, 2)
    d_price[i] = round(val, 2)
    historical_data[i].append(round(val, 2))
    total_Asset += (float(val) * j)
    time.sleep(5)

for i in index_ticker:
    url = f"https://finance.yahoo.com/quote/^{i}/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'html.parser')
    class1 = "livePrice yf-mgkamr"
    val = soup.find(class_= class1).text
    val = float(val.strip("'").replace(",",""))
    index_dic[i] = val
    time.sleep(5)
    

class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def calculate_percentage_change(current_value, reference_value):
    if reference_value == 0:
        return 0
    return ((current_value - reference_value) / reference_value) * 100

def format_change_percentage(change_percentage):
    """Format the change percentage with + or - sign."""
    if change_percentage >= 0:
        return f"+{change_percentage:.2f} %"
    elif change_percentage < 0:
        return f"{change_percentage:.2f} %"
    else:
        return f"0.00 %"

root = tk.Tk()
notebook = ttk.Notebook(root)


def create_table():
    # Create main window

    # Format the current time in AM/PM format
    formatted_time = now.strftime("%I:%M %p")

    root.title(f"Portfolio {formatted_time}")

    # Define window size and position
    window_width = 400
    window_height = 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = screen_width - window_width
    y = 0
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Create a Notebook (Tabs)

    # Portfolio Tab
    portfolio_frame = ttk.Frame(notebook)
    notebook.add(portfolio_frame, text="Portfolio")

    # Index's Tab (Placeholder)
    index_frame = ttk.Frame(notebook)
    notebook.add(index_frame, text="Index")

    notebook.pack(expand=True, fill='both')

    create_day_change_tab(notebook)

    # Create Treeview for Portfolio Tab
    tree = ttk.Treeview(portfolio_frame, columns=("Ticker", "Value", "Change %"), show='headings', style='Treeview')
    tree2 = ttk.Treeview(index_frame, columns=("Ticker", "Value", "Change %"), show='headings', style='Treeview')
    
    tree.heading("Ticker", text="Ticker")
    tree.heading("Value", text="Value")
    tree.heading("Change %", text="Change %")

    tree.column("Ticker", width=int(window_width/3), anchor='w')
    tree.column("Value", width=int(window_width/3), anchor='e')
    tree.column("Change %", width=int(window_width/3)-20, anchor='e')
   
    tree2.heading("Ticker", text="Ticker")
    tree2.heading("Value", text="Value")
    tree2.heading("Change %", text="Change %")

    tree2.column("Ticker", width=int(window_width/3), anchor='w')
    tree2.column("Value", width=int(window_width/3), anchor='e')
    tree2.column("Change %", width=int(window_width/3)-20, anchor='e')

    style = ttk.Style()
    style.configure('Treeview', font=('Courier New', 10))
    style.configure("TNotebook.Tab", font=("Courier New", 11, "bold"))


    # Define color tags
    tree.tag_configure("red", foreground="red")
    tree.tag_configure("green", foreground="green")
    tree.tag_configure("bold_green", font=("Courier New", 10, "bold"), foreground="green")
    tree.tag_configure("bold_red", font=("Courier New", 10, "bold"), foreground="red")

    tree2.tag_configure("red", foreground="red")
    tree2.tag_configure("green", foreground="green")
    tree2.tag_configure("bold_green", font=("Courier New", 10, "bold"), foreground="green")
    tree2.tag_configure("bold_red", font=("Courier New", 10, "bold"), foreground="red")

    # Insert data into Treeview
    create_portfolio(tree)

    create_index(tree2)

    tree.bind("<Double-1>", lambda event: open_link(event, "portfolio"))
    tree2.bind("<Double-1>", lambda event: open_link(event, "index"))

    # Add Treeview to the Portfolio Tab
    tree.pack(expand=True, fill='both', padx=10, pady=10)
    tree2.pack(expand=True, fill='both', padx=10, pady=10)

    # Run the Tkinter event loop
    root.mainloop()


def create_portfolio(tree = None):
    for ticker, value in d.items():
        reference_value = loaded_portfolio_dict.get(ticker, float('inf'))
        change_percentage = calculate_percentage_change(value, reference_value)
        formatted_change = format_change_percentage(change_percentage)
        color = "red" if value < reference_value else "green"
        tree.insert("", "end", values=(ticker, f"{value:.2f}", formatted_change), tags=(color,))

    # Insert total row
    total_value = sum(d.values())
    reference_value = loaded_portfolio_dict.get('total', float('inf'))
    change_percentage = calculate_percentage_change(total_value, reference_value)
    formatted_change = format_change_percentage(change_percentage)

    if total_value < float(loaded_portfolio_dict['total']):
        tree.insert("", "end", values=("Total", f"{total_value:.2f}", formatted_change), tags=("bold_red",))
    else:
        tree.insert("", "end", values=("Total", f"{total_value:.2f}", formatted_change), tags=("bold_green",))
    
def create_index(tree2 = None):
    for ticker, value in index_dic.items():
        reference_value = loaded_index_dict.get(ticker, float('inf'))
        change_percentage = calculate_percentage_change(value, reference_value)
        formatted_change = format_change_percentage(change_percentage)
        color = "red" if value < reference_value else "green"
        tree2.insert("", "end", values=(index_mapper[ticker], f"{value:.2f}", formatted_change), tags=(color,))      



def create_day_change_tab(notebook):
    # Create Day Change Tab
    day_change_frame = ttk.Frame(notebook)
    notebook.add(day_change_frame, text="Day Change")

    # Create a Canvas widget
    canvas = tk.Canvas(day_change_frame)
    canvas.pack(side='left', fill='both', expand=True)

    # Create a Scrollbar widget
    scrollbar = ttk.Scrollbar(day_change_frame, orient='vertical', command=canvas.yview)
    scrollbar.pack(side='right', fill='y')

    # Create a Frame inside the Canvas
    frame_container = ttk.Frame(canvas)
    
    # Create a window in the Canvas that will hold the Frame
    canvas.create_window((0, 0), window=frame_container, anchor='nw')
    
    # Update the scroll region of the Canvas
    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame_container.bind("<Configure>", on_frame_configure)

    # Example values for each ticker, dynamically adjusting graph length
    values_list = [
        [9, 2, 4, 1, 5, 6, 2],
        [3456, 3498, 3476, 3499, 3401, 3452],
        [9],
        [9, 2, 4],
        [9, 2, 4, 1],
        [9, 2, 4, 1, 5, 6],
        [9, 2, 4, 1, 5, 6]
    ]

    # Example reference values (loaded_data[ticker])
    loaded_data = {
        "NAM-INDIA": 5,
        "NTPC": 3490,
        "PNB": 10,
        "IRFC": 8,
        "HAL": 6,
        "TATAMOTORS": 7,
        "TATATECH": 3
    }
    
    count = 0
    # Create and plot graphs
    for ticker in d.keys():
        # Frame for each row
        row_frame = ttk.Frame(frame_container)
        row_frame.pack(pady=5, fill='x')
        
        # Label for ticker name
        label = ttk.Label(row_frame, text=f"{ticker}", anchor='w', width=13)
        label.pack(side='left', padx=5, anchor='w')  # Reduced padding for closer alignment
        
        # Create a Figure and Canvas for graph
        fig = plt.Figure(figsize=(4, 0.5), dpi=65)  # Reduced width
        canvas_graph = FigureCanvasTkAgg(fig, master=row_frame)
        canvas_graph.get_tk_widget().pack(side='right', fill='both', expand=True)
        
        # Plot the graph with dynamic values and reference line
        plot_graph(canvas_graph, historical_data[ticker], loaded_closing_dict[ticker])
        count += 1

    # Update the scroll region of the Canvas
    canvas.update_idletasks()  # Ensure the scroll region is updated
    canvas.config(scrollregion=canvas.bbox("all"))

def open_link(event, tab):
    # Determine which Treeview was clicked
    widget = event.widget
    item_id = widget.selection()[0]  # Get selected item
    item_values = widget.item(item_id, "values")  # Get the values of the selected item
    ticker = item_values[0]  # Assume the ticker is the first column
    if ticker == "Total":
        return
    # Define a mapping of tickers to URLs
    
    if tab == "portfolio":
        url_portfolio = f"https://www.google.com/finance/quote/{ticker}:NSE"
        webbrowser.open(url_portfolio)
    else:
        url_index = f"https://finance.yahoo.com/quote/^{reverse_index_mapper[ticker]}/"
        webbrowser.open(url_index)

  


create_table()

def save_historical_data():
    with open('/home/vikram/Desktop/day_historical.txt', 'w') as file:
        json.dump(historical_data, file)
    print("day historical saved to file.")
        

save_historical_data()




# Save the dictionary to file if time is after 3:15 PM
now = datetime.now()
comparison_time = now.replace(hour=15, minute=15, second=0, microsecond=0)

if now > comparison_time:
    d["total"] = total_Asset
    dumping_dic = {'portfolio' : d , 'index' : index_dic, 'closing_price' : d_price}
    with open('/home/vikram/Desktop/closing_price.txt', 'w') as file:
        json.dump(dumping_dic, file)

    print("Closing Price saved to file.")

else:
    print("Current time is not later than 3:15 PM. Dictionary not saved.")

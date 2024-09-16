import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns


def plot_multiple_lines(df, x_field: str, y_fields: list, title: str):
    """
    Creates a line plot with multiple y-axis fields on the same chart.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the data.
    x_field (str): The column name for the x-axis.
    y_fields (list): A list of column names for the y-axis.
    title (str): The title of the plot.
    """
    if x_field not in df.columns:
        raise ValueError(f"Specified x-field {x_field} is not in the Dat
aFrame")

    for y_field in y_fields:
        if y_field not in df.columns:
            raise ValueError(f"Specified y-field {y_field} is not in the
 DataFrame")

    plt.figure(figsize=(10, 6))

    # Creating a slight vertical offset for overlapping lines
    offsets = np.linspace(0, 0.5, len(y_fields))

    for i, y_field in enumerate(y_fields):
           plt.plot(df[x_field], df[y_field] + offsets[i], label=y_field, marker='o')

    plt.title(title)
    plt.xlabel(x_field)
    plt.ylabel('Values')
    plt.legend()
    plt.grid(True)

    # Adjust X-axis formatting to integer with ₪ sign
    plt.gca().xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x)} ₪"))

    plt.show()


def create_3d_scatter_plot(df: pd.DataFrame, field_x1: str, field_x2: str, field_y: str):
    """
    Creates a 3D scatter plot to show how two factors affect a third one.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the data.
    field_x1 (str): The column name for the first factor (x-axis).
    field_x2 (str): The column name for the second factor (y-axis).
    field_y (str): The column name for the dependent variable (z-axis).
    """
    if field_x1 not in df.columns or field_x2 not in df.columns or field_y not in df.columns:
        raise ValueError("Specified fields are not in the DataFrame")

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    x1 = df[field_x1]
    x2 = df[field_x2]
    y = df[field_y]

    scatter = ax.scatter(x1, x2, y, c=y, cmap='viridis', marker='o')
    ax.set_title(f'3D Scatter Plot of {field_x1}, {field_x2} vs {field_y}')
    ax.set_xlabel(field_x1)
    ax.set_ylabel(field_x2)
    ax.set_zlabel(field_y)
    fig.colorbar(scatter, ax=ax, shrink=0.5, aspect=5)

    plt.show()


def create_scatter_plot_with_line(df: pd.DataFrame, field_x: str, field_y: str):
    """
    Creates a scatter plot with a regression line from two specified fields in the DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the data.
    field_x (str): The column name for the x-axis.
    field_y (str): The column name for the y-axis.
    """
    if field_x not in df.columns or field_y not in df.columns:
        raise ValueError("Specified fields are not in the DataFrame")

    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=field_x, y=field_y, data=df, s=100, edgecolor='w', alpha=0.7)
    sns.lineplot(x=field_x, y=field_y, data=df, color='red')
    plt.title(f'Scatter Plot with Line of {field_x} vs {field_y}')
    plt.xlabel(field_x)
    plt.ylabel(field_y)
    plt.grid(True)
    plt.show()
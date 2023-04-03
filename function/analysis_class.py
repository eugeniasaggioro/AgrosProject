"""
This module contains classes and methods for data analysis.
"""

from typing import Union, List
import os.path
import warnings
import pandas as pd
import requests
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
from statsmodels.tsa.arima.model import ARIMA


warnings.filterwarnings("ignore")


class Analysis:
    """
    Class to read the Agriculture Total Factor Productivity (USDA) Dataset and
    perform the analysis by reading the dataset as a pandas dataframe.

    Attributes
    ----------
    None

    Methods
    --------
    download_save_data()
        Downloads the agriculture data from a remote CSV file and saves it to a local
        file in a "downloads" directory. Perform some data cleaning by removing aggregates
        such as continents, regions and income classes from the list of entities.

    countries_list()
        Prints the list of countries in the dataset.

    plot_quantity_correlations()
        Plots a correlation matrix of the columns in the agriculture data that end with "_quantity".

    plot_output_area()
        Plots an area chart of crop, animal, and fish output quantities over time for
        a given geographical area.

    compare_output_for_countries()
        Compare the total output of crop, animal, and fish for the specified countries over time.
        Plot a line graph to visualize the comparison.

    gapminder()
        Creates a scatter plot of fertilizer quantity vs. output quantity, with bubble sizes
        representing irrigation quantity. The plot is colored based on agricultural land quantity.

    choropleth()
        Plots a choropleth map of Total Factor Productivity (tfp) for the countries present
        both in the geopandas dataframe and in the Agricultural Dataset for years before 2019.

    predict_tfp()
        Plot the Total Factor Productivity data for the specified countries and their
        ARIMA predictions up to 2050.


    """

    def __init__(self):
        self.dataframe = None
        self.geodata = None
        self.merge_dict = {}

    def download_save_data(self):
        """
        Downloads a CSV file from a specified URL and saves it to a local directory.
        If the file exists in the local directory, it reads the file into a pandas dataframe.
        Perform some data cleaning by removing aggregates such as continents, regions and
        income classes from the list of entities.

        Returns:
        --------
        Nothing.
        """
        file_path = os.path.join("downloads", "Dataset.csv")
        url = "https://raw.githubusercontent.com/owid/owid-datasets/master/datasets/Agricultural%20total%20factor%20productivity%20(USDA)/Agricultural%20total%20factor%20productivity%20(USDA).csv"

        self.geodata = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

        try:
            # Try to open file from local directory
            self.dataframe = pd.read_csv(file_path)

        except FileNotFoundError:
            # If file does not exist, download it from url
            download = requests.get(url, timeout=40)
            download.raise_for_status()

            # Create the downloads directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Save the downloaded file to local directory
            with open(file_path, "wb") as file:
                file.write(download.content)

            # Read the downloaded file into pandas dataframe
            self.dataframe = pd.read_csv(file_path)
            print(
                "The file has been stored in the downloads directory with the name Dataset.csv"
            )

        else:
            # If file already exists, read it into pandas dataframe
            self.dataframe = pd.read_csv(file_path)
            print("The path and file already exist")

        # Remove rows containing aggregate entities
        entities_to_remove = [
            "Asia",
            "Caribbean",
            "Central Africa",
            "Central America",
            "Central Asia",
            "Central Europe",
            "French Guiana",
            "Developed Asia",
            "Developed countries",
            "East Africa",
            "Eastern Europe",
            "Europe",
            "High income",
            "Horn of Africa",
            "Latin America and the Caribbean",
            "Least developed countries",
            "Low income",
            "Upper-middle income",
            "Lower-middle income",
            "North Africa",
            "North Macedonia",
            "North America",
            "Northeast Asia",
            "Northern Europe",
            "Oceania",
            "West Africa",
            "West Asia",
            "Western Europe",
            "World",
            "Pacific",
            "Polynesia",
            "South Asia",
            "Southeast Asia",
            "Southern Africa",
            "Southern Europe",
            "Sub-Saharan Africa",
        ]
        self.dataframe = self.dataframe[
            ~self.dataframe["Entity"].isin(entities_to_remove)
        ]

    def countries_list(self):
        """
        Returns a list of all unique countries in the agriculture data.
        """

        countries_list = self.dataframe["Entity"].unique().tolist()
        return countries_list

    def plot_quantity_correlations(self):
        """
        Plots a correlation matrix of the columns in the agriculture data that end with "_quantity".
        """
        quantity_cols = [
            col for col in self.dataframe.columns if col.endswith("_quantity")
        ]
        quantity_corr = self.dataframe[quantity_cols].corr()
        mask = np.zeros_like(quantity_corr, dtype=bool)
        mask[np.triu_indices_from(mask)] = True

        plt.figure(figsize=(15, 10))
        sns.heatmap(quantity_corr, annot=True, cmap="Oranges", mask=mask, square=True)
        plt.title("Correlation Matrix of Quantity Columns")
        txt = "Source: Agriculture Total Factor Productivity (USDA) Dataset"
        plt.figtext(
            0.5, -0.1, txt, wrap=True, horizontalalignment="center", fontsize=12
        )
        plt.show()

    def plot_output_area(self, entity, normalize):
        """
        Plots an area chart of crop, animal, and fish output quantities over time for
        a given geographical area.

        Parameters
        -----------
        self: class
            The Analysis class itself
        entity: str
            Name of the entity to plot, e.g. "United States". When receiving None or "World",
            it plots the World's total output.
        normalize: bool
            If equal to True, it normalizes the output values in relative terms.

        Returns
        --------
        Nothing.
        """

        # Select the columns to plot
        columns_to_plot = [
            "crop_output_quantity",
            "animal_output_quantity",
            "fish_output_quantity",
        ]

        # Filter the dataset to include only the selected entity
        # If None or World it groups by year to plot world output
        if entity is None or entity == "World":
            df_plot = self.dataframe.groupby("Year").sum()[columns_to_plot]
            title = "World Output"
        else:
            df_plot = self.dataframe[self.dataframe["Entity"] == entity].set_index(
                "Year"
            )[columns_to_plot]
            if df_plot.empty:
                raise ValueError(f"Entity '{entity}' not found")
            title = f"{entity} Output"

        # Normalize the output values if required
        if normalize is True:
            df_plot = df_plot.div(df_plot.sum(axis=1), axis=0) * 100

        # Plot the area chart
        txt = "Source: Agriculture Total Factor Productivity (USDA) Dataset"
        df_plot.plot.area(title=title, xlabel="Year", ylabel="Output")
        plt.legend(loc="upper left")
        plt.title(title)
        plt.xlabel("Year")
        plt.ylabel("Output")
        plt.figtext(
            0.5, -0.1, txt, wrap=True, horizontalalignment="center", fontsize=12
        )
        plt.xticks(rotation=45)
        plt.show()

    def compare_output_for_countries(self, countries: Union[str, List[str]]):
        """
        Compare the total output of crop, animal, and fish for the specified countries over time.
        Plot a line graph to visualize the comparison.

        Parameters:
        -----------
        countries: str or List[str]
            A string or a list of strings containing the names of countries to compare.

        Returns:
        --------
        Nothing.
        """

        if isinstance(countries, str):
            countries = [countries]
        elif not isinstance(countries, list) or not all(
            isinstance(country, str) for country in countries
        ):
            raise TypeError("Countries must be a string or a list of strings.")

        invalid_countries = set(countries) - set(self.dataframe["Entity"].unique())
        if invalid_countries:
            raise ValueError(
                f"The following countries are not in the dataset: {invalid_countries}"
            )

        # Filter the dataframe to only include rows for the specified countries
        filtered_data = self.dataframe[self.dataframe["Entity"].isin(countries)].copy()

        # Calculate the total output for each country and year
        filtered_data.loc[:, "Total Output"] = filtered_data[
            ["crop_output_quantity", "animal_output_quantity", "fish_output_quantity"]
        ].sum(axis=1)
        total_output = (
            filtered_data.groupby(["Entity", "Year"])["Total Output"]
            .sum()
            .reset_index()
        )

        # Create a line plot of the total output for each country over time
        for country in countries:
            country_data = total_output[total_output["Entity"] == country]
            plt.plot(country_data["Year"], country_data["Total Output"], label=country)

        # Add a legend to the plot indicating which line corresponds to each country
        plt.legend(title="Countries")

        # Add axis labels and a title to the plot
        txt = "Source: Agriculture Total Factor Productivity (USDA) Dataset"
        plt.xlabel("Year")
        plt.ylabel("Total Output")
        plt.title("Comparison of Total Outputs among selected Countries over time")
        plt.figtext(
            0.5, -0.1, txt, wrap=True, horizontalalignment="center", fontsize=12
        )

        # Show the plot
        plt.show()

    def gapminder(self, year: int, log_scale: bool = True):
        """
        Creates a scatter plot of fertilizer quantity vs. output quantity, with bubble sizes
        representing irrigation quantity. The plot is colored based on agricultural land quantity.

        Parameters:
        -----------
        year: integer
            An integer number that specifies the year to plot the values

        log_scale: boolean
            A Boolean indicating whether the displayed values will be transformed
            with a logarithm or not.

        Returns:
        --------
        Nothing
        """
        try:
            year = int(year)
        except ValueError as exc:
            raise TypeError("Year must be an integer") from exc

        # Filter the data to include only the specified year
        filtered_data = self.dataframe[self.dataframe["Year"] == year]

        # Create the scatter plot
        if log_scale == True:
            sns.set_theme(style="white")
            colors = sns.color_palette("viridis", as_cmap=True)
            filtered_data["fertilizer_quantity_logs"] = np.log(
                filtered_data["fertilizer_quantity"]
            )
            filtered_data["output_quantity_logs"] = np.log(
                filtered_data["output_quantity"]
            )
            sns.relplot(
                x="fertilizer_quantity_logs",
                y="output_quantity_logs",
                size="irrigation_quantity",
                hue="ag_land_quantity",
                sizes=(60, 600),
                alpha=0.5,
                palette=colors,
                height=6,
                data=filtered_data,
                legend="brief",
            )
        elif log_scale == False:
            sns.set_theme(style="white")
            colors = sns.color_palette("viridis", as_cmap=True)
            sns.relplot(
                x="fertilizer_quantity",
                y="output_quantity",
                size="irrigation_quantity",
                hue="ag_land_quantity",
                sizes=(60, 600),
                alpha=0.5,
                palette=colors,
                height=6,
                data=filtered_data,
                legend="brief",
            )
        else:
            raise TypeError("log_scale parameter must be a Boolean")

        # Add axis labels and a title to the plot
        txt = "Source: Agriculture Total Factor Productivity (USDA) Dataset"
        plt.xlabel("Fertilizer Quantity")
        plt.ylabel("Output Quantity")
        plt.title(f"Output vs. Fertilizer Quantity ({year})")
        plt.figtext(
            0.5, -0.1, txt, wrap=True, horizontalalignment="center", fontsize=12
        )

        # Show the plot
        plt.show()

    def choropleth(self, year: int):
        """
        Plots a choropleth map of Total Factor Productivity (tfp) for the countries present
        both in the geopandas dataframe and in the Agricultural Dataset for years before 2019.
        The plot is colored using a colorbar.

        Parameters:
        -----------
        year: integer
            An integer number that specifies the year to plot the values

        Returns:
        --------
        Nothing
        """
        try:
            year = int(year)
        except ValueError as exc:
            raise TypeError("Year must be an integer") from exc

        # Check whether year is present in the dataset, otherwise return an error
        try:
            self.dataframe[self.dataframe["Year"] == year] is not self.dataframe.empty
        except:
            raise ValueError("Year is not present in the Dataset")

        # Create a dictionary to rename countries in compatible way
        self.merge_dict = {
            "Dem. Rep. Congo": "Democratic Republic of Congo",
            "Bosnia and Herz.": "Bosnia and Herzegovina",
            "eSwatini": "Eswatini",
            "Solomon Is.": "Solomon Islands",
            "Central African Rep.": "Central African Republic",
            "United States of America": "United States",
        }
        self.geodata["name"] = self.geodata["name"].replace(self.merge_dict)

        # Merging the dataset and geodata on country names of geodata
        merged = self.geodata.merge(
            self.dataframe, how="left", left_on="name", right_on="Entity"
        )

        # Filter the merged data to include only the specified year
        filtered_data = merged[merged["Year"] == year]

        # Create the Choropleth map
        vmin = self.dataframe["tfp"].min()
        vmax = self.dataframe["tfp"].max()
        filtered_data.plot(
            column="tfp",
            legend=True,
            figsize=[20, 10],
            vmin=vmin,
            vmax=vmax,
            legend_kwds={"label": "Total factor productivity (TFP)"},
        )

        # Show the plot

        txt = "Source: Agriculture Total Factor Productivity (USDA) Dataset merged with Geodata taken from Natural Earth Dataset"
        plt.title("Level of TFP in the World ")
        plt.figtext(
            0.5, -0.05, txt, wrap=True, horizontalalignment="center", fontsize=12
        )
        plt.show()

    def predict_tfp(self, countries: List[str]):
        """
        Plot the TFP data for the specified countries and their ARIMA predictions up to 2050.

        Parameters:
        -----------
        countries: List[str]
            A list of up to three countries to plot.

        Returns:
        --------
        Nothing
        """
        # Check if the input is a list
        if not isinstance(countries, list):
            raise TypeError("Input must be a list of countries.")

        # Check that at least one country is specified
        if not countries:
            print("Please specify at least one country.")
            return

        # Limit the number of countries to a maximum of 3
        chosen_countries = countries[:3]

        # Check that all specified countries are in the dataframe
        available_countries = self.countries_list()
        valid_countries = []
        for country in chosen_countries:
            if country in available_countries:
                valid_countries.append(country)
            else:
                print(f"{country} is not available in the dataset and will be ignored.")

        # If none of the specified countries are in the dataframe, raise an error message
        if not valid_countries:
            error_message = f"None of the countries listed are available. Available countries are: {', '.join(available_countries)}"
            raise ValueError(error_message)

        # Set the plot title and legend labels
        title = f"Actual and Predicted TFP for {', '.join(valid_countries)}"
        legend_labels = []

        # Plot the TFP data for the specified countries
        _fig, axis = plt.subplots()
        for i, country in enumerate(valid_countries):
            data = self.dataframe[self.dataframe["Entity"] == country]
            axis.plot(
                data["Year"],
                data["tfp"],
                color=f"C{i}",
                linestyle="-",
                label=f"{country} actual",
            )
            # Generate ARIMA predictions for each country
            arima_model = ARIMA(data["tfp"], order=(1, 2, 2))
            arima_fit = arima_model.fit()
            arima_pred = arima_fit.predict(
                start=len(data), end=len(data) + 27, typ="levels"
            )
            axis.plot(
                range(data["Year"].max() + 1, data["Year"].max() + 29),
                arima_pred.values,
                color=f"C{i}",
                linestyle="--",
                label=f"{country} predicted",
            )
            legend_labels.extend([f"{country} actual", f"{country} predicted"])

        # Set the plot title and labels
        axis.set_title(title)
        axis.set_xlabel("Year")
        axis.set_ylabel("TFP")
        txt = "Source: Agriculture Total Factor Productivity (USDA) Dataset"
        plt.figtext(
            0.5, -0.1, txt, wrap=True, horizontalalignment="center", fontsize=12
        )

        axis.legend(legend_labels)

        plt.show()

# Group_09



## Authors and acknowledgment

Welcome! I am happy to introduce you to our group. We are a team of four Data Analysts working on the Agros Project for our company. What is showed in this repository is the result of a two-days hackathon.  If you have any questions or concerns, please find our contact details provided below.


| Name               | Matricula | Email     |
|-----------------------|--------|-----------|
| Maria Baglieri Occhipinti | 49638  | 49638@novasbe.pt |
| Eugenia Saggioro          | 50958  | 50958@novasbe.pt |
| Kevin Quan Nguyen          | 51316  | 51316@novasbe.pt |
| Raffaele Gino Geneletti | 57125  | 57125@novasbe.pt |


## Agros Project

This project repository is mainly focused on the analysis of the agricultural outputs and inputs of various countries overtime (1961-2019). The analysis is based on a developed class that integrated multiple methods, useful for our data analysis.

The functions provided in this class include downloading data from online sources, filtering the data based on user-specified criteria, and generating visualizations to aid in data exploration and understanding. 

These methods can be used to understand historical patterns in agricultural productivity and pinpoint areas for development.

## Getting Started

To use this project, follow the instructions below:

1. To get started, you first need to clone the repository onto your local machine. You can do this by running the following command in your terminal: ```git clone git@gitlab.com:eugeniasaggioro/group_09.git```. Change directory to ```group_09```.

2. Create a new conda environment using the YAML file provided in the repository. Open a terminal window and navigate to the repository folder. Run the command:  ```conda env create -f environment.yml```. This will create a new environment with all the necessary dependencies to run the project.

3. Activate the environment using the command:  ```conda activate agros_project ```. 
4. Run the code in the **showcase_notebook_09.ipynb** to see our results and understand the main insights of our analysis. The notebook includes examples of how to use the methods developed in the **Analysis** class. You can find this class within the **function** folder. You can also find an explanation of all the methods and the dataset in the following paragraphs.

That's it! You should now be able to use the project on your local machine. If you have any questions or issues, please feel free to contact us.

## Dataset
For this project, we will be using data from [Our World in Data](https://ourworldindata.org/). The dataset can be found [here](https://github.com/owid/owid-datasets/blob/master/datasets/Agricultural%20total%20factor%20productivity%20(USDA)/Agricultural%20total%20factor%20productivity%20(USDA).csv).

Here a brief description of the variables. Some descriptions are still missing.

|    Name              | Type   | Description                                                                                               |
|----------------------|--------|-----------------------------------------------------------------------------------------------------------|
| Entity               | string |                                                                                                           |
| Year                 | year   |                                                                                                           |
| tfp                  | any    |                                                                                                           |
| output               | any    |                                                                                                           |
| inputs               | any    |                                                                                                           |
| ag_land_index        | any    |                                                                                                           |
| labor_index          | any    |                                                                                                           |
| capital_index        | any    |                                                                                                           |
| materials_index      | any    |                                                                                                           |
| output_quantity      | any    |                                                                                                           |
| crop_output_quantity | any    |                                                                                                           |
| animal_output_quantity | any  |                                                                                                           |
| fish_output_quantity | any    |                                                                                                           |
| ag_land_quantity     | any    | Agricultural land is the sum of croplands and pasture used for livestock grazing.                         |
| labor_quantity       | any    |                                                                                                           |
| capital_quantity     | any    |                                                                                                           |
| machinery_quantity   | any    |                                                                                                           |
| livestock_quantity   | any    | Livestock counts are measured in heads of standard livestock units.                                       |
| fertilizer_quantity  | any    | Fertilizer consumption is measured as the sum of synthetic inputs of nitrogen, potassium and phosphorous, plus organic nitrogen inputs. |
| animal_feed_quantity | any    | Animal feed production is measured in Mcal of metabolizable energy.                                       |
| cropland_quantity    | any    |                                                                                                           |
| pasture_quantity     | any    | Pasture is grassland used for livestock grazing.                                                          |
| irrigation_quantity  | any    |                                                                                                           |



## Class: Analysis

The Analysis class provides a set of methods for analyzing agricultural data. It includes methods for downloading and saving data, generating a list of countries in the dataset, plotting correlation matrices, and generating line graphs and area charts.

Here below we briefly describe each method:

#### download_save_data()

This method downloads the agriculture data from a remote CSV file and saves it to a local file in a "downloads" directory. It takes no parameters and reads the data as a pandas dataframe. 

#### countries_list()
This method simply returns a list of all unique countries in the dataset. It takes no parameters.

#### plot_quantity_correlations()
This method plots a correlation matrix (heatmap) of the variables in the agriculture data that consider inputs and outputs' quantities. It takes no parameters.

#### plot_output_area(entity, normalize)
This method plots an area chart of crop, animal, and fish output quantities over time for a given geographical area. The entity parameter is the name of the country to plot (e.g. "_United States_"). When receiving _None or "World"_, it plots the World's total output. The _normalize_ parameter is a boolean value that, when set to _True_, normalizes the output values in relative terms.

#### compare_output_for_countries(countries)
This method compares the total output of crop, animal, and fish for the specified countries over time. It plots a line graph to visualize how these production quantities evolve for each country.

The _countries_ parameter is a string or a list of strings containing the names of countries to compare.

#### gapminder(year):

The gapminder method creates a scatter plot of fertilizer quantity versus output quantity, with bubble sizes representing irrigation quantity. The plot is colored based on agricultural land quantity.

The _year_ parameter is an integer specifying the year of production. This graph is useful to analyze the world's agricultural production.

#### choropleth(year)

This method plots a choropleth map of Total Factor Productivity (tfp) for the countries present in the Agricultural Dataset. A choropleth map is a type of thematic map that displays data using color-coded regions, defined by countries. We here use geodata to plot the map. 

The _year_ parameter is an integer specifying the year of production.
        
#### predict_tfp()

This method plots the Total Factor Productivity data for the specified countries and their ARIMA predictions up to year 2050. 

The _countries_ parameter is a list of up to three countries to consider in the line graph.

## Repository

The project was created using Python 3.8 and makes use of various libraries including pandas, requests, seaborn, and matplotlib.

This repository includes: 

- **showcase_notebook_09.ipynb**: notebook that imports the main class and demonstrates its usage for a brief data analysis. 
- **downloads**: directory with the dataset CSV
- **function**: directory storing the class and the methods.
- **prototypes**: directory that contains files with trials from different authors, which were used in the development of the project's class.
- **YAML file**: with all the required dependencies
- **LICENSE**: see the paragraph below for details abot the License. 
- **.gitignore**: file that specifies which files and directories should be ignored by Git. Ignoring certain files can help keep your repository clean and organized, and prevent unnecessary files from being committed to version control

To use this project, simply import the Analysis class or check the Showcase Notebook to understand better our initial analysis.

## License
This repository is licensed under the Apache License Version 2.0. This allows you to use, distribute and modify the software freely, subject to certain conditions such as retaining the original copyright notice and disclaimer.

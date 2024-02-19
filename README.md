# README: 
## Project Setup
```bash 
# clone repository at a desired location on your machine
git clone https://github.com/Pulkit-m/mean-reversion.git

# cd into the root directory: 
cd mean-reversion 

# set-up a virtual environment if you prefer so. 
# python -m venv ./venv 
# ./venv/Scripts/activate (windows) 

# install dependencies: 
pip3 install -r requirements.txt 
``` 

### Downloading data from source: 
Scripts to download source data have already been provided in `data/scripts` folder.  
**You should run those scripts without changing your working directory.** 
```bash
# downloads the index composition
python ./data/scripts/download_index_composition.py 
# downloads the stock data.
python ./data/scripts/download_stocks_data.py
```
The stock history data shall be stored in two separate directories: `./data/raw/insample/` and `./data/raw/outsample` for insample and outsample data respectively. 
___

The Project is now all setup and ready to run. 
The following are some files of interest: 
* `utils.indicators.py`: This file Contains functions for indicators that shall help us identify overbought and oversold regions for our strategies. You do not need to edit this file
* `utils.strategies.py`: This file contains a few coded strategies that we shall use. You do not need to edit this file
* `main.py`: You can directly run this file to test any strategy, on data of your choice, with default parameters or optimized parameters. This also generates a results csv in the `./results` folder and corresponding trades executed can be visualized in plots that can be found in `./results/plots` folder. You can run this file directly with appropriate command line arguments. 
    ```bash
    python main.py --strategy bb --data_folder ./data/raw/outsample --plots True --opt_params ./data/opt_params.csv
    #strategy options: 'macd', 'bb' 
    #--plots is False by default
    ```
* `parameter_optimization.ipynb`: This Jupyter notebook is used to load strategies and optimize them using Grid Search Methodology. The Optimized parameters are stored in a csv file at `./data/opt_params.csv`
    * If the notebook does not open or malfunction, you can try uploading it on google colab. 




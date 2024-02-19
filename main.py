import pandas as pd 
import matplotlib.pyplot as plt 

import os 
from glob import glob 
from tqdm import tqdm
import random
import warnings
warnings.filterwarnings("ignore")

import pandas as pd 
import matplotlib.pyplot as plt

from utils.indicators import movingAverageConverganceDivergance as macd 
from utils.indicators import relativeStrengthIndex as rsi 
from utils.indicators import averageTrueRange as atr 
from utils.indicators import bollingerBands as bbands 
from utils.indicators import stochasticIndicator as sti

from utils.strategies import BollingerBandsStrategy 
from utils.strategies import MACDStrategy 
from utils.strategies import BuyAndHoldStrategy 
from utils.strategies import SimpleMovingAverageStrategy

from backtesting import Backtest, Strategy 
from backtesting.lib import crossover, barssince, SignalStrategy, TrailingStrategy


import argparse 
parser = argparse.ArgumentParser(
                    prog='Strategy Tester',
                    description='applies the strategy on test data available in data/outsample folder',
                    epilog='Kindly run the Scripts available in the data/Scripts folder before running this script to ensure availability of data. ')
parser.add_argument('--strategy', default='bb', choices=['bb','macd','sma','bnh'],
                     help="bb: Bollinger Bands; \
                        macd: MovingAverage Convergance Divergance; \
                            sma: Simple Moving Average;\
                                bnh: Buy And Hold", dest="strategy")
parser.add_argument('--data_folder', default="./data/raw/outsample") 
parser.add_argument('--opt_params', default='./data/opt_params.csv')
parser.add_argument('--num_stocks', default = 500, type=int)
parser.add_argument('--random_seed', default=None, type = int, help="\
                    set to any integer otherwise None by Default")
parser.add_argument('--ticker', default = None)
parser.add_argument('--plots', default=False, type = bool)

args = vars(parser.parse_args())
strategy = None 
if(args['strategy'] == 'bb'): 
    strategy = BollingerBandsStrategy 
elif(args['strategy'] == 'macd'): 
    strategy = MACDStrategy 
elif args['strategy'] == 'sma': 
    strategy = SimpleMovingAverageStrategy 
elif args['strategy'] == 'bnh': 
    strategy = BuyAndHoldStrategy

opt_param_file = args['opt_params'] 
num_stocks = args['num_stocks'] 
data_folder = args['data_folder']
random_seed = args['random_seed']
stock_name = args['ticker']
trade_plots = args['plots']


def runBuyAndHoldStrategy(stock_df): 
    bt = Backtest(stock_df, BuyAndHoldStrategy, cash=10_000) 
    stats = bt.run()
    profit_buy_and_hold = stats['Equity Final [$]'] - 10000 
    return stats , profit_buy_and_hold


def runBollingerBandsStrategy(stock_name, stock_df, opt_params = None, plot_path = None): 
    if opt_params is None: 
        bt = Backtest(stock_df, BollingerBandsStrategy, cash = 10_000) 
        stats = bt.run() 
        if trade_plots: 
             bt.plot(open_browser=False, filename = plot_path)
        profit_strategy = stats['Equity Final [$]'] - 10000 
        return stats, profit_strategy
    
    else: 
        bt = Backtest(stock_df, BollingerBandsStrategy, cash = 10_000) 
        name = stock_name.split('\\')[-1].split('.')[0].split('_')[-1]
        params = opt_params.loc[opt_params_df.ticker == name]
        stats = bt.run(bb_window = params['bb_window'].values[0] ,
            rsi_window = params['rsi_window'].values[0],
            rsi_smooth_window = params['rsi_smooth_window'].values[0],
            rsi_upper_thres = params['rsi_upper_thres'].values[0] ,
            rsi_lower_thres = params['rsi_lower_thres'].values[0] )
        
        if trade_plots: 
             bt.plot(open_browser=False, filename = plot_path)
        profit_strategy = stats['Equity Final [$]'] - 10000
        return stats, profit_strategy
    


def runMACDStrategy(stock_name, stock_df, opt_params = None, plot_path = None): 
    if opt_params is None: 
        bt = Backtest(stock_df, MACDStrategy, cash = 10_000) 
        stats = bt.run() 
        if trade_plots: 
             bt.plot(open_browser=False, filename = plot_path)
        profit_strategy = stats['Equity Final [$]'] - 10000 
        return stats, profit_strategy
    
    else: 
        bt = Backtest(stock_df, MACDStrategy, cash = 10_000) 
        name = stock_name.split('\\')[-1].split('.')[0].split('_')[-1]
        params = opt_params.loc[opt_params_df.ticker == name]
        stats = bt.run(macd_fast_ma_length = params['macd_fast_ma_length'].values[0], 
                macd_slow_ma_length = params['macd_slow_ma_length'].values[0],
                macd_signal_ma_length = params['macd_signal_ma_length'].values[0] )
        
        if trade_plots: 
             bt.plot(open_browser=False, filename = plot_path)
        profit_strategy = stats['Equity Final [$]'] - 10000
        return stats, profit_strategy
    

def runSimpleMovingAverageStrategy(stock_name, stock_df, opt_params = None): 
    pass 



if __name__ == '__main__': 
    opt_params_df = None
    if not os.path.exists(opt_param_file): 
        print("Optimized Parameters not found, Continueing with Default Parameter Values")
    else:
        opt_params_df = pd.read_csv(opt_param_file) 
        print("Using Optimized Params...")

    if not os.path.exists(data_folder): 
        raise Exception ("Test Data Not Found. Kindly Run the Scripts available in data/Scripts folder. For more detail refer README.md")
    
    
    stock_names = [] 
    if stock_name is not None: 
        stock_names.append(f'{data_folder}/history_stock_{stock_name}.csv') 
    else: 
        stock_names = glob(f'{data_folder}/*') 
        if random_seed: 
            random.seed(random_seed) 
        stock_names = random.sample(stock_names,k = num_stocks) 

    
    if not os.path.exists("./results"): 
        os.makedirs("./results", exist_ok=True)
    if not os.path.exists("./results/plots"): 
        os.makedirs("./results/plots", exist_ok= True)


    results = {
        "ticker": [],
        "return": [], 
        "buy and hold return": [], 
        "Max. Drawdown [%]": [],
        "Avg. Drawdown [%]": [],       
        "Max. Drawdown Duration": [],  
        "Avg. Drawdown Duration" : [], 
        "Num Trades": [],                
        "Win Rate [%]": [],            
        "Best Trade [%]": [],          
        "Worst Trade [%]": [],         
        "Avg. Trade [%]": [],          
        "Max. Trade Duration": [],     
        "Avg. Trade Duration": [],
        "plot_path": []
    }
    
    profit_buy_and_hold = 0
    profit_strategy = 0
    all_trades = None 
    for stock_name in tqdm(stock_names): 
        stock_df = pd.read_csv(stock_name, index_col=False)
        if(stock_df.shape[0]==0): continue
        
        stats_bnh, profit_bnh = runBuyAndHoldStrategy(stock_df)
        profit_buy_and_hold += profit_bnh

        name = stock_name.split('\\')[-1].split('.')[0].split('_')[-1]
        plot_path = f"./results/plots/{name}.html" 
        if args['strategy'] == 'bb': 
            stats_strat, profit_strat = runBollingerBandsStrategy(stock_name, stock_df, opt_params_df, plot_path)
        elif args['strategy'] == 'macd': 
            stats_strat, profit_strat = runMACDStrategy(stock_name, stock_df, opt_params_df, plot_path)
        elif args['strategy'] == 'sma': 
            stats_strat, profit_strat = runSimpleMovingAverageStrategy(stock_name, stock_df, opt_params_df, plot_path)
        profit_strategy += profit_strat 


        plot_path = f"./results/plots/{stock_name}.html" 
        results['ticker'].append(name)
        results['return'].append(stats_strat['Return [%]']) 
        results['buy and hold return'].append(stats_strat['Buy & Hold Return [%]'])
        results['plot_path'].append(plot_path) 
        results['Avg. Drawdown [%]'].append(stats_strat['Avg. Drawdown [%]'])
        results['Avg. Drawdown Duration'].append(stats_strat['Avg. Drawdown Duration']) 
        results['Avg. Trade [%]'].append(stats_strat['Avg. Trade [%]'])
        results['Avg. Trade Duration'].append(stats_strat['Avg. Trade Duration'])
        results['Best Trade [%]'].append(stats_strat['Best Trade [%]'])
        results['Max. Drawdown [%]'].append(stats_strat['Max. Drawdown [%]'])
        results['Max. Drawdown Duration'].append(stats_strat['Max. Drawdown Duration'])
        results['Max. Trade Duration'].append(stats_strat['Max. Trade Duration'])
        results['Num Trades'].append(stats_strat['# Trades'])
        results['Win Rate [%]'].append(stats_strat['Win Rate [%]'])
        results['Worst Trade [%]'].append(stats_strat['Worst Trade [%]'])


        if all_trades is not None: 
            all_trades = pd.concat([all_trades, stats_strat._trades]) 
        else: 
            all_trades = stats_strat._trades


    print(f"\n\nProfit from Simple Buy and Hold Strategy: {profit_buy_and_hold}. ") 
    print(f"Profit from {args['strategy']} strategy: {profit_strategy}")

    pd.DataFrame(results).to_csv(f"./results/results_{args['strategy']}.csv", index = False)
    print("Results saved in Results Folder. ")


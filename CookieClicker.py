"""
Cookie Clicker Simulator

Author: John Liu
Date: 2014-23-Jun
"""

import simpleplot

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(60)

import poc_clicker_provided as provided
import math

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._current_time = 0.0
        self._total_cookies = 0.0
        self._current_cookies = 0.0
        self._cookies_per_second = 1.0
        self._history = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        return ("time = " + str(self._current_time) + "\n" +
                "cookies = " + str(self._current_cookies) + "\n" +
                "cps = " + str(self._cookies_per_second) + "\n" +
                "total =" + str(self._total_cookies))
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._cookies_per_second
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: (0.0, None, 0.0, 0.0)
        """
        return self._history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if self._current_cookies > cookies:
            return 0.
        else:
            return math.ceil((cookies-self._current_cookies)/self._cookies_per_second)
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0
        """
        if time <= 0:
            return
        self._current_time += time
        self._current_cookies += time * self._cookies_per_second
        self._total_cookies += time * self._cookies_per_second
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self._current_cookies < cost:
            return
        
        self._current_cookies -= cost
        self._cookies_per_second += additional_cps
        self._history.append((self._current_time,
                             item_name,
                             cost,
                             self._total_cookies))
   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to game.
    """
    my_state = ClickerState()
    my_build_info = build_info.clone()
    
    while my_state.get_time() <= duration:
        my_item = strategy(my_state.get_cookies(),
                               my_state.get_cps(),
                               duration - my_state.get_time(),
                               my_build_info)
        if (my_item == None):
            break
        time_needed = my_state.time_until(my_build_info.get_cost(my_item))
        if (time_needed > duration - my_state.get_time()):
            break
        my_state.wait(time_needed)
        my_state.buy_item(my_item,
                          my_build_info.get_cost(my_item),
                          my_build_info.get_cps(my_item))
        my_build_info.update_item(my_item)
        
    if my_state.get_time() < duration:
        my_state.wait(duration - my_state.get_time())
        
    if my_item != None:
        while my_state.get_cookies() > my_build_info.get_cost(my_item):
            my_state.buy_item(my_item,
                              my_build_info.get_cost(my_item),
                              my_build_info.get_cps(my_item))
            my_build_info.update_item(my_item)

    
    return my_state


def strategy_cursor(cookies, cps, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic strategy does not properly check whether
    it can actually buy a Cursor in the time left.  Your strategy
    functions must do this and return None rather than an item you
    can't buy in the time left.
    """
    return "Cursor"

def strategy_none(cookies, cps, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that you can use to help debug
    your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, time_left, build_info):
    """
    Always pick cheapest strategy
    """
    low_item = None
    low_cost = 999999999.
    for item in build_info.build_items():
        item_cost = build_info.get_cost(item)
        if (item_cost <= cookies + cps * time_left) and (item_cost < low_cost):
            low_item = item
            low_cost = item_cost
            
    return low_item    
        
def strategy_expensive(cookies, cps, time_left, build_info):
    """
    Always pick most expensive strategy
    """
    hi_item = None
    hi_cost = 0.
    for item in build_info.build_items():
        item_cost = build_info.get_cost(item)
        if (item_cost <= cookies + cps * time_left) and (item_cost > hi_cost):
            hi_item = item
            hi_cost = item_cost
            
    return hi_item    

def strategy_best(cookies, cps, time_left, build_info):
    """
    My best strategy
    """
    best_item = None
    best_cps = 0.
    for item in build_info.build_items():
        item_cost = build_info.get_cost(item)
        item_cps = build_info.get_cps(item)
        if (item_cost <= cookies + cps * time_left) and (item_cps/item_cost > best_cps ):
            best_item = item
            best_cps = item_cps/item_cost
            
    return best_item    
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation with one strategy
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_cursor)

    # Add calls to run_strategy to run additional strategies
    # run_strategy("Cheap", SIM_TIME, strategy_cheap)
    # run_strategy("Expensive", SIM_TIME, strategy_expensive)
    # run_strategy("Best", SIM_TIME, strategy_best)
    
#run()
    


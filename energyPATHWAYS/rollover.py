# -*- coding: utf-8 -*-
"""
Created on Thu Oct 01 09:26:56 2015

@author: ryan
"""

import numpy as np
import util

class Rollover(object):
    def __init__(self, vintaged_markov_matrix, initial_markov_matrix, num_years, num_vintages, num_techs,
                 initial_stock=None, sales_share=None, stock_changes=None, specified_stock=None,
                 specified_retirements=None, specified_sales=None, steps_per_year=1, stock_changes_as_min=False):
        """
        initial stock of NaN is assumed to be zero
        """
        if np.any(np.isnan(vintaged_markov_matrix)) or np.any(np.isnan(initial_markov_matrix)):
            raise ValueError('Markov Matrix cannot contain NaN')
        
        if steps_per_year < 1:
            raise ValueError('Running stock rollover with fewer than one step per year is not supported')
        
        # required inputs
        self.spy = steps_per_year
        self.vintaged_markov_matrix = vintaged_markov_matrix
        self.initial_markov_matrix = initial_markov_matrix
        self.num_years, self.num_vintages, self.num_techs = num_years, num_vintages, num_techs

        # additional inputs
        self.initialize_initial_stock(initial_stock)
        self.initialize_sales_share(sales_share)
        self.initialize_stock_changes(stock_changes)
        self.initialize_specified_retirements(specified_retirements)
        self.initialize_specified_stock(specified_stock)
        self.initialize_specified_sales(specified_sales)
        
        self.stock_changes_as_min = stock_changes_as_min
        self.all_techs = np.arange(self.num_techs, dtype=int)
        self.stock = np.zeros((self.num_techs, self.num_vintages*self.spy + 1, self.num_years*self.spy))
        self.rolloff_record = np.zeros((self.num_years*self.spy, self.num_techs))
        self.natural_rolloff = np.zeros((self.num_years*self.spy, self.num_techs))
        self.sales_record = np.zeros((self.num_years*self.spy, self.num_techs))
        self.prinxy = np.zeros(self.num_techs)
        self.i = 0
        
        # eventual outputs
        self.stock_new = np.zeros(np.shape(self.stock))
        self.stock_replacement = np.zeros(np.shape(self.stock))
        self.new_sales = np.zeros(np.shape(self.sales_record))
        self.replacement_sales = np.zeros(np.shape(self.sales_record))
        self.new_sales_fraction = np.zeros(np.shape(self.sales_record))
        self.early_retirements = np.zeros((self.num_years*self.spy, self.num_techs))

    def initialize_initial_stock(self, initial_stock):
        if initial_stock is None:
            self.initial_stock = np.zeros(self.num_techs)
        else:
            self.initial_stock = np.nanmax((np.zeros(self.num_techs), np.array(util.ensure_iterable_and_not_string(initial_stock))), axis=0)

    def initialize_sales_share(self, sales_share):
        """ Sales shares are constant over all periods within the year
        """
        shape = (self.num_years*self.spy, self.num_techs, self.num_techs)
        if sales_share is None:
            self.sales_share = np.ones(shape)/self.num_techs
        else:
            self.sales_share = np.reshape(np.repeat(sales_share, self.spy, axis=0), shape)

    def initialize_stock_changes(self, stock_changes):
        """ Stock changes get spread equally over all periods within the year
        """
        shape = self.num_years*self.spy
        if stock_changes is None:
            self.stock_changes = np.zeros(shape)
        else:
            self.stock_changes = np.reshape(np.repeat(stock_changes/self.spy, self.spy, axis=0), shape)

    def initialize_specified_retirements(self, specified_retirements):
        """ Specified retirements get spread equally over all periods within the year
        """
        shape = self.num_years*self.spy
        if specified_retirements is None:
            self.specified_retirements = np.zeros(shape)
        else:
            self.specified_retirements = np.reshape(np.repeat(specified_retirements/self.spy, self.spy, axis=0), shape)
        
        if np.any(self.specified_retirements<0):
            raise ValueError('Specified retirements cannot be negative. Grow stock by specifying positive stock changes.')

    def initialize_specified_stock(self, specified_stock):
        """ Stock gets specified in the past period of the year
        """
        shape = (self.num_years*self.spy, self.num_techs)
        if specified_stock is None:
            self.specified_stock = np.empty(shape)
            self.specified_stock.fill(np.nan)
        else:
            self.specified_stock = np.array(util.flatten_list([[[np.nan]*self.num_techs]*(self.spy-1) + [list(util.ensure_iterable_and_not_string(ss))] for ss in specified_stock]))
#            if self.spy == 1:
#                self.specified_stock = specified_stock
#            else:
#                self.specified_stock = np.array(util.flatten_list([[[np.nan]*self.num_techs]*(self.spy-1) + [list(util.ensure_iterable_and_not_string(ss))] for ss in specified_stock]))
#                if self.num_techs == 1:
#                    self.specified_stock = self.specified_stock.flatten()
        if np.any(self.specified_stock<0):
            raise ValueError("Specified stock cannot be initialized with negative numbers")

    def initialize_specified_sales(self, specified_sales):
        """ Divide sales equally over all periods within the year
        """
        shape = (self.num_years*self.spy, self.num_techs)
        if specified_sales is None:
            self.specified_sales = np.empty(shape)
            self.specified_sales.fill(np.nan)
        else:
            self.specified_sales = np.reshape(np.repeat(specified_sales/self.spy, self.spy, axis=0), shape)
        if np.any(self.specified_sales<0):
            raise ValueError("Specified sales cannot be initialized with negative numbers")

    def calc_initial_stock_rolloff(self, prinxy, mode='rolloff'):
        i = self.i  # make an int
        if mode == 'rolloff':
            return (self.initial_stock if i == 0 else self.stock[:, 0, i - 1]) * (1 - self.initial_markov_matrix[self.all_techs, i, prinxy])
        elif mode == 'remaining':
            return (self.initial_stock if i == 0 else self.stock[:, 0, i - 1]) * self.initial_markov_matrix[self.all_techs, i, prinxy]

    def calc_vintaged_stock_rolloff(self, prinxy, mode='rolloff'):
        i = self.i  # make an int
        if mode == 'rolloff':
            return self.stock[:, 1:i + 1, i - 1] * (0 if i == 0 else (1 - self.vintaged_markov_matrix[self.all_techs, i - 1::-1, prinxy]))
        elif mode == 'remaining':
            return self.stock[:, 1:i + 1, i - 1] * (0 if i == 0 else self.vintaged_markov_matrix[self.all_techs, i - 1::-1, prinxy])

    def sum_vintaged_stock_rolloff(self, prinxy):
        return 0 if self.i == 0 else np.sum(self.calc_vintaged_stock_rolloff(prinxy), axis=1)

    def sum_rolloff(self, prinxy):
        return self.calc_initial_stock_rolloff(prinxy) + self.sum_vintaged_stock_rolloff(prinxy)

    def calc_stock_rolloff(self, prinxy):
        f_prinxy, c_prinxy = np.array(np.floor(prinxy), dtype=int), np.array(np.ceil(prinxy), dtype=int)
        if np.all(f_prinxy == c_prinxy):
            return self.sum_rolloff(np.array(prinxy, dtype=int))
        else:
            f_rolloff = self.sum_rolloff(f_prinxy)
            c_rolloff = self.sum_rolloff(c_prinxy)
            return f_rolloff + (prinxy - f_prinxy) * (c_rolloff - f_rolloff)

    def update_prinxy(self, incremental_retirement, retireable):
        """ A positive incremental retirement means that retirements are increasing
        """
        if incremental_retirement == 0 or sum(self.prior_year_stock[retireable]) == 0:
            return

        if incremental_retirement > sum(self.prior_year_stock[retireable]):
            raise ValueError('specified incremental stock retirements are greater than retireable stock size')

        starting_rolloff = np.sum(self.calc_stock_rolloff(self.prinxy))
        old_rolloff, new_rolloff = starting_rolloff, starting_rolloff
        temp_prinxy = np.copy(self.prinxy)

        inc = 1 if incremental_retirement > 0 else -1
        temp_prinxy[retireable] = np.floor(temp_prinxy[retireable]) if incremental_retirement > 0 else np.ceil(
            temp_prinxy[retireable])
        while inc * incremental_retirement > inc * (new_rolloff - starting_rolloff):
            if (np.all(temp_prinxy[retireable] == 0) and inc == -1) or (
                        np.all(temp_prinxy[retireable] == self.num_years - 1) and inc == 1):
                self.prinxy = temp_prinxy
                return
            temp_prinxy[retireable] = np.clip(temp_prinxy[retireable] + inc, 0, self.num_years - 1)
            old_rolloff, new_rolloff = new_rolloff, np.sum(self.calc_stock_rolloff(temp_prinxy))
        temp_prinxy[retireable] -= inc * (
            1 - (incremental_retirement + starting_rolloff - old_rolloff) / (new_rolloff - old_rolloff))
        self.prinxy = temp_prinxy

    def calc_remaining_stock_initial(self):
        f_prinxy, c_prinxy = np.array(np.floor(self.prinxy), dtype=int), np.array(np.ceil(self.prinxy), dtype=int)
        if np.all(f_prinxy == c_prinxy):
            return self.calc_initial_stock_rolloff(np.array(self.prinxy, dtype=int), mode='remaining')
        else:
            f_rolloff = self.calc_initial_stock_rolloff(f_prinxy, mode='remaining')
            c_rolloff = self.calc_initial_stock_rolloff(c_prinxy, mode='remaining')
        return f_rolloff + (self.prinxy - f_prinxy) * (c_rolloff - f_rolloff)

    def calc_remaining_stock_vintaged(self):
        f_prinxy, c_prinxy = np.array(np.floor(self.prinxy), dtype=int), np.array(np.ceil(self.prinxy), dtype=int)
        if np.all(f_prinxy == c_prinxy):
            return self.calc_vintaged_stock_rolloff(np.array(self.prinxy, dtype=int), mode='remaining')
        else:
            f_rolloff = self.calc_vintaged_stock_rolloff(f_prinxy, mode='remaining')
            c_rolloff = self.calc_vintaged_stock_rolloff(c_prinxy, mode='remaining')
        return f_rolloff + ((self.prinxy - f_prinxy) * (c_rolloff - f_rolloff).T).T

    def update_stock(self):
        i = self.i  # make an int
        self.stock[:, 0, i] = self.calc_remaining_stock_initial()
        self.stock[:, 1:i + 1, i] = self.calc_remaining_stock_vintaged()
        self.stock[:, i + 1, i] = self.stock_change_by_tech

    def account_for_specified_stock(self):
        i = self.i
        if np.any((self.specified_sales[i]!=self.specified_stock[i])[np.array(list(set(self.stock_specified) & set(self.sales_specified)), dtype=int)]):
            raise RuntimeError('Missmatch between specified sales and specified stock with no existing stock')
        
        # if you have specified stock, it implies sales that supersede natural sales
        self.defined_sales = self.specified_stock[i] - (self.prior_year_stock - self.rolloff) # may result in a negative
        self.defined_sales[self.sales_specified] = self.specified_sales[i, self.sales_specified]
        
        # a negative specified sale means you need to do early retirement
        self.sum_defined_sales = np.sum(self.defined_sales[self.specified])

        if len(self.specified) and np.sum(self.prior_year_stock):
            if not self.stock_changes_as_min and round(sum(self.specified_stock[i][self.stock_specified]), 6) > round(np.sum(self.prior_year_stock) + self.stock_changes[i], 6):
                raise RuntimeError('Specified stock in a given year is greater than the total stock')

            # if we have both a specified stock and specified sales for a tech, we need to true up the vintaged stock to make both match, if possible
            if len(set(self.sales_specified) & set(self.stock_specified)):
                for overlap_index in set(self.sales_specified) & set(self.stock_specified):
                    retireable = np.array([overlap_index], dtype=int)
                    needed_retirements = self.specified_sales[i, overlap_index] - (self.specified_stock[i, overlap_index] - (self.prior_year_stock[overlap_index] - self.rolloff[overlap_index]))
                    if needed_retirements < 0:
                        raise RuntimeError('Missmatch between specified sales and specified stock implying a growth of vintaged stock')
                    self.update_prinxy(needed_retirements, retireable)
                # Because of the retirements, we have a new natural rolloff number
                self.update_rolloff()

            # if specified sales are negative, we need to accelerate retirement for that technology
            if np.any(self.defined_sales[self.specified] < 0):
                for neg_index in np.nonzero(self.defined_sales < 0)[0]:
                    retireable = np.array([neg_index], dtype=int)
                    # negative is needed before self.defined_sales because a postive number indicates retirement
                    self.update_prinxy(-self.defined_sales[neg_index], retireable)
                    self.defined_sales[neg_index] = 0
                self.sum_defined_sales = np.sum(self.defined_sales[self.specified])
                # Because of the retirements, we have a new natural rolloff number
                self.update_rolloff()

            # Here, if stock changes as min
            if self.stock_changes_as_min:
                self.stock_changes[i] = max(self.stock_changes[i], self.sum_defined_sales - self.rolloff_summed)

            # We need additional early retirement to make room for defined_sales
            if round(self.sum_defined_sales, 6) > round(self.rolloff_summed + self.stock_changes[i], 6):
                # print 'We need additional early retirement to make room for defined_sales ' + str(i)
                incremental_retirement = self.sum_defined_sales - (self.rolloff_summed + self.stock_changes[i])
                self.update_prinxy(incremental_retirement, self.solvable)

                # Because of the retirements, we have a new natural rolloff number
                self.update_rolloff()

    def account_for_specified_retirements(self):
        i = self.i  # make an int
        if (np.sum(self.prior_year_stock) > 0) and (self.specified_retirements is not None) and (self.specified_retirements[i] > 0):
            self.update_prinxy(self.specified_retirements[i], self.all_techs)

    def account_for_stock_shrinkage(self):
        i = self.i  # make an int
        if round(self.stock_changes[i], 6) < round(self.sum_defined_sales - self.rolloff_summed, 6):
            # print 'stock change is less than specified sales minus rolloff, we need additional retirements ' + str(i)
            incremental_retirement = (self.sum_defined_sales - self.rolloff_summed) - self.stock_changes[i]
            self.update_prinxy(incremental_retirement, self.solvable)
            self.update_rolloff()

    def update_rolloff(self):
        self.rolloff = self.calc_stock_rolloff(self.prinxy)
        self.rolloff_summed = np.sum(self.rolloff)

    def set_final_stock_changes(self):
        i = self.i  # make an int
        # calculate final sales
        if np.sum(self.rolloff):
            self.stock_change_by_tech = np.dot(self.sales_share[i], self.rolloff)  # natural sales
        else:
            self.stock_change_by_tech = np.mean(np.linalg.matrix_power(self.sales_share[i], 100), axis=1) * self.stock_changes[i]

        #stock changes are greater than all defined sales, so all sales need to increase to agree with stock changes
        if self.stock_changes_as_min and (self.stock_changes[i] > self.sum_defined_sales):
            self.stock_change_by_tech *= (self.stock_changes[i] + self.rolloff_summed) / np.sum(self.stock_change_by_tech)
            self.stock_change_by_tech[self.specified] = np.nanmax((self.defined_sales[self.specified], self.stock_change_by_tech[self.specified]), axis=0)
            if np.sum(self.stock_change_by_tech[self.solvable]):
                self.stock_change_by_tech[self.solvable] *= (np.sum(self.stock_change_by_tech)-np.sum(self.stock_change_by_tech[self.specified])) / np.sum(self.stock_change_by_tech[self.solvable])
        else:
            if len(self.specified):
                self.stock_change_by_tech[self.specified] = self.defined_sales[self.specified]
            
            # True up the residual
            if np.sum(self.stock_change_by_tech[self.solvable]):
                self.stock_change_by_tech[self.solvable] *= round((self.stock_changes[i] + self.rolloff_summed) - self.sum_defined_sales, 9) / np.sum(self.stock_change_by_tech[self.solvable])

    def set_final_sales(self):        
        # gross up for retirements within the period (approximation)
        self.sales_by_tech = self.stock_change_by_tech/self.vintaged_markov_matrix[:,0,0]
        # this division assumes that stock that retires within the period has an equal chance of also having the replacement replaced
        # this is a conservative assumption

    def introduce_inputs_override(self, num, introduced_stock_changes, introduced_specified_stock, introduced_specified_sales, decimals=10):
        list_steps = range(self.i, self.num_years*self.spy) if num is None else range(self.i, min(self.i+num*self.spy, self.num_years*self.spy))        
        if introduced_stock_changes is not None:
            if num!=len(util.ensure_iterable_and_not_string(introduced_stock_changes)):
                raise ValueError("length of annual stock_changes must match the number of years to run")
            if np.any(np.isnan(introduced_stock_changes)):
                raise ValueError("introduced annual stock_changes cannot be nan")
            self.stock_changes[list_steps] = np.reshape(np.repeat(introduced_stock_changes/self.spy, self.spy, axis=0), len(list_steps))

        if introduced_specified_stock is not None:
            if num!=len(util.ensure_iterable_and_not_string(introduced_specified_stock)):
                raise ValueError("length of annual specified_stock must match the number of years to run")
            self.specified_stock[list_steps] = np.array(util.flatten_list([[[np.nan]*self.num_techs]*(self.spy-1) + [list(util.ensure_iterable_and_not_string(ss))] for ss in np.round(introduced_specified_stock, decimals)]))
            if np.any(self.specified_stock[list_steps]<0):
                raise ValueError("introduced specified stock cannot be negative")
            
#            self.specified_stock[list_steps] = np.reshape(np.repeat(introduced_specified_stock, self.spy, axis=0), len(list_steps))

        if introduced_specified_sales is not None:
            if num!=len(util.ensure_iterable_and_not_string(introduced_specified_sales)):
                raise ValueError("length of annual specified_sales must match the number of years to run")
            self.specified_sales[list_steps] = np.reshape(np.repeat(np.round(introduced_specified_sales, decimals)/self.spy, self.spy, axis=0), len(list_steps))
            if np.any(self.specified_sales[list_steps]<0):
                raise ValueError("introduced specified sales cannot be negative")

    def factor_adjust_current_year(self, factor, decimals=10):
        if np.round(factor, decimals)<0:
            raise ValueError('Current year adjustment factor as given as ' + str(factor) + ' but cannot be negative')
        factor = np.round(factor, decimals)
        i = self.i-self.spy
        self.sales_record[i] *= factor
        self.stock[:, i + 1, i] *= factor
        list_steps = range(i, min(i+self.spy, self.num_years*self.spy))
        self.check_outputs()
        self.calculate_outputs(list_steps)

    def run(self, num=None, introduced_stock_changes=None, introduced_specified_stock=None, introduced_specified_sales=None):
        """
        num_years: number of years to simulate
        stock_changes: annual increase (positive) or decrease (negative) in total stock
        """
        list_steps = range(self.i, self.num_years*self.spy) if num is None else range(self.i, min(self.i+num*self.spy, self.num_years*self.spy))
        self.introduce_inputs_override(num, introduced_stock_changes, introduced_specified_stock, introduced_specified_sales)
        
        for i in list_steps:
            self.i = i
            self.prinxy = np.zeros(self.num_techs)  # probability of retiring in next x years

            self.stock_specified = np.nonzero(~np.isnan(self.specified_stock[i]))[0]
            self.sales_specified = np.nonzero(~np.isnan(self.specified_sales[i]))[0]
            self.specified = np.array(list(set(self.stock_specified) | set(self.sales_specified)), dtype=int)
            self.solvable = np.array(list(set(self.all_techs).difference(set(self.specified))), dtype=int)

            # Get prior year's stock
            self.prior_year_stock = self.initial_stock if i == 0 else np.sum(self.stock[:, :i + 1, i - 1], axis=1)

            # Get natural retirements
            self.natural_rolloff[i] = self.calc_stock_rolloff(self.prinxy)

            # specified early retirements are done first
            self.account_for_specified_retirements()

            # Get natural rolloff (with specified early retirements)
            self.update_rolloff()

            # We have specified stock
            self.account_for_specified_stock()

            # if stock change is less than specified sales minus rolloff, we need additional retirements
            self.account_for_stock_shrinkage()

            self.set_final_stock_changes()
            self.update_stock()
            self.set_final_sales()
            
            self.sales_record[i] = self.sales_by_tech
            self.rolloff_record[i] = self.rolloff
        
        if list_steps:
            self.check_outputs()
            self.calculate_outputs(list_steps)
            #increment self.i, this saves the position where the rollover left off
            self.i = min(self.num_years, i+1)

    def rewind(self, num_years):
        self.i -= num_years*self.spy

    def check_outputs(self):
        if np.any(np.isnan(self.stock)):
            raise ValueError('Stock values of NaN encountered while checking outputs')
        
        if np.any(self.stock<0):
            raise ValueError('Negative stock values encountered while checking outputs')

    def calculate_outputs(self, list_steps):
        self.early_retirements[list_steps] = self.rolloff_record[list_steps] - self.natural_rolloff[list_steps]
        self.new_sales[list_steps] = np.clip(self.sales_record[list_steps] - self.natural_rolloff[list_steps], a_min=0, a_max=self.sales_record[list_steps])
        self.replacement_sales[list_steps] = np.clip(self.natural_rolloff[list_steps], a_min=0, a_max=self.sales_record[list_steps])

        self.new_sales_fraction[list_steps] = self.new_sales[list_steps] / self.sales_record[list_steps]
        self.new_sales_fraction[np.isnan(self.new_sales_fraction)] = 0
        
        # new sales fraction starts from the beginning of the simulated years. stock has an additional pre vintage row 0. This is why we have np.array(list_steps)+1
        self.stock_new[:, np.array(list_steps)+1, :] = np.transpose(np.transpose(self.stock[:, np.array(list_steps)+1, :], [2, 1, 0]) * self.new_sales_fraction[list_steps], [2, 1, 0])
        self.stock_replacement[:, np.array(list_steps)+1, :] = np.transpose(np.transpose(self.stock[:, np.array(list_steps)+1, :], [2, 1, 0]) * (1 - self.new_sales_fraction[list_steps]), [2, 1, 0])

        #first year
        if 0 in list_steps:
            self.stock_new[:, 0, :] = np.transpose(np.transpose(self.stock[:, 0, :]) * self.new_sales_fraction[0])
            self.stock_replacement[:, 0, :] = np.transpose(np.transpose(self.stock[:, 0, :]) * (1 - self.new_sales_fraction[0]))
    
    def _aggregate_tech_vintage_year_shape(self, x):
        if self.spy==1:
            return x
        else:
            return util.sum_chunk(util.sum_chunk_vintage(x, self.spy, axis=1), self.spy, axis=2)

    def _aggregate_tech_year_shape(self, x):
        if self.spy==1:
            return x
        else:
            return util.sum_chunk(x, self.spy, axis=0)

    def return_formatted_stock(self, year_offset=None, stock_type='stock'):
        """
        year_offset=None returns all the years
        year_offset=0 returns the current year
        year_offset-1 returns the last year
        year_offset=1 returns the next year (based only on existing stock and natural rolloff)
        """
        data = getattr(self, stock_type)
        shape1 = (self.num_techs * (self.num_vintages + 1), self.num_years)
        reshaped_data = np.reshape(self._aggregate_tech_vintage_year_shape(data), shape1)
        if year_offset is None:
            return reshaped_data
        elif year_offset < 1:
            return reshaped_data[:,self.i+year_offset-1]
        elif year_offset >= 1:
            future_initial_rolloffs = self.calc_initial_stock_rolloff(np.array([year_offset-1], dtype=int))
            future_vintaged_rolloffs = self.calc_vintaged_stock_rolloff(np.array([year_offset-1], dtype=int))
            future_rolloffs = np.vstack((future_initial_rolloffs, future_vintaged_rolloffs.T, np.zeros((self.num_vintages-self.i, self.num_techs)))).T
            return reshaped_data[:,self.i-1] - np.reshape(future_rolloffs, self.num_techs * (self.num_vintages + 1))

    def return_formatted_outputs(self, year_offset=None):
        shape2 = self.num_techs if year_offset is not None else (self.num_techs * self.num_years)
        slice2 = self.i+year_offset-1 if year_offset is not None else slice(None)
        # stock
        # stock new
        # stock replacement
        # total rolloff
        # natural rolloff
        # early retirements
        # total sales
        # new sales
        # replacement sales
        return (self.return_formatted_stock(year_offset, stock_type='stock'),
                self.return_formatted_stock(year_offset, stock_type='stock_new'),
                self.return_formatted_stock(year_offset, stock_type='stock_replacement'),
                np.reshape(self._aggregate_tech_year_shape(self.rolloff_record)[slice2], shape2),
                np.reshape(self._aggregate_tech_year_shape(self.natural_rolloff)[slice2], shape2),
                np.reshape(self._aggregate_tech_year_shape(self.early_retirements)[slice2], shape2),
                np.reshape(self._aggregate_tech_year_shape(self.sales_record)[slice2], shape2),
                np.reshape(self._aggregate_tech_year_shape(self.new_sales)[slice2], shape2),
                np.reshape(self._aggregate_tech_year_shape(self.replacement_sales)[slice2], shape2))


# setup
# def create_markov_matrix(markov, num_techs, num_years):
# markov_matrix = np.zeros((num_techs, num_years+1, num_years))
# for i in range(num_years):
# markov_matrix[:, :-i-1, i] = np.transpose(markov[i:-1])
# return np.cumprod(markov_matrix, axis=2)

# vintaged_markov = 1-decay_vintaged[1:,:]/survival_vintaged[:-1,:]
# initial_markov = 1-decay_initial_stock[1:,:]/survival_initial_stock[:-1,:]
#
# vintaged_markov = np.vstack((vintaged_markov, vintaged_markov[-1]))
# initial_markov = np.vstack((initial_markov, initial_markov[-1]))
#
# vintaged_markov_matrix = create_markov_matrix(vintaged_markov, num_techs, num_years)
# initial_markov_matrix = create_markov_matrix(initial_markov, num_techs, num_years)

#    def __init__(self, vintaged_markov_matrix, initial_markov_matrix, num_years, num_vintages, num_techs,
#                 initial_stock=None, sales_share=None, stock_changes=None, specified_stock=None,
#                 specified_retirements=None, specified_sales=None, steps_per_year=1, stock_changes_as_min=False):

#self.initial_markov_matrix

#num_techs = [1, 5]
#num_years = [1, 2, 10]
#initial_stock = [None, 100]
#sale_sh
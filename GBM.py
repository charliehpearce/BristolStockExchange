# Copied from https://towardsdatascience.com/brownian-motion-with-python-9083ebc46ff0
# accessed 6th Feb 2021
# article dataed 22 Jul 2020, author is Tirthajyoti Sarkar

import numpy as np

class Brownian():
    """
    A Brownian motion class constructor
    """

    def __init__(self, x0=0):
        """
        Init class
        """
        assert (type(x0) == float or type(x0) == int or x0 is None), "Expect a float or None for the initial value"

        self.x0 = float(x0)

    def gen_random_walk(self, n_step=100):
        """
        Generate motion by random walk

        Arguments:
            n_step: Number of steps

        Returns:
            A NumPy array with `n_steps` points
        """
        # Warning about the small number of steps
        if n_step < 30:
            print("WARNING! The number of steps is small. It may not generate a good stochastic process sequence!")

        w = np.ones(n_step) * self.x0

        for i in range(1, n_step):
            # Sampling from the Normal distribution with probability 1/2
            yi = np.random.choice([1, -1])
            # Weiner process
            w[i] = w[i - 1] + (yi / np.sqrt(n_step))

        return w

    def gen_normal(self, n_step=100):
        """
        Generate motion by drawing from the Normal distribution

        Arguments:
            n_step: Number of steps

        Returns:
            A NumPy array with `n_steps` points
        """
        if n_step < 30:
            print("WARNING! The number of steps is small. It may not generate a good stochastic process sequence!")

        w = np.ones(n_step) * self.x0

        for i in range(1, n_step):
            # Sampling from the Normal distribution
            yi = np.random.normal()
            # Weiner process
            w[i] = w[i - 1] + (yi / np.sqrt(n_step))

        return w
    
    @staticmethod
    def gen_mu_sigma_vector(n, mu_fn, sigma_fn):
        mu = np.array([mu_fn(x) for x in range(n)])
        sigma = np.array([sigma_fn(x) for x in range(n)])
        return (mu - ((sigma**2)/2)), mu, sigma 

    def stock_price(
            self,
            s0=100,
            mu_fn = lambda x: 0.2,
            sigma_fn = lambda x: 0.68,
            deltaT=52,
            dt=0.1
    ):
        """
        Models a stock price S(t) using the Weiner process W(t) as
        `S(t) = S(0).exp{(mu-(sigma^2/2).t)+sigma.W(t)}`

        Arguments:
            s0: Inital stock price, default 100
            mu: 'Drift' of the stock (upwards or downwards), default 1
            sigma: 'Volatility' function of the stock, default 1
            deltaT: The time period for which the future prices are computed, default 52 (as in 52 weeks)
            dt (optional): The granularity of the time-period, default 0.1
        Returns:
            s: A NumPy array with the simulated stock prices over the time-period deltaT
        """
        n_step = int(deltaT / dt)
        #mu_vector = return vector of changing mu values of length t, will need to be d/dx of mu function
        time_vector = np.linspace(0, deltaT, num=n_step)
        # Stock variation
        #(mu - (sigma ** 2 / 2))
        mu_sig_vec, _, sig_vec = self.gen_mu_sigma_vector(n_step, mu_fn, sigma_fn)
        stock_var = np.multiply(mu_sig_vec, time_vector)
        
        # Forcefully set the initial value to zero for the stock price simulation
        self.x0 = 0
        # Weiner process (calls the `gen_normal` method)
        normal_gen = self.gen_normal(n_step)
        weiner_process = np.multiply(sig_vec,normal_gen)
        # Add two time series, take exponent, and multiply by the initial stock price
        s = s0 * (np.exp(stock_var + weiner_process))

        return s - s0

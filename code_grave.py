class GBMOffset(Brownian):
    """
    Geometric Brownian Motion Offset FN
    """
    def __init__(self, dt, deltaT, mu_fn, sigma_fn) -> None:
        super().__init__()
        self.dt = dt
        self.gbm_offset_vec = self.stock_price(mu_fn=mu_fn, sigma_fn=sigma_fn, dt=0.05, deltaT=deltaT/0.05)

        np.save('./offset.npy', np.array(self.gbm_offset_vec))

    def GBM_schedule_offsetfn(self, t):
        # get index for time t
        # return item
        try:
            offset = self.gbm_offset_vec[math.floor(t/self.dt)]
            return int(round(offset, 0))
        except:
            # For some reason, some time idx seem to go off the end
            print('WARNING: schedule offset clipped')
            return int(round(self.gbm_offset_vec[-1],0))
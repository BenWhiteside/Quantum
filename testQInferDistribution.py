import numpy as np
from qinfer import Distribution

class RingDistribution(Distribution):
    @property
    def n_rvs(self):
        return 2

    def sample(self, n=1):
        r = np.random.randn(n, 1)*0.1+1
        th = np.random.random((n, 1))*2*np.pi

        x = r*np.cos(th)
        y = r*np.sin(th)

        return np.concatenate([x, y], axis=1)



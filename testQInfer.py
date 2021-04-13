import numpy as np
from qinfer import simple_est_prec

omega_max = 100
true_omega = 70.3
ts = np.arange(1, 51)/(2 * omega_max)
counts = np.random.binomial(40, p=np.sin(true_omega*ts/2)**2)

data = np.column_stack([counts, ts, np.ones_like(counts)*40])

mean, cov = simple_est_prec(data, freq_max=omega_max)

print(mean)

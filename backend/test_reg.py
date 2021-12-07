import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
num = 12
X = np.arange(num).reshape(-1, 1)
print(X)
print(X.shape)
# y = 1 * x_0 + 2 * x_1 + 3
y = np.random.rand(num) * 100

print(y)
reg = LinearRegression().fit(X, y)
print("Score: ", reg.score(X, y))
#
# reg.coef_
#
# reg.intercept_

res = reg.predict(np.array([[num + 3], [num + 6], [num + num]]))

print(res)
# print(res[0])

plt.figure(1)
plt.plot(X, y)
plt.plot(X, reg.predict(X))
plt.show()
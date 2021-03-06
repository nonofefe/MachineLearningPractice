# requirement
import numpy as np
import matplotlib.pyplot as plt
import cvxpy as cv
import os

def st_ops(x, lam):
    x_proj = np.zeros(x.shape)
    for i in range(len(x)):
        sum = np.sum(x[i])
        if sum > lam:
            x_proj[i] = x[i] - lam * x[i] / sum
        else:
            x_proj[i] = x[i] * 0
    return x_proj

# we need to control this parameter to generate multiple figures
#lam = 2
#lam = 4
lam = 6
#lam = 3.89;



x_1 = np.arange(-1.5, 3, 0.01)
x_2 = np.arange(-1.5, 3, 0.02)

X1, X2 = np.mgrid[-1.5:3:0.01, -1.5:3:0.02]
fValue = np.zeros((len(x_1), len(x_2)))

A = np.array([[3, 0.5],
              [0.5, 1]])
mu = np.array([[1],
               [2]])

for i in range(len(x_1)):
    for j in range(len(x_2)):
        inr = np.vstack([x_1[i], x_2[j]])
        fValue[i, j] = np.dot(np.dot((inr - mu).T, A), (inr - mu)) + lam * (np.abs(x_1[i]) + np.abs(x_2[j]))

# cvx
#variable west(d+1,1)
# minimize( 0.5 / n * (x_tilde * west - y)’ * (x_tilde * west - y) + ...
#     lambda * (norm(west(g{1}), 2.0) + ...
#     norm(west(g{2}), 2.0) + ...
#     norm(west(g{3}), 2.0) + ...
#     norm(west(g{4}), 2.0) + ...
#     norm(west(g{5}), 2.0) ))

# cvx
w_lasso = cv.Variable((2, 1))
obj_fn = cv.quad_form(w_lasso - mu, A) + lam * (cv.norm(w_lasso[0],2) + cv.norm(w_lasso[1], 2))
objective = cv.Minimize(obj_fn)
constraints = []
prob = cv.Problem(objective, constraints)
result = prob.solve(solver=cv.CVXOPT)
w_lasso = w_lasso.value

plt.contour(X1, X2, fValue)

x_init = np.array([[3],
                   [-1]])
L = 1.01 * np.max(np.linalg.eig(2 * A)[0])

x_history = []
xt = x_init
for t in range(1000):
    x_history.append(xt.T)
    grad = 2 * np.dot(A, xt - mu)
    xth = xt - 1 / L * grad
    xt = st_ops(xth, lam * 1 / L)

x_history = np.vstack(x_history)

plt.plot(x_history[:, 0], x_history[:, 1], 'ro-', markersize=3, linewidth=0.5)
plt.plot(w_lasso[0], w_lasso[1], 'ko')

plt.xlim(-1.5, 3)
plt.ylim(-1.5, 3)
dirname = "figures/"
os.makedirs(dirname, exist_ok=True)
filename = dirname + "2-3" + "_lam=" +str(lam)+ ".pdf"
plt.savefig(filename)
plt.show()
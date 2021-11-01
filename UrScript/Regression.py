import numpy as np
from sklearn.linear_model import LinearRegression

x_camara = np.array([0.0,0.4,0.2888,0.0984]).reshape((-1, 1))
x_robot = np.array([0.31,0.71,0.5917,0.407])

y_camara = np.array([0.0,0.41,0.155,0.3116]).reshape((-1, 1))
y_robot = np.array([0.13,-0.28,-0.0107,-0.150])

model_x = LinearRegression()
model_y= LinearRegression()

model_x.fit(x_camara, x_robot)
model_y.fit(y_camara,y_robot)



def regresion_x(x):
    x_pred_array = model_x.predict(np.array(x).reshape(1, -1))
    x_pred= x_pred_array[0]

    return x_pred


def regresion_y(y):
    y_pred_array = model_y.predict(np.array(y).reshape(1, -1))
    y_pred=y_pred_array[0]

    return y_pred




r_sq = model_x.score(x_camara, x_robot)
# print('coefficient of determination:', r_sq)
#
# print('intercept:', model_x.intercept_)
#
# print('slope:', model_x.coef_)

# print('predicted response:', x_pred, sep='\n')


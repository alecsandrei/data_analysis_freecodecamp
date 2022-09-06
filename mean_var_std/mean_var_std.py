import numpy as np


def calculate(list):
    output = {}
    try:
        list = np.array(list)
        list = list.reshape(3, 3)
        functions = {'mean': 'mean',
                     'variance': 'var',
                     'standard deviation': 'std',
                     'max': 'max',
                     'min': 'min',
                     'sum': 'sum'}
        for key, value in functions.items():
            method_call = eval(f'np.{value}')
            output[key] = [method_call(list, axis=0).tolist(),
                           method_call(list, axis=1).tolist(),
                           method_call(list.reshape(9)).tolist()]
    except ValueError:
        raise ValueError("List must contain nine numbers.")
    return output

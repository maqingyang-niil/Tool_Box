import sys
sys.path.append("/home/cronusiius/Code/python/Tool_Box")
import matrix
import numpy as np


class MatrixController:
    def add_matrices(self, A:np.ndarray, B:np.ndarray) -> np.ndarray:
        if A.shape != B.shape:
            raise ValueError("矩阵维度不匹配，无法相加")
        return matrix.add_matrices(A, B)
    
    def sub_matrices(self, A:np.ndarray, B:np.ndarray) -> np.ndarray:
        if A.shape != B.shape:
            raise ValueError("矩阵维度不匹配，无法相减")
        return matrix.sub_matrices(A, B)
    
    def multiply_matrices(self, A:np.ndarray, B:np.ndarray) -> np.ndarray:
        if A.shape[1] != B.shape[0]:
            raise ValueError("矩阵维度不匹配，无法相乘")
        return matrix.multiply_matrices(A, B)
    
    def inverse_matrix(self, A:np.ndarray) -> np.ndarray:
        if A.shape[0] != A.shape[1]:
            raise ValueError("矩阵必须是方阵才能求逆")
        return matrix.inverse_matrix(A)
    
    def determinant_matrix(self, A:np.ndarray) -> float:
        if A.shape[0] != A.shape[1]:
            raise ValueError("矩阵必须是方阵才能计算行列式")
        return matrix.determinant_matrix(A)
    
    def transpose_matrix(self, A:np.ndarray) -> np.ndarray:
        return matrix.transpose_matrix(A)
    
    def compute_eigenvalues(self, A:np.ndarray) -> np.ndarray:
        if A.shape[0] != A.shape[1]:
            raise ValueError("矩阵必须是方阵才能计算特征值")
        return matrix.compute_eigenvalues(A)    
    
    def compute_eigenvectors(self, A:np.ndarray) -> np.ndarray:
        if A.shape[0] != A.shape[1]:
            raise ValueError("矩阵必须是方阵才能计算特征向量")
        return matrix.compute_eigenvectors(A)
    


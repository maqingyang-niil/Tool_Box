import numpy as np

class MatrixController:
    def add_matrices(self, A: np.ndarray, B: np.ndarray) -> np.ndarray:
        if A.shape != B.shape:
            raise ValueError("矩阵维度不匹配，无法相加")
        return A + B

    def sub_matrices(self, A: np.ndarray, B: np.ndarray) -> np.ndarray:
        if A.shape != B.shape:
            raise ValueError("矩阵维度不匹配，无法相减")
        return A - B

    def multiply_matrices(self, A: np.ndarray, B: np.ndarray) -> np.ndarray:
        if A.shape[1] != B.shape[0]:
            raise ValueError("矩阵维度不匹配，无法相乘")
        return A @ B

    def inverse_matrix(self, A: np.ndarray) -> np.ndarray:
        if A.shape[0] != A.shape[1]:
            raise ValueError("矩阵必须是方阵才能求逆")
        return np.linalg.inv(A)

    def determinant_matrix(self, A: np.ndarray) -> float:
        if A.shape[0] != A.shape[1]:
            raise ValueError("矩阵必须是方阵才能计算行列式")
        return float(np.linalg.det(A))

    def transpose_matrix(self, A: np.ndarray) -> np.ndarray:
        return A.T

    def compute_eigenvalues(self, A: np.ndarray) -> np.ndarray:
        if A.shape[0] != A.shape[1]:
            raise ValueError("矩阵必须是方阵才能计算特征值")
        return np.linalg.eigvals(A)

    def compute_eigenvectors(self, A: np.ndarray) -> np.ndarray:
        if A.shape[0] != A.shape[1]:
            raise ValueError("矩阵必须是方阵才能计算特征向量")
        _, eigenvectors = np.linalg.eig(A)
        return eigenvectors
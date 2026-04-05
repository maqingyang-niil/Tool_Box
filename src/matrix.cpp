#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include <Eigen/Dense>

namespace py = pybind11;
using MatrixXd = Eigen::MatrixXd;
using VectorXcd= Eigen::VectorXcd;

//相加
MatrixXd add_matrices(const MatrixXd& a, const MatrixXd& b) {
    return a + b;
}

//相减
MatrixXd subtract_matrices(const MatrixXd& a, const MatrixXd& b) {
    return a - b;
}

//相乘
MatrixXd multiply_matrices(const MatrixXd& a, const MatrixXd& b) {
    return a * b;
}

//转置
MatrixXd transpose_matrix(const MatrixXd& a) {
    return a.transpose();
}

//求特征值和特征向量
VectorXcd compute_eigenvalues(const MatrixXd& a){
    Eigen::EigenSolver<MatrixXd> solver(a);
    return solver.eigenvalues();
}

//求矩阵的逆
MatrixXd inverse_matrix(const MatrixXd& a) {
    if (a.determinant() == 0) {
        throw std::invalid_argument("Matrix is singular and cannot be inverted.");
    }
    return a.inverse();
}











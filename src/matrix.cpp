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

//求特征值
VectorXcd compute_eigenvalues(const MatrixXd& a){
    Eigen::EigenSolver<MatrixXd> solver(a);
    return solver.eigenvalues();
}

//求特征向量
VectorXcd compute_eigenvectors(const MatrixXd& a){
    Eigen::EigenSolver<MatrixXd> solver(a);
    return solver.eigenvectors();
}

//求矩阵的逆
MatrixXd inverse_matrix(const MatrixXd& a) {
    if (a.determinant() == 0) {
        throw std::invalid_argument("Matrix is singular and cannot be inverted.");
    }
    return a.inverse();
}

//求行列式
double determinant_matrix(const MatrixXd& a) {
    return a.determinant();
}

PYBIND11_MODULE(matrix, m) {
    m.doc() = "Matrix operations using Eigen";
    m.def("add_matrices",       &add_matrices,       "Matrix addition");
    m.def("subtract_matrices",  &subtract_matrices,  "Matrix subtraction");
    m.def("multiply_matrices",  &multiply_matrices,  "Matrix multiplication");
    m.def("transpose_matrix",   &transpose_matrix,   "Matrix transpose");
    m.def("compute_eigenvalues",&compute_eigenvalues,"Compute eigenvalues");
    m.def("compute_eigenvectors",&compute_eigenvectors,"Compute eigenvectors");
    m.def("inverse_matrix",     &inverse_matrix,     "Matrix inverse");
    m.def("determinant_matrix", &determinant_matrix, "Matrix determinant");
}










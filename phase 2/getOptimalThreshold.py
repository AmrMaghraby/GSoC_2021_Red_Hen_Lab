import numpy as np
import argparse

from modAL.models import BayesianOptimizer
from modAL.acquisition import max_EI
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern
from EvaluationUtils import EvaluationUtils
from InputUtils import InputUtils


def run_optimal_threshold_evaluator():
    n_queries = 10
    X = np.arange(0, 100)

    parser = argparse.ArgumentParser(description="Evaluates optimal threshold evaluator for pyScene tool")
    parser.add_argument("video_dir", type=str, help="Directory for the video input")
    parser.add_argument("optimal_results_data_dir", type=str, help="Directory for the optimal result")
    args = parser.parse_args()
    video_dir = args.video_dir
    optimal_results_data_dir = args.optimal_results_data_dir

    kernel = Matern(length_scale=1.0)
    regressor = GaussianProcessRegressor(kernel=kernel)
    optimizer = BayesianOptimizer(
        estimator=regressor,
        query_strategy=max_EI
    )

    video_files = InputUtils.get_files('mp4', video_dir)
    results_files = InputUtils.read_files(optimal_results_data_dir)

    # Bayesian optimization: func is to be optimized
    for n_query in range(n_queries):
        query_idx, query_inst = optimizer.query(X.reshape(-1, 1))
        optimizer.teach(X[query_idx].reshape(1, -1), EvaluationUtils.pyscene_evaluator((X[query_idx]).reshape(1, -1),
                                                                                       video_files, results_files))
    X_max, y_max = optimizer.get_max()
    print(X_max, y_max)


if __name__ == '__main__':
    run_optimal_threshold_evaluator()

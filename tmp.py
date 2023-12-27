from keras.datasets import cifar10
import numpy as np
from sklearn.decomposition import PCA
from sklearn.metrics import mean_squared_error
from numpy.linalg import pinv

# CIFAR-10データセットの読み込み
(x_train, y_train), (x_test, y_test) = cifar10.load_data()

# データの平坦化（32x32x3 -> 3072）
x_train_flat = x_train.reshape(len(x_train), 3072)
x_test_flat = x_test.reshape(len(x_test), 3072)

# PCAの適用と一般化逆行列の作成
dimensions = [512, 256, 128, 64] # 次元数のリスト
pca_models = {} # 各次元でのPCAモデルを保存
generalized_inverses = {} # 各次元での一般化逆行列を保存

for dim in dimensions:
    # PCAモデルの作成とデータへの適用
    pca = PCA(n_components=dim)
    pca.fit(x_train_flat)
    x_train_pca = pca.transform(x_train_flat)
    x_test_pca = pca.transform(x_test_flat)

    # 一般化逆行列の計算
    generalized_inverse = pinv(pca.components_.T)

    # 結果の保存
    pca_models[dim] = {
        'model': pca,
        'x_train_pca': x_train_pca,
        'x_test_pca': x_test_pca
    }
    generalized_inverses[dim] = generalized_inverse

# 結果の確認
pca_models.keys(), generalized_inverses.keys()

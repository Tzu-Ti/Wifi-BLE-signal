#import package
from sklearn import model_selection, ensemble, metrics
import numpy as np
import pandas as pd

# load numpy array of data
section1_rssi = np.load("0rssi.npy")
section2_rssi = np.load("1rssi.npy")
section1_label = np.load("0label.npy")
section2_label = np.load("1label.npy")
all_rssi = np.concatenate((section1_rssi, section2_rssi), axis=0)
all_label = np.concatenate((section1_label, section2_label), axis=0)

# convert to pd.DataFrame
wifi_dict = {
    "rssi": all_rssi,
    "label": all_label
}
wifi_pd = pd.DataFrame(wifi_dict["rssi"])
label_pd = pd.DataFrame(wifi_dict["label"])

# split train and test data
train_x, test_x, train_y, test_y = model_selection.train_test_split(wifi_pd, label_pd, test_size = 0.3)
train_y = np.ravel(train_y)
test_y = np.ravel(test_y)

# create model
# 建立 random forest 模型
forest = ensemble.RandomForestClassifier(n_estimators = 100)
forest_fit = forest.fit(train_x, train_y)

# 預測
test_y_predicted = forest.predict(test_x)
print(test_y_predicted)

# 績效
accuracy = metrics.accuracy_score(test_y, test_y_predicted)
print(accuracy)

from os import path
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# setting path
import os, sys

# current_dir = os.path.abspath("")
# parent_dir = os.path.dirname(current_dir)
# sys.path.append(parent_dir)


from source.utils.probing_tasks_utils import test_probing_task


def test_visualize_probing_task(
    FILE_NAME, PROBING_NAME, EMBEDDING_PATH, REPO_PATH, TYPE, SIZE, MODEL_TYPE
):
    """Train and test probing task model and save plots to file

    Parameters
    ----------
    FILE_NAME : str
        name of file with embeddings and labels
    PROBING_NAME : str
        name of probing task, this name will be in plot title and plot image name
    EMBEDDING_PATH : str
        
    REPO_PATH : str
        
    TYPE : str
        type of dataset
    SIZE : str
        size of dataset
    MODEL_TYPE : str
        type of model: pre_trained or fine_tuned
    """

    # paths to dataframe with embeddings and labels
    df = path.join(EMBEDDING_PATH, "probing", FILE_NAME)

    X, y = df.drop(["label"], axis=1), df["label"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    # ----- Multi Class  -----
    clfLR = LogisticRegression(
        multi_class="multinomial", random_state=42, penalty="l1", solver="saga"
    )

    # ----- Binary Class  -----
    clfLR = LogisticRegression(penalty="l1", solver="liblinear")

    clfRF = RandomForestClassifier(random_state=42)

    clfXGB = XGBClassifier(random_state=42)

    pred_rf, acc_rf, f_score_rf = test_probing_task(
        X_train, X_test, y_train, y_test, clfRF
    )

    pred_lr, acc_lr, f_score_lr = test_probing_task(
        X_train, X_test, y_train, y_test, clfLR
    )

    pred_xg, acc_xg, f_score_xg = test_probing_task(
        X_train, X_test, y_train, y_test, clfXGB
    )

    values = [acc_lr, acc_rf, acc_xg]
    classifier_name = ["LogisticRegression", "RandomForest", "XGB"]

    plt.bar(classifier_name, values)
    plt.ylim([0, 100])
    plt.ylabel("accuracy")
    plt.title(
        f"Accuracy Score for probing task:{PROBING_NAME}. Dataset: {TYPE}, {SIZE}, {MODEL_TYPE}"
    )

    PLOT_SAVE_PATH_accuracy = os.path.join(
        REPO_PATH, "project_2_output/visualizations", f"{PROBING_NAME}_accuracy.png"
    )
    plt.savefig(PLOT_SAVE_PATH_accuracy, bbox_inches="tight")

    plt.show()

    values_fscore = [f_score_rf, f_score_lr, f_score_xg]
    plt.bar(classifier_name, values_fscore)
    plt.ylim([0, 100])
    plt.ylabel("F-score")
    plt.title(
        f"F-score for probing task:{PROBING_NAME}. Dataset: {TYPE}, {SIZE}, {MODEL_TYPE}"
    )

    PLOT_SAVE_PATH_fscore = os.path.join(
        REPO_PATH, "project_2_output/visualizations", f"{PROBING_NAME}_fscore.png"
    )
    plt.savefig(PLOT_SAVE_PATH_fscore, bbox_inches="tight")

    plt.show()

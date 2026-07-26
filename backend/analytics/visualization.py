import matplotlib.pyplot as plt

def plot_category(df, column):

    df[column].value_counts().plot(kind="bar")

    plt.title(column)

    plt.show()

def plot_pie(df, column):

    df[column].value_counts().plot(kind="pie")
    df["absences"].hist()



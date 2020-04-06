## Added by Gowun


import matplotlib.pyplot as plt

def comparison_figure(x_points, y_points_list, label_list, x_label_name, y_label_name):
  plt.figure()
  for i, l in enumerate(label_list):
    plt.plot(list(x_points), list(y_points_list[i]), label=l)
  plt.legend()
  plt.xlabel(x_label_name)
  plt.ylabel(y_label_name)
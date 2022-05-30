from cProfile import label
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal as scisig

activities = {1: ["W", "orange", 'o'], 2: ["W_UP", "darkgreen", 'o'],
              3: ["W_D", "gold", 'o'],
              4: ["SIT", "cyan", 'd'], 5: ["STAND", "blue", 'd'], 6: ["LAY", "brown", 'd'],
              7: ["STAND_TO_SIT", "lightgreen", '+'], 8: ["SIT_TO_STAND", "red", '+'],
              9: ["SIT_TO_LIE", "darkred", '+'],
              10: ["LIE_TO_SIT", "pink", '+'], 11: ["STAND_TO_LIE", "olive", '+'], 12: ["LIE_TO_STAND", "purple", '+']}

mag_max_x = []
mag_max_y = []
mag_max_z = []

mag_min_x = []
mag_min_y = []
mag_min_z = []

# Dinâmicos
walking_x = [[], [], [], [], [], [], [], []]
walking_y = [[], [], [], [], [], [], [], []]
walking_z = [[], [], [], [], [], [], [], []]
walking_upstairs_x = [[], [], [], [], [], [], [], []]
walking_upstairs_y = [[], [], [], [], [], [], [], []]
walking_upstairs_z = [[], [], [], [], [], [], [], []]
walking_downstairs_x = [[], [], [], [], [], [], [], []]
walking_downstairs_y = [[], [], [], [], [], [], [], []]
walking_downstairs_z = [[], [], [], [], [], [], [], []]

# Estáticos
sitting_x = [[], [], [], [], [], [], [], []]
sitting_y = [[], [], [], [], [], [], [], []]
sitting_z = [[], [], [], [], [], [], [], []]
standing_x = [[], [], [], [], [], [], [], []]
standing_y = [[], [], [], [], [], [], [], []]
standing_z = [[], [], [], [], [], [], [], []]
laying_x = [[], [], [], [], [], [], [], []]
laying_y = [[], [], [], [], [], [], [], []]
laying_z = [[], [], [], [], [], [], [], []]

# Transição
stand_sit_x = [[], [], [], [], [], [], [], []]
stand_sit_y = [[], [], [], [], [], [], [], []]
stand_sit_z = [[], [], [], [], [], [], [], []]
sit_stand_x = [[], [], [], [], [], [], [], []]
sit_stand_y = [[], [], [], [], [], [], [], []]
sit_stand_z = [[], [], [], [], [], [], [], []]
sit_lay_x = [[], [], [], [], [], [], [], []]
sit_lay_y = [[], [], [], [], [], [], [], []]
sit_lay_z = [[], [], [], [], [], [], [], []]
lay_sit_x = [[], [], [], [], [], [], [], []]
lay_sit_y = [[], [], [], [], [], [], [], []]
lay_sit_z = [[], [], [], [], [], [], [], []]
stand_lay_x = [[], [], [], [], [], [], [], []]
stand_lay_y = [[], [], [], [], [], [], [], []]
stand_lay_z = [[], [], [], [], [], [], [], []]
lay_stand_x = [[], [], [], [], [], [], [], []]
lay_stand_y = [[], [], [], [], [], [], [], []]
lay_stand_z = [[], [], [], [], [], [], [], []]

array_activities = [walking_x, walking_y, walking_z, walking_upstairs_x, walking_upstairs_y, walking_upstairs_z,
                    walking_downstairs_x, walking_downstairs_y, walking_downstairs_z, sitting_x, sitting_y, sitting_z,
                    standing_x, standing_y, standing_z, laying_x, laying_y, laying_z, stand_sit_x, stand_sit_y,
                    stand_sit_z, sit_stand_x, sit_stand_y, sit_stand_z, sit_lay_x, sit_lay_y, sit_lay_z, lay_sit_x,
                    lay_sit_y, lay_sit_z, stand_lay_x, stand_lay_y, stand_lay_z, lay_stand_x, lay_stand_y,
                    lay_stand_z]
array_max = []
experience = []
user = []
x = []
y = []
z = []
labels = []

# ------------------------------Questão 1


def save_data():
    count = 42
    for i in range(21, 25):
        user.append(i)
        for j in range(2):
            if(len(str(i)) == 1):
                us = "0"+str(i)
            else:
                us = str(i)
            if(len(str(count)) == 1):
                exp = "0"+str(count)
            else:
                exp = str(count)
            experience.append(count)
            count += 1
            string = "C:\\Users\\nunoa\Desktop\\Projeto_ATD\\RawData\\" + \
                "acc_exp"+exp+"_user"+us+".txt"
            readfile(string)
    array = []
    with open("C:\\Users\\nunoa\Desktop\\Projeto_ATD\\RawData\\labels.txt", "r") as file9:
        for i in file9:
            array.append([int(i.split()[0]), int(i.split()[1]), int(
                i.split()[2]), int(i.split()[3]), int(i.split()[4])])
        global labels
        labels = np.array(array)

    for i in array_max:
        x.append(i[0])
        y.append(i[1])
        z.append(i[2])


def readfile(nome):
    aux = []
    with open(nome, "r") as file:
        for i in file:
            aux.append([float(i.split()[0]), float(
                i.split()[1]), float(i.split()[2])])
        array = np.array(aux)
    array_max.append(array)
# ------------------------------Questão 2


def generate_plots(array, exp, us):
    tempo = []
    aux_x = []
    aux_y = []
    aux_z = []
    aux_labels = []
    eixos = ['ACC_X', 'ACC_Y', 'ACC_Z']
    aux = [aux_x, aux_y, aux_z]

    for i in range(len(array)):
        tempo.append((i / 50) / 60)
        aux_x.append(array[i][0])
        aux_y.append(array[i][1])
        aux_z.append(array[i][2])

    for i in range(len(labels)):
        if labels[i][0] == exp and labels[i][1] == us:
            aux_labels.append([labels[i][2], labels[i][3], labels[i][4]])

    plt.figure(figsize=(24, 15))
    for i in range(3):
        plt.subplot(3, 1, i + 1)
        plt.title("Experience " + str(exp) + "- User " + str(us))
        plt.plot(tempo, aux[i], 'black')
        plt.xlabel("Tempo (min)")
        plt.ylabel(str(eixos[i]))
        for j in range(len(aux_labels)):
            plt.plot(tempo[aux_labels[j][1]:aux_labels[j][2]], aux[i][aux_labels[j][1]:aux_labels[j][2]],
                     activities[aux_labels[j][0]][1])
            if j % 2 == 0:
                plt.text((((aux_labels[j][1] + aux_labels[j][2]) // 2) / 50) / 60, min(aux[i]),
                         activities[aux_labels[j][0]][0])
            else:
                plt.text((((aux_labels[j][1] + aux_labels[j][2]) // 2) / 50) / 60, max(aux[i]),
                         activities[aux_labels[j][0]][0])
    plt.subplots_adjust(
        bottom=0.1,
        top=0.9,
        wspace=0.4,
        hspace=0.4)
    plt.show()

    aux_x.clear()
    aux_y.clear()
    aux_z.clear()
    tempo.clear()


def ex_2():
    for i in range(len(experience)):
        generate_plots(array_max[i], experience[i], user[i // 2])


if __name__ == "__main__":

    save_data()
    ex_2()

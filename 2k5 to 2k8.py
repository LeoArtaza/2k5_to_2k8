#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import os
pd.options.display.max_columns = 300

folder = 'C:/Users/leo_a/Documents/APF 2k8/2k5_to_2k8 Project/AllTeams_2K5/'
files_2k5 = []
for f in os.listdir(folder):
    if '2K5' in f:
        files_2k5.append(folder + f)

for f in files_2k5:
    k5 = pd.read_csv(f, ';')

    k5.columns = k5.iloc[0]
    k5.drop(index=0, inplace=True)

    k8 = pd.read_csv(folder + '2k8_Template.txt', '|')
    og_columns = list(k8.columns)
    extra_columns = ['c0', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6']
    k8 = k8.reset_index()
    k8.columns = og_columns + extra_columns

    k5.Position = k5.Position.apply(lambda x: x.replace('RB', 'HB'))

    dif = k5.Position.value_counts() - k8.Position.value_counts()
    # dif = dif.apply(lambda x:0 if x<0 else x)

    dfs = []
    for i, pos in enumerate(dif):
        if dif[i] > 0:
            dfs.append(k5[k5.Position == dif.index[i]].iloc[:-dif[i]])
        else:
            dfs.append(k5[k5.Position == dif.index[i]])

    k5 = pd.concat(dfs)
    k5.Position.value_counts()

    newdif = k5.Position.value_counts() - k8.Position.value_counts()

    newdif[newdif < 0]

    for i in range(len(newdif)):
        for j in range(abs(newdif[i])):
            k5 = k5.append(k5[-1:])
            k5.iloc[-1, k5.columns.get_loc('Position')] = newdif.index[i]
            k5.iloc[-1, k5.columns.get_loc('First')] = 'Filler'
            k5.iloc[-1, k5.columns.get_loc('Last')] = 'Filler'

    k5.reset_index(inplace=True)

    k5 = k5.sort_values(by=["Position", "index"]).drop('index', axis=1).reset_index(drop=True)

    k8 = k8.assign(Depth3=k8['Depth1'] * k8['Depth2']).sort_values(["Position", "Depth3", "Depth1"]).drop('Depth3',
                                                                                                          axis=1)
    k8.reset_index(inplace=True, drop=True)

    k5.columns = (k5.columns.str.replace(' ', '').str.replace('Jumping', 'Jump').str.replace('Blocking', 'Block').
                  str.replace('HoldOnToBall', 'SecureBall').str.replace('KickAccuracy', 'KickCoverage').
                  str.replace('Jersey#', 'Number').str.replace('YearsPro', 'YrsPro').str.replace('PowerRunStyle', 'RunStyle'))

    k5.Hand = k5.Hand.apply(lambda x: 'Right' if x == '1' else 'Left')
    k5.EyeBlack = k5.EyeBlack.apply(lambda x: True if x == '1' else False)
    k5.FaceMask = 'Type' + k5.FaceMask
    k5.FaceMask = k5.FaceMask.apply(lambda x: 'Type7' if x == 'Type3' else x)

    skins_dic = {0: 'Lightest',
                 1: 'Light',
                 2: 'LightMedium',
                 3: 'DarkMedium',
                 4: 'Dark',
                 5: 'Darkest'}
    body_dic = {'0': 'Skinny',
                '1': 'Normal',
                '2': 'Large',
                '3': 'Fat'}
    shield_dic = {'0': 'None',
                  '1': 'Clear',
                  '2': 'Dark'}

    k5.Skin = k5.Skin.apply(lambda x: int(x) % 8).replace(skins_dic)
    k5.Body = k5.Body.replace(body_dic)
    k5.FaceShield = k5.FaceShield.replace(shield_dic)

    cols_to_replace = (k8.columns & k5.columns).drop(
        ['Photo', 'Face', 'Helmet', 'Dreads', 'LeftGlove', 'RightGlove', 'LeftWrist', 'RightWrist',
         'LeftElbow', 'RightElbow', 'LeftShoe', 'RightShoe', 'NeckRoll', ])

    k8[k8.columns & k5.columns].iloc[10:20, :].append(k5[k8.columns & k5.columns].iloc[0:50, :])

    k8[cols_to_replace] = k5[cols_to_replace]

    k8.Photo = 0
    k8.PBP = 0
    k8.Muscle = 'Normal'
    k8.Tier = 'None'
    k8.Type = 'Generic'
    k8.iloc[:, k8.columns.get_loc('FourthQuarterComeback'):k8.columns.get_loc('LBRunStyle')] = 0
    k8.iloc[:, k8.columns.get_loc('LeadershipBonus'):k8.columns.get_loc('HighStep')] = 0
    k8.TeamCity = 'UNK'
    k8.TeamFullCity = 'Unknown City Unknown City'
    team = f.split('/')[-1].split('_')[0]
    k8.Team = team
    k8.NickName = None

    k8.columns = extra_columns + og_columns
    k8 = k8.reset_index(drop=True).set_index(extra_columns)

    k8.index.names = [None] * 7

    outfile = team + '_2k5to2k8.txt'

    k8.to_csv(outfile, '|')

    with open(outfile, 'r') as file:
        txt = file.read()

    with open(outfile, 'w') as file:
        file.write(txt[7:].replace('RunCoverage.1', 'RunCoverage'))

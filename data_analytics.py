import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from basic_tests import dorchester_arr, malden_arr, totten_arr
from day_aggregate import plot_any, plot_one
import pandas_bokeh

plt.close('all')

pd.set_option('plotting.backend', 'pandas_bokeh')

intersections = [dorchester_arr, malden_arr, totten_arr]
agg_i = []
agg_grouped = []

for i in range(3):
    merge_df = pd.concat(intersections[i])
    agg_df = merge_df.resample('15min').sum()
    agg_i.append(agg_df)

for i in range (3):
    agg_grouped.append(agg_i[i].groupby([agg_i[i].index.hour, agg_i[i].index.minute]).mean())
    print(agg_grouped[i].describe())

# This finds the total amount of traffic going to a given destination
def destination_traffic(dest):
    df = pd.DataFrame()
    df['Start Time'] = agg_i[0].index #pd.to_datetime(agg_i.index)
    df.set_index(['Start Time'], inplace=True)
    if dest == 0:
        #dest 0: dnt, del, dwr, dsu, tnt, tel, twr, tsu, mnt, mel, mwn, msu
        df['N Huron Church-D'] = agg_i[0][['Thru', 'Left.1', 'Right.3', 'U-Turn.2']].sum(axis=1)
        df['N Huron Church-T'] = agg_i[1][['Thru', 'Left.1', 'Right.3', 'U-Turn.2']].sum(axis=1)
        df['N Huron Church-M'] = agg_i[2][['Thru', 'Left.1', 'Right.3', 'U-Turn.2']].sum(axis=1)
        df['N Huron Church'] = df[['N Huron Church-D', 'N Huron Church-M', 'N Huron Church-T']].sum(axis=1)
    elif dest == 1:
        #dest 1: dnr, det, dwu, dsl, tnt, tel, twr, tsu, mnt, mel, mwr, msu
        df['E Dorch-D'] = agg_i[0][['Right', 'Thru.1', 'U-Turn.3', 'Left.2']].sum(axis=1)
        df['E Dorch-T'] = agg_i[0][['Thru', 'Left.1', 'Right.3', 'U-Turn.2']].sum(axis=1)
        df['E Dorch-M'] = agg_i[0][['Thru', 'Left.1', 'Right.3', 'U-Turn.2']].sum(axis=1)
        df['E Dorchester'] = df[['E Dorch-D', 'E Dorch-M', 'E Dorch-T']].sum(axis=1)
    elif dest == 2:
        #dest 2: tnr, tet, twu, tsl, dnu, der, dwl, dst, mnt, mel, mwr, msu
        df['E Totten-D'] = agg_i[0][['U-Turn', 'Right.1', 'Left.3', 'Thru.2']].sum(axis=1)
        df['E Totten-T'] = agg_i[0][['Right', 'Thru.1', 'U-Turn.3', 'Left.2']].sum(axis=1)
        df['E Totten-M'] = agg_i[0][['Thru', 'Left.1', 'Right.3', 'U-Turn.2']].sum(axis=1)
        df['E Totten'] = df[['E Totten-D', 'E Totten-M', 'E Totten-T']].sum(axis=1)
    elif dest == 3:
        #dest3: mnu, mer, mwl, mst, tnu, ter, twl, tst, dnu, der, dwl, dst
        df['S Huron Church-D'] = agg_i[0][['U-Turn', 'Right.1', 'Left.3', 'Thru.2']].sum(axis=1)
        df['S Huron Church-T'] = agg_i[1][['U-Turn', 'Right.1', 'Left.3', 'Thru.2']].sum(axis=1)
        df['S Huron Church-M'] = agg_i[2][['U-Turn', 'Right.1', 'Left.3', 'Thru.2']].sum(axis=1)
        df['S Huron Church'] = df[['S Huron Church-D', 'S Huron Church-M', 'S Huron Church-T']].sum(axis=1)
    elif dest == 4:
        #dest 4: mnl, meu, mwt, msr, tnu, ter, twl, tst, dnu, der, dwl, dst
        df['W Malden-D'] = agg_i[0][['U-Turn', 'Right.1', 'Left.3', 'Thru.2']].sum(axis=1)
        df['W Malden-T'] = agg_i[0][['U-Turn', 'Right.1', 'Left.3', 'Thru.2']].sum(axis=1)
        df['W Malden-M'] = agg_i[0][['Left', 'U-Turn.1', 'Thru.3', 'Right.2']].sum(axis=1)
        df['W Malden'] = df[['W Malden-D', 'W Malden-M', 'W Malden-T']].sum(axis=1)
    elif dest == 5:
        #dnl, deu, dwt, dsr, tnl, teu, twt, tsr, mnt, mel, mwr, msu
        df['W Dorch-D'] = agg_i[0][['Left', 'U-Turn.1', 'Thru.3', 'Right.2']].sum(axis=1)
        df['W Dorch-T'] = agg_i[0][['Left', 'U-Turn.1', 'Thru.3', 'Right.2']].sum(axis=1)
        df['W Dorch-M'] = agg_i[0][['Thru', 'Left.1', 'Right.3', 'U-Turn.2']].sum(axis=1)
        df['W Dorchester'] = df[['W Dorch-D', 'W Dorch-M', 'W Dorch-T']].sum(axis=1)
    return df

def plot_dests():
    dests = []
    dests_grouped = []
    for i in range(6):
        dests.append(destination_traffic(i))
        dests_grouped.append(dests[i].groupby([dests[i].index.hour, dests[i].index.minute]).mean())
    all = pd.concat([dests_grouped[0]['N Huron Church'], dests_grouped[1]['E Dorchester'], dests_grouped[2]['E Totten'], dests_grouped[3]['S Huron Church'], dests_grouped[4]['W Malden'], dests_grouped[5]['W Dorchester']],
                    axis=1)
    # print(all)
    all.plot(title="Traffic along destination routes", xlabel='Time of day (hour, minute)', ylabel='Number of Vehicles')
    # plt.legend(loc="upper right")
    # plt.title("Traffic along destination routes")
    plt.show()
    # plt.ylabel('Amount of Traffic')
    # plt.xlabel('Date/Time')

    # fig = plt.figure()
    # for frame in dests_grouped:
    #     plt.plot(frame.index, frame[[-1]])
    # ax = dests_grouped[0]['N Huron Church-All'].plot()#(label='N Huron Church')
    # dests_grouped[1]['E Dorch-All'].plot(ax=ax)#(label='E Dorch', ax=ax)
    # dests_grouped[2]['E Totten-All'].plot(ax=ax)#(label='E Totten', ax=ax)
    # dests_grouped[3]['S Huron Church-All'].plot(ax=ax)#(label='S Huron Church', ax=ax)
    # dests_grouped[4]['W Malden-All'].plot(ax=ax)#(label='W Malden', ax=ax)
    # dests_grouped[5]['W Dorch-All'].plot(ax=ax)#(label='W Dorch', ax=ax)
    # plt.legend(loc="upper right")
    # plt.title("Traffic along destination routes")
    # plt.show()



# dest_1 = destination_traffic(0)
# dest_2 = destination_traffic(1)
# dest_1_grouped = dest_1.groupby([dest_1.index.hour, dest_1.index.minute]).mean()
# dest_2_grouped = dest_2.groupby([dest_2.index.hour, dest_2.index.minute]).mean()
# # print(dest_1)
# plt.ylabel('Amount of Traffic')
# plt.xlabel('Date/Time')
# dest_1_grouped['N Huron Church-All'].plot()
# dest_2_grouped['E Dorch-All'].plot()
# plt.show()
# ax1 = agg_i[intersection]['ns_max'].plot(label="N-S Traffic")
# ax2 = agg_i[intersection]['ew_max'].plot(label="E-W Traffic")
# plt.legend(loc="upper right")
# plt.show()

# This gets the max amount of traffic going in N-S and E-W and then plots them against each other
def agg_dir_traffic(intersection):
    intersection_dict = {0: 'Huron Church & Dorchester', 1: 'Huron Church & Malden', 2: 'Huron Church & Totten'}

    agg_i[intersection]['n_sum'] = agg_i[intersection][['Right', 'Thru', 'Left', 'U-Turn', 'Peds CW', 'Peds CCW']].sum(axis=1)
    agg_i[intersection]['e_sum'] = agg_i[intersection][['Right.1', 'Thru.1', 'Left.1', 'U-Turn.1', 'Peds CW.1', 'Peds CCW.1']].sum(axis=1)
    agg_i[intersection]['s_sum'] = agg_i[intersection][['Right.2', 'Thru.2', 'Left.2', 'U-Turn.2', 'Peds CW.2', 'Peds CCW.2']].sum(axis=1)
    agg_i[intersection]['w_sum'] = agg_i[intersection][['Right.3', 'Thru.3', 'Left.3', 'U-Turn.3', 'Peds CW.3', 'Peds CCW.3']].sum(axis=1)
    agg_i[intersection]['N-S Traffic'] = agg_i[intersection][['n_sum', 's_sum']].max(axis=1)
    agg_i[intersection]['E-W Traffic'] = agg_i[intersection][['e_sum', 'w_sum']].max(axis=1)

    agg_grouped = agg_i[intersection].groupby([agg_i[intersection].index.hour, agg_i[intersection].index.minute]).mean()
    ax1 = agg_grouped[['N-S Traffic', 'E-W Traffic']].plot(title = "N-S vs. E-W traffic on " + intersection_dict[intersection],
                                                           xlabel='Time of day (hour, minute)', ylabel='# of vehicles')#(label="N-S Traffic")
    # ax2 = agg_grouped['ew_max'].plot()#(label="E-W Traffic")
    # plt.ylabel('Amount of Traffic')
    # plt.xlabel('Time of day (hour, minute)')
    # plt.legend(loc="upper right")
    plt.title("N-S vs. E-W traffic on " + intersection_dict[intersection])
    plt.show()

f = open("static/views/graph" + "dests" + ".html", "wb")
pandas_bokeh.output_file("static/views/graph" + "dests" + ".html")
plot_dests()
f.close()

# agg_dir_traffic(0)
# agg_dir_traffic(1)
# agg_dir_traffic(2)
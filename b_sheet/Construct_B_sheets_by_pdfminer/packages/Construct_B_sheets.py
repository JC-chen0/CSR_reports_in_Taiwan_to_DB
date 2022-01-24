import pandas as pd


def construct_gri_df():
    col_name_list = list()
    col_name_list.append("corporate_name")
    for temp in range(56):
        pointer = "102-" + str(temp + 1)
        col_name_list.append(pointer)

    for temp in range(3):
        pointer = "103-" + str(temp + 1)
        col_name_list.append(pointer)

    for temp in range(4):
        pointer = "201-" + str(temp + 1)
        col_name_list.append(pointer)

    for temp in range(2):
        pointer = "202-" + str(temp + 1)
        col_name_list.append(pointer)

    for temp in range(2):
        pointer = "203-" + str(temp + 1)
        col_name_list.append(pointer)

    for temp in range(1):
        pointer = "204-" + str(temp + 1)
        col_name_list.append(pointer)

    for temp in range(3):
        pointer = "205-" + str(temp + 1)
        col_name_list.append(pointer)

    for temp in range(1):
        pointer = "206-" + str(temp + 1)
        col_name_list.append(pointer)

    for temp in range(3):
        pointer = "301-" + str(temp + 1)
        col_name_list.append(pointer)

    for temp in range(5):
        pointer = "302-" + str(temp + 1)
        col_name_list.append(pointer)

    for temp in range(3):
        pointer = "303-" + str(temp + 1)
        col_name_list.append(pointer)

    for temp in range(4):
        pointer = "304-" + str(temp + 1)
        col_name_list.append(pointer)

    for temp in range(7):
        pointer = "305-" + str(temp + 1)
        col_name_list.append(pointer)

    for temp in range(5):
        pointer = "306-" + str(temp + 1)
        col_name_list.append(pointer)

    for temp in range(1):
        pointer = "307-" + str(temp + 1)
        col_name_list.append(pointer)

    for temp in range(2):
        pointer = "308-" + str(temp + 1)
        col_name_list.append(pointer)

    for temp in range(3):
        pointer = "401-" + str(temp + 1)
        col_name_list.append(pointer)

    for temp in range(1):
        pointer = "402-" + str(temp + 1)
        col_name_list.append(pointer)

    for temp in range(10):
        pointer = "403-" + str(temp + 1)
        col_name_list.append(pointer)

    for temp in range(3):
        pointer = "404-" + str(temp + 1)
        col_name_list.append(pointer)

    for temp in range(2):
        pointer = "405-" + str(temp + 1)
        col_name_list.append(pointer)

    for temp in range(1):
        pointer = "406-" + str(temp + 1)
        col_name_list.append(pointer)

    for temp in range(1):
        pointer = "407-" + str(temp + 1)
        col_name_list.append(pointer)

    for temp in range(1):
        pointer = "408-" + str(temp + 1)
        col_name_list.append(pointer)

    for temp in range(1):
        pointer = "409-" + str(temp + 1)
        col_name_list.append(pointer)

    for temp in range(1):
        pointer = "410-" + str(temp + 1)
        col_name_list.append(pointer)

    for temp in range(1):
        pointer = "411-" + str(temp + 1)
        col_name_list.append(pointer)

    for temp in range(3):
        pointer = "412-" + str(temp + 1)
        col_name_list.append(pointer)

    for temp in range(2):
        pointer = "413-" + str(temp + 1)
        col_name_list.append(pointer)

    for temp in range(2):
        pointer = "414-" + str(temp + 1)
        col_name_list.append(pointer)

    for temp in range(1):
        pointer = "415-" + str(temp + 1)
        col_name_list.append(pointer)

    for temp in range(2):
        pointer = "416-" + str(temp + 1)
        col_name_list.append(pointer)

    for temp in range(3):
        pointer = "417-" + str(temp + 1)
        col_name_list.append(pointer)

    for temp in range(1):
        pointer = "418-" + str(temp + 1)
        col_name_list.append(pointer)

    for temp in range(1):
        pointer = "419-" + str(temp + 1)
        col_name_list.append(pointer)

    col_name_list.append('reveal_num')
    col_name_list.append('unreveal_num')

    df = pd.DataFrame(index=range(1, 514), columns=col_name_list)
    df.to_csv('testing_reports\\gri_pointers_b_frame.csv', encoding='utf_8_sig')

construct_gri_df()

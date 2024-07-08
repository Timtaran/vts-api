def merge_dicts(main_dict: dict, *other_dicts: dict):
    final_dict = main_dict.copy()

    for _dict in other_dicts:
        final_dict.update(_dict)

        for value in main_dict:
            if main_dict[value]:
                final_dict[value] = main_dict[value]

    return final_dict

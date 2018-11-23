from __future__ import division


from sc_2_1_select_sub_samples import load_data_personnes_paris_best_trip


def define_option(data):
    data = data.query('age > 18')
    data['centre_ville'] = 1 * (data['rescour'] == '1')
    data['utilise_vp'] = 1 * (data['nbdeplvp'] > 0)
    data['utilise_tc'] = 1 * (data['nbdepltc'] > 0)

    data['option_downtown'] = data['centre_ville']
    data['option_private_trans'] = data['utilise_vp'] - data['utilise_vp'] * data['centre_ville']
    data['option_public_trans'] = (
        data['utilise_tc']
        - data['utilise_tc'] * data['centre_ville']
        - data['utilise_tc'] * data['utilise_vp']
        + data['utilise_tc'] * data['centre_ville'] * data['utilise_vp']
        )

    return data


if __name__ == "__main__":
    weekend = False
    selection = 0
    data = load_data_personnes_paris_best_trip(weekend, selection)
    data = define_option(data)

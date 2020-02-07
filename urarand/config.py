#!/usr/bin/env python3

import urarand.entropy_generator as ent_gen

ENTROPY_GENERATOR = [
        ent_gen.EntropyGenerator(),
        ent_gen.EntropyGenerator_2_bits()
    ]

def get_config():
    config = {}

    config["ent_gen"] = ENTROPY_GENERATOR[1]

    return config

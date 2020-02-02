#!/usr/bin/env python3

import urarand.entropy_generator as ent_gen

def get_config():
    config = {}
    config["output"] = "entropy.bin"
    config["ent_gen"] = ent_gen.EntropyGenerator(config["output"])

    return config

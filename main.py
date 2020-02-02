#!/usr/bin/env python3

import urarand.config
import urarand.collect

def main():
    config = urarand.config.get_config()
    urarand.collect.collect()

if __name__ == "__main__":
    main()

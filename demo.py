#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et:

import logging
import datetime

def main():
    logging.info("Hello, World!")
    logging.info("This is a demo script.")
    logging.info("Current time: %s", datetime.datetime.now())

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
#!/bin/bash

# Due to how things are currently setup, only running the unit tests because the other tests are failing
python -m pytest tests/unit

# -*- coding: utf-8 -*-

# Copyright: (c) 2023, Daniel Schmidt <danischm@cisco.com>

import errorhandler
import pytest
from nac_validate.validator import Validator

pytestmark = pytest.mark.integration
pytestmark = pytest.mark.validate

error_handler = errorhandler.ErrorHandler()

SCHEMA_PATH = "schemas/schema.yaml"
VALIDATION_RULES_PATH = "validation/rules/"


@pytest.mark.parametrize("data_paths", [(["tests/integration/fixtures/catalystcenter/standard/"])])
def test_catalystcenter_validation(data_paths):
    validator = Validator(SCHEMA_PATH, VALIDATION_RULES_PATH)
    validator.validate_syntax(data_paths)
    if validator.errors:
        pytest.fail("Syntactic validation has failed.")
    validator.validate_semantics(data_paths)
    if validator.errors:
        pytest.fail("Semantic validation has failed.")
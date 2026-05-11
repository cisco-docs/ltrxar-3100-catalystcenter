# -*- coding: utf-8 -*-

# Copyright: (c) 2023, Daniel Schmidt <danischm@cisco.com>

import errorhandler
from nac_test.robot_writer import RobotWriter

error_handler = errorhandler.ErrorHandler()


def render_templates(
    data_paths, output_path, templates_path, filters_path="", tests_path=""
):
    """Render templates using iac-test package"""
    writer = RobotWriter(data_paths, filters_path, tests_path)
    writer.write(templates_path, output_path)
    if error_handler.fired:
        return "Template rendering failed."
    return ""
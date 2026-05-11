"""
Catalyst Center Integration Tests

IMPORTANT: Before running these tests, you must generate the Terraform configurations
from Jinja2 templates.

PREREQUISITES:
    1. Run the test configuration generator script:
       python3 scripts/generate_test_configs.py --branch <branch> --max-timeout 600

    2. This generates main.tf files from main.tf.j2 templates in:
       tests/integration/fixtures/catalystcenter/terraform_*/

    3. Optional flags for the generator:
       --use-bulk-api          Generate configs with use_bulk_api enabled
       --provider-version      Specify Catalyst Center provider version (e.g., 0.5.0)

EXAMPLES (from Jenkinsfile):
    Without use_bulk_api:
        python3 scripts/generate_test_configs.py --branch main --max-timeout 600

    With use_bulk_api:
        python3 scripts/generate_test_configs.py --branch main --max-timeout 600 --use-bulk-api

    With specific provider version:
        python3 scripts/generate_test_configs.py --branch main --provider-version 0.5.0 --max-timeout 600

For complete workflow examples, see the 'Generate Test Configurations' stage in Jenkinsfile.
"""

import os
import shutil

import errorhandler
import nac_test.pabot
import pytest
import tftest
from util import render_templates


pytestmark = pytest.mark.integration
pytestmark = pytest.mark.cc

error_handler = errorhandler.ErrorHandler()

CATALYSTCENTER_TEST_TEMPLATES_PATH = "templates/catalyst_center/test/"
NAC_TEST_EXCLUDE_TAGS = ["devices"]

def get_managed_sites_from_terraform(terraform_path):
    """Parse managed_sites and manage_specific_sites_only from Terraform module configuration"""
    import re

    main_tf_path = os.path.join(terraform_path, "main.tf")

    if not os.path.exists(main_tf_path):
        return "", "false"  # Default to empty (all sites), manage children

    with open(main_tf_path, 'r') as f:
        content = f.read()

    # Extract managed_sites from module block
    # Pattern: managed_sites = ["Global/AREA_0"] or managed_sites = []
    match = re.search(r'managed_sites\s*=\s*\[(.*?)\]', content, re.DOTALL)

    if not match:
        managed_sites = ""  # No managed_sites defined = manage all
    else:
        sites_str = match.group(1).strip()
        if not sites_str:
            managed_sites = ""  # Empty list = manage all
        else:
            # Extract site names from quoted strings
            sites = re.findall(r'"([^"]+)"', sites_str)
            managed_sites = ",".join(sites)

    # Extract manage_specific_sites_only from module block
    # Pattern: manage_specific_sites_only = true or false
    match_specific = re.search(r'manage_specific_sites_only\s*=\s*(true|false)', content)
    manage_specific_only = match_specific.group(1) if match_specific else "false"

    return managed_sites, manage_specific_only


def catalystcenter_render_run_tests(catalystcenter_url, data_paths, output_path, exclude_tags=None):
    """Render CatalystCenter test suites and run them using nac-test"""
    error = render_templates(data_paths, output_path, CATALYSTCENTER_TEST_TEMPLATES_PATH)
    if error:
        pytest.fail(error)
    os.environ["CC_URL"] = catalystcenter_url

    # Use provided exclude_tags or fall back to default
    tags_to_exclude = exclude_tags if exclude_tags is not None else NAC_TEST_EXCLUDE_TAGS

    try:
        exit_code = nac_test.pabot.run_pabot(output_path, exclude=tags_to_exclude)
    except SystemExit as e:
        # nac-test <= 1.2.1 called sys.exit(), capture the exit code
        exit_code = e.code
    if exit_code != 0:
        return "Robot testing failed."
    return None


def full_catalystcenter_terraform_test(data_paths, terraform_path, catalystcenter_url, version, tmpdir, exclude_tags=None, skip_destroy=False):
    """Deploy config to CatalystCenter instance using Terraform"""

    # Allow CC_URL env var to override parametrized URL (for local testing)
    catalystcenter_url = os.getenv("CC_URL", catalystcenter_url)
    os.environ["CC_URL"] = catalystcenter_url

    tf = tftest.TerraformTest(terraform_path)

    try:
        tf.setup(cleanup_on_exit=False, upgrade="upgrade")

        # Parse managed_sites and manage_specific_sites_only from Terraform config (single source of truth)
        # Empty string means validate all sites (single-state mode)
        managed_sites, manage_specific_only = get_managed_sites_from_terraform(terraform_path)
        os.environ["MANAGED_SITES"] = managed_sites
        os.environ["MANAGE_SPECIFIC_SITES_ONLY"] = manage_specific_only
        print(f"MANAGED_SITES set to: '{managed_sites}'")
        print(f"MANAGE_SPECIFIC_SITES_ONLY set to: '{manage_specific_only}'")

        tf.apply()

        # check idempotency
        output = tf.apply()
        if "No changes. Your infrastructure matches the configuration." not in output:
            pytest.fail(output)

        # Run tests
        data_paths.append(os.path.join(terraform_path, "defaults.yaml"))
        error = catalystcenter_render_run_tests(
            catalystcenter_url, data_paths, os.path.join(tmpdir, "results/"), exclude_tags
        )
        shutil.copy(
            os.path.join(tmpdir, "results/", "log.html"),
            "catalystcenter_tf_{}_log.html".format(version),
        )
        shutil.copy(
            os.path.join(tmpdir, "results/", "report.html"),
            "catalystcenter_tf_{}_report.html".format(version),
        )
        shutil.copy(
            os.path.join(tmpdir, "results/", "output.xml"),
            "catalystcenter_tf_{}_output.xml".format(version),
        )
        shutil.copy(
            os.path.join(tmpdir, "results/", "xunit.xml"),
            "catalystcenter_tf_{}_xunit.xml".format(version),
        )
        if error:
            pytest.fail(error)
    finally:
        if not skip_destroy:
            try:
                tf.destroy()
            except:
                tf.destroy()
            state_path = os.path.join(terraform_path, "terraform.tfstate")
            state_backup_path = os.path.join(terraform_path, "terraform.tfstate.backup")
            if os.path.exists(state_path):
                os.remove(state_path)
            if os.path.exists(state_backup_path):
                os.remove(state_backup_path)


@pytest.mark.cc_2379
@pytest.mark.terraform
@pytest.mark.single_state
@pytest.mark.parametrize(
    "data_paths, terraform_path, catalystcenter_url, version",
    [
        (
            [
                "tests/integration/fixtures/catalystcenter/standard/",
                "tests/integration/fixtures/catalystcenter/standard_single_state/",
                "defaults/"
            ],
            "tests/integration/fixtures/catalystcenter/terraform_2379",
            "https://10.62.190.224",
            "2.3.7.9",
        ),
    ],
)
def test_catalystcenter_terraform_2379(data_paths, terraform_path, catalystcenter_url, version, tmpdir):
    full_catalystcenter_terraform_test(data_paths, terraform_path, catalystcenter_url, version, tmpdir)


@pytest.mark.cc_2379
@pytest.mark.terraform
@pytest.mark.multi_state
@pytest.mark.global_state
@pytest.mark.run(order=1)
@pytest.mark.parametrize(
    "data_paths, terraform_path, catalystcenter_url, version",
    [
        (
            [
                "tests/integration/fixtures/catalystcenter/standard/",
                "tests/integration/fixtures/catalystcenter/standard_multi_state/",
                "defaults/"
            ],
            "tests/integration/fixtures/catalystcenter/terraform_2379_multistate_global",
            "https://10.62.190.224",
            "2.3.7.9_multistate_global",
        ),
    ],
)
def test_catalystcenter_multistate_global_2379(data_paths, terraform_path, catalystcenter_url, version, tmpdir):
    full_catalystcenter_terraform_test(data_paths, terraform_path, catalystcenter_url, version, tmpdir, exclude_tags=["devices", "site_specific"], skip_destroy=True)


@pytest.mark.cc_2379
@pytest.mark.terraform
@pytest.mark.multi_state
@pytest.mark.site_state
@pytest.mark.run(order=2)
@pytest.mark.parametrize(
    "data_paths, terraform_path, catalystcenter_url, version",
    [
        (
            [
                "tests/integration/fixtures/catalystcenter/standard/",
                "tests/integration/fixtures/catalystcenter/standard_multi_state/",
                "defaults/"
            ],
            "tests/integration/fixtures/catalystcenter/terraform_2379_multistate_site_a",
            "https://10.62.190.224",
            "2.3.7.9_multistate_site_a",
        ),
    ],
)
def test_catalystcenter_multistate_site_a_2379(data_paths, terraform_path, catalystcenter_url, version, tmpdir):
    full_catalystcenter_terraform_test(data_paths, terraform_path, catalystcenter_url, version, tmpdir, skip_destroy=True)


@pytest.mark.cc_2379
@pytest.mark.terraform
@pytest.mark.multi_state
@pytest.mark.site_state
@pytest.mark.run(order=2)
@pytest.mark.parametrize(
    "data_paths, terraform_path, catalystcenter_url, version",
    [
        (
            [
                "tests/integration/fixtures/catalystcenter/standard/",
                "tests/integration/fixtures/catalystcenter/standard_multi_state/",
                "defaults/"
            ],
            "tests/integration/fixtures/catalystcenter/terraform_2379_multistate_site_b",
            "https://10.62.190.224",
            "2.3.7.9_multistate_site_b",
        ),
    ],
)
def test_catalystcenter_multistate_site_b_2379(data_paths, terraform_path, catalystcenter_url, version, tmpdir):
    full_catalystcenter_terraform_test(data_paths, terraform_path, catalystcenter_url, version, tmpdir, skip_destroy=True)


@pytest.mark.cc_2379
@pytest.mark.terraform
@pytest.mark.single_state
@pytest.mark.use_bulk_api
@pytest.mark.parametrize(
    "data_paths, terraform_path, catalystcenter_url, version",
    [
        (
            [
                "tests/integration/fixtures/catalystcenter/standard/",
                "tests/integration/fixtures/catalystcenter/standard_single_state/",
                "defaults/"
            ],
            "tests/integration/fixtures/catalystcenter/terraform_2379",
            "https://10.62.190.224",
            "2.3.7.9_bulk",
        ),
    ],
)
def test_catalystcenter_terraform_2379_bulk(data_paths, terraform_path, catalystcenter_url, version, tmpdir):
    full_catalystcenter_terraform_test(data_paths, terraform_path, catalystcenter_url, version, tmpdir)


@pytest.mark.cc_2379
@pytest.mark.terraform
@pytest.mark.multi_state
@pytest.mark.global_state
@pytest.mark.use_bulk_api
@pytest.mark.run(order=1)
@pytest.mark.parametrize(
    "data_paths, terraform_path, catalystcenter_url, version",
    [
        (
            [
                "tests/integration/fixtures/catalystcenter/standard/",
                "tests/integration/fixtures/catalystcenter/standard_multi_state/",
                "defaults/"
            ],
            "tests/integration/fixtures/catalystcenter/terraform_2379_multistate_global",
            "https://10.62.190.224",
            "2.3.7.9_multistate_global_bulk",
        ),
    ],
)
def test_catalystcenter_multistate_global_2379_bulk(data_paths, terraform_path, catalystcenter_url, version, tmpdir):
    full_catalystcenter_terraform_test(data_paths, terraform_path, catalystcenter_url, version, tmpdir, exclude_tags=["devices", "site_specific"], skip_destroy=True)


@pytest.mark.cc_2379
@pytest.mark.terraform
@pytest.mark.multi_state
@pytest.mark.site_state
@pytest.mark.use_bulk_api
@pytest.mark.run(order=2)
@pytest.mark.parametrize(
    "data_paths, terraform_path, catalystcenter_url, version",
    [
        (
            [
                "tests/integration/fixtures/catalystcenter/standard/",
                "tests/integration/fixtures/catalystcenter/standard_multi_state/",
                "defaults/"
            ],
            "tests/integration/fixtures/catalystcenter/terraform_2379_multistate_site_a",
            "https://10.62.190.224",
            "2.3.7.9_multistate_site_a_bulk",
        ),
    ],
)
def test_catalystcenter_multistate_site_a_2379_bulk(data_paths, terraform_path, catalystcenter_url, version, tmpdir):
    full_catalystcenter_terraform_test(data_paths, terraform_path, catalystcenter_url, version, tmpdir, skip_destroy=True)


@pytest.mark.cc_2379
@pytest.mark.terraform
@pytest.mark.multi_state
@pytest.mark.site_state
@pytest.mark.use_bulk_api
@pytest.mark.run(order=2)
@pytest.mark.parametrize(
    "data_paths, terraform_path, catalystcenter_url, version",
    [
        (
            [
                "tests/integration/fixtures/catalystcenter/standard/",
                "tests/integration/fixtures/catalystcenter/standard_multi_state/",
                "defaults/"
            ],
            "tests/integration/fixtures/catalystcenter/terraform_2379_multistate_site_b",
            "https://10.62.190.224",
            "2.3.7.9_multistate_site_b_bulk",
        ),
    ],
)
def test_catalystcenter_multistate_site_b_2379_bulk(data_paths, terraform_path, catalystcenter_url, version, tmpdir):
    full_catalystcenter_terraform_test(data_paths, terraform_path, catalystcenter_url, version, tmpdir, skip_destroy=True)


@pytest.mark.cc_2379
@pytest.mark.terraform
@pytest.mark.multi_state
@pytest.mark.cleanup
@pytest.mark.use_bulk_api
@pytest.mark.run(order=3)
def test_catalystcenter_multistate_cleanup_2379_bulk():
    """Cleanup multi-state deployment in reverse order: SITE_B -> SITE_A -> GLOBAL

    IMPORTANT: Site instances (site_b, site_a) must be destroyed BEFORE global state.
    This ensures proper cleanup order and prevents dependency issues.
    """
    import tftest

    # Define cleanup order: site instances first, then global
    site_states = [
        ("SITE_B", "tests/integration/fixtures/catalystcenter/terraform_2379_multistate_site_b"),
        ("SITE_A", "tests/integration/fixtures/catalystcenter/terraform_2379_multistate_site_a"),
    ]

    global_state = [
        ("GLOBAL", "tests/integration/fixtures/catalystcenter/terraform_2379_multistate_global"),
    ]

    # Step 1: Destroy all site instances first
    print("\n=== Phase 1: Destroying site instances ===")
    for state_name, terraform_path in site_states:
        print(f"\nDestroying {state_name} state...")
        tf = tftest.TerraformTest(terraform_path)
        try:
            tf.destroy()
        except Exception as e:
            print(f"Warning: Error destroying {state_name}: {e}")
            try:
                tf.destroy()
            except:
                pass

        # Clean up state files
        state_path = os.path.join(terraform_path, "terraform.tfstate")
        state_backup_path = os.path.join(terraform_path, "terraform.tfstate.backup")
        if os.path.exists(state_path):
            os.remove(state_path)
        if os.path.exists(state_backup_path):
            os.remove(state_backup_path)

        print(f"{state_name} state destroyed successfully")

    # Step 2: Destroy global state only after all sites are destroyed
    print("\n=== Phase 2: Destroying global state ===")
    for state_name, terraform_path in global_state:
        print(f"\nDestroying {state_name} state...")
        tf = tftest.TerraformTest(terraform_path)
        try:
            tf.destroy()
        except Exception as e:
            print(f"Warning: Error destroying {state_name}: {e}")
            try:
                tf.destroy()
            except:
                pass

        # Clean up state files
        state_path = os.path.join(terraform_path, "terraform.tfstate")
        state_backup_path = os.path.join(terraform_path, "terraform.tfstate.backup")
        if os.path.exists(state_path):
            os.remove(state_path)
        if os.path.exists(state_backup_path):
            os.remove(state_backup_path)

        print(f"{state_name} state destroyed successfully")

    print("\n=== Cleanup completed: All site instances destroyed, then global ===")


# ============================================================
# CatalystCenter 2.3.7.10 Tests
# ============================================================

@pytest.mark.cc_23710
@pytest.mark.terraform
@pytest.mark.single_state
@pytest.mark.parametrize(
    "data_paths, terraform_path, catalystcenter_url, version",
    [
        (
            [
                "tests/integration/fixtures/catalystcenter/standard/",
                "tests/integration/fixtures/catalystcenter/standard_single_state/",
                "defaults/"
            ],
            "tests/integration/fixtures/catalystcenter/terraform_23710",
            "https://10.62.190.222",
            "2.3.7.10",
        ),
    ],
)
def test_catalystcenter_terraform_23710(data_paths, terraform_path, catalystcenter_url, version, tmpdir):
    full_catalystcenter_terraform_test(data_paths, terraform_path, catalystcenter_url, version, tmpdir)


@pytest.mark.cc_23710
@pytest.mark.terraform
@pytest.mark.multi_state
@pytest.mark.global_state
@pytest.mark.run(order=1)
@pytest.mark.parametrize(
    "data_paths, terraform_path, catalystcenter_url, version",
    [
        (
            [
                "tests/integration/fixtures/catalystcenter/standard/",
                "tests/integration/fixtures/catalystcenter/standard_multi_state/",
                "defaults/"
            ],
            "tests/integration/fixtures/catalystcenter/terraform_23710_multistate_global",
            "https://10.62.190.222",
            "2.3.7.10_multistate_global",
        ),
    ],
)
def test_catalystcenter_multistate_global_23710(data_paths, terraform_path, catalystcenter_url, version, tmpdir):
    full_catalystcenter_terraform_test(data_paths, terraform_path, catalystcenter_url, version, tmpdir, exclude_tags=["devices", "site_specific"], skip_destroy=True)


@pytest.mark.cc_23710
@pytest.mark.terraform
@pytest.mark.multi_state
@pytest.mark.site_state
@pytest.mark.run(order=2)
@pytest.mark.parametrize(
    "data_paths, terraform_path, catalystcenter_url, version",
    [
        (
            [
                "tests/integration/fixtures/catalystcenter/standard/",
                "tests/integration/fixtures/catalystcenter/standard_multi_state/",
                "defaults/"
            ],
            "tests/integration/fixtures/catalystcenter/terraform_23710_multistate_site_a",
            "https://10.62.190.222",
            "2.3.7.10_multistate_site_a",
        ),
    ],
)
def test_catalystcenter_multistate_site_a_23710(data_paths, terraform_path, catalystcenter_url, version, tmpdir):
    full_catalystcenter_terraform_test(data_paths, terraform_path, catalystcenter_url, version, tmpdir, skip_destroy=True)


@pytest.mark.cc_23710
@pytest.mark.terraform
@pytest.mark.multi_state
@pytest.mark.site_state
@pytest.mark.run(order=2)
@pytest.mark.parametrize(
    "data_paths, terraform_path, catalystcenter_url, version",
    [
        (
            [
                "tests/integration/fixtures/catalystcenter/standard/",
                "tests/integration/fixtures/catalystcenter/standard_multi_state/",
                "defaults/"
            ],
            "tests/integration/fixtures/catalystcenter/terraform_23710_multistate_site_b",
            "https://10.62.190.222",
            "2.3.7.10_multistate_site_b",
        ),
    ],
)
def test_catalystcenter_multistate_site_b_23710(data_paths, terraform_path, catalystcenter_url, version, tmpdir):
    full_catalystcenter_terraform_test(data_paths, terraform_path, catalystcenter_url, version, tmpdir, skip_destroy=True)


@pytest.mark.cc_23710
@pytest.mark.terraform
@pytest.mark.single_state
@pytest.mark.use_bulk_api
@pytest.mark.parametrize(
    "data_paths, terraform_path, catalystcenter_url, version",
    [
        (
            [
                "tests/integration/fixtures/catalystcenter/standard/",
                "tests/integration/fixtures/catalystcenter/standard_single_state/",
                "defaults/"
            ],
            "tests/integration/fixtures/catalystcenter/terraform_23710",
            "https://10.62.190.222",
            "2.3.7.10_bulk",
        ),
    ],
)
def test_catalystcenter_terraform_23710_bulk(data_paths, terraform_path, catalystcenter_url, version, tmpdir):
    full_catalystcenter_terraform_test(data_paths, terraform_path, catalystcenter_url, version, tmpdir)


@pytest.mark.cc_23710
@pytest.mark.terraform
@pytest.mark.multi_state
@pytest.mark.global_state
@pytest.mark.use_bulk_api
@pytest.mark.run(order=1)
@pytest.mark.parametrize(
    "data_paths, terraform_path, catalystcenter_url, version",
    [
        (
            [
                "tests/integration/fixtures/catalystcenter/standard/",
                "tests/integration/fixtures/catalystcenter/standard_multi_state/",
                "defaults/"
            ],
            "tests/integration/fixtures/catalystcenter/terraform_23710_multistate_global",
            "https://10.62.190.222",
            "2.3.7.10_multistate_global_bulk",
        ),
    ],
)
def test_catalystcenter_multistate_global_23710_bulk(data_paths, terraform_path, catalystcenter_url, version, tmpdir):
    full_catalystcenter_terraform_test(data_paths, terraform_path, catalystcenter_url, version, tmpdir, exclude_tags=["devices", "site_specific"], skip_destroy=True)


@pytest.mark.cc_23710
@pytest.mark.terraform
@pytest.mark.multi_state
@pytest.mark.site_state
@pytest.mark.use_bulk_api
@pytest.mark.run(order=2)
@pytest.mark.parametrize(
    "data_paths, terraform_path, catalystcenter_url, version",
    [
        (
            [
                "tests/integration/fixtures/catalystcenter/standard/",
                "tests/integration/fixtures/catalystcenter/standard_multi_state/",
                "defaults/"
            ],
            "tests/integration/fixtures/catalystcenter/terraform_23710_multistate_site_a",
            "https://10.62.190.222",
            "2.3.7.10_multistate_site_a_bulk",
        ),
    ],
)
def test_catalystcenter_multistate_site_a_23710_bulk(data_paths, terraform_path, catalystcenter_url, version, tmpdir):
    full_catalystcenter_terraform_test(data_paths, terraform_path, catalystcenter_url, version, tmpdir, skip_destroy=True)


@pytest.mark.cc_23710
@pytest.mark.terraform
@pytest.mark.multi_state
@pytest.mark.site_state
@pytest.mark.use_bulk_api
@pytest.mark.run(order=2)
@pytest.mark.parametrize(
    "data_paths, terraform_path, catalystcenter_url, version",
    [
        (
            [
                "tests/integration/fixtures/catalystcenter/standard/",
                "tests/integration/fixtures/catalystcenter/standard_multi_state/",
                "defaults/"
            ],
            "tests/integration/fixtures/catalystcenter/terraform_23710_multistate_site_b",
            "https://10.62.190.222",
            "2.3.7.10_multistate_site_b_bulk",
        ),
    ],
)
def test_catalystcenter_multistate_site_b_23710_bulk(data_paths, terraform_path, catalystcenter_url, version, tmpdir):
    full_catalystcenter_terraform_test(data_paths, terraform_path, catalystcenter_url, version, tmpdir, skip_destroy=True)


@pytest.mark.cc_23710
@pytest.mark.terraform
@pytest.mark.multi_state
@pytest.mark.cleanup
@pytest.mark.use_bulk_api
@pytest.mark.run(order=3)
def test_catalystcenter_multistate_cleanup_23710_bulk():
    """Cleanup multi-state deployment in reverse order: SITE_B -> SITE_A -> GLOBAL

    IMPORTANT: Site instances (site_b, site_a) must be destroyed BEFORE global state.
    This ensures proper cleanup order and prevents dependency issues.
    """
    import tftest

    site_states = [
        ("SITE_B", "tests/integration/fixtures/catalystcenter/terraform_23710_multistate_site_b"),
        ("SITE_A", "tests/integration/fixtures/catalystcenter/terraform_23710_multistate_site_a"),
    ]

    global_state = [
        ("GLOBAL", "tests/integration/fixtures/catalystcenter/terraform_23710_multistate_global"),
    ]

    print("\n=== Phase 1: Destroying site instances ===")
    for state_name, terraform_path in site_states:
        print(f"\nDestroying {state_name} state...")
        tf = tftest.TerraformTest(terraform_path)
        try:
            tf.destroy()
        except Exception as e:
            print(f"Warning: Error destroying {state_name}: {e}")
            try:
                tf.destroy()
            except:
                pass

        state_path = os.path.join(terraform_path, "terraform.tfstate")
        state_backup_path = os.path.join(terraform_path, "terraform.tfstate.backup")
        if os.path.exists(state_path):
            os.remove(state_path)
        if os.path.exists(state_backup_path):
            os.remove(state_backup_path)

        print(f"{state_name} state destroyed successfully")

    print("\n=== Phase 2: Destroying global state ===")
    for state_name, terraform_path in global_state:
        print(f"\nDestroying {state_name} state...")
        tf = tftest.TerraformTest(terraform_path)
        try:
            tf.destroy()
        except Exception as e:
            print(f"Warning: Error destroying {state_name}: {e}")
            try:
                tf.destroy()
            except:
                pass

        state_path = os.path.join(terraform_path, "terraform.tfstate")
        state_backup_path = os.path.join(terraform_path, "terraform.tfstate.backup")
        if os.path.exists(state_path):
            os.remove(state_path)
        if os.path.exists(state_backup_path):
            os.remove(state_backup_path)

        print(f"{state_name} state destroyed successfully")

    print("\n=== Cleanup completed: All site instances destroyed, then global ===")


@pytest.mark.cc_23710
@pytest.mark.terraform
@pytest.mark.multi_state
@pytest.mark.cleanup
@pytest.mark.run(order=3)
def test_catalystcenter_multistate_cleanup_23710():
    """Cleanup multi-state deployment in reverse order: SITE_B -> SITE_A -> GLOBAL

    IMPORTANT: Site instances (site_b, site_a) must be destroyed BEFORE global state.
    This ensures proper cleanup order and prevents dependency issues.
    """
    import tftest

    site_states = [
        ("SITE_B", "tests/integration/fixtures/catalystcenter/terraform_23710_multistate_site_b"),
        ("SITE_A", "tests/integration/fixtures/catalystcenter/terraform_23710_multistate_site_a"),
    ]

    global_state = [
        ("GLOBAL", "tests/integration/fixtures/catalystcenter/terraform_23710_multistate_global"),
    ]

    print("\n=== Phase 1: Destroying site instances ===")
    for state_name, terraform_path in site_states:
        print(f"\nDestroying {state_name} state...")
        tf = tftest.TerraformTest(terraform_path)
        try:
            tf.destroy()
        except Exception as e:
            print(f"Warning: Error destroying {state_name}: {e}")
            try:
                tf.destroy()
            except:
                pass

        state_path = os.path.join(terraform_path, "terraform.tfstate")
        state_backup_path = os.path.join(terraform_path, "terraform.tfstate.backup")
        if os.path.exists(state_path):
            os.remove(state_path)
        if os.path.exists(state_backup_path):
            os.remove(state_backup_path)

        print(f"{state_name} state destroyed successfully")

    print("\n=== Phase 2: Destroying global state ===")
    for state_name, terraform_path in global_state:
        print(f"\nDestroying {state_name} state...")
        tf = tftest.TerraformTest(terraform_path)
        try:
            tf.destroy()
        except Exception as e:
            print(f"Warning: Error destroying {state_name}: {e}")
            try:
                tf.destroy()
            except:
                pass

        state_path = os.path.join(terraform_path, "terraform.tfstate")
        state_backup_path = os.path.join(terraform_path, "terraform.tfstate.backup")
        if os.path.exists(state_path):
            os.remove(state_path)
        if os.path.exists(state_backup_path):
            os.remove(state_backup_path)

        print(f"{state_name} state destroyed successfully")

    print("\n=== Cleanup completed: All site instances destroyed, then global ===")
@pytest.mark.cc_2379
@pytest.mark.terraform
@pytest.mark.multi_state
@pytest.mark.cleanup
@pytest.mark.run(order=3)
def test_catalystcenter_multistate_cleanup_2379():
    """Cleanup multi-state deployment in reverse order: SITE_B -> SITE_A -> GLOBAL

    IMPORTANT: Site instances (site_b, site_a) must be destroyed BEFORE global state.
    This ensures proper cleanup order and prevents dependency issues.
    """
    import tftest

    # Define cleanup order: site instances first, then global
    site_states = [
        ("SITE_B", "tests/integration/fixtures/catalystcenter/terraform_2379_multistate_site_b"),
        ("SITE_A", "tests/integration/fixtures/catalystcenter/terraform_2379_multistate_site_a"),
    ]

    global_state = [
        ("GLOBAL", "tests/integration/fixtures/catalystcenter/terraform_2379_multistate_global"),
    ]

    # Step 1: Destroy all site instances first
    print("\n=== Phase 1: Destroying site instances ===")
    for state_name, terraform_path in site_states:
        print(f"\nDestroying {state_name} state...")
        tf = tftest.TerraformTest(terraform_path)
        try:
            tf.destroy()
        except Exception as e:
            print(f"Warning: Error destroying {state_name}: {e}")
            try:
                tf.destroy()
            except:
                pass

        # Clean up state files
        state_path = os.path.join(terraform_path, "terraform.tfstate")
        state_backup_path = os.path.join(terraform_path, "terraform.tfstate.backup")
        if os.path.exists(state_path):
            os.remove(state_path)
        if os.path.exists(state_backup_path):
            os.remove(state_backup_path)

        print(f"{state_name} state destroyed successfully")

    # Step 2: Destroy global state only after all sites are destroyed
    print("\n=== Phase 2: Destroying global state ===")
    for state_name, terraform_path in global_state:
        print(f"\nDestroying {state_name} state...")
        tf = tftest.TerraformTest(terraform_path)
        try:
            tf.destroy()
        except Exception as e:
            print(f"Warning: Error destroying {state_name}: {e}")
            try:
                tf.destroy()
            except:
                pass

        # Clean up state files
        state_path = os.path.join(terraform_path, "terraform.tfstate")
        state_backup_path = os.path.join(terraform_path, "terraform.tfstate.backup")
        if os.path.exists(state_path):
            os.remove(state_path)
        if os.path.exists(state_backup_path):
            os.remove(state_backup_path)

        print(f"{state_name} state destroyed successfully")

    print("\n=== Cleanup completed: All site instances destroyed, then global ===")

    
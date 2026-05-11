#!/usr/bin/env python3
"""
Generate Terraform test configurations from Jinja2 templates.
This script finds all main.tf.j2 templates and renders them with branch-specific variables.
"""

import argparse
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape


def generate_main_tf_from_jinja(template_path, output_path, context, show_content=False):
    """Generate main.tf from Jinja2 template"""
    # Setup Jinja2 environment
    env = Environment(
        loader=FileSystemLoader(template_path.parent),
        autoescape=select_autoescape()
    )

    # Load and render template
    template = env.get_template(template_path.name)
    rendered = template.render(**context)

    # Write output
    with open(output_path, 'w') as f:
        f.write(rendered)

    print(f"✓ Generated {output_path}")
    print(f"  Branch: {context['branch_ref']}")

    # Show provider version or local binary usage
    if context.get('provider_version'):
        print(f"  Provider version: {context['provider_version']}")
    else:
        print(f"  Provider: Local binary (dev_overrides)")

    # Show use_bulk_api setting
    if context.get('use_bulk_api'):
        print(f"  use_bulk_api: enabled")

    # Show generated content if requested
    if show_content:
        print(f"\n  === Content of {output_path.name} ===")
        for i, line in enumerate(rendered.splitlines(), 1):
            print(f"  {i:3d} | {line}")
        print(f"  === End of {output_path.name} ===")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate Terraform configs from Jinja2 templates'
    )
    parser.add_argument(
        '--branch',
        required=True,
        help='Branch name for module ref (e.g., dev, master)'
    )
    parser.add_argument(
        '--provider-version',
        default=None,
        help='Provider version (optional, if not specified on dev branch uses local binary)'
    )
    parser.add_argument(
        '--max-timeout',
        default=600,
        type=int,
        help='Provider max timeout in seconds (default: 600)'
    )
    parser.add_argument(
        '--use-bulk-api',
        action='store_true',
        help='Enable use_bulk_api in module configurations'
    )
    parser.add_argument(
        '--show-content',
        action='store_true',
        help='Display generated main.tf file content for troubleshooting'
    )
    args = parser.parse_args()

    # Context variables for template rendering
    context = {
        'branch_ref': args.branch,
        'provider_version': args.provider_version if args.provider_version else None,
        'max_timeout': args.max_timeout,
    }

    # Only add use_bulk_api to context if explicitly set
    if args.use_bulk_api:
        context['use_bulk_api'] = True

    # Validate: non-dev branches must specify provider version
    if args.branch != 'dev' and not args.provider_version:
        print("ERROR: --provider-version is required for non-dev branches")
        exit(1)

    # Find all Jinja2 templates in test fixtures
    fixtures_dir = Path('tests/integration/fixtures/catalystcenter')
    template_files = list(fixtures_dir.rglob('main.tf.j2'))

    if not template_files:
        print("⚠ No main.tf.j2 templates found in fixtures directory")
        exit(1)

    print(f"\nGenerating {len(template_files)} Terraform configuration(s)...\n")

    for template_file in template_files:
        output_file = template_file.parent / 'main.tf'
        generate_main_tf_from_jinja(template_file, output_file, context, show_content=args.show_content)
        print()

    print(f"✓ Successfully generated {len(template_files)} main.tf file(s)")

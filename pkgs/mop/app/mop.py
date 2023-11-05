import yaml
import sys
import logging
import requests
import argparse
from string import Template

logging.basicConfig(level=logging.ERROR)

FLAKE_TEMPLATE = """
{
    inputs = {
        nixpkgs.url = "github:nixos/nixpkgs/$nixpkgs_tag";
$inputs
    };

    outputs = {self, nixpkgs, ...}@inputs:
    let
        system = "$nix_system";
        pkgs = nixpkgs.legacyPackages.${system};
$imports
    in
    {
        devShells.${system} = {
$shells
        };
    };
}
"""

def read_yaml(filename):
    with open(filename, 'r') as file:
        data = yaml.safe_load(file)
    return data

def ask_nixhub_io(package, version):
    resp = requests.get(f"https://www.nixhub.io/packages/{package}?_data=routes/_nixhub.packages.$pkg._index")
    resp_dict = resp.json()
    logging.info(f"GET DATA: {resp_dict}")
    releases = resp_dict["releases"]
    for release in releases:
        if release["version"] == version:
            last_update = release["last_updated"]
            for x in release["platforms"]:
                if x["date"] == last_update:
                    return x["commit_hash"]
    return None

def generate_nix_flake_inputs(nix_inputs):
    return "\n".join([f"\t\t{i['input_name']}.url = \"{i['url']}\";" for i in nix_inputs])

def generate_nix_flake_imports(nix_inputs):
    return "\n".join([f"\t\tpkgs_{i['input_name']} = inputs.{i['input_name']}.legacyPackages.${{system}};" for i in nix_inputs])

def generate_nix_shell_packages(nix_inputs):
    return "\n".join([f"\t\t\t\t\tpkgs_{i['input_name']}.{i['package_name']}" for i in nix_inputs])

def generate_nix_shell(nix_inputs):
    return "\n".join([f"\t\t\t{shell_name} = pkgs.mkShell {{ packages = [{' '.join(packages)}]; }};" for shell_name, packages in nix_inputs.items()])

def main():
    parser = argparse.ArgumentParser(description="Generate Nix shells with desired package versions")
    parser.add_argument("--output", "-o", type=str, default="flake.nix", help="file to store the generated flake.nix")
    parser.add_argument("description", type=str, help="YAML file containing the description of the shells")
    parser.add_argument("--nixpkgs-tag", type=str, default="23.05", help="tag for the default import of nixpkgs (default: 23.05)")
    parser.add_argument("--system", type=str, default="x86_64-linux", help="system (default: x86_64-linux)")
    parser.add_argument("--verbose", action="store_true", help="behind the scene access")

    args = parser.parse_args()
    if args.verbose:
        logging.getLogger().setLevel(logging.INFO)

    filename = args.description
    logging.info(f"Filename: {filename}")
    data = read_yaml(filename)
    logging.info(f"YAML data: {data}")

    flake_inputs = []
    flake_shells = {}

    for shell in data:
        shell_name = shell["shell"]
        flake_shells[shell_name] = []
        for package in shell["packages"]:
            logging.info(f"package: {package}")
            package_name = package["name"]
            package_version = package["version"]
            package_derivation = package["derivation"]

            logging.info(f"Asking for version '{package_version}' of {package_name}")
            nixpkgs_commit = ask_nixhub_io(package_name, package_version)
            if nixpkgs_commit:
                logging.info(f"Found version `{package_version}' of {package_name} at commit {nixpkgs_commit}")
                flake_input_name = f"{package_name}_{package_version.replace('.', '_')}"

                flake_inputs.append({"package_name": package_name, "input_name": flake_input_name, "url": f"github:nixos/nixpkgs?rev={nixpkgs_commit}", "version": package_version, "package_derivation": package_derivation})
                flake_shells[shell_name].append(f"pkgs_{flake_input_name}.{package_derivation}")
        logging.info(f"flake inputs = {flake_inputs}")


    sub_data = {
            "inputs": generate_nix_flake_inputs(flake_inputs),
            "nix_system": args.system,
            "imports": generate_nix_flake_imports(flake_inputs),
            "packages": generate_nix_shell_packages(flake_inputs),
            "shells": generate_nix_shell(flake_shells),
            "nixpkgs_tag": args.nixpkgs_tag
    }

    template_flake = Template(FLAKE_TEMPLATE)
    flake = template_flake.safe_substitute(sub_data)

    with open(args.output, "w") as flake_file:
        flake_file.write(flake)
    logging.info(f"Flake written at '{args.output}'")

    return 0

if __name__ == "__main__":
    main()

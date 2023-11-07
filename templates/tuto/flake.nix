{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/23.05";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let pkgs = import nixpkgs { inherit system; };
      in {
        devShells = {
          default = pkgs.mkShell { packages = with pkgs; [ snakemake ]; };
          pyshell = pkgs.mkShell { packages = with pkgs; [ python3 ]; };
          texshell = pkgs.mkShell { packages = with pkgs; [ texlive.combined.scheme-basic rubber ]; };
          rshell = pkgs.mkShell {
            packages = with pkgs;
              [
                (rWrapper.override {
                  packages = with rPackages; [ tidyverse ];
                })
              ];
          };
        };
      });
}

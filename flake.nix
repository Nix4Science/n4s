{
  description = "Utils for Nix4Science";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/23.05";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let pkgs = import nixpkgs { inherit system; };
      in rec {
        lib = import ./lib.nix { inherit pkgs; gotainer = self.packages.${system}.gotainer; };
        packages = rec {
            gotainer = pkgs.callPackage ./pkgs/gotainer { };
        };
        # devShells = {
        #   default = pkgs.mkShell { buildInputs = with pkgs; [ gcc ]; };
        # };
      });
}

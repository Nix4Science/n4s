{ pkgs, gotainer }: {
  mkShell = { containerize ? false, ... }@shellInputs:
    let
      gotainer = self.outputs.packages.${system}.gotainer;
      underlyingShell = pkgs.mkShell shellInputs;
    in if containerize then
      pkgs.mkShell {
        buildInputs = [ gotainer ];
        shellHook = ''
          ${gotainer}/bin/gotainer run ${underlyingShell} ${pkgs.bashInteractive}
          exit
        '';
      }
    else
      underlyingShell;
  mkShellContainer = shellInputs:
    let
      gotainer = self.outputs.packages.${system}.gotainer;
      underlyingShell = pkgs.mkShell shellInputs;
    in pkgs.writeShellScriptBin "nix-shell-container" ''
      ${gotainer}/bin/gotainer run ${underlyingShell} ${pkgs.bashInteractive} $@
    '';
}

{ snakemake }:

snakemake.overrideAttrs (finalAttrs: previousAttrs: {
  pname = previousAttrs.pname + "-nix";
  patches = [ ./0001-add_nix_flake_v7.25.3.patch ./0002-nix-flake-deployment.patch ./0003-nix-flake-jobs.patch  ./0004-oops-jobs.patch ];
})

